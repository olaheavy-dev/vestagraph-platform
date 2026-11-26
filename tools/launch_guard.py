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

# (status, content type, body). Raises OSError or http.client.HTTPException
# if the page cannot be read.
Fetch = Callable[[str], tuple[int, str, bytes]]

_WHITESPACE = re.compile(r"\s+")


def _say(message: str, stream: TextIO | None = None) -> None:
    (stream or sys.stdout).write(message + "\n")


def fetch_url(url: str, timeout_s: int = DEFAULT_PAGE_TIMEOUT_S) -> tuple[int, str, bytes]:
    """Fetch a page. An HTTP error status (404, 500) is returned, not raised."""
    request = urllib.request.Request(  # noqa: S310 - the URL comes from the workflow, not a user
        url, headers={"User-Agent": "vestagraph-launch-guard"}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:  # noqa: S310
            return response.status, response.headers.get("Content-Type", ""), response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.headers.get("Content-Type", ""), error.read()


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
    """Decode HTML entities and turn every run of whitespace (including &nbsp;) into one space."""
    return _WHITESPACE.sub(" ", html.unescape(text)).strip()


def find_strings(body: bytes, strings: Sequence[str]) -> list[str]:
    """Return the listed strings that appear in the body, in list order."""
    text = normalise(body.decode("utf-8", errors="replace"))
    return [string for string in strings if normalise(string) in text]


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("a", "link"):
            for name, value in attrs:
                if name == "href" and value:
                    self.hrefs.append(value)


def same_site_links(page_url: str, html_text: str) -> list[str]:
    """Links on the page to the same scheme and host, without fragments, in first-seen order."""
    parser = _LinkParser()
    parser.feed(html_text)
    parser.close()
    page = urlsplit(page_url)
    links: list[str] = []
    for href in parser.hrefs:
        url = urldefrag(urljoin(page_url, href.strip())).url
        target = urlsplit(url)
        if (target.scheme, target.netloc) == (page.scheme, page.netloc) and url not in links:
            links.append(url)
    return links


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
            status, content_type, body = fetch(url)
        except (OSError, http.client.HTTPException) as error:
            errors.append((url, f"could not be read ({error})"))
            continue
        pages_read += 1
        if status not in (200, 404):
            errors.append((url, f"answered {status}"))
            continue
        findings.extend((url, found) for found in find_strings(body, strings))
        if status == 200 and content_type.lower().startswith("text/html"):
            for link in same_site_links(url, body.decode("utf-8", errors="replace")):
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

    def fetch(url: str) -> tuple[int, str, bytes]:
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
