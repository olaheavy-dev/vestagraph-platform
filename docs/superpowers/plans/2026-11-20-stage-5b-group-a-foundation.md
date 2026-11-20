# Stage 5b group A (the foundation): implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove the pilot's foundation end to end with a placeholder app (a health page only): an approved release, a rollback, encrypted secrets, logs free of IP addresses and postcodes, a Neon database with a tried restore, and alerts, so the eight launch blockers in the design are closed before the app shell (#86) and the API (#93) exist.

**Architecture:** This repository gets a tiny standard-library Python app, its container build, a Compose file with placeholders and one workflow that builds images, pushes them to GHCR by commit and, after the founder's approval in the `production` environment, tags one image `production`. The server's own Watchtower instance follows only that tag. Everything about the server, Cloudflare and secrets is done in the founder's private infrastructure repository, under its own rules; this plan names that work but never its contents.

**Tech Stack:** Python 3.14 standard library (`http.server`, `urllib`), Docker and Docker Compose, GitHub Actions with the `docker` command line only (no new actions), GHCR, Watchtower, Caddy, Cloudflare (proxy and one rate-limit rule), SOPS with age, Neon (PostgreSQL with PostGIS).

**Spec:** [`docs/superpowers/specs/2026-11-19-stage-5b-foundation-design.md`](../specs/2026-11-19-stage-5b-foundation-design.md), decision [0060](../../decisions/0060-pilot-foundation-hosting-and-database.md).

**When:** written 20 Nov 2026; **built once groups B to D are decided** (0046: decisions first; design, "Building starts once groups B to D are decided"). Task 1 to Task 4 may be built earlier only if the founder says so.

## Founder's choices on this plan (20 Nov 2026, prompt window)
- **Secrets after a reboot:** "Re-run after reboot (Recommended)": the decryption key stays only on the founder's machine; after a reboot the secrets play is run again (runbook step), and the uptime check alerts if it was missed.
- **The server's public address:** "Lock and proxy all apps" (over the agent's "Lock Vestagraph only"): Caddy answers Vestagraph only through Cloudflare (the origin lock), and the founder's other apps move to proxied records too, so the address stops being published (Task 8).
- **How to build:** "Subagent-driven (Recommended)".

## Global Constraints
- Never in a tracked file of this repository: a server address, hostname, credential, private repository path, the retired app's name, or anything copied from the private infrastructure repository (0022, `AGENTS.md`).
- No visitor IP address or searched postcode in our server, Caddy or app logs; no postcode in Cloudflare's logs (0014, 0046). Postcodes travel in the request body or the URL fragment, never the path or query string.
- Images are tagged `sha-<full commit>` and `production` only. Never `latest`, never `main`.
- A merged change reaches the live site only after the founder approves the `production` environment.
- No new packages and no new third-party actions: the placeholder uses the standard library only; the workflow uses `actions/checkout` (already pinned) and the `docker` command line on the runner. FastAPI and its packages wait for #93 (0049).
- Neon: Frankfurt region, Launch plan, one Vestagraph project, autoscaling capped at 0.25 compute units, history window 7 days, PostGIS installed, TLS connections only.
- Spending alert at Neon about $25 a month for Vestagraph (design, "Monitoring and spending").
- Live address `vestagraph.com`; `vestagraph.co.uk` redirects to it. Environments: the founder's laptop and live only.
- Test names follow `test_<method>_<condition>_<result>` (0039). `make check` passes before every push.
- Founder merges: the pull request that adds the workflow (CI permissions, `packages: write`) and any change to repository settings (the `production` environment). Agents merge in the private infrastructure repository after review and tests (0060 point 9); destructive steps get one last confirmation first.

## Review Focus
1. **The server's address is already public.** The founder's other apps use DNS-only Cloudflare records, so proxying Vestagraph does not hide the server's address, and anyone can send a request straight to the server with `Host: vestagraph.com`, skipping Cloudflare's rate limit. Expected: the server answers Vestagraph's hosts only for requests that come from Cloudflare's address ranges (Task 7, the origin lock), and Task 7's check proves a direct request is refused.
2. **The approved commit has no image, or Watchtower never pulls it.** Expected: the release job fails before moving the tag if `sha-<commit>` is missing, and fails with a clear message (and the rollback command) if `/healthz` does not report the commit within 15 minutes (Task 3, Task 4).
3. **A server reboot empties the secrets.** Secrets are files on a memory-only folder (Task 6), so after a reboot the container cannot start until the secrets play runs again. Expected: the app refuses to start without its secret file (Task 1), the uptime check alerts (Task 9), and the reboot runbook says to run the secrets play.
4. **An error or a stray query string leaks into the app log.** Expected: an unexpected exception or a request with `?postcode=` writes no client address, path, query or body to the app's output (Task 1 tests).
5. **Docker keeps environment variables in plain text on disk** (in each container's stored configuration). Expected: secrets reach the container as mounted files, never `environment:` or `env_file:` entries (Task 2, Task 6).

---

## Part 1: this repository (one pull request, founder merges)

Branch `feat/group-a-placeholder-release`. Tasks 1 to 4 ship together; Task 5 is the founder's settings.

### Task 1: The placeholder app

**Files:**
- Create: `packages/vestagraph-placeholder/pyproject.toml` (no dependencies; same build backend as the other packages)
- Create: `packages/vestagraph-placeholder/src/vestagraph_placeholder/__init__.py`, `app.py`, `__main__.py`
- Create: `packages/vestagraph-placeholder/tests/test_placeholder_app.py`
- Modify: `pyproject.toml` (add `packages/vestagraph-placeholder/tests` to pytest `pythonpath` only if a helper module is needed), `uv.lock` (workspace member)

**Interfaces:**
- Produces: `load_secret_check(path: pathlib.Path) -> str` (raises `SystemExit` with a message naming the path, never the value, if the file is missing or empty); `make_handler(commit: str) -> type[http.server.BaseHTTPRequestHandler]`; `main() -> None` reading `VESTAGRAPH_COMMIT` (default `"unknown"`), `VESTAGRAPH_SECRET_CHECK_FILE` (default `/run/secrets/secret_check`) and `PORT` (default `8080`), serving on `0.0.0.0` with `http.server.ThreadingHTTPServer`.
- Routes: `GET /healthz` → `200`, `application/json`, body `{"status": "ok", "commit": "<commit>"}`; `POST /api/area-check` → reads and discards the body (the log test's "test search"), `204`; anything else → `404` with an empty body. Response header `Cache-Control: no-store` on every response.

- [ ] **Step 1: Write the failing tests** (start a real server on port 0 in a thread; capture `sys.stderr` and the `logging` root output)
  - `test_healthz_get_returns_status_and_commit`: body equals `{"status": "ok", "commit": "abc123"}`, status 200, `Cache-Control` is `no-store`.
  - `test_area_check_post_with_postcode_body_returns_204_and_logs_nothing`: POST body `{"postcode": "ZZ99 9ZZ"}`; captured output contains neither `ZZ99`, `127.0.0.1` nor `/api/area-check`.
  - `test_unknown_path_with_postcode_query_returns_404_and_logs_nothing`: GET `/?postcode=ZZ99%209ZZ`; 404; captured output has no `ZZ99`, `postcode` or `127.0.0.1`.
  - `test_handler_exception_logs_no_client_address`: patch the handler so `GET /healthz` raises; the captured output has no `127.0.0.1` and no path (override `log_message`, `log_error` and `handle_error`'s output).
  - `test_load_secret_check_missing_file_exits_without_value`: `SystemExit` whose message names the path.
  - `test_load_secret_check_empty_file_exits`.
  - `test_load_secret_check_present_returns_value`.
- [ ] **Step 2: Run** `uv run pytest packages/vestagraph-placeholder/tests -v`: expect failures (module not found).
- [ ] **Step 3: Implement** in `app.py`. Override `log_message` and `log_error` to do nothing, and set the server's `handle_error` to write one fixed line (`"request failed"`) with no address. `main()` calls `load_secret_check` before serving (fail fast).
- [ ] **Step 4: Run** the tests again: all pass. Run `make check`: passes (mypy strict and ruff cover the new package).
- [ ] **Step 5: Commit** `feat: placeholder app with a health page and no request logging`

### Task 2: Container build and Compose file with placeholders

**Files:**
- Create: `deploy/placeholder.Dockerfile`, `deploy/compose.yml`, `deploy/README.md`, `deploy/secrets.example` (names only, one per line: `secret_check`)
- Modify: `docs/references/third-party.md` (the Python base image and Watchtower), `.github/dependabot.yml` (the `docker` ecosystem for `deploy/`, if not already covered)

**Interfaces:**
- Consumes: Task 1's `python -m vestagraph_placeholder`.
- Produces: image built with `--build-arg VESTAGRAPH_COMMIT=<sha>`, listening on 8080, user `10001`, label `org.opencontainers.image.source=https://github.com/olaheavy-dev/vestagraph-platform`. Compose service `placeholder`: image `ghcr.io/olaheavy-dev/vestagraph-placeholder:production`, label `com.centurylinklabs.watchtower.scope=vestagraph`, network `<CADDY_NETWORK>` (external placeholder), secret `secret_check` from `file: <SECRETS_DIR>/secret_check`, `read_only: true`, `security_opt: [no-new-privileges:true]`, `cap_drop: [ALL]`, `restart: unless-stopped`, a `healthcheck` calling `/healthz` with the standard library, json-file logging capped at 10 MB × 3. **No `environment:` secret and no `env_file:`.**

- [ ] **Step 1:** Write the Dockerfile: `python:3.14-slim` pinned by digest, copy only the placeholder package source, no `pip install` (standard library only; set `PYTHONPATH`), non-root user, `ENV VESTAGRAPH_COMMIT=$VESTAGRAPH_COMMIT`.
- [ ] **Step 2: Verify the build:** `docker build -f deploy/placeholder.Dockerfile --build-arg VESTAGRAPH_COMMIT=test -t vg-placeholder:test .` succeeds.
- [ ] **Step 3: Verify it runs and refuses without the secret:** `docker run --rm vg-placeholder:test` exits non-zero with the path in the message; with `-v "$PWD/tmp-secret:/run/secrets/secret_check:ro"` and `-p 8080:8080`, `curl -s localhost:8080/healthz` prints `{"status": "ok", "commit": "test"}` and `docker logs` is empty after a `curl -X POST -d '{"postcode":"ZZ99 9ZZ"}' localhost:8080/api/area-check`. Delete the test container, image and secret file.
- [ ] **Step 4: Verify the Compose file:** with placeholders replaced in a scratch copy, `docker compose -f <copy> config` succeeds; `grep -n "environment\|env_file" deploy/compose.yml` finds no secret.
- [ ] **Step 5:** `deploy/README.md`: what each file is, the placeholders, and that the server copy lives in the private infrastructure repository. **Commit** `feat: container build and compose file for the placeholder`.

### Task 3: The release check script

**Files:**
- Create: `tools/release_check.py`, `tools/tests/test_release_check.py`

**Interfaces:**
- Produces: `is_live(body: bytes, commit: str) -> bool` (true only for valid JSON with `status == "ok"` and `commit == commit`); `wait_for_commit(url: str, commit: str, timeout_s: int, interval_s: int, fetch: Callable[[str], bytes]) -> bool`; CLI `python tools/release_check.py --url URL --commit SHA [--timeout 900] [--interval 20]`, exit 0 when live, exit 1 with the message `"<url> did not report <commit> within <timeout> s; to roll back, run the Images workflow with an earlier commit"`.

- [ ] **Step 1: Write the failing tests:** `test_is_live_matching_commit_returns_true`; `test_is_live_other_commit_returns_false`; `test_is_live_invalid_json_returns_false`; `test_is_live_status_not_ok_returns_false`; `test_wait_for_commit_becomes_live_on_third_poll_returns_true` (fake `fetch` and a zero interval); `test_wait_for_commit_fetch_errors_until_timeout_returns_false` (a fake `fetch` that raises `OSError` is treated as not yet live).
- [ ] **Step 2: Run** `uv run pytest tools/tests/test_release_check.py -v`: fails.
- [ ] **Step 3: Implement** with `urllib.request` (10 s timeout per request, `Cache-Control: no-cache` request header) and `time.monotonic`.
- [ ] **Step 4: Run** the tests and `make check`: pass.
- [ ] **Step 5: Commit** `feat: release check waits for the live health page to report the commit`

### Task 4: The Images workflow (build, publish, approved release, rollback)

**Files:**
- Create: `.github/workflows/images.yml`
- Modify: `docs/references/third-party.md` if it lists workflows; `SECURITY.md` only if it describes the release path

**Interfaces:**
- Consumes: Task 2's Dockerfile, Task 3's CLI.
- Triggers: `pull_request` (job `build` only, no push); `push` to `main` (jobs `build` → `publish` → `release`); `workflow_dispatch` with input `commit` (40 hex characters; job `release` only, for a re-release or rollback).
- Jobs:
  - `build`: `docker build` with the commit build argument. `permissions: contents: read`.
  - `publish`: log in to `ghcr.io` with `GITHUB_TOKEN` through `--password-stdin`; push `ghcr.io/olaheavy-dev/vestagraph-placeholder:sha-${GITHUB_SHA}`. `permissions: contents: read, packages: write`.
  - `release`: `environment: production` (the founder approves). Validate the commit input with a shell pattern before use, passing it through an `env:` value, never `${{ }}` inside `run:` (zizmor's template-injection rule). Check the tag exists (`docker buildx imagetools inspect`), else fail. `docker buildx imagetools create -t …:production …:sha-<commit>`. Then `uv run --no-project python tools/release_check.py --url https://vestagraph.com/healthz --commit <commit>`. `permissions: contents: read, packages: write`. `concurrency: release-production` (no cancel in progress).
  - Every job: `persist-credentials: false` on checkout, `timeout-minutes`, pinned `actions/checkout` and `astral-sh/setup-uv` (the existing pins).

- [ ] **Step 1:** Write the workflow.
- [ ] **Step 2: Verify:** run actionlint and zizmor the same way `workflow-lint.yml` does (the pinned actionlint image; zizmor locally or in the pull request): no findings.
- [ ] **Step 3: Verify the pull request path:** on the pull request, `build` runs and passes; `publish` and `release` are skipped.
- [ ] **Step 4:** Pre-flight (search for `GHCR`, `production`, `Watchtower`, `0060`, `IN-04`, `placeholder` and fix stale text), update `docs/planning/status.md`, run `make check`, then the pre-push Opus review with `code-security-reviewer`. **Commit** `feat: images workflow with an approved production release`. Open the pull request (founder merges: CI permissions).

### Task 5: The founder's settings (after the pull request merges)
- [ ] The founder creates the GitHub environment `production`: required reviewer the founder, "Prevent self-review" off (the founder is the only reviewer), deployment branches `main` only. (Repository settings: founder only.)
- [ ] After the first `publish` run, the founder sets the `vestagraph-placeholder` package to **public** and links it to the repository (the design: public images, no secrets in them), or tells the agent to keep it private and add the server's pull credential instead.
- [ ] **Verify:** `docker pull ghcr.io/olaheavy-dev/vestagraph-placeholder:sha-<commit>` works without logging in, and the first `release` run shows "Waiting for review".

## Part 2: the private infrastructure repository (agents merge there)

The agent writes this part as one phase plan in that repository's `wiki/plan/`, following its `AGENTS.md` (branch naming, wiki pages, its checks), with the details this public plan leaves out. Nothing from it comes back here. Each task names the launch blocker it closes.

### Task 6: Retire the app being wound down, then secrets with SOPS and age (blockers 1 and 2)
- [ ] Show the founder exactly what will be deleted (containers, volumes, data, DNS records, keys at outside providers), **ask once more in a prompt window**, then delete; revoke the app's outside keys. Record it in the wiki.
- [ ] Add SOPS with age: the founder makes the age key pair on their machine (the private key never goes on the server, as for the backups). Vestagraph's secrets file (`secret_check` now; `DATABASE_URL` from Task 10; later Better Auth, AI and email keys) is committed only encrypted.
- [ ] An Ansible play decrypts on the operator machine and writes each secret as its own file, mode `0400`, into a **memory-only (tmpfs) folder** on the server that the Compose file mounts as `secrets:`; nothing decrypted is written to disk on either machine. *Agent's call*, because Docker stores environment variables in each container's configuration on disk (Review Focus 5).
- [ ] Add "run the secrets play" to the reboot runbook (Review Focus 3).
- [ ] **Verify:** `grep` the server's app folder and the operator's working folder for the secret's value: no match; the container's stored configuration (`docker inspect`) has no secret value.

### Task 7: Caddy route, Cloudflare and Watchtower (blockers 3, 5 and part of 4)
- [ ] Copy `deploy/compose.yml` from this repository (at a named commit) with the placeholders filled, the way the infrastructure repository already deploys an app whose Compose file it does not own.
- [ ] A Watchtower instance of its own, scope `vestagraph`, interval 300 s, the same pinned image as the other instances. It sees only `:production` because that is the only tag in the Compose file.
- [ ] Caddy: a site block for `vestagraph.com` with **no `log` directive** (Caddy writes no access log without one); reverse proxy to `placeholder:8080`; **origin lock**: requests whose address is not in Cloudflare's published ranges (https://www.cloudflare.com/ips/) get `403` (Review Focus 1; the ranges are kept in a file with the date read and checked in the monthly maintenance); `vestagraph.co.uk` redirects permanently to `https://vestagraph.com{uri}`.
- [ ] Cloudflare (Terraform, existing module): proxied records for `vestagraph.com` and `vestagraph.co.uk`; SSL mode Full (strict). Caddy's automatic certificate is tried first; if it cannot be issued behind the proxy, use a free Cloudflare Origin CA certificate held in SOPS, and record which.
- [ ] One rate-limiting rule (the free plan allows one: a 10-second window counted per IP address, the action is block for 10 seconds; [Cloudflare's feature table](https://developers.cloudflare.com/learning-paths/application-security/rate-limiting/features/)): path starts with `/api/`, **60 requests in 10 seconds**, block. *Starting values* (design: "numbers are set in the build plan"), revisited when #93's area endpoints exist and a page's real call count is known. Check the dashboard's options first: the documentation disagrees on the free plan's periods.
- [ ] **Verify:** `curl -sI https://vestagraph.co.uk/x` → `301` to `https://vestagraph.com/x`; `dig +short vestagraph.com` returns Cloudflare addresses only; a request straight to the server with `Host: vestagraph.com` gets `403`.

### Task 8: Proxy the other apps too (founder's choice; finishes blocker 5's intent)
- [ ] After Task 7 works, move each of the founder's other apps' Cloudflare records to proxied, one app at a time, each with SSL mode Full (strict) and the same certificate approach Task 7 settled. Add the origin lock to each app's Caddy site block only once its own record is proxied.
- [ ] **Verify for each app:** its public address answers as before (status and a page check), `dig +short` returns Cloudflare addresses only, and a direct request to the server gets `403`. Roll an app back to DNS only if its check fails, and record why.
- [ ] Record in that repository's wiki that the server's address was public before this change, so it may still sit in old DNS history; a new address would need a server rebuild, which is not planned.

### Task 9: Uptime, spending and documentation checks (blockers 6 and 8, part)
- [ ] Add `https://vestagraph.com/healthz` to the infrastructure repository's scheduled uptime workflow (GitHub's failure email reaches the founder).
- [ ] Hetzner: check whether the console offers a cost alert; set it if so, otherwise record that and use the monthly invoice check in the maintenance runbook.
- [ ] Add a check to that repository's check scripts that fails on an IPv4 or IPv6 address in its tracked documentation, apart from documentation ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32`) and private ranges; fix what it finds.
- [ ] Memory and disk check after the retirement (`free -m`, `df -h`, `docker stats --no-stream`); resize only with the founder's approval (running cost).

## Part 3: Neon (the founder's account, the agent's steps)

### Task 10: The Neon project (blocker 8, part)
- [ ] **Founder:** create the Neon account on the Launch plan with their payment card (running cost). Then the agent, in the console, with each setting written down in the infrastructure repository (the official Terraform provider `neondatabase/neon` is still a beta `0.x` release, so by hand for now, as the design allows; revisit when it leaves beta):
  - project `vestagraph`, region AWS Europe (Frankfurt), the newest PostgreSQL major Neon offers with PostGIS;
  - autoscaling minimum and maximum 0.25 compute units; scale to zero on (the default);
  - history (restore) window 7 days;
  - `CREATE EXTENSION postgis;` and the schemas `personal` and `area` (0058: personal and public data apart), owned by a role `vestagraph_app` that is not the project owner;
  - spending notification at $25 a month; if the Launch plan has no such setting, record that and use the stand-in: a monthly check of Neon's usage page in the maintenance runbook, until a better one is found.
- [ ] The pooled connection string with `sslmode=require` goes into the SOPS file as `DATABASE_URL` (nothing reads it yet; #93 does).
- [ ] **Verify:** from the founder's machine, `psql "$DATABASE_URL" -c "select postgis_full_version();"` prints a version; a connection with `sslmode=disable` is refused.

### Task 11: The restore drill (blocker 7)
- [ ] In the `area` schema, create table `restore_drill (id int primary key, note text)` and insert `(1, 'before')`; note the time to the second (UTC); one minute later, delete the row.
- [ ] Create a branch from the moment noted (Neon's point-in-time branch); on that branch, `select * from area.restore_drill` returns `(1, 'before')`. Time how long it took.
- [ ] Delete the branch and the drill table.
- [ ] Write `docs/reviews/<date>-neon-restore-drill.md` in this repository: what was done, how long it took, and what to do in a real restore (restore the branch or copy the rows back). No project IDs, hosts or connection strings.

## Part 4: Prove it end to end

### Task 12: First release, rollback and the log check (blockers 3 and 4)
- [ ] Merge any small change to `main` (commit A), approve `release`: the job passes and `/healthz` reports A.
- [ ] Merge a second change (commit B), approve: `/healthz` reports B.
- [ ] Run the Images workflow by hand with `commit` = A, approve: `/healthz` reports A again (the rollback works), then re-release B.
- [ ] **The log check:** from the founder's network, `curl -X POST https://vestagraph.com/api/area-check -d '{"postcode":"ZZ99 9ZZ"}'` and `curl "https://vestagraph.com/?postcode=ZZ99%209ZZ"`. Then:
  - `docker logs` of the placeholder and of Caddy, over the last hour: no `ZZ99`, no client address (the founder's public address, looked up at the time and never written down);
  - Cloudflare's security analytics for the hour: the requests show paths `/api/area-check` and `/` with no postcode in the path; note that the `?postcode=` request **does** show a query string there, which is why the real app must never put a postcode in a query string (0046).
- [ ] Write `docs/reviews/<date>-group-a-launch-blockers.md`: each of the eight blockers, its evidence (dates, commands, results; no addresses or IDs) and "closed" or "open". Record in it that the log check is **repeated with the real app** once #86 and #93 replace the placeholder, and add that to their issues.
- [ ] Update `docs/planning/status.md` and the register lines IN-01 to IN-05.

## After this plan
- When #86 and #93 ship, they replace the placeholder: the `vestagraph-placeholder` package, its Dockerfile, its Compose service and its GHCR package are removed in the same pull request (clean up what you replace), and the release workflow builds `vestagraph-web` and `vestagraph-api` instead. The OpenAPI contract (BE-02) and OpenTelemetry (0025) arrive with #93.
- Group C names Neon, Hetzner and Cloudflare as processors and states Neon's 7-day history in the retention text (design, "For group C").
