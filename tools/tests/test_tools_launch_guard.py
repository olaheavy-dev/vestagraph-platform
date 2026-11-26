"""Tests for tools/launch_guard.py (OP-06). No test touches the network: a fake serves the pages."""

import ast
import http.server
import json
import threading
from collections.abc import Iterator, Mapping
from pathlib import Path

import launch_guard
import pytest

BASE = "http://127.0.0.1:8080"
DRAFT = "To be written before launch (SE-02)"
HTML = "text/html; charset=utf-8"

Page = tuple[int, str, bytes]


def _fake(
    pages: Mapping[str, Page | launch_guard.Response], calls: list[str] | None = None
) -> launch_guard.Fetch:
    """A fetch that serves `pages` (no Location unless given); any other URL cannot be read."""

    def fetch(url: str) -> launch_guard.Response:
        if calls is not None:
            calls.append(url)
        if url not in pages:
            raise OSError(f"connection refused: {url}")
        page = pages[url]
        if len(page) == 3:
            return (page[0], page[1], page[2], "")
        return page

    return fetch


def _html(body: str) -> Page:
    return (200, HTML, f"<html><body>{body}</body></html>".encode())


def _strings_file(tmp_path: Path, data: object) -> Path:
    path = tmp_path / "strings.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


# ---- load_strings ----


def test_load_strings_valid_list_returns_strings(tmp_path: Path) -> None:
    assert launch_guard.load_strings(_strings_file(tmp_path, [DRAFT, "Other"])) == [DRAFT, "Other"]


def test_load_strings_empty_list_exits(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        launch_guard.load_strings(_strings_file(tmp_path, []))


def test_load_strings_non_string_entry_exits(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        launch_guard.load_strings(_strings_file(tmp_path, [DRAFT, 3]))


def test_load_strings_blank_entry_exits(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        launch_guard.load_strings(_strings_file(tmp_path, ["  "]))


def test_load_strings_not_json_exits(tmp_path: Path) -> None:
    path = tmp_path / "strings.json"
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(SystemExit):
        launch_guard.load_strings(path)


# ---- find_strings ----


def test_find_strings_exact_text_returns_match() -> None:
    assert launch_guard.find_strings(f"<p>{DRAFT}</p>".encode(), [DRAFT]) == [DRAFT]


def test_find_strings_entities_and_line_breaks_returns_match() -> None:
    body = b"<p>To be written\n      before&nbsp;launch (SE&#45;02)</p>"
    assert launch_guard.find_strings(body, [DRAFT]) == [DRAFT]


def test_find_strings_no_draft_returns_empty() -> None:
    assert launch_guard.find_strings(b"<p>Written in full.</p>", [DRAFT]) == []


def test_find_strings_several_returns_them_in_list_order() -> None:
    other = "Contact details to be added before launch"
    body = f"{other} and {DRAFT}".encode()
    assert launch_guard.find_strings(body, [DRAFT, other]) == [DRAFT, other]


# ---- same_site_links ----


def test_same_site_links_relative_and_absolute_are_resolved() -> None:
    html = '<a href="/privacy">P</a><a href="how-it-works">H</a><a href="http://127.0.0.1:8080/x">X</a>'
    assert launch_guard.same_site_links(f"{BASE}/", html) == [
        f"{BASE}/privacy",
        f"{BASE}/how-it-works",
        f"{BASE}/x",
    ]


def test_same_site_links_other_host_and_mailto_are_dropped() -> None:
    html = (
        '<a href="https://www.gov.uk/flood">G</a><a href="mailto:privacy@vestagraph.co.uk">M</a>'
        '<a href="https://127.0.0.1:8080/other-scheme">S</a><a href="/kept">K</a>'
    )
    assert launch_guard.same_site_links(f"{BASE}/", html) == [f"{BASE}/kept"]


def test_same_site_links_fragment_is_removed() -> None:
    html = '<a href="/privacy#maps">A</a><a href="/privacy">B</a><a href="#top">C</a>'
    assert launch_guard.same_site_links(f"{BASE}/", html) == [f"{BASE}/privacy", f"{BASE}/"]


def test_same_site_links_link_tag_is_followed() -> None:
    html = '<link rel="stylesheet" href="/style.css"><a>no href</a>'
    assert launch_guard.same_site_links(f"{BASE}/", html) == [f"{BASE}/style.css"]


# ---- wait_until_up ----


def test_wait_until_up_answers_on_second_try_returns_true() -> None:
    answers: list[launch_guard.Response | None] = [None, (200, "application/json", b"{}", "")]

    def fetch(url: str) -> launch_guard.Response:
        assert url == f"{BASE}/healthz"
        answer = answers.pop(0)
        if answer is None:
            raise OSError("not yet")
        return answer

    assert launch_guard.wait_until_up(BASE, timeout_s=5, interval_s=0, fetch=fetch) is True


def test_wait_until_up_never_answers_returns_false() -> None:
    assert launch_guard.wait_until_up(BASE, timeout_s=0, interval_s=0, fetch=_fake({})) is False


def test_wait_until_up_non_200_is_not_up() -> None:
    fetch = _fake({f"{BASE}/healthz": (503, "text/plain", b"")})
    assert launch_guard.wait_until_up(BASE, timeout_s=0, interval_s=0, fetch=fetch) is False


# ---- scan_site ----


def test_scan_site_draft_on_linked_page_is_found() -> None:
    pages = {
        f"{BASE}/": _html('<a href="/privacy">Privacy notice</a>'),
        f"{BASE}/privacy": _html(f"<section>{DRAFT}</section>"),
    }
    result = launch_guard.scan_site(BASE, ["/"], [DRAFT], _fake(pages), page_limit=200)
    assert result.findings == [(f"{BASE}/privacy", DRAFT)]
    assert result.errors == []
    assert result.pages_read == 2
    assert result.ok is False


def test_scan_site_clean_pages_is_ok() -> None:
    pages = {f"{BASE}/": _html("Finished text.")}
    result = launch_guard.scan_site(BASE, ["/"], [DRAFT], _fake(pages), page_limit=200)
    assert result.ok is True
    assert result.pages_read == 1


def test_scan_site_404_is_not_an_error() -> None:
    pages = {f"{BASE}/privacy": (404, "", b"")}
    result = launch_guard.scan_site(BASE, ["/privacy"], [DRAFT], _fake(pages), page_limit=200)
    assert result.ok is True
    assert result.pages_read == 1


def test_scan_site_404_body_is_still_checked() -> None:
    pages = {f"{BASE}/x": (404, HTML, DRAFT.encode())}
    result = launch_guard.scan_site(BASE, ["/x"], [DRAFT], _fake(pages), page_limit=200)
    assert result.findings == [(f"{BASE}/x", DRAFT)]


def test_scan_site_server_error_is_reported() -> None:
    pages = {
        f"{BASE}/": _html('<a href="/broken">B</a><a href="/gone">G</a>'),
        f"{BASE}/broken": (500, HTML, b""),
    }
    result = launch_guard.scan_site(BASE, ["/"], [DRAFT], _fake(pages), page_limit=200)
    assert [url for url, _ in result.errors] == [f"{BASE}/broken", f"{BASE}/gone"]
    assert "500" in result.errors[0][1]
    assert result.ok is False


def test_scan_site_cyclic_links_reads_each_page_once() -> None:
    calls: list[str] = []
    pages = {
        f"{BASE}/": _html('<a href="/a">A</a><a href="/">Home</a>'),
        f"{BASE}/a": _html('<a href="/">Home</a><a href="/a#top">Top</a><a href="/a">Self</a>'),
    }
    result = launch_guard.scan_site(BASE, ["/", "/a"], [DRAFT], _fake(pages, calls), page_limit=200)
    assert sorted(calls) == [f"{BASE}/", f"{BASE}/a"]
    assert result.pages_read == 2


def test_scan_site_page_limit_with_pages_left_sets_limit_reached() -> None:
    pages = {
        f"{BASE}/": _html('<a href="/a">A</a><a href="/b">B</a>'),
        f"{BASE}/a": _html(""),
        f"{BASE}/b": _html(""),
    }
    result = launch_guard.scan_site(BASE, ["/"], [DRAFT], _fake(pages), page_limit=2)
    assert result.pages_read == 2
    assert result.limit_reached is True
    assert result.ok is False


def test_scan_site_page_limit_exactly_met_is_ok() -> None:
    pages = {f"{BASE}/": _html('<a href="/a">A</a>'), f"{BASE}/a": _html("")}
    result = launch_guard.scan_site(BASE, ["/"], [DRAFT], _fake(pages), page_limit=2)
    assert result.limit_reached is False
    assert result.ok is True


def test_scan_site_json_page_links_are_not_followed() -> None:
    calls: list[str] = []
    pages = {f"{BASE}/healthz": (200, "application/json", b'{"x": "<a href=\\"/hidden\\">"}')}
    launch_guard.scan_site(BASE, ["/healthz"], [DRAFT], _fake(pages, calls), page_limit=200)
    assert calls == [f"{BASE}/healthz"]


# ---- main ----

_UP = (200, "application/json", b'{"status": "ok"}')


def test_main_clean_site_returns_0(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    pages = {f"{BASE}/healthz": _UP, f"{BASE}/": _html("Done.")}
    monkeypatch.setattr(launch_guard, "fetch_url", lambda url, timeout_s=10: _fake(pages)(url))
    code = launch_guard.main(
        ["--base-url", BASE, "--strings", str(_strings_file(tmp_path, [DRAFT])), "--path", "/"]
    )
    assert code == 0
    assert "Launch guard passed: 1 pages read, no draft text." in capsys.readouterr().out


def test_main_draft_found_returns_1(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    pages = {f"{BASE}/healthz": _UP, f"{BASE}/": _html(DRAFT)}
    monkeypatch.setattr(launch_guard, "fetch_url", lambda url, timeout_s=10: _fake(pages)(url))
    code = launch_guard.main(
        ["--base-url", BASE, "--strings", str(_strings_file(tmp_path, [DRAFT])), "--path", "/"]
    )
    err = capsys.readouterr().err
    assert code == 1
    assert f'{BASE}/: "{DRAFT}"' in err
    assert "Launch guard failed (OP-06)" in err
    assert "Nothing was released." in err


def test_main_default_paths_are_the_four_pages(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[str] = []
    fetch = _fake({f"{BASE}/healthz": _UP}, calls)

    def fake_fetch_url(url: str, timeout_s: int = 10) -> launch_guard.Response:
        try:
            return fetch(url)
        except OSError:
            return (404, "", b"", "")

    monkeypatch.setattr(launch_guard, "fetch_url", fake_fetch_url)
    code = launch_guard.main(
        ["--base-url", BASE, "--strings", str(_strings_file(tmp_path, [DRAFT]))]
    )
    assert code == 0
    assert calls[1:] == [f"{BASE}{p}" for p in ("/", "/how-it-works", "/privacy", "/accessibility")]


def test_main_app_never_starts_returns_1(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(launch_guard, "fetch_url", lambda url, timeout_s=10: _fake({})(url))
    code = launch_guard.main(
        [
            "--base-url",
            BASE,
            "--strings",
            str(_strings_file(tmp_path, [DRAFT])),
            "--start-timeout",
            "0",
        ]
    )
    assert code == 1
    assert "The app did not answer /healthz within 0 s." in capsys.readouterr().err


def test_launch_guard_source_parses_as_python_312() -> None:
    # The runner uses Python 3.12; ast rejects 3.14-only forms (`except A, B:`) for that version.
    source = Path(launch_guard.__file__).read_text(encoding="utf-8")
    ast.parse(source, feature_version=(3, 12))


# ---- review fixes (26 Nov 2026) ----


def test_find_strings_split_by_react_comments_returns_match() -> None:
    body = b"<p>To be written before launch (<!-- -->SE-02<!-- -->)</p>"
    assert launch_guard.find_strings(body, [DRAFT]) == [DRAFT]


def test_find_strings_split_by_inline_tag_returns_match() -> None:
    body = b"<p>To be written <em>before</em> launch (SE-02)</p>"
    assert launch_guard.find_strings(body, [DRAFT]) == [DRAFT]


def test_find_strings_soft_hyphen_and_zero_width_returns_match() -> None:
    body = "<p>To be writ&shy;ten be​fore launch (SE-02)</p>".encode()
    assert launch_guard.find_strings(body, [DRAFT]) == [DRAFT]


def test_find_strings_declared_charset_is_used() -> None:
    body = f"<p>{DRAFT}</p>".encode("utf-16")
    assert launch_guard.find_strings(body, [DRAFT], "text/html; charset=utf-16") == [DRAFT]


def test_find_strings_unknown_charset_falls_back_to_utf8() -> None:
    body = DRAFT.encode()
    assert launch_guard.find_strings(body, [DRAFT], "text/html; charset=nonsense") == [DRAFT]


def test_same_site_links_invalid_url_is_skipped() -> None:
    html = '<a href="http://[bad">X</a><a href="/kept">K</a>'
    assert launch_guard.same_site_links(f"{BASE}/", html) == [f"{BASE}/kept"]


def test_scan_site_fetch_value_error_is_reported() -> None:
    def fetch(url: str) -> launch_guard.Response:
        raise UnicodeEncodeError("ascii", url, 0, 1, "not ascii")

    result = launch_guard.scan_site(BASE, ["/café"], [DRAFT], fetch, page_limit=200)
    assert [url for url, _ in result.errors] == [f"{BASE}/café"]


def test_scan_site_same_site_redirect_is_followed() -> None:
    pages: dict[str, launch_guard.Response] = {
        f"{BASE}/old": (302, "", b"", "/privacy"),
        f"{BASE}/privacy": (200, HTML, DRAFT.encode(), ""),
    }
    result = launch_guard.scan_site(BASE, ["/old"], [DRAFT], _fake(pages), page_limit=200)
    assert result.findings == [(f"{BASE}/privacy", DRAFT)]
    assert result.errors == []


def test_scan_site_other_site_redirect_is_not_followed() -> None:
    calls: list[str] = []
    pages: dict[str, launch_guard.Response] = {
        f"{BASE}/privacy": (301, "", b"", "https://vestagraph.com/privacy"),
    }
    result = launch_guard.scan_site(BASE, ["/privacy"], [DRAFT], _fake(pages, calls), 200)
    assert calls == [f"{BASE}/privacy"]
    assert result.ok is True


# ---- fetch_url against a real local server ----


class _Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        routes: dict[str, tuple[int, dict[str, str], bytes]] = {
            "/ok": (200, {"Content-Type": HTML}, b"hello"),
            "/missing": (404, {"Content-Type": HTML}, b"no page"),
            "/moved": (302, {"Location": "https://vestagraph.com/elsewhere"}, b""),
            "/huge": (200, {"Content-Type": HTML}, b"x" * (launch_guard.MAX_BODY_BYTES + 1)),
        }
        status, headers, body = routes.get(self.path, (500, {}, b""))
        self.send_response(status)
        for name, value in headers.items():
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        pass


@pytest.fixture
def local_server() -> Iterator[str]:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()


def test_fetch_url_200_returns_status_type_and_body(local_server: str) -> None:
    assert launch_guard.fetch_url(local_server + "/ok") == (200, HTML, b"hello", "")


def test_fetch_url_404_is_returned_not_raised(local_server: str) -> None:
    assert launch_guard.fetch_url(local_server + "/missing") == (404, HTML, b"no page", "")


def test_fetch_url_redirect_is_not_followed(local_server: str) -> None:
    status, _, _, location = launch_guard.fetch_url(local_server + "/moved")
    assert (status, location) == (302, "https://vestagraph.com/elsewhere")


def test_fetch_url_body_over_limit_raises(local_server: str) -> None:
    with pytest.raises(OSError, match="larger than"):
        launch_guard.fetch_url(local_server + "/huge")


# ---- Codex review fixes (26 Nov 2026) ----


def test_find_strings_br_between_words_returns_match() -> None:
    body = b"<p>To be written<br>before launch (SE-02)</p>"
    assert launch_guard.find_strings(body, [DRAFT]) == [DRAFT]


def test_find_strings_block_elements_between_words_returns_match() -> None:
    body = b"<div>To be written</div><div>before launch (SE-02)</div>"
    assert launch_guard.find_strings(body, [DRAFT]) == [DRAFT]


def test_scan_site_self_redirect_is_reported() -> None:
    pages: dict[str, launch_guard.Response] = {f"{BASE}/privacy": (302, "", b"", "/privacy")}
    result = launch_guard.scan_site(BASE, ["/privacy"], [DRAFT], _fake(pages), page_limit=200)
    assert [url for url, _ in result.errors] == [f"{BASE}/privacy"]
    assert "redirect loop" in result.errors[0][1]
    assert result.ok is False


def test_scan_site_two_page_redirect_cycle_is_reported() -> None:
    pages: dict[str, launch_guard.Response] = {
        f"{BASE}/privacy": (301, "", b"", "/privacy/"),
        f"{BASE}/privacy/": (301, "", b"", "/privacy"),
    }
    result = launch_guard.scan_site(BASE, ["/privacy"], [DRAFT], _fake(pages), page_limit=200)
    assert result.errors
    assert all("redirect loop" in reason for _, reason in result.errors)
    assert result.ok is False


def test_scan_site_long_redirect_chain_is_reported() -> None:
    pages: dict[str, launch_guard.Response] = {
        f"{BASE}/r{i}": (302, "", b"", f"/r{i + 1}") for i in range(launch_guard.MAX_REDIRECTS + 2)
    }
    result = launch_guard.scan_site(BASE, ["/r0"], [DRAFT], _fake(pages), page_limit=200)
    assert [url for url, _ in result.errors] == [f"{BASE}/r0"]
    assert result.ok is False


def test_scan_site_redirect_to_page_already_read_is_ok() -> None:
    pages: dict[str, launch_guard.Response] = {
        f"{BASE}/": (200, HTML, b"<p>Done.</p>", ""),
        f"{BASE}/home": (302, "", b"", "/"),
    }
    result = launch_guard.scan_site(BASE, ["/", "/home"], [DRAFT], _fake(pages), page_limit=200)
    assert result.ok is True
