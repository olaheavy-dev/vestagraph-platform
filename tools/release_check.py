"""Release check (stage 5b group A): wait until the live health page reports a given commit.

The release workflow runs this on the runner's own python3 (3.12) after a deploy. It polls the
health page until the page answers `{"status": "ok", "commit": "<commit>"}`, and exits 1 if that
does not happen within the timeout. Standard library only.
"""

import argparse
import http.client
import json
import sys
import time
import urllib.request
from collections.abc import Callable, Sequence
from typing import TextIO

REQUEST_TIMEOUT_S = 10


def _say(message: str, stream: TextIO = sys.stdout) -> None:
    stream.write(message + "\n")


def is_live(body: bytes, commit: str) -> bool:
    """True only for valid JSON with status "ok" and the expected commit."""
    try:
        data = json.loads(body)
    except ValueError:
        return False
    return isinstance(data, dict) and data.get("status") == "ok" and data.get("commit") == commit


def fetch_url(url: str) -> bytes:
    """Fetch the page. The headers stop Cloudflare's browser checks from challenging the request."""
    request = urllib.request.Request(  # noqa: S310 - the URL comes from the workflow, not a user
        url,
        headers={"Cache-Control": "no-cache", "User-Agent": "vestagraph-release-check"},
    )
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_S) as response:  # noqa: S310
        body: bytes = response.read()
    return body


def wait_for_commit(
    url: str,
    commit: str,
    timeout_s: int,
    interval_s: int,
    fetch: Callable[[str], bytes],
) -> bool:
    """Poll `url` until it reports `commit`; False if `timeout_s` passes first.

    Always polls at least once. A failed or cut-off request (OSError, HTTPException) counts as "not live yet".
    """
    deadline = time.monotonic() + timeout_s
    while True:
        try:
            if is_live(fetch(url), commit):
                return True
        except OSError, http.client.HTTPException:
            pass
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        time.sleep(max(0.0, min(interval_s, remaining)))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="health page URL")
    parser.add_argument("--commit", required=True, help="commit the page must report")
    parser.add_argument("--timeout", type=int, default=900, help="seconds to wait (default 900)")
    parser.add_argument(
        "--interval", type=int, default=20, help="seconds between polls (default 20)"
    )
    args = parser.parse_args(argv)
    if wait_for_commit(args.url, args.commit, args.timeout, args.interval, fetch_url):
        _say(f"{args.url} reports {args.commit}")
        return 0
    _say(
        f"{args.url} did not report {args.commit} within {args.timeout} s; "
        "to roll back, run the Images workflow with an earlier commit",
        sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
