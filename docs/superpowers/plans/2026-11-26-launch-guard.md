# Launch guard (OP-06) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The release job fails, before the image is pushed, while any listed draft string ("To be written before launch (SE-02)" and the others) is in the pages the new image serves.

**Architecture:** A list file of exact draft strings, kept in step with the specifications by a test. A standard-library Python tool starts from a base URL, waits for `/healthz`, reads a fixed set of paths plus same-site links, and reports every draft string found or page it could not read. A new step in the release job runs the freshly built image on the runner and runs `main`'s copy of the tool against it.

**Tech Stack:** Python standard library only (`urllib`, `html`, `html.parser`), runnable on the runner's Python 3.12; pytest; GitHub Actions; Docker.

**Spec:** `docs/superpowers/specs/2026-11-26-launch-guard-design.md`

## Global Constraints

- The tool uses the standard library only and Python 3.12 syntax (the runner's `python3`); add it to `per-file-target-version` in `pyproject.toml` as `tools/release_check.py` is.
- No test touches the network: the tool takes a `fetch` function, and tests pass a fake.
- Default fixed paths: `/`, `/how-it-works`, `/privacy`, `/accessibility`. Page limit 200. Start-up timeout 60 s. Per-page timeout 10 s.
- "Could not check" is never a pass: start-up timeout, a failed fetch, a status other than 200 or 404, or reaching the page limit with pages left all fail the guard.
- A 404 means "no page here": its body is still checked; it is not an error.
- Test names follow `test_<method>_<condition>_<result>`.
- The release step uses `main`'s copy of the tool and list (copied before the checkout of the released commit).
- No agent attribution in commits or the pull request.

## Review Focus

- A draft string split across lines or with HTML entities (`&#39;`, `&amp;`, `&nbsp;`) in the page: still found. Test in Task 2 (`test_find_strings_entities_and_line_breaks_returns_match`).
- A page that links to itself, back to `/`, or with `#fragment` variants: read once, no loop. Test in Task 2 (`test_scan_site_cyclic_links_reads_each_page_once`).
- A link to another site (`https://gov.uk/...`) or a `mailto:` link: never fetched. Test in Task 2 (`test_same_site_links_other_host_and_mailto_are_dropped`).
- The app never answers `/healthz` (it crashed on start): the guard fails with a clear message, not a pass. Test in Task 2 (`test_main_app_never_starts_returns_1`).
- A page answering 500 or timing out: reported as an error and the guard fails. Test in Task 2 (`test_scan_site_server_error_is_reported`).

---

### Task 1: The list of draft strings and its sync test

**Files:**
- Create: `tools/launch_placeholders.json`
- Create: `tools/tests/test_tools_launch_placeholders.py`

**Interfaces:**
- Produces: `tools/launch_placeholders.json`, a JSON array of non-empty strings, read by Task 2's `load_strings`.

- [ ] **Step 1: Write the failing test** `test_specs_every_before_launch_string_is_in_the_list`: read every `docs/specs/**/*.feature` (path from the repository root, found from `Path(__file__)`), collect each match of `"([^"\n]*before launch[^"\n]*)"`, and assert each is in the JSON list; the failure message names the file and line of each missing string. Also `test_list_entries_are_unique_non_empty_strings`.
- [ ] **Step 2: Run** `uv run --locked pytest tools/tests/test_tools_launch_placeholders.py -v`. Expected: FAIL (file not found).
- [ ] **Step 3: Create the list** with exactly these four entries: `"To be written before launch (SE-02)"`, `"Contact details to be added before launch"`, `"To be completed after testing, before launch"`, `"Draft wording, to be confirmed before launch (0057)."`
- [ ] **Step 4: Run** the same command. Expected: PASS.
- [ ] **Step 5: Commit** `test: launch guard draft-string list kept in step with the specifications (OP-06)`

### Task 2: The guard tool

**Files:**
- Create: `tools/launch_guard.py`
- Create: `tools/tests/test_tools_launch_guard.py`
- Modify: `pyproject.toml` (add `"tools/launch_guard.py" = "py312"` to `per-file-target-version`)

**Interfaces:**
- Consumes: `tools/launch_placeholders.json` (Task 1).
- Produces, all in `launch_guard`:
  - `Fetch = Callable[[str], tuple[int, str, bytes]]`: returns (status, content type, body); raises `OSError` or `http.client.HTTPException` when the page cannot be read.
  - `fetch_url(url: str, timeout_s: int = 10) -> tuple[int, str, bytes]`: the real one; an `urllib.error.HTTPError` is returned as its status and body, not raised.
  - `load_strings(path: Path) -> list[str]`: raises `SystemExit` with a message if the file is not a non-empty JSON array of non-empty strings.
  - `normalise(text: str) -> str`: `html.unescape`, then every run of whitespace (including the non-breaking space) becomes one space.
  - `find_strings(body: bytes, strings: Sequence[str]) -> list[str]`: decodes UTF-8 with `errors="replace"`, normalises body and each string, returns the strings found, in list order.
  - `same_site_links(page_url: str, html_text: str) -> list[str]`: `href` values from `<a>` and `<link>` resolved with `urljoin`, fragment removed, kept only when scheme and host match `page_url`; in first-seen order, no duplicates.
  - `wait_until_up(base_url: str, timeout_s: int, interval_s: float, fetch: Fetch) -> bool`: True once `base_url + "/healthz"` returns 200; always tries at least once; a raised error counts as "not up yet".
  - `ScanResult` (frozen dataclass): `pages_read: int`, `findings: list[tuple[str, str]]` (url, string), `errors: list[tuple[str, str]]` (url, reason), `limit_reached: bool`; property `ok -> bool` is True only when findings and errors are empty and the limit was not reached.
  - `scan_site(base_url: str, paths: Sequence[str], strings: Sequence[str], fetch: Fetch, page_limit: int) -> ScanResult`: breadth-first from the fixed paths; 200 → check the body, follow links only if the content type starts with `text/html`; 404 → check the body only; any other status or a raised error → an error entry; each URL read once; `limit_reached` is True when unread URLs remain after `page_limit` pages.
  - `main(argv: Sequence[str] | None = None) -> int`: options `--base-url` (required), `--strings` (required path), `--path` (repeatable; default the four fixed paths), `--start-timeout` 60, `--page-timeout` 10, `--page-limit` 200. Prints each finding as `<url>: "<string>"` and each error as `<url>: <reason>` to stderr, ending with `Launch guard failed (OP-06): draft text or unread pages. Nothing was released.`; on success prints `Launch guard passed: <n> pages read, no draft text.` Returns 1 if the app does not start in time (message `The app did not answer /healthz within <n> s.`), 0 or 1 from `ScanResult.ok` otherwise.

- [ ] **Step 1: Write the failing tests** with a fake fetch built from a dict `{url: (status, content_type, body)}` (a missing URL raises `OSError`):
  - `test_load_strings_valid_list_returns_strings`; `test_load_strings_empty_list_exits`; `test_load_strings_non_string_entry_exits`
  - `test_find_strings_exact_text_returns_match`; `test_find_strings_entities_and_line_breaks_returns_match` (body `To be written\n  before launch (SE&#45;02)` style and `&nbsp;`); `test_find_strings_no_draft_returns_empty`
  - `test_same_site_links_relative_and_absolute_are_resolved`; `test_same_site_links_other_host_and_mailto_are_dropped`; `test_same_site_links_fragment_is_removed`
  - `test_wait_until_up_answers_on_second_try_returns_true`; `test_wait_until_up_never_answers_returns_false`
  - `test_scan_site_draft_on_linked_page_is_found` (`/` links to `/privacy`, which holds `To be written before launch (SE-02)`; finding is `("http://127.0.0.1:8080/privacy", "To be written before launch (SE-02)")`)
  - `test_scan_site_404_is_not_an_error`; `test_scan_site_server_error_is_reported` (500 and a raised `OSError`); `test_scan_site_cyclic_links_reads_each_page_once`; `test_scan_site_page_limit_with_pages_left_sets_limit_reached`; `test_scan_site_json_page_links_are_not_followed`
  - `test_main_clean_site_returns_0`; `test_main_draft_found_returns_1`; `test_main_app_never_starts_returns_1` (patch `fetch_url` and use `--start-timeout 0`)
  - `test_launch_guard_source_parses_as_python_312` (as the release check's test does, if it has one; otherwise `ast.parse(source, feature_version=(3, 12))`)
- [ ] **Step 2: Run** `uv run --locked pytest tools/tests/test_tools_launch_guard.py -v`. Expected: FAIL (`ModuleNotFoundError: launch_guard`).
- [ ] **Step 3: Implement** the interfaces above in `tools/launch_guard.py`, module docstring in the style of `release_check.py`. Link parsing uses `html.parser.HTMLParser`.
- [ ] **Step 4: Run** the same command, then `make check`. Expected: all PASS.
- [ ] **Step 5: Commit** `feat: launch guard tool reads a site's pages for draft text (OP-06)`

### Task 3: Run the guard in the release job, and the records

**Files:**
- Modify: `.github/workflows/images.yml` (paths list; the "Keep this run's release check" step; a new step after "Build the image from the approved commit")
- Modify: `deploy/README.md` (the release paragraph)
- Modify: `docs/decisions/README.md` (the OP-06 line)
- Modify: `docs/planning/status.md`

**Interfaces:**
- Consumes: `python3 "$RUNNER_TEMP/launch_guard.py" --base-url http://127.0.0.1:8080 --strings "$RUNNER_TEMP/launch_placeholders.json"` (Task 2); exit 0 means pass.

- [ ] **Step 1: Paths.** Add `tools/launch_guard.py` and `tools/launch_placeholders.json` to `&image-paths`.
- [ ] **Step 2: Keep main's copy.** Rename the step to "Keep this run's release check and launch guard" and also copy `tools/launch_guard.py` and `tools/launch_placeholders.json` to `$RUNNER_TEMP`.
- [ ] **Step 3: The new step** "Check the new image's pages for draft text (launch guard, OP-06)", before "Log in to GHCR": make a temporary folder, write a throwaway value to `secret_check` there (mode 644, so the image's user 10001 can read it); `docker run -d --name launch-guard --read-only --cap-drop ALL --security-opt no-new-privileges:true -p 127.0.0.1:8080:8080 -v "<file>:/run/secrets/secret_check:ro" "${LIVE_IMAGE}:sha-${COMMIT}"`; run the guard, keeping its exit code; on failure print `docker logs launch-guard`; always `docker rm -f launch-guard`; exit with the guard's code. Add a comment naming OP-06 and the design doc.
- [ ] **Step 4: Verify locally** that the step's commands work against the placeholder: `docker build -f deploy/placeholder.Dockerfile --build-arg VESTAGRAPH_COMMIT=test -t launch-guard-test .`, run it as in Step 3 (with the local tag), run the guard. Expected: `Launch guard passed: 4 pages read, no draft text.` Then show it fails: run the guard with `--path /healthz` and a temporary strings file (in the scratchpad) holding `["status"]`, a word the health page contains. Expected: exit 1, naming `http://127.0.0.1:8080/healthz` and `"status"`. Remove the container and the image.
- [ ] **Step 5: Lint the workflow** with the repository's workflow lint (`make check` does not cover it; run what `.github/workflows/workflow-lint.yml` runs, such as actionlint and zizmor, if installed; otherwise rely on the pull request's check).
- [ ] **Step 6: Records.** OP-06 line: add "Built 26 Nov 2026: runs at release only, before the push, against the new image's pages (founder: "Release only (Recommended)", "Now, wired into the release (Recommended)", "A. Run image, read pages (Recommended)"); design `docs/superpowers/specs/2026-11-26-launch-guard-design.md`." `deploy/README.md`: say a release can stop at the launch guard, that its log names each page and string, and that the fix is to write the text (or, for a rollback, choose a commit without drafts); add the two tool files to the list of paths that start a release. Status file: launch guard done (pending the founder's merge, which also queues a release that tests the step for real); next is #86 and #93.
- [ ] **Step 7: Run** `make check`. Expected: PASS.
- [ ] **Step 8: Commit** `ci: run the launch guard before a release is pushed (OP-06)`

## After the tasks

- Pre-flight check: search for `OP-06`, `launch guard`, `release_check.py` and the image paths list in docs, and update any stale statement.
- Pre-push review (fresh-context Opus, Code Review Rules) with `code-security-reviewer`; then the pull request (founder merges: `images.yml`). Merging queues a release (the workflow file changed): the founder approves it, and its log should show `Launch guard passed: 4 pages read, no draft text.`
