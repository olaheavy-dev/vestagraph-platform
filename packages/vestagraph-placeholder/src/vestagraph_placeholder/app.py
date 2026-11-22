"""The placeholder app: a health page and nothing else.

It uses only the standard library. It never logs a request, so a postcode
typed into the real app later can never reach a log through this layer.
"""

import json
import os
import pathlib
import socketserver
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DEFAULT_SECRET_CHECK_PATH = "/run/secrets/secret_check"  # noqa: S105 (a path, not a secret)
DEFAULT_PORT = 8080


class PlaceholderServer(ThreadingHTTPServer):
    """A threading HTTP server whose failures log one fixed line."""

    def handle_error(
        self,
        request: socketserver._RequestType,  # pyright: ignore[reportPrivateUsage]
        client_address: socketserver._AfInetAddress,  # pyright: ignore[reportPrivateUsage]
    ) -> None:
        # The default prints the client address and a traceback; print neither.
        sys.stderr.write("request failed\n")
        sys.stderr.flush()


def load_secret_check(path: pathlib.Path) -> str:
    """Return the secret's value, or exit with a message naming only the path."""
    if path.is_dir():
        raise SystemExit(f"secret check file is a directory, not a file: {path}")
    try:
        value = path.read_text().strip()
    except FileNotFoundError:
        raise SystemExit(f"secret check file is missing: {path}") from None
    except OSError:
        raise SystemExit(f"secret check file cannot be read: {path}") from None
    if not value:
        raise SystemExit(f"secret check file is empty: {path}")
    return value


def make_handler(commit: str) -> type[BaseHTTPRequestHandler]:
    """Build the request handler that reports the given commit."""

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            """Log nothing: a request line holds the path and client address."""

        def log_error(self, format: str, *args: object) -> None:
            """Log nothing, for the same reason."""

        def _respond(self, status: int, body: bytes = b"", content_type: str | None = None) -> None:
            self.send_response(status)
            self.send_header("Cache-Control", "no-store")
            if content_type is not None:
                self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            if self.path == "/healthz":
                body = json.dumps({"status": "ok", "commit": commit}).encode()
                self._respond(200, body, "application/json")
            else:
                self._respond(404)

        def do_POST(self) -> None:
            if self.path == "/api/area-check":
                # Read and discard the body: it stands in for a postcode search.
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self._respond(204)
            else:
                self._respond(404)

    return Handler


def main() -> None:
    commit = os.environ.get("VESTAGRAPH_COMMIT", "unknown")
    secret_path = pathlib.Path(
        os.environ.get("VESTAGRAPH_SECRET_CHECK_FILE", DEFAULT_SECRET_CHECK_PATH)
    )
    port = int(os.environ.get("PORT", str(DEFAULT_PORT)))
    load_secret_check(secret_path)  # Fail fast; the value is never printed.
    PlaceholderServer(("0.0.0.0", port), make_handler(commit)).serve_forever()  # noqa: S104
