# The pilot API (#93): design

Date: 26 Nov 2026. Size: a project. Status: approved (founder, 26 Nov 2026, prompt window: "Approve (Recommended)", with the agent's calls listed after the builder check). Issue: #93 (rewritten 26 Nov 2026). Decisions it follows: 0040 and 0049 (the founder's FastAPI template, a one-time trimmed copy), 0046 (the public area check first), 0060 (BE-02: the generated OpenAPI description is the contract), 0014 (no postcode or IP address in logs or URLs), 0029 (Live, Cached, Fallback, Unavailable labels), the launch guard (OP-06, #406).

## Intent and why

`vestagraph.com` serves a placeholder today. #93 replaces it with the pilot's real API: a visitor's postcode goes in, the official facts about that area come out, each with its source. It is the backend the web app (#86) calls next, and the base that group B's real data (Neon) plugs into. The founder chose to build it before #86 ("#93 the API first (Recommended)", 26 Nov 2026) because the pages call it and its OpenAPI document gives #86 its types (#95).

## Founder's choices (26 Nov 2026, prompt windows)

- **Template scope:** "Web layer only (Recommended)". From `house-template-fastapi`, only the web layer: app start-up, settings, logging, error handling (problem details), security headers and body limit, health. No database, AI gateway, storage or sign-in now; group B copies the template's database parts later (SQLAlchemy, Alembic and psycopg are already approved, 0062).
- **Packages:** "Approve, standard bundle" (over the agent's slim set). Runtime: `fastapi[standard-no-fastapi-cloud-cli]` (0.162.x, held to one minor, as the template does), `pydantic-settings`, `structlog`; 54 runtime packages in all, every licence read from PyPI on 26 Nov 2026 and on the allow-list in `.github/workflows/dependency-review.yml`. Tests only: `httpx`, `asgi-lifespan`, `import-linter` (all on the allow-list). FastAPI is a direct `0.` dependency, so its minor updates count as major under the merge rules.
- **Privacy before searches (0014):** "Live, area check closed (Recommended)". The API goes live and replaces the placeholder, but `POST /api/area-check` answers the public with a problem-details 503 "not available yet" (and reads no body) until the Privacy notice covers typed postcodes, because 0014 says search inputs "must be covered before real searches are accepted, even though searches aren't stored". One setting, `AREA_CHECK_OPEN` (default off; on in tests and local runs), opens it; turning it on in production is a later founder decision, with the Privacy notice.
- **Go-live:** "New image vestagraph-api-live (Recommended)". The release writes a new package, `ghcr.io/olaheavy-dev/vestagraph-api-live`; the server's Compose service and Caddy upstream move to it; the placeholder's package, code and Compose service are then removed. The founder locks the new package down in GitHub after its first release, as on 22 Nov 2026.

## Goals

1. `POST /api/area-check` with a JSON body `{"postcode": "<text>"}` answers with a `state` and, when found, the area result for that postcode (one entry of `packages/fixtures/generated/area-result.json`) plus the records it rests on (each with its source, edition date and level), from the synthetic fixture data: NB1 4XY (found), NB7 1RR (found, sparse), NB9 9ZZ (`notFound`, with no facts, never an empty or zero result, rule 7), and a new synthetic Welsh sample postcode (`notCovered`, rule 6; the states follow the specifications, for example LAND-16). Closed to the public until the Privacy notice is live (founder's choice above).
2. `GET /healthz` keeps the placeholder's exact answer, `{"status": "ok", "commit": "<sha>"}`, so `tools/release_check.py` and the Compose health check work unchanged.
3. The OpenAPI description is generated, committed and checked: `make check` fails when the committed file is stale (BE-02).
4. Nothing identifying reaches a log: no postcode, request body, query string or client address (0014; launch blocker 4).
5. It goes live through the existing approved release, with the launch guard, rollback and the health check, under the new image name.

## Non-goals

- Real data, the database and the data pipeline (group B).
- Endpoints for topics, maps, councils, the energy certificate, the chat or the MCP server (#97, later slices).
- Sign-in, accounts and rate limits in the app (Cloudflare's `/api/` rate limit stays the only limit for now).
- The web pages (#86).

## Anti-goals

- The API calculating or typing a figure itself (rule 2): every figure comes from `vestagraph-area`'s tested functions or the fixture inputs.
- A postcode in a URL, a log line or an error message.
- A missing value shown as zero, empty or clean (rule 7).
- FastAPI's interactive docs (`/docs`, `/redoc`) public in production: they load scripts from an outside CDN and are not needed by visitors. `/openapi.json` stays served, because it is the public contract anyway.

## Constraints

- One `uv` workspace and one `uv.lock` (`AGENTS.md`); Python 3.14 for the project's code (0049); mypy strict and ruff as today.
- Everything in `make check` runs without Docker (the web-only scope keeps it so).
- The container keeps the placeholder's hardening: read-only root file system, all capabilities dropped, `no-new-privileges`, 128 MB, 64 processes, user 10001, no host ports.
- Changes to `deploy/`, `.github/workflows/images.yml` and `.claude/settings.json` are founder merges; the founder has asked the agent to merge on their behalf this session ("merge it"), which covers merging, never approving a release.

## Approaches considered (how the answer is produced)

- **A. Work the answer out per request with `vestagraph-area` (chosen; the agent's call).** At start-up the API reads the fixture data with the area package's readers; for each request it calls the same functions the generator uses to build `area-result.json`. A test proves the API's answer equals `area-result.json` for every sample postcode. Group B then swaps only the data source (fixtures for Neon); the route and the logic stay.
- B. Serve the generated `area-result.json`: least code, but only pre-made postcodes work, and group B would rewrite the core.
- C. One endpoint per area tool (find-area, nearby, topic and so on): flexible, but several calls per postcode, and it repeats the MCP server's tool design (#97).

The founder asked for this choice to be explained, then said they did not understand the question; the agent took it as an internal building detail and chose A. It changes nothing a visitor sees.

## Design

### Where the code lives (the agent's call)

A new workspace package, `packages/vestagraph-api` (module `vestagraph_api`), beside the others, instead of the template's separate `backend/` folder, so the one lock file and `make check` cover it. Template files are rendered with Copier from v0.11.1 (the latest release on 26 Nov 2026; the pull request records the exact tag and commit) into a scratch folder with `database=false`, `llm=none`, `storage=false`, so the `.jinja` variants resolve, then copied in and renamed from `app` to `vestagraph_api`; the AGENTS.md exception for the founder's own templates covers this. Kept and adapted: `main.py` (`create_app`, lifespan), `settings.py` (without database, storage and model settings), `log.py`, `problems.py`, `limits.py` (`BodyLimit`, `SecurityHeaders`), `health.py`. Dropped: `auth.py`, `api/me.py`, `api/pagination.py`, `db.py`, `models.py`, `llm/`, `prompts/`, `storage.py`, migrations, compose files and their tests.

### The endpoint

- `POST /api/area-check`, body `{"postcode": "<string, at most 16 characters>"}`; the template's `BodyLimit` caps the body (the placeholder's 16 KiB stays the cap).
- The postcode is normalised as `council_for_postcode` already does (spaces removed, case folded), then matched against the data; there is no postcode shape rule (one would need a cited source, rule 3), so any text not in the data is `notFound`. Only a missing, empty, non-string or over-long value returns a problem-details 422, whose text never repeats the input (the template's `problems.py` drops `input` from 422 errors).
- The answer is a tagged union on `state`: `found` (the area result and its records), `notFound`, `notCovered` (with the nation). Unknown postcodes are sorted out before `at_a_glance()` is called, which raises on a postcode with no records.
- A new synthetic Welsh sample postcode is added to `postcode-area.json` with `nation` set (schema, validator and regenerated files updated in the same change); real postcodes get their nation from the ONS Postcode Directory in group B.
- Every fact keeps its source, edition date and level from its record in `postcode-area.json`. The decision 0029 labels (Live, Cached, Fallback, Unavailable) do not exist in the fixtures yet; they arrive with group B's adapters (builder check).

### Health

`GET /healthz` as today. The template's `/health/live` and `/health/ready` are kept too (ready has no checks until group B adds the database).

### Logging

The template's structlog JSON lines, with one change: the access line records the method, the **route template** (for example `/api/area-check`), the status, the duration and the request id, and never the raw path, query string, body or client address. Uvicorn's own access log is off. A test posts a postcode and asserts that no captured log line contains it.

### The contract

`packages/vestagraph-api/openapi.json` is generated from the app by a small script and committed; a `make generated-check`-style step regenerates it and fails if anything changed. A test checks that each `found` answer's area result validates against `area-result.json`'s schema and equals the generated entry, so the two contracts cannot drift.

### Sharing the generator's logic (builder check)

The per-postcode assembly now inline in `vestagraph_generator.area_generator.generate_area` (the JSON shaping, `json_number` strings, the distance and bus filters) moves into a public function in `vestagraph_area`; the generator calls it, and so does the API (the import-linter contract forbids the API importing the generator). `generated-check` proves `area-result.json` stays byte-identical. No new calculations.

### Architecture rule

An import-linter contract: `vestagraph_api` may import `vestagraph_area`; nothing in `vestagraph_area`, `vestagraph_engine` or `vestagraph_generator` may import `vestagraph_api`. It runs in `make check`.

### Image and release

- `deploy/api.Dockerfile` replaces `deploy/placeholder.Dockerfile`: `python:3.14-slim` pinned by digest (the project's own Python, 0049; the placeholder's 3.15 was for the placeholder only), the workspace's locked install of `vestagraph-api` and its workspace dependencies only, user 10001, the fixture data copied in read-only, `uvicorn` on port 8080.
- `.github/workflows/images.yml`: the build and the release write `vestagraph-api-live` instead of `vestagraph-placeholder-live`; the paths list adds `packages/vestagraph-api/**`, `packages/vestagraph-area/**`, `packages/vestagraph-engine/**` and `packages/fixtures/data/**` (and drops the placeholder's), so a data or area change rebuilds the image; the launch guard and the health check run as now (the API's 404s on the guard's pages count as "no page here"), and the guard step's `secret_check` mount and comment go with the secret.
- `deploy/compose.yml`: the service becomes `api` with the new image; the same hardening, labels and secret. (The placeholder's `secret_check` file is kept only if the API still needs a start-up secret; the agent's call: drop it, since the web layer has no secret, and remove it from the server in the cut-over.)

### Cut-over (infrastructure repository, private)

In order, each step checked before the next:
1. Merge this repository's pull request; the founder approves the release; it builds and pushes `vestagraph-api-live` (the launch guard passes against the new image on the runner).
2. The founder locks the new package down in GitHub (public, no repository under Actions access).
3. In the infrastructure repository (worktree `~/source/code/infra-lon1`), one pull request: `scripts/deploy-vestagraph.sh` fills the new Compose file; the Caddy `vestagraph` block's upstream becomes `api:8080`; the wiki page `vestagraph-deployment.md` is updated. The agent may merge there after review and tests (standing approval, 19 Nov 2026).
4. Run the deploy for `apps-lon1` only: start `api`, check `https://vestagraph.com/healthz` reports the commit, then remove the `placeholder` container. A short gap of seconds is accepted (no visitors yet).
5. Repeat launch blocker 4's log check with the API: a request with a postcode (answered "not available yet", the area check being closed) leaves no trace in `docker logs` of Caddy or the API.
6. A follow-up pull request here removes `packages/vestagraph-placeholder`, its tests and the old Dockerfile; the founder deletes the old GHCR package `vestagraph-placeholder-live` (founder step: package settings).

Rollback: until step 6, the placeholder image still exists, so the server can return to it by restoring the old Compose file and Caddy upstream (the infrastructure repository keeps both in git).

## The agent's calls after the builder check (26 Nov 2026)

States as a tagged union (the specifications already define them); a synthetic Welsh sample postcode; sources, dates and levels from the records, with 0029 labels deferred to group B; normalisation as the council search does it, with no shape rule; the generator's per-postcode logic moved into `vestagraph_area`; the template rendered with Copier; the release paths widened; the secret dropped. The template already logs the route template and turns uvicorn's access log off, so goal 4 is mostly inherited.

## Left to the builder

- Exact request and response model names, and how the response model is built from the area package's types.
- The script that writes `openapi.json` and its Make target name.
- Which existing `vestagraph-area` entry point the API calls, if the generator's own call path needs a small public function to share (no new calculations).
- Test names, following `test_<method>_<condition>_<result>`.

## Teaching

Feature pull request: "How it works" and "Concepts to learn" (FastAPI, Pydantic models, ASGI and uvicorn, OpenAPI, structlog, import-linter), with official links.
