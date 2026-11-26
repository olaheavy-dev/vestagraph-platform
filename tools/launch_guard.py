"""Launch guard (OP-06): fail a release while draft text is in the pages a new image serves.

The pilot's pages show unfinished text on purpose (SE-07), such as "To be written before launch
(SE-02)". The release workflow starts the newly built image on the runner and runs this tool against
it before the image is pushed. The tool waits for `/healthz`, reads a fixed list of paths and every
same-site page they link to, and exits 1 if any listed draft string is found, or if any page could
not be read: "could not check" is never a pass. A 404 means "no page here" and is not an error.

Runs on the runner's own python3 (3.12). Standard library only.
Design: docs/superpowers/specs/2026-11-26-launch-guard-design.md
"""

import argparse
import html
import http.client
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import deque
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import TextIO
from urllib.parse import urldefrag, urljoin, urlsplit

DEFAULT_PATHS = ("/", "/how-it-works", "/privacy", "/accessibility")
DEFAULT_PAGE_LIMIT = 200
DEFAULT_START_TIMEOUT_S = 60
DEFAULT_PAGE_TIMEOUT_S = 10
START_INTERVAL_S = 1.0
MAX_BODY_BYTES = 5 * 1024 * 1024  # 5 MB: far more than any page; a bigger answer fails the guard

# (status, content type, body, Location header or ""). Redirects are returned, never followed.
Response = tuple[int, str, bytes, str]
# Raises OSError, http.client.HTTPException or ValueError if the page cannot be read.
Fetch = Callable[[str], Response]

_WHITESPACE = re.compile(r"\s+")
# Characters a browser does not show between letters: soft hyphen, zero-width spaces and joiners.
_INVISIBLE = dict.fromkeys(map(ord, "\u00ad\u200b\u200c\u200d\u2060\ufeff"))
_CHARSET = re.compile(r"charset=[\"']?([\w.:-]+)", re.IGNORECASE)


def _say(message: str, stream: TextIO | None = None) -> None:
    (stream or sys.stdout).write(message + "\n")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Return a redirect as the answer, so the guard never leaves the site on its own."""

    def redirect_request(self, *args: object, **kwargs: object) -> None:
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def _read_capped(response: http.client.HTTPResponse | urllib.error.HTTPError) -> bytes:
    body: bytes = response.read(MAX_BODY_BYTES + 1)
    if len(body) > MAX_BODY_BYTES:
        raise OSError(f"the page is larger than {MAX_BODY_BYTES} bytes")
    return body


def fetch_url(url: str, timeout_s: int = DEFAULT_PAGE_TIMEOUT_S) -> Response:
    """Fetch a page. An HTTP error or redirect status (404, 500, 302) is returned, not raised."""
    request = urllib.request.Request(  # noqa: S310 - the URL comes from the workflow, not a user
        url, headers={"User-Agent": "vestagraph-launch-guard"}
    )
    try:
        with _OPENER.open(request, timeout=timeout_s) as response:
            headers = response.headers
            return response.status, headers.get("Content-Type", ""), _read_capped(response), ""
    except urllib.error.HTTPError as error:
        with error:
            headers = error.headers
            body = _read_capped(error)
        return error.code, headers.get("Content-Type", ""), body, headers.get("Location", "")


def load_strings(path: Path) -> list[str]:
    """Read the list of draft strings; exit with a message unless it lists non-empty strings."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise SystemExit(f"cannot read the draft-string list {path}: {error}") from None
    if (
        not isinstance(data, list)
        or not data
        or not all(isinstance(entry, str) and entry.strip() for entry in data)
    ):
        raise SystemExit(f"{path} must be a non-empty JSON array of non-empty strings")
    return data


def normalise(text: str) -> str:
    """Decode HTML entities, drop invisible characters, and make each whitespace run one space."""
    return _WHITESPACE.sub(" ", html.unescape(text).translate(_INVISIBLE)).strip()


def decode(body: bytes, content_type: str = "") -> str:
    """Decode with the charset the Content-Type declares, or UTF-8 if it names none or a bad one."""
    match = _CHARSET.search(content_type)
    if match:
        try:
            return body.decode(match.group(1), errors="replace")
        except LookupError:
            pass
    return body.decode("utf-8", errors="replace")


class _PageParser(HTMLParser):
    """Collects link targets and the text between tags (comments are left out)."""

    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("a", "link"):
            for name, value in attrs:
                if name == "href" and value:
                    self.hrefs.append(value)

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def _parse(text: str) -> _PageParser:
    parser = _PageParser()
    parser.feed(text)
    parser.close()
    return parser


def find_strings(body: bytes, strings: Sequence[str], content_type: str = "") -> list[str]:
    """Return the listed strings in the body, in list order.

    Searches both the raw body and its text with tags and comments taken out, so a string that
    markup splits (React's `<!-- -->` between text parts, or `<em>`) is still found.
    """
    raw = decode(body, content_type)
    texts = (normalise(raw), normalise("".join(_parse(raw).text)))
    return [s for s in strings if any(normalise(s) in text for text in texts)]


def same_site_links(page_url: str, html_text: str) -> list[str]:
    """Links on the page to the same scheme and host, without fragments, in first-seen order."""
    links: list[str] = []
    for href in _parse(html_text).hrefs:
        url = _same_site(page_url, href)
        if url is not None and url not in links:
            links.append(url)
    return links


def _same_site(page_url: str, href: str) -> str | None:
    """The link resolved against the page, without its fragment, or None if it leaves the site.

    A link that is not a valid URL (`http://[bad`) is None too: it cannot be a page.
    """
    try:
        url = urldefrag(urljoin(page_url, href.strip())).url
        page, target = urlsplit(page_url), urlsplit(url)
    except ValueError:
        return None
    return url if (target.scheme, target.netloc) == (page.scheme, page.netloc) else None


def wait_until_up(base_url: str, timeout_s: int, interval_s: float, fetch: Fetch) -> bool:
    """True once `/healthz` answers 200; False if `timeout_s` passes first. Always tries once."""
    deadline = time.monotonic() + timeout_s
    while True:
        try:
            if fetch(base_url + "/healthz")[0] == 200:
                return True
        except (OSError, http.client.HTTPException):
            pass
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        time.sleep(max(0.0, min(interval_s, remaining)))


@dataclass(frozen=True)
class ScanResult:
    pages_read: int
    findings: list[tuple[str, str]] = field(default_factory=list)  # (url, draft string)
    errors: list[tuple[str, str]] = field(default_factory=list)  # (url, reason)
    limit_reached: bool = False

    @property
    def ok(self) -> bool:
        return not self.findings and not self.errors and not self.limit_reached


def scan_site(
    base_url: str, paths: Sequence[str], strings: Sequence[str], fetch: Fetch, page_limit: int
) -> ScanResult:
    """Read the fixed paths and the same-site pages they link to, breadth first, each URL once."""
    queue: deque[str] = deque()
    seen: set[str] = set()

    def add(url: str) -> None:
        if url not in seen:
            seen.add(url)
            queue.append(url)

    for path in paths:
        add(urldefrag(base_url + path).url)

    findings: list[tuple[str, str]] = []
    errors: list[tuple[str, str]] = []
    pages_read = 0
    while queue and pages_read < page_limit:
        url = queue.popleft()
        try:
            status, content_type, body, location = fetch(url)
        except (OSError, http.client.HTTPException, ValueError) as error:
            errors.append((url, f"could not be read ({error})"))
            continue
        pages_read += 1
        if 300 <= status < 400:
            # A redirect is followed only when it stays on the site (never to the live site).
            target = _same_site(url, location) if location else None
            if target is not None:
                add(target)
            continue
        if status not in (200, 404):
            errors.append((url, f"answered {status}"))
            continue
        findings.extend((url, found) for found in find_strings(body, strings, content_type))
        if status == 200 and content_type.lower().startswith("text/html"):
            for link in same_site_links(url, decode(body, content_type)):
                add(link)
    return ScanResult(pages_read, findings, errors, limit_reached=bool(queue))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="where the new image answers")
    parser.add_argument("--strings", required=True, type=Path, help="JSON list of draft strings")
    parser.add_argument("--path", action="append", dest="paths", help="a path to read (repeatable)")
    parser.add_argument("--start-timeout", type=int, default=DEFAULT_START_TIMEOUT_S)
    parser.add_argument("--page-timeout", type=int, default=DEFAULT_PAGE_TIMEOUT_S)
    parser.add_argument("--page-limit", type=int, default=DEFAULT_PAGE_LIMIT)
    args = parser.parse_args(argv)

    strings = load_strings(args.strings)
    base_url = args.base_url.rstrip("/")

    def fetch(url: str) -> Response:
        return fetch_url(url, args.page_timeout)

    if not wait_until_up(base_url, args.start_timeout, START_INTERVAL_S, fetch):
        _say(f"The app did not answer /healthz within {args.start_timeout} s.", sys.stderr)
        _say(
            "Launch guard failed (OP-06): the pages could not be read. Nothing was released.",
            sys.stderr,
        )
        return 1

    result = scan_site(base_url, args.paths or DEFAULT_PATHS, strings, fetch, args.page_limit)
    if result.ok:
        _say(f"Launch guard passed: {result.pages_read} pages read, no draft text.")
        return 0
    for url, found in result.findings:
        _say(f'{url}: "{found}"', sys.stderr)
    for url, reason in result.errors:
        _say(f"{url}: {reason}", sys.stderr)
    if result.limit_reached:
        _say(f"More than {args.page_limit} pages: the rest were not read.", sys.stderr)
    _say(
        "Launch guard failed (OP-06): draft text or unread pages. Nothing was released.", sys.stderr
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
