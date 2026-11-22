"""Tests for tools/release_check.py (stage 5b group A, task 3). No test touches the network."""

import ast
import http.client
import json
from pathlib import Path

import pytest
import release_check

COMMIT = "abc123"
URL = "https://example.invalid/healthz"


def _body(status: str = "ok", commit: str = COMMIT) -> bytes:
    return json.dumps({"status": status, "commit": commit}).encode()


def test_is_live_matching_commit_returns_true() -> None:
    assert release_check.is_live(_body(), COMMIT) is True


def test_is_live_other_commit_returns_false() -> None:
    assert release_check.is_live(_body(commit="old999"), COMMIT) is False


def test_is_live_invalid_json_returns_false() -> None:
    assert release_check.is_live(b"<html>challenge</html>", COMMIT) is False


def test_is_live_status_not_ok_returns_false() -> None:
    assert release_check.is_live(_body(status="starting"), COMMIT) is False


def test_is_live_json_not_an_object_returns_false() -> None:
    assert release_check.is_live(b"[1, 2]", COMMIT) is False


def test_wait_for_commit_becomes_live_on_third_poll_returns_true() -> None:
    bodies = [_body(commit="old999"), _body(commit="old999"), _body()]
    calls: list[str] = []

    def fetch(url: str) -> bytes:
        calls.append(url)
        return bodies[len(calls) - 1]

    assert release_check.wait_for_commit(URL, COMMIT, 60, 0, fetch) is True
    assert calls == [URL, URL, URL]


def test_wait_for_commit_fetch_errors_until_timeout_returns_false() -> None:
    def fetch(url: str) -> bytes:
        raise OSError("connection refused")

    assert release_check.wait_for_commit(URL, COMMIT, 0, 0, fetch) is False


def test_wait_for_commit_dropped_connection_then_live_returns_true() -> None:
    results: list[bytes | Exception] = [http.client.IncompleteRead(b""), _body()]

    def fetch(url: str) -> bytes:
        result = results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    assert release_check.wait_for_commit(URL, COMMIT, 60, 0, fetch) is True


def test_main_not_live_returns_one_with_rollback_message(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(release_check, "wait_for_commit", lambda *a, **k: False)
    code = release_check.main(["--url", URL, "--commit", COMMIT, "--timeout", "5"])
    assert code == 1
    assert capsys.readouterr().err.strip() == (
        f"{URL} did not report {COMMIT} within 5 s; "
        "to roll back, run the Images workflow with an earlier commit"
    )


def test_main_live_returns_zero_with_message(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(release_check, "wait_for_commit", lambda *a, **k: True)
    code = release_check.main(["--url", URL, "--commit", COMMIT])
    assert code == 0
    assert capsys.readouterr().out.strip() == f"{URL} reports {COMMIT}"


def test_release_check_source_python_312_parses() -> None:
    # The runner uses Python 3.12; ast rejects 3.14-only forms (`except A, B:`) for that version.
    source = Path(release_check.__file__).read_text(encoding="utf-8")
    ast.parse(source, feature_version=(3, 12))
