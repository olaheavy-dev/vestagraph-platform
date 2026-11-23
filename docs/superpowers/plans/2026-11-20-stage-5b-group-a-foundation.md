# Stage 5b group A (the foundation): implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove the pilot's foundation end to end with a placeholder app (a health page only): an approved release, a rollback, encrypted secrets, logs free of IP addresses and postcodes, a Neon database with a tried restore, and alerts, so the eight launch blockers in the design are closed before the app shell (#86) and the API (#93) exist.

**Architecture:** This repository gets a tiny standard-library Python app, its container build, a Compose file with placeholders and one workflow that builds the image and, after the founder's approval in the `production` environment, builds it again from the approved commit and pushes it to GHCR as `sha-<commit>` and `production` (22 Nov 2026: one package, `vestagraph-placeholder-live`, written only by the release job with an environment token; nothing else pushes images). The server's own Watchtower instance follows only that tag. Everything about the server, Cloudflare and secrets is done in the founder's private infrastructure repository, under its own rules; this plan names that work but never its contents.

**Tech Stack:** Python 3.14 standard library (`http.server`, `urllib`), Docker and Docker Compose, GitHub Actions with the `docker` command line only (no new actions), GHCR, Watchtower (the maintained fork `ghcr.io/nicholas-fedor/watchtower` the server already runs; the original project was archived in December 2025), Caddy, Cloudflare (proxy and one rate-limit rule), SOPS with age, Neon (PostgreSQL with PostGIS).

**Spec:** [`docs/superpowers/specs/2026-11-19-stage-5b-foundation-design.md`](../specs/2026-11-19-stage-5b-foundation-design.md), decision [0060](../../decisions/0060-pilot-foundation-hosting-and-database.md).

**Amended 22 Nov 2026 ([0063](../../decisions/0063-pilot-privacy-and-anonymous-chat-first.md)):** Better Auth and its secret leave this plan (Task 6's secrets list); nothing else in it named sign-in.

**Amended 23 Nov 2026 ([0067](../../decisions/0067-own-server-in-london-and-neon-london.md)):** the app moves to its own OVHcloud VPS-2 in London, and Neon is created in London. OVH had no Linux stock on 23 Nov 2026, so the app stays on the Hetzner server until a stock watch reports it; Task 12 runs on the Hetzner server now, and Tasks 10 and 11 (Neon and the restore drill) move to the start of the group B build (founder, 23 Nov 2026: "At the start of group B (Recommended)", because the first real-app deploy uses no database); the checks are repeated on the new server, whose move is planned in the private infrastructure repository (Phase 22). The Hetzner cost-alert step also covers OVH.

**When:** written 20 Nov 2026; **built once groups B to D are decided** (0046: decisions first; design, "Building starts once groups B to D are decided"). Task 1 to Task 4 may be built earlier only if the founder says so.

## Founder's choices on this plan (20 Nov 2026, prompt window)
- **Secrets after a reboot:** "Re-run after reboot (Recommended)": the decryption key stays only on the founder's machine; after a reboot the secrets play is run again (runbook step), and the uptime check alerts if it was missed.
- **The server's public address:** "Lock and proxy all apps" (over the agent's "Lock Vestagraph only"): Caddy answers Vestagraph only through Cloudflare (the origin lock), and the founder's other apps move to proxied records too, so the address stops being published (Task 8).
- **How to build:** "Subagent-driven (Recommended)".
- **Who can move the live image (22 Nov 2026, prompt window):** "Separate live image (Recommended)", over "Build now, fix before the real app" and "Accept and document". Why: Task 4's review found that GitHub runs a workflow from the branch's own copy, so a workflow on any branch of this repository could get a `GITHUB_TOKEN` with `packages: write` and move `production` with no merge and no approval. Only `release` writes the live image, `ghcr.io/olaheavy-dev/vestagraph-placeholder-live:production`, with a classic personal access token (the only other credential GHCR accepts, [GitHub docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)) held as the `production` environment's secret `GHCR_RELEASE_TOKEN` (environment secrets reach only jobs that use the environment, after its rules pass, [GitHub docs](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)). This repository's `GITHUB_TOKEN` has no access to the live package once the founder locks it down straight after the first release (Task 5). (The same day the design changed again: see the next choice.) Cost: the founder looks after one more token (it can write the founder's other packages too, and is renewed before it expires). Tasks 2, 4, 5 and 12 below carry the change.
- **Build at release (22 Nov 2026, prompt window):** "A. Build at release (Recommended)", over "B. Lock the first package too" and "C. Copy by fingerprint". Why: the final reviews found that the release copied the mutable tag `sha-<commit>` from a package that any branch workflow could overwrite with `GITHUB_TOKEN` before approval or before a rollback. So there is no `publish` job and no first package. The `release` job, after approval, checks the commit is on `main`, builds the image from that commit, and pushes `sha-<commit>` and `production` (the same digest) to `vestagraph-placeholder-live` with the environment token. A rollback is a manual run with an earlier `main` commit, which rebuilds that commit. No job in the workflow has `packages: write`.
- **Dependabot and `deploy/` (22 Nov 2026, prompt window):** "You merge them (Recommended)", over "Merge on green". Why: Dependabot's base-image updates in `deploy/` change what the release builds, so they are founder merges like every other `deploy/` change.

## Global Constraints
- Never in a tracked file of this repository: a server address, hostname, credential, private repository path, the retired app's name, or anything copied from the private infrastructure repository (0022, `AGENTS.md`).
- No visitor IP address or searched postcode in our server, Caddy or app logs; no postcode in Cloudflare's logs (0014, 0046). Postcodes travel in the request body or the URL fragment, never the path or query string.
- Images are tagged `sha-<full commit>` and `production` only. Never `latest`, never `main`.
- A merged change reaches the live site only after the founder approves the `production` environment.
- No new packages and no new third-party actions: the placeholder uses the standard library only; the workflow uses `actions/checkout` (already pinned), the runner's own `python3` and the `docker` command line. FastAPI and its packages wait for #93 (0049). The new images (the `python:3.14-slim` base image here; Watchtower and Caddy on the server) are recorded with their licences in `docs/references/third-party.md`.
- Neon: London region (AWS `aws-eu-west-2`, [0067](../../decisions/0067-own-server-in-london-and-neon-london.md); was Frankfurt), Launch plan, one Vestagraph project, autoscaling capped at 0.25 compute units, history window 7 days, PostGIS installed, TLS connections only.
- Spending alert at Neon about $25 a month for Vestagraph (design, "Monitoring and spending").
- Live address `vestagraph.com`; `vestagraph.co.uk` redirects to it. Environments: the founder's laptop and live only.
- Test names follow `test_<method>_<condition>_<result>` (0039). `make check` passes before every push.
- Founder merges: the pull request that adds the workflow (CI permissions; a base image not on the pre-approved list; the `AGENTS.md` and `.claude/settings.json` changes in Task 4), **every later change to `.github/workflows/images.yml` or `deploy/`** (the release job builds and writes the live image with the founder's token; this includes Dependabot's base-image updates in `deploy/`), and any change to repository settings (the `production` environment). **Agents never approve a release.** Agents merge in the private infrastructure repository after review and tests (0060 point 9); destructive steps get one last confirmation first.

## Review Focus
1. **The server's address is already public.** The founder's other apps use DNS-only Cloudflare records, so proxying Vestagraph does not hide the server's address, and anyone can send a request straight to the server with `Host: vestagraph.com`, skipping Cloudflare's rate limit. Expected: the server answers Vestagraph's hosts only for requests that come from Cloudflare's address ranges (Task 7, the origin lock), and Task 7's check proves a direct request is refused.
2. **The approved commit has no image, or Watchtower never pulls it.** Expected: the release job fails before building if the commit is not on `main`, and fails with a clear message (and the rollback command) if `/healthz` does not report the commit within 15 minutes (Task 3, Task 4).
3. **Caddy's error log is not its access log.** With no `log` directive Caddy writes no access log, but a failed upstream (a 502 while the placeholder restarts) still writes an error entry with the client address, the URI with any query string, and the headers (`Cf-Connecting-Ip`, `X-Forwarded-For`). Expected: Vestagraph's error entries are filtered so none of these reach the log (Task 7), and the log check includes the failure path (Task 12).
4. **A server reboot empties the secrets.** Secrets are files on a memory-only folder (Task 6), so after a reboot the container cannot start until the secrets play runs again (and Docker may create an empty directory where the file was). Expected: the app refuses to start without a readable secret file (Task 1), the uptime check alerts (Task 9), and the reboot runbook says to run the secrets play.
5. **An error or a stray query string leaks into the app log.** Expected: an unexpected exception or a request with `?postcode=` writes no client address, path, query or body to the app's output (Task 1 tests).
6. **Docker keeps environment variables in plain text on disk** (in each container's stored configuration). Expected: secrets reach the container as mounted files, never `environment:` or `env_file:` entries (Task 2, Task 6). Compose ignores `uid`, `gid` and `mode` for file secrets ([Compose secrets](https://docs.docker.com/reference/compose-file/services/#secrets)), so the files on the server must already be readable by the image's user `10001` (Task 6).

---

## Part 1: this repository (one pull request, founder merges)

Branch `feat/group-a-placeholder-release`. Tasks 1 to 4 ship together; Task 5 is the founder's settings, and its first part is a **condition for merging** that pull request.

### Task 1: The placeholder app

**Files:**
- Create: `packages/vestagraph-placeholder/pyproject.toml` (no dependencies; same build backend as the other packages)
- Create: `packages/vestagraph-placeholder/src/vestagraph_placeholder/__init__.py`, `app.py`, `__main__.py`
- Create: `packages/vestagraph-placeholder/tests/test_placeholder_app.py`
- Modify: `pyproject.toml`: add `packages/vestagraph-placeholder/src` and `packages/vestagraph-placeholder/tests` to `[tool.mypy] files`, the `src` folder to `mypy_path`, and `vestagraph_placeholder` to coverage's `source_pkgs` (mypy lists its files one by one, so without this the package is not type-checked); `uv.lock` (workspace member)

**Interfaces:**
- Produces: `load_secret_check(path: pathlib.Path) -> str` (raises `SystemExit` with a message naming the path, never the value, if the path is missing, a directory, unreadable or empty); `make_handler(commit: str) -> type[http.server.BaseHTTPRequestHandler]`; `main() -> None` reading `VESTAGRAPH_COMMIT` (default `"unknown"`), `VESTAGRAPH_SECRET_CHECK_FILE` (default `/run/secrets/secret_check`) and `PORT` (default `8080`), serving on `0.0.0.0` with `http.server.ThreadingHTTPServer`.
- Routes: `GET /healthz` → `200`, `application/json`, body `{"status": "ok", "commit": "<commit>"}`; `POST /api/area-check` → reads and discards the body (the log test's "test search"), `204`; anything else → `404` with an empty body. Response header `Cache-Control: no-store` on every response.

- [ ] **Step 1: Write the failing tests** (start a real server on port 0 in a thread; capture `sys.stderr` and the `logging` root output)
  - `test_healthz_get_returns_status_and_commit`: body equals `{"status": "ok", "commit": "abc123"}`, status 200, `Cache-Control` is `no-store`.
  - `test_area_check_post_with_postcode_body_returns_204_and_logs_nothing`: POST body `{"postcode": "ZZ99 9ZZ"}`; captured output contains neither `ZZ99`, `127.0.0.1` nor `/api/area-check`.
  - `test_unknown_path_with_postcode_query_returns_404_and_logs_nothing`: GET `/?postcode=ZZ99%209ZZ`; 404; captured output has no `ZZ99`, `postcode` or `127.0.0.1`.
  - `test_handler_exception_logs_no_client_address`: patch the handler so `GET /healthz` raises; the captured output has no `127.0.0.1` and no path (override `log_message`, `log_error` and `handle_error`'s output).
  - `test_load_secret_check_missing_file_exits_without_value`: `SystemExit` whose message names the path.
  - `test_load_secret_check_empty_file_exits`.
  - `test_load_secret_check_directory_exits` (Docker creates a directory at a missing bind-mount source).
  - `test_load_secret_check_unreadable_file_exits` (mode `000`; skip when running as root).
  - `test_load_secret_check_present_returns_value`.
- [ ] **Step 2: Run** `uv run pytest packages/vestagraph-placeholder/tests -v`: expect failures (module not found).
- [ ] **Step 3: Implement** in `app.py`. Override `log_message` and `log_error` to do nothing, and set the server's `handle_error` to write one fixed line (`"request failed"`) with no address. `main()` calls `load_secret_check` before serving (fail fast).
- [ ] **Step 4: Run** the tests again: all pass. Run `make check`: passes (mypy strict and ruff cover the new package).
- [ ] **Step 5: Commit** `feat: placeholder app with a health page and no request logging`

### Task 2: Container build and Compose file with placeholders

**Files:**
- Create: `deploy/placeholder.Dockerfile`, `deploy/compose.yml`, `deploy/README.md` (including: each secret file must be owned by user `10001`, mode `0400`), `deploy/secrets.example` (names only, one per line: `secret_check`; replaces the design's `.env.example`, because secrets travel as files)
- Modify: `docs/references/third-party.md` (the Python base image and Watchtower), `.github/dependabot.yml` (the `docker` ecosystem for `deploy/`, if not already covered)

**Interfaces:**
- Consumes: Task 1's `python -m vestagraph_placeholder`.
- Produces: image built with `--build-arg VESTAGRAPH_COMMIT=<sha>`, listening on 8080, user `10001`, label `org.opencontainers.image.source=https://github.com/olaheavy-dev/vestagraph-platform`. Compose service `placeholder`: image `ghcr.io/olaheavy-dev/vestagraph-placeholder-live:production` (22 Nov 2026: the live package, founder's choice above), labels `com.centurylinklabs.watchtower.enable=true` (added 22 Nov 2026: the server's Watchtower updates only containers marked so) and `com.centurylinklabs.watchtower.scope=vestagraph`, network `<CADDY_NETWORK>` (external placeholder), secret `secret_check` from `file: <SECRETS_DIR>/secret_check`, `read_only: true`, `security_opt: [no-new-privileges:true]`, `cap_drop: [ALL]`, `restart: unless-stopped`, a `healthcheck` calling `/healthz` with the standard library, json-file logging capped at 10 MB × 3. **No `environment:` secret and no `env_file:`.**

- [ ] **Step 1:** Write the Dockerfile: `python:3.14-slim` pinned by digest, copy only the placeholder package source, no `pip install` (standard library only; set `PYTHONPATH`), non-root user, `ENV VESTAGRAPH_COMMIT=$VESTAGRAPH_COMMIT`.
- [ ] **Step 2: Verify the build:** `docker build -f deploy/placeholder.Dockerfile --build-arg VESTAGRAPH_COMMIT=test -t vg-placeholder:test .` succeeds.
- [ ] **Step 3: Verify it runs and refuses without the secret:** `docker run --rm vg-placeholder:test` exits non-zero with the path in the message; with a secret file in a scratch folder outside the repository, owned by `10001`, mounted by `-v "<scratch>/secret_check:/run/secrets/secret_check:ro"` and `-p 8080:8080`, `curl -s localhost:8080/healthz` prints `{"status": "ok", "commit": "test"}` and `docker logs` is empty after a `curl -X POST -d '{"postcode":"ZZ99 9ZZ"}' localhost:8080/api/area-check`. Delete the test container, image and secret file.
- [ ] **Step 4: Verify the Compose file:** with placeholders replaced in a scratch copy, `docker compose -f <copy> config` succeeds; `grep -n "environment\|env_file" deploy/compose.yml` finds no secret.
- [ ] **Step 5:** `deploy/README.md`: what each file is, the placeholders, and that the server copy lives in the private infrastructure repository. **Commit** `feat: container build and compose file for the placeholder`.

### Task 3: The release check script

**Files:**
- Create: `tools/release_check.py`, `tools/tests/test_tools_release_check.py` (unique test file names, as `test_tools_mutation_score.py`). The script must also run on the runner's `python3` (3.12): no syntax newer than 3.12.

**Interfaces:**
- Produces: `is_live(body: bytes, commit: str) -> bool` (true only for valid JSON with `status == "ok"` and `commit == commit`); `wait_for_commit(url: str, commit: str, timeout_s: int, interval_s: int, fetch: Callable[[str], bytes]) -> bool`; CLI `python tools/release_check.py --url URL --commit SHA [--timeout 900] [--interval 20]`, exit 0 when live, exit 1 with the message `"<url> did not report <commit> within <timeout> s; to roll back, run the Images workflow with an earlier commit"`.

- [ ] **Step 1: Write the failing tests:** `test_is_live_matching_commit_returns_true`; `test_is_live_other_commit_returns_false`; `test_is_live_invalid_json_returns_false`; `test_is_live_status_not_ok_returns_false`; `test_wait_for_commit_becomes_live_on_third_poll_returns_true` (fake `fetch` and a zero interval); `test_wait_for_commit_fetch_errors_until_timeout_returns_false` (a fake `fetch` that raises `OSError` is treated as not yet live).
- [ ] **Step 2: Run** `uv run pytest tools/tests/test_tools_release_check.py -v`: fails.
- [ ] **Step 3: Implement** with `urllib.request` (10 s timeout per request, request headers `Cache-Control: no-cache` and `User-Agent: vestagraph-release-check`, so Cloudflare's browser checks don't challenge it) and `time.monotonic`.
- [ ] **Step 4: Run** the tests and `make check`: pass.
- [ ] **Step 5: Commit** `feat: release check waits for the live health page to report the commit`

### Task 4: The Images workflow (build, approved release, rollback)

**Files:**
- Create: `.github/workflows/images.yml`
- Modify: `docs/references/third-party.md` if it lists workflows; `SECURITY.md` only if it describes the release path; `AGENTS.md` (founder-only list: changes to `.github/workflows/images.yml` and `deploy/`; agents never approve a release); `.claude/settings.json` (deny `gh api` calls whose path contains `pending_deployments` or `/deployments`)

**Interfaces:**
- Consumes: Task 2's Dockerfile, Task 3's CLI.
- Triggers: `pull_request` (job `build` only, no push); `push` to `main` (jobs `build` → `release`); `workflow_dispatch` with input `commit` (40 hex characters; job `release` only, for a re-release or rollback, which rebuilds that commit).
- Jobs:
  - Top level: `permissions: {}`; each job sets its own.
  - `build`: `docker build` with the commit build argument. `permissions: contents: read`.
  - No `publish` job and no job with `packages: write` (22 Nov 2026: build at release, founder's choice above).
  - `release`: `environment: production` (the founder approves). The commit comes from `inputs.commit` or `GITHUB_SHA`, passed through `env:`, never `${{ }}` inside `run:` (zizmor's template-injection rule), and must match `^[0-9a-f]{40}$`. Check out with `fetch-depth: 0`, keep a copy of `tools/release_check.py` from the run's own checkout, fail unless `git merge-base --is-ancestor "$COMMIT" origin/main`, then `git checkout --detach "$COMMIT"`. Fail early if `GHCR_RELEASE_TOKEN` is empty. Build the image from that commit and tag it `…-live:sha-<commit>` and `…-live:production`; log in to `ghcr.io` with the `GHCR_RELEASE_TOKEN` secret (not `GITHUB_TOKEN`) through `--password-stdin`; push both tags; check `docker buildx imagetools inspect --format '{{.Manifest.Digest}}'` of `production` equals the pushed digest. `docker logout` (always). Then run the kept copy of `release_check.py --url https://vestagraph.com/healthz --commit <commit>`. `permissions: contents: read` only. `concurrency: release-production` (no cancel in progress; a newer release waiting in the queue replaces an older waiting one, which shows as cancelled).
  - Every job: `persist-credentials: false` on checkout, `timeout-minutes`, the existing `actions/checkout` pin. No `setup-uv` and no caches (zizmor's cache-poisoning rule in a publishing workflow).

- [ ] **Step 1:** Write the workflow.
- [ ] **Step 2: Verify:** run actionlint and zizmor the same way `workflow-lint.yml` does (the pinned actionlint image; zizmor locally or in the pull request): no findings.
- [ ] **Step 3: Verify the pull request path:** on the pull request, `build` runs and passes; `release` is skipped.
- [ ] **Step 4:** Pre-flight (search for `GHCR`, `production`, `Watchtower`, `0060`, `IN-04`, `placeholder` and fix stale text), update `docs/planning/status.md`, run `make check`, then the pre-push Opus review with `code-security-reviewer`. **Commit** `feat: images workflow with an approved production release`. Open the pull request (founder merges: CI permissions). It merges only after Task 5's environment check passes.

### Task 5: The founder's settings
- [ ] **Before the Task 4 pull request merges** (its first push to `main` runs `release`, and GitHub creates a missing environment with no protection rules, [Managing environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments#creating-an-environment)): the founder creates the GitHub environment `production`: required reviewer the founder, "Prevent self-review" off (the founder is the only reviewer), deployment branches `main` only. (Repository settings: founder only.)
- [ ] **Before the Task 4 pull request merges, the release token** (founder's choices of 22 Nov 2026 above): the founder creates a classic personal access token from `https://github.com/settings/tokens/new?scopes=write:packages` (GitHub's normal token page also ticks the whole `repo` scope together with `write:packages`; this link does not) with an expiry date (a calendar reminder to renew it before then). Before saving it, check on the token list page that its scopes are only `write:packages` and `read:packages`. Save it as the `production` environment's secret `GHCR_RELEASE_TOKEN` (not a repository secret). The agent never sees the value.
- [ ] **Verify before merging:** `gh api repos/olaheavy-dev/vestagraph-platform/environments/production --jq '.protection_rules'` lists a `required_reviewers` rule naming the founder, and `--jq '.deployment_branch_policy'` is not null. If either check fails, the pull request does not merge.
- [ ] **After the merge:** the first push to `main` starts `release` and it waits for approval ("Waiting for review"). The founder approves it knowing that **the first approved release is expected to fail its last step** (the health check), because vestagraph.com does not answer until Part 2. The image is still written. Do not roll back; the failure is expected until Part 2.
- [ ] **Straight after the first release's "Push the live image" step** (it creates `vestagraph-placeholder-live`, and the image's source label links it to this repository), without waiting for Part 2: in the live package's settings the founder turns off "Inherit access from source repository", makes sure this repository is not listed under "Manage Actions access", and sets the package to public (GitHub says public cannot be undone, [package visibility](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility); images hold no secrets). Until this is done, push no branch that changes a workflow. **Verify:** `docker pull ghcr.io/olaheavy-dev/vestagraph-placeholder-live:production` works without logging in, and Task 12's branch test is refused.

## Part 2: the private infrastructure repository (agents merge there)

The agent writes this part as one phase plan in that repository's `wiki/plan/`, following its `AGENTS.md` (branch naming, wiki pages, its checks), with the details this public plan leaves out. Nothing from it comes back here. Each task names the launch blocker it closes.

### Task 6: Retire the app being wound down, then secrets with SOPS and age (blockers 1 and 2)
- [ ] Show the founder exactly what will be deleted (containers, volumes, data, DNS records, keys at outside providers), **ask once more in a prompt window**, then delete; revoke the app's outside keys. Record it in the wiki.
- [ ] Add SOPS with age: the founder makes the age key pair on their machine (the private key never goes on the server, as for the backups). Vestagraph's secrets file (`secret_check` now; `DATABASE_URL` from Task 10; later the AI keys. No Better Auth secret or keys and no email key: sign-in waits until later, [0063](../../decisions/0063-pilot-privacy-and-anonymous-chat-first.md)) is committed only encrypted.
- [ ] An Ansible play decrypts on the operator machine and writes each secret as its own file, **owned by user `10001`, mode `0400`**, into a **memory-only (tmpfs) folder** on the server that the Compose file mounts as `secrets:`. Ansible normally copies content through temporary files on disk, so the task uses `no_log: true`, `diff: false` and SSH pipelining, and writes through standard input (for example `install -o 10001 -m 0400 /dev/stdin <dest>` with `stdin:`) or sets `remote_tmp` to a memory-only folder; confirm against the Ansible documentation for the version in use. *Agent's call*, because Docker stores environment variables in each container's configuration on disk (Review Focus 5).
- [ ] Add "run the secrets play" to the reboot runbook (Review Focus 3).
- [ ] **Verify:** `grep` the server's app folder, Ansible's temporary folders and the operator's working folder for the secret's value: no match; the play's output with `-v` shows no value; the container's stored configuration (`docker inspect`) has no secret value.

### Task 7: Caddy route, Cloudflare and Watchtower (blockers 3, 5 and part of 4)
- [ ] Copy `deploy/compose.yml` from this repository (at a named commit) with the placeholders filled, the way the infrastructure repository already deploys an app whose Compose file it does not own.
- [ ] A Watchtower instance of its own, scope `vestagraph`, interval 300 s, the same maintained fork, pinned by digest, as the other instances. No deploy user is needed: the server pulls, and nothing logs in to it to deploy (the design's "deploy user's narrow permissions"). It sees only `:production` because that is the only tag in the Compose file.
- [ ] Caddy: a site block for `vestagraph.com` with **no `log` directive** (Caddy writes no access log without one); **error entries for Vestagraph's hosts filtered** (a `filter` encoder deleting `request>remote_ip`, `request>client_ip`, `request>uri` and `request>headers`, or those entries dropped; check TLS handshake errors too), confirmed against the Caddy documentation for the version in use; reverse proxy to `placeholder:8080`; **origin lock** with the `remote_ip` matcher (not `client_ip`, which reads forwarded headers and would compare the visitor's address): requests whose address is not in Cloudflare's published IPv4 and IPv6 ranges (https://www.cloudflare.com/ips/) get `403` (Review Focus 1; the ranges are kept in a file with the date read and checked in the monthly maintenance); `vestagraph.co.uk` redirects permanently to `https://vestagraph.com{uri}`.
- [ ] Cloudflare (Terraform, existing module): proxied records for `vestagraph.com` and `vestagraph.co.uk`; SSL mode Full (strict). Caddy's automatic certificate is tried first; if it cannot be issued behind the proxy, use a free Cloudflare Origin CA certificate held in SOPS, and record which.
- [ ] One rate-limiting rule (the free plan allows one: a 10-second window counted per IP address, the action is block for 10 seconds; [Cloudflare's feature table](https://developers.cloudflare.com/learning-paths/application-security/rate-limiting/features/)): path starts with `/api/`, **60 requests in 10 seconds**, block. *Starting values* (design: "numbers are set in the build plan"), revisited when #93's area endpoints exist and a page's real call count is known. Check the dashboard's options first: the documentation disagrees on the free plan's periods.
- [ ] Consider Cloudflare's Authenticated Origin Pulls (free; a certificate proves the request came from this zone, which the range check cannot) and record the choice.
- [ ] **Verify:** `curl -sI https://vestagraph.co.uk/x` → `301` to `https://vestagraph.com/x`; `dig +short A vestagraph.com` and `dig +short AAAA vestagraph.com` return Cloudflare addresses only; `curl -sk --resolve vestagraph.com:443:<server address> https://vestagraph.com/healthz` → `403`, over IPv4 and IPv6; `/healthz` answers a request from a GitHub runner (no Cloudflare challenge).

### Task 8: Proxy the other apps too (founder's choice; finishes blocker 5's intent)
- [ ] After Task 7 works, move every DNS-only record that points at the server (apps, and any admin or other hostnames, A and AAAA) to proxied where it carries web traffic (records for SSH or mail cannot be proxied: remove or rename them so they don't name the server, or record why they stay), one app at a time, each with SSL mode Full (strict) and the same certificate approach Task 7 settled. Add the origin lock to each app's Caddy site block only once its own record is proxied.
- [ ] **Verify for each app:** its public address answers as before (status and a page check), `dig +short` returns Cloudflare addresses only, and a direct request to the server gets `403`. Roll an app back to DNS only if its check fails, and record why.
- [ ] Record in that repository's wiki that the server's address was public before this change, so it may still sit in old DNS history; a new address would need a server rebuild, which is not planned.

### Task 9: Uptime, spending and documentation checks (blockers 6 and 8, part)
- [ ] Add `https://vestagraph.com/healthz` to the infrastructure repository's scheduled uptime workflow (GitHub's failure email reaches the founder).
- [ ] Hetzner and OVHcloud (0067): check whether each console offers a cost alert; set it if so, otherwise record that, use the monthly invoice check in the maintenance runbook, and update register line IN-05 and 0060 with a dated note (they say "a Hetzner billing alert now").
- [ ] Add a check to that repository's check scripts that fails on an IPv4 or IPv6 address in its tracked documentation, apart from documentation ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32`) and private ranges; fix what it finds.
- [ ] Memory and disk check after the retirement (`free -m`, `df -h`, `docker stats --no-stream`); resize only with the founder's approval (running cost).

## Part 3: Neon (the founder's account, the agent's steps)

### Task 10: The Neon project (blocker 8, part)
- [ ] **Founder:** create the Neon account on the Launch plan with their payment card (running cost). Then the agent, in the console, with each setting written down in the infrastructure repository (the official Terraform provider `neondatabase/neon` is still a beta `0.x` release, so by hand for now, as the design allows; revisit when it leaves beta):
  - project `vestagraph`, region AWS Europe (London) (0067; check that PostGIS and the Launch plan's prices match before creating it, and stop and ask if not), the newest PostgreSQL major Neon offers with PostGIS;
  - autoscaling minimum and maximum 0.25 compute units; scale to zero on (the default);
  - history (restore) window 7 days;
  - `CREATE EXTENSION postgis;` and the schemas `personal` and `area` (0058: personal and public data apart), owned by a role `vestagraph_app` that is not the project owner;
  - spending notification at $25 a month; if the Launch plan has no such setting, record that and use the stand-in: a monthly check of Neon's usage page in the maintenance runbook, until a better one is found.
- [ ] The pooled connection string with `sslmode=verify-full` (and `channel_binding=require` if Neon's string carries it; check [Neon: connect securely](https://neon.com/docs/connect/connect-securely)) goes into the SOPS file as `DATABASE_URL`, and the direct (unpooled) string as `DATABASE_URL_DIRECT` for migrations and `CREATE EXTENSION` (nothing reads them yet; #93 does).
- [ ] **Verify:** from the founder's machine, `psql "$DATABASE_URL" -c "select postgis_full_version();"` prints a version; a connection with `sslmode=disable` is refused.

### Task 11: The restore drill (blocker 7)
- [ ] In the `area` schema, create table `restore_drill (id int primary key, note text)` and insert `(1, 'before')`; note the time to the second (UTC); one minute later, delete the row.
- [ ] Create a branch from the moment noted (Neon's point-in-time branch); on that branch, `select * from area.restore_drill` returns `(1, 'before')`. Time how long it took.
- [ ] Delete the branch and the drill table.
- [ ] Write `docs/reviews/<date>-neon-restore-drill.md` in this repository, on a `docs/` branch with its own pull request (or with Task 12's): what was done, how long it took, and what to do in a real restore (restore the branch or copy the rows back). No project IDs, hosts or connection strings.

## Part 4: Prove it end to end

### Task 12: First release, rollback and the log check (blockers 3 and 4)
- [ ] Tell the founder first: a newer release waiting for approval replaces an older waiting one. Merge any small change to `main` (commit A), the founder approves `release`: the job passes and `/healthz` reports A.
- [ ] Merge a second change (commit B), approve: `/healthz` reports B.
- [ ] Run the Images workflow by hand with `commit` = A, approve: the job rebuilds A, and `/healthz` reports A again (the rollback works), then re-release B.
- [ ] **The branch test (founder's choice of 22 Nov 2026):** on a throwaway branch that is never merged, a workflow run on `pull_request` with `packages: write` tries to push a test tag to `vestagraph-placeholder-live` with `GITHUB_TOKEN`: the push is refused. A second job on that branch with `environment: production` is refused by the deployment branch rule and gets no `GHCR_RELEASE_TOKEN`. Delete the branch, its runs' test tags (if any were created) and the pull request. Record both results in the launch-blockers review.
- [ ] **The log check, failure path:** stop the placeholder container, then `curl "https://vestagraph.com/?postcode=ZZ99%209ZZ"` (a 502); start it again. Caddy's log: no `ZZ99`, no client address, no `Cf-Connecting-Ip` value.
- [ ] **The log check, healthy path:** from the founder's network, `curl -X POST https://vestagraph.com/api/area-check -d '{"postcode":"ZZ99 9ZZ"}'` and `curl "https://vestagraph.com/?postcode=ZZ99%209ZZ"`. Then:
  - `docker logs` of the placeholder and of Caddy, over the last hour: no `ZZ99`, no client address (the founder's public address, looked up at the time and never written down);
  - Cloudflare's security analytics for the hour: the requests show paths `/api/area-check` and `/` with no postcode in the path; note that the `?postcode=` request **does** show a query string there, which is why the real app must never put a postcode in a query string (0046).
- [ ] Write `docs/reviews/<date>-group-a-launch-blockers.md` on a `docs/` branch with its own pull request: each of the eight blockers, its evidence (dates, commands, results; no addresses or IDs) and "closed" or "open". Record in it that the log check is **repeated with the real app** once #86 and #93 replace the placeholder, and add that to their issues.
- [ ] Update `docs/planning/status.md` and the register lines IN-01 to IN-05.

## After this plan
- When #86 and #93 ship, they replace the placeholder: the `vestagraph-placeholder` app, its Dockerfile, its Compose service and its `vestagraph-placeholder-live` GHCR package are removed in the same pull request (clean up what you replace), and the release workflow builds `vestagraph-web` and `vestagraph-api` instead. The OpenAPI contract (BE-02) and OpenTelemetry (0025) arrive with #93.
- Group C names Neon, Hetzner (0067: OVHcloud instead of Hetzner once the London server runs) and Cloudflare as processors and states Neon's 7-day history in the retention text (design, "For group C").
