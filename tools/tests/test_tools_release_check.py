"""Tests for tools/release_check.py (stage 5b group A, task 3). No test touches the network."""

import json

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
