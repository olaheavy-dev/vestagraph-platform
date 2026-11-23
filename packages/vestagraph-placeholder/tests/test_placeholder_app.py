"""Tests for the placeholder app. Each starts a real server on a free port."""

import contextlib
import http.client
import json
import os
import pathlib
import socket
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


def raw_response(port: int, raw: bytes) -> tuple[int, bytes, bytes]:
    """Send raw bytes; return the status, the lower-cased header block and the body."""
    with socket.create_connection(("127.0.0.1", port), timeout=5) as sock:
        sock.sendall(raw)
        data = b""
        while chunk := sock.recv(4096):
            data += chunk
    head, _, body = data.partition(b"\r\n\r\n")
    return int(head.split(b" ")[1]), head.lower(), body


def raw_status(port: int, raw: bytes) -> tuple[int, bytes]:
    status, head, body = raw_response(port, raw)
    assert b"cache-control: no-store" in head
    return status, body


@pytest.mark.parametrize("length", ["-5", "abc"])
def test_area_check_post_with_bad_content_length_returns_400(
    length: str, capfd: pytest.CaptureFixture[str]
) -> None:
    raw = f"POST /api/area-check HTTP/1.1\r\nContent-Length: {length}\r\n\r\n".encode()
    with running_server(app.make_handler("abc123")) as port:
        status, body = raw_status(port, raw)
    captured = capfd.readouterr()
    assert status == 400
    assert body == b""
    assert captured.out + captured.err == ""


def test_unsupported_method_returns_501_empty_no_store_and_logs_nothing(
    capfd: pytest.CaptureFixture[str],
) -> None:
    raw = b"PUT /healthz?postcode=ZZ99 HTTP/1.1\r\nContent-Length: 0\r\n\r\n"
    with running_server(app.make_handler("abc123")) as port:
        status, body = raw_status(port, raw)
    captured = capfd.readouterr()
    assert status == 501
    assert body == b""
    assert captured.out + captured.err == ""


def test_load_secret_check_non_utf8_file_exits_without_value(
    tmp_path: pathlib.Path,
) -> None:
    bad = tmp_path / "secret_check"
    bad.write_bytes(b"\xff\xfe\xfa")
    with pytest.raises(SystemExit) as caught:
        app.load_secret_check(bad)
    assert str(bad) in str(caught.value)


def test_area_check_post_with_too_large_content_length_returns_413_empty_and_logs_nothing(
    capfd: pytest.CaptureFixture[str],
) -> None:
    raw = b"POST /api/area-check HTTP/1.1\r\nContent-Length: 16385\r\n\r\n"
    with running_server(app.make_handler("abc123")) as port:
        status, body = raw_status(port, raw)
    captured = capfd.readouterr()
    assert status == 413
    assert body == b""
    assert captured.out + captured.err == ""


def test_area_check_post_at_the_size_limit_returns_204() -> None:
    body = b"x" * app.MAX_BODY_BYTES
    with running_server(app.make_handler("abc123")) as port:
        status, _, _ = request(port, "POST", "/api/area-check", body)
    assert status == 204


def test_area_check_post_with_huge_digit_string_returns_413_and_logs_nothing(
    capfd: pytest.CaptureFixture[str],
) -> None:
    raw = b"POST /api/area-check HTTP/1.1\r\nContent-Length: " + b"9" * 5000 + b"\r\n\r\n"
    with running_server(app.make_handler("abc123")) as port:
        status, body = raw_status(port, raw)
    captured = capfd.readouterr()
    assert status == 413
    assert body == b""
    assert captured.out + captured.err == ""


def test_response_server_header_does_not_name_python() -> None:
    with running_server(app.make_handler("abc123")) as port:
        _, headers, _ = request(port, "GET", "/healthz")
    assert "Python" not in headers["Server"]
    assert headers["Server"] == "vestagraph"


def test_handler_has_a_connection_timeout() -> None:
    handler = app.make_handler("abc123")
    assert handler.timeout == 10


def test_malformed_request_line_gets_no_body_and_logs_nothing(
    capfd: pytest.CaptureFixture[str],
) -> None:
    # A single word is read as an HTTP/0.9 request: the standard library sends the 400 without
    # headers, so the raw reply is empty or a bare 400 status line with no body.
    with (
        running_server(app.make_handler("abc123")) as port,
        socket.create_connection(("127.0.0.1", port), timeout=5) as sock,
    ):
        sock.sendall(b"GARBAGE\r\n\r\n")
        data = b""
        while chunk := sock.recv(4096):
            data += chunk
    captured = capfd.readouterr()
    assert data == b"" or data.startswith(b"HTTP/1.0 400")
    assert b"<" not in data
    assert captured.out + captured.err == ""


def test_main_missing_secret_exits_before_binding_the_server(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path
) -> None:
    created: list[object] = []

    class Spy:
        def __init__(self, *args: object, **kwargs: object) -> None:
            created.append(args)

    monkeypatch.setattr(app, "PlaceholderServer", Spy)
    monkeypatch.setenv("VESTAGRAPH_SECRET_CHECK_FILE", str(tmp_path / "missing"))
    with pytest.raises(SystemExit):
        app.main()
    assert created == []


@pytest.mark.parametrize(
    ("method", "path"),
    [("GET", "/healthz"), ("GET", "/missing"), ("POST", "/api/area-check"), ("DELETE", "/")],
)
def test_respond_any_route_sends_nosniff_header(method: str, path: str) -> None:
    with running_server(app.make_handler("abc123")) as port:
        _, headers, _ = request(port, method, path, body=b"" if method == "POST" else None)
    assert headers["X-Content-Type-Options"] == "nosniff"


@pytest.mark.parametrize(("length", "expected"), [("abc", 400), ("99999999", 413)])
def test_respond_rejected_area_check_sends_nosniff_header(length: str, expected: int) -> None:
    raw = f"POST /api/area-check HTTP/1.1\r\nContent-Length: {length}\r\n\r\n".encode()
    with running_server(app.make_handler("abc123")) as port:
        status, head, _ = raw_response(port, raw)
    assert status == expected
    assert b"x-content-type-options: nosniff" in head
