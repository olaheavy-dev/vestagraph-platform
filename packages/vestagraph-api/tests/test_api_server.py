"""The real server command (deploy/api.Dockerfile CMD) must not log a path or client address.

Decision 0014: a postcode in a URL must never reach logs. uvicorn logs a rejected WebSocket upgrade
on its own logger, with path, query string and client address, unless WebSocket handling is off
(--ws none).
"""

import contextlib
import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parents[3]
DOCKERFILE = REPO_ROOT / "deploy" / "api.Dockerfile"


def _image_command() -> list[str]:
    match = re.search(r"^CMD (\[.*\])\s*$", DOCKERFILE.read_text(), re.MULTILINE)
    assert match, "no JSON CMD in deploy/api.Dockerfile"
    command: list[str] = json.loads(match.group(1))
    return command


def _local_arguments(command: list[str], port: int) -> list[str]:
    arguments = list(command)
    arguments[arguments.index("--host") + 1] = "127.0.0.1"
    arguments[arguments.index("--port") + 1] = str(port)
    assert arguments[0] == "uvicorn"
    return [sys.executable, "-m", *arguments]


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def test_server_command_websocket_upgrade_logs_no_path_or_address() -> None:
    port = _free_port()
    environment = {
        **os.environ,
        "APP_ENV": "production",
        "LOG_JSON": "true",
        "ENV_FILE": "",
        "FIXTURES_DIR": str(REPO_ROOT / "packages" / "fixtures"),
    }
    server = subprocess.Popen(  # noqa: S603 - fixed command from our own Dockerfile
        _local_arguments(_image_command(), port),
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        deadline = time.monotonic() + 30
        while True:
            assert server.poll() is None, "server exited before it was ready"
            try:
                if httpx.get(f"http://127.0.0.1:{port}/healthz", timeout=1).status_code == 200:
                    break
            except httpx.HTTPError:
                pass
            assert time.monotonic() < deadline, "server not ready in 30 seconds"
            time.sleep(0.1)

        request = (
            "GET /api/area-check?postcode=NB14XY HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{port}\r\n"
            "Connection: Upgrade\r\nUpgrade: websocket\r\n"
            "Sec-WebSocket-Version: 13\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n\r\n"
        )
        with socket.create_connection(("127.0.0.1", port), timeout=5) as client:
            client.sendall(request.encode())
            client.settimeout(5)
            with contextlib.suppress(OSError):
                client.recv(4096)
        time.sleep(0.5)  # let the server finish logging before it is stopped
    finally:
        server.terminate()
        try:
            stdout, stderr = server.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
            stdout, stderr = server.communicate()

    # The start-up line names the bind address (127.0.0.1 here); it is not request data.
    output = "\n".join(
        line for line in (stdout + stderr).splitlines() if "Uvicorn running on" not in line
    )
    for forbidden in ("NB14XY", "postcode=", "127.0.0.1"):
        assert forbidden not in output, f"{forbidden!r} found in server output:\n{output}"
