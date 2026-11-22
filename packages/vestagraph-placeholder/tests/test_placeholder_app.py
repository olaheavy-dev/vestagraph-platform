"""Tests for the placeholder app. Each starts a real server on a free port."""

import contextlib
import http.client
import json
import os
import pathlib
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler

import pytest
from vestagraph_placeholder import app


@contextmanager
def running_server(handler: type[BaseHTTPRequestHandler]) -> Iterator[int]:
    server = app.PlaceholderServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server.server_address[1]
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def request(
    port: int, method: str, path: str, body: bytes | None = None
) -> tuple[int, http.client.HTTPMessage, bytes]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        connection.request(method, path, body=body)
        response = connection.getresponse()
        return response.status, response.headers, response.read()
    finally:
        connection.close()


def test_healthz_get_returns_status_and_commit() -> None:
    with running_server(app.make_handler("abc123")) as port:
        status, headers, body = request(port, "GET", "/healthz")
    assert status == 200
    assert headers["Content-Type"] == "application/json"
    assert headers["Cache-Control"] == "no-store"
    assert json.loads(body) == {"status": "ok", "commit": "abc123"}


def test_area_check_post_with_postcode_body_returns_204_and_logs_nothing(
    capfd: pytest.CaptureFixture[str],
) -> None:
    with running_server(app.make_handler("abc123")) as port:
        status, headers, body = request(
            port, "POST", "/api/area-check", b'{"postcode": "ZZ99 9ZZ"}'
        )
    captured = capfd.readouterr()
    output = captured.out + captured.err
    assert status == 204
    assert headers["Cache-Control"] == "no-store"
    assert body == b""
    for forbidden in ("ZZ99", "127.0.0.1", "/api/area-check"):
        assert forbidden not in output


def test_unknown_path_with_postcode_query_returns_404_and_logs_nothing(
    capfd: pytest.CaptureFixture[str],
) -> None:
    with running_server(app.make_handler("abc123")) as port:
        status, headers, body = request(port, "GET", "/?postcode=ZZ99%209ZZ")
    captured = capfd.readouterr()
    output = captured.out + captured.err
    assert status == 404
    assert headers["Cache-Control"] == "no-store"
    assert body == b""
    for forbidden in ("ZZ99", "postcode", "127.0.0.1"):
        assert forbidden not in output


def test_handler_exception_logs_no_client_address(
    capfd: pytest.CaptureFixture[str],
) -> None:
    class Failing(app.make_handler("abc123")):  # type: ignore[misc]
        def do_GET(self) -> None:  # noqa: N802
            raise RuntimeError("boom")

    # The server drops the connection after the failure.
    with (
        running_server(Failing) as port,
        contextlib.suppress(http.client.HTTPException, OSError),
    ):
        request(port, "GET", "/healthz")
    captured = capfd.readouterr()
    output = captured.out + captured.err
    assert "request failed" in output
    for forbidden in ("127.0.0.1", "/healthz", "boom", "Traceback"):
        assert forbidden not in output


def test_load_secret_check_missing_file_exits_without_value(
    tmp_path: pathlib.Path,
) -> None:
    missing = tmp_path / "secret_check"
    with pytest.raises(SystemExit) as caught:
        app.load_secret_check(missing)
    assert str(missing) in str(caught.value)


def test_load_secret_check_empty_file_exits(tmp_path: pathlib.Path) -> None:
    empty = tmp_path / "secret_check"
    empty.write_text("")
    with pytest.raises(SystemExit) as caught:
        app.load_secret_check(empty)
    assert str(empty) in str(caught.value)


def test_load_secret_check_directory_exits(tmp_path: pathlib.Path) -> None:
    with pytest.raises(SystemExit) as caught:
        app.load_secret_check(tmp_path)
    assert str(tmp_path) in str(caught.value)


@pytest.mark.skipif(os.geteuid() == 0, reason="root can read mode 000 files")
def test_load_secret_check_unreadable_file_exits(tmp_path: pathlib.Path) -> None:
    locked = tmp_path / "secret_check"
    locked.write_text("hunter2-value")
    locked.chmod(0o000)
    try:
        with pytest.raises(SystemExit) as caught:
            app.load_secret_check(locked)
    finally:
        locked.chmod(0o600)
    assert str(locked) in str(caught.value)
    assert "hunter2-value" not in str(caught.value)


def test_load_secret_check_present_returns_value(tmp_path: pathlib.Path) -> None:
    present = tmp_path / "secret_check"
    present.write_text("the-value\n")
    assert app.load_secret_check(present) == "the-value"
