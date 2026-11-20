# Stage 5b group B (data): implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the data pipeline's core (editions, checks, switch live, roll back), the licence register, freshness alerts, our own postcode lookup, two model sources end to end (crime and flood risk by postcode), the walking-time build (Sheffield first), and Dagster to run it, so every other source is then a small ticket in the same pattern.

**Architecture:** A plain Python package, `vestagraph-pipeline`, holds everything that decides anything (adapters, tidy, checks, editions, switching, freshness, postcode lookup) and never imports Dagster. Each source's edition is its own table in the `area` schema; a `_current` view points at the live one and is switched in one transaction under a per-source lock. A separate `vestagraph-dagster` package wraps the core as assets, checks, schedules and a rollback job. Heavy builds run on GitHub Actions and hand results back as workflow artifacts that the server pulls; no database credential lives in GitHub.

**Tech Stack:** Python 3.14, psycopg 3, SQLAlchemy 2 (Core) and Alembic (0062), PostgreSQL with PostGIS (Neon in production, a throwaway PostGIS container in tests), Dagster 1.x with SQLite run storage (0061), Valhalla (container image), GitHub Actions, Cloudflare R2.

**Spec:** [`docs/superpowers/specs/2026-11-20-stage-5b-data-design.md`](../specs/2026-11-20-stage-5b-data-design.md); decisions [0061](../../decisions/0061-pilot-data-pipeline-postcodes-and-walking-times.md) and [0062](../../decisions/0062-database-packages-and-test-database.md).

**When:** written 20 Nov 2026; **built after groups C and D are decided** (0046, 0061), after group A's build ([plan](2026-11-20-stage-5b-group-a-foundation.md)), whose Task 9 measures the server's free memory (this plan's Task 9 stop point).

## Global Constraints
- No pilot source goes live unless its register record says `cleared`, and only the founder sets `cleared`, case by case (0061).
- A failed edition never goes live; the live edition stays. Missing values stay missing (never zero, rule 7); an empty answer is valid only where the record says so.
- Every calculated figure shown comes from `vestagraph_area` (rule 2); SQL selects and filters inputs only. Walking times are an input (DA-18), stored with their method and OpenStreetMap date.
- Freshness counts from the last **confirmed** fetch: content that passed every check, or matched an edition that already passed; a fetch that fails tidy, checks or switch leaves it unchanged (0061, Codex P2).
- Keep 3 passed editions per source, 2 for the big ones (walking times, the postcode directory, bus timetable inputs). Row-change limit 20% unless the record says otherwise.
- No database credential in GitHub; GitHub jobs return artifacts that the server pulls (0061). Changes to the build workflows and `deploy/` are founder merges (group A plan, `AGENTS.md`).
- Searched postcodes never leave our systems or reach a log (0046).
- Packages: `psycopg[binary,pool]` 3.x with its licence exception, `sqlalchemy` 2.x, `alembic` 1.x (0062); `dagster`, `dagster-webserver` (0061). Anything else (for example `boto3` for R2) is proposed to the founder in its pull request. The pull request that first adds a package is a founder merge (0035).
- Test names `test_<method>_<condition>_<result>`; `make check` passes after every task; test expectations are worked out by hand, with their working (rule 2).

## Review Focus
1. **Two runs switching the same source at once** (an overlapping run and a rollback): the second waits for the lock and never leaves a half-switched view (Task 3).
2. **A publisher's file changes shape** (a renamed or missing column): the edition fails its checks with a named reason, the live one stays, and the source goes late if it keeps happening (Tasks 3, 5, 6).
3. **A source returns exactly the same file again**: no new edition, but freshness is confirmed (Task 5).
4. **A postcode typed in any case or spacing** ("nb14xy", " NB1  4XY ") finds the same row; a malformed one is "not a postcode", never "unknown" (Task 7).
5. **A walking route that doesn't exist** (an island, a fenced site) is `no_route`, and a place beyond the build's reach is `not_computed`; neither is ever shown as 0 minutes (Task 8).

---

### Task 1: Package, migrations and the test database
**Files:** Create `packages/vestagraph-pipeline/` (`pyproject.toml`, `src/vestagraph_pipeline/__init__.py`, `db.py`, `migrations/` with Alembic's `env.py` and the first revision), `packages/vestagraph-pipeline/tests/conftest.py`; Modify `pyproject.toml` (mypy files and paths, coverage `source_pkgs`, pytest `testpaths`/`pythonpath`), `Makefile` (a `test-db` step), `.github/workflows/ci.yml` (a PostGIS service), `.github/workflows/dependency-review.yml` (the psycopg exception, citing 0062), `AGENTS.md` ("Commands": Docker needed), `docs/references/third-party.md`.

**Interfaces:**
- Produces: `engine_from_url(url: str) -> sqlalchemy.Engine`; the first migration creates schemas `area` and `personal` (0058), extension `postgis`, table `area.editions(source text, edition int, fetched_at timestamptz, publisher_date date null, row_count int null, raw_sha256 text, checks jsonb, status text check in ('candidate','live','failed','retired'), primary key (source, edition))` and table `area.source_state(source text primary key, last_confirmed_at timestamptz null, last_failure text null)`.
- Test fixture `pg_url` (session scope): the `VESTAGRAPH_TEST_DATABASE_URL` environment variable if set (CI), otherwise a PostGIS container started with `docker run` (image pinned by digest, a random free port) and removed at session end.

- [ ] **Step 1:** Write `test_migrations_upgrade_head_creates_schemas_and_editions` (after `alembic upgrade head`: both schemas exist, `postgis` is installed, `area.editions` has the columns above) and `test_migrations_downgrade_base_removes_them`.
- [ ] **Step 2:** Run them: they fail.
- [ ] **Step 3:** Implement; the `Makefile` runs the container before `test` only when the variable is unset and always removes it (a trap); CI sets the variable from its service.
- [ ] **Step 4:** `make check` passes locally (with Docker) and the CI change passes on the pull request.
- [ ] **Step 5:** Commit `feat: pipeline package, migrations and a real test database (0062)`. This pull request is a founder merge (new packages, CI change).

### Task 2: The licence register
**Files:** Create `packages/fixtures/schema/source-register.schema.json`, `packages/fixtures/reference/source-register.json`; Modify `packages/fixtures/reference/README.md`, the fixture validator's file list; Test `packages/vestagraph-fixture-validator/tests/test_fixtures_source_register.py`, `packages/vestagraph-pipeline/tests/test_pipeline_register.py`.

**Interfaces:**
- Record fields (0061 design, DA-05): `id`, `name`, `publisher`, `sourceUrl`, `licence` {`name`, `url`}, `licenceReadOn` (date), `attribution`, `restrictions` (list), `personalData` (`none` or a description), `status` (`cleared`|`open`|`blocked`), `statusDecision` (the founder's words and date; required when `cleared`), `featureSwitch`, `cadence`, `allowedAge` (ISO 8601 duration), `bigSource` (bool), `emptyIsValid` (bool), `rowChangeLimit` (default 0.2), `notes`.
- Produces: `load_register(path: Path) -> dict[str, SourceRecord]`; `require_cleared(record: SourceRecord) -> None` (raises `SourceNotCleared` naming the source).
- First records: `police-uk-crime`, `ea-flood-risk-postcode`, `ons-postcode-directory`, `openstreetmap-england`, `ea-flood-zones`, `defra-noise-round-4`, `dft-connectivity`, `bods-timetables`. The four the founder cleared on 20 Nov 2026 (flood zones, noise, connectivity, BODS) are `cleared` with their `statusDecision` and the links in the design (re-read each publisher page and record the date); the others are `open` until the founder decides each.

- [ ] **Step 1:** Write `test_source_register_cleared_without_decision_rejected`, `test_source_register_unknown_status_rejected`, `test_require_cleared_open_source_raises` and `test_require_cleared_cleared_source_passes`.
- [ ] **Step 2:** Run: fail. **Step 3:** Implement and write the records. **Step 4:** `make check` passes.
- [ ] **Step 5:** Bring each `open` record to the founder in a prompt window (case by case) and record the answers; commit `feat: source licence register (DA-05)`.

### Task 3: Editions, checks, switch live and roll back
**Files:** Create `src/vestagraph_pipeline/editions.py`, `checks.py`; Test `tests/test_pipeline_editions.py`, `tests/test_pipeline_checks.py`.

**Interfaces:**
- `CheckResult(name: str, passed: bool, detail: str)`; `run_checks(rows: Sequence[Mapping[str, object]], record: SourceRecord, previous_count: int | None) -> list[CheckResult]` (always runs: required columns, allowed values or ranges, row-change limit; an empty list fails unless `emptyIsValid`).
- `save_edition(conn, source: str, rows, raw_sha256: str, publisher_date: date | None) -> int` (creates `area.<source>_e<n>`, inserts rows, writes an `editions` row with status `candidate`; returns `n`).
- `switch_live(conn, source: str, edition: int) -> None`: takes `pg_advisory_xact_lock(hashtext(source))`; refuses an edition whose checks did not all pass (`EditionNotPassed`); in one transaction drops and recreates `area.<source>_current` (so a column change works), marks the edition `live` and the old one `retired`; then prunes passed editions beyond 3 (2 when `bigSource`), never the live one.
- `rollback(conn, source: str, edition: int) -> None`: `switch_live` to an earlier passed edition.

- [ ] **Step 1:** Write tests: `test_switch_live_failed_edition_refused_live_unchanged`; `test_switch_live_column_change_recreates_view`; `test_rollback_to_failed_edition_refused`; `test_switch_live_concurrent_second_waits_for_lock` (two connections in threads; the view is never missing); `test_prune_keeps_three_or_two_for_big_sources`; `test_run_checks_empty_rows_fail_unless_empty_is_valid`; `test_run_checks_missing_value_stays_none_not_zero`; `test_run_checks_row_change_over_twenty_percent_fails` (worked example: previous 1,000 rows, new 790 → 21% drop → fail; 801 → 19.9% → pass).
- [ ] **Step 2:** Run: fail. **Step 3:** Implement. **Step 4:** `make check` passes.
- [ ] **Step 5:** Commit `feat: pipeline editions, checks, switch live and roll back`.

### Task 4: Raw files
**Files:** Create `src/vestagraph_pipeline/raw_store.py`; Test `tests/test_pipeline_raw_store.py`.

**Interfaces:** `RawStore` protocol: `put(source: str, data: bytes) -> str` (returns the SHA-256), `has(source: str, sha256: str) -> bool`, `prune(source: str, keep: int) -> None`; `LocalRawStore(root: Path)` for tests and development; `R2RawStore(bucket: str, endpoint: str)` (S3 API to an EU bucket; the client package is proposed to the founder in this task's pull request; credentials from the server's secret files, never from the environment).

- [ ] **Step 1:** Write `test_local_raw_store_same_bytes_same_hash`, `test_local_raw_store_prune_keeps_newest_three`. **Step 2:** fail. **Step 3:** implement; R2 is exercised only by a contract test outside the merge gate (0029). **Step 4:** pass. **Step 5:** Commit `feat: raw file store`.

### Task 5: Running a source and freshness
**Files:** Create `src/vestagraph_pipeline/run.py`, `freshness.py`; Test `tests/test_pipeline_run.py`, `tests/test_pipeline_freshness.py`.

**Interfaces:**
- `Adapter` protocol: `fetch() -> bytes`, `tidy(raw: bytes) -> TidyResult(rows, publisher_date)` (raises `TidyError` with a reason).
- `run_source(conn, store: RawStore, record: SourceRecord, adapter: Adapter, now: datetime) -> RunOutcome` (`unchanged` | `live` | `failed`): `require_cleared`; fetch; if the raw hash matches the live edition's, confirm and return `unchanged`; else store raw, tidy, check, save, switch live; set `source_state.last_confirmed_at = now` only on `unchanged` or `live`; on failure write `last_failure`.
- `freshness(conn, register, now: datetime) -> dict[str, Literal["fresh","late","failing"]]` (`late` when `now - last_confirmed_at > allowedAge` or never confirmed; `failing` when the last run failed); `write_state_file(path: Path, states) -> None` (JSON, source ids and states only; written atomically). The API's `/healthz/data` (#93) serves this file; nothing reads the database per request.

- [ ] **Step 1:** Write `test_run_source_same_raw_twice_confirms_without_new_edition`; `test_run_source_tidy_error_keeps_live_and_last_confirmed`; `test_run_source_not_cleared_raises_before_fetch`; `test_freshness_failed_fetches_go_late_after_allowed_age` (worked example: allowed age P45D, last confirmed 1 Oct, now 16 Nov → 46 days → late); `test_write_state_file_contains_no_rows`.
- [ ] **Step 2:** fail. **Step 3:** implement. **Step 4:** pass. **Step 5:** Commit `feat: run a source and track freshness`.

### Task 6: Model sources, crime and flood risk by postcode
**Files:** Create `src/vestagraph_pipeline/sources/police_uk_crime.py`, `sources/ea_flood_risk_postcode.py`, small sample files under `tests/samples/` (synthetic, shaped like each publisher's format; or a few real rows with their licence recorded in the sample's README); Test `tests/test_sources_police_uk_crime.py`, `tests/test_sources_ea_flood_risk_postcode.py`.

**Interfaces:** each module exports `ADAPTER: Adapter` and the source id matching the register. Tidy keeps each fact's official level (DA-14) and the publisher's date; it never computes a shown figure (rule 2).

- [ ] **Step 1:** For each source, tests for: a good sample tidies to the expected rows (counts worked by hand in the test); a renamed column fails with the column named; a missing value stays `None`. Crime: the publisher's month (about two months behind) becomes `publisher_date`, and freshness still counts from the fetch.
- [ ] **Step 2:** fail. **Step 3:** implement, checking each publisher's current file format and terms on its official page first (record the date in the register). **Step 4:** pass; a nightly contract test (outside the merge gate) fetches each live. **Step 5:** Commit `feat: crime and flood risk by postcode sources`.

### Task 7: Postcode lookup (DA-06)
**Files:** Create `sources/ons_postcode_directory.py`, `src/vestagraph_pipeline/postcodes.py`; Test `tests/test_pipeline_postcodes.py`.

**Interfaces:** `normalise_postcode(text: str) -> str | None` (upper case, one space before the last three characters; `None` when not a postcode); `lookup_postcode(conn, text: str) -> PostcodeResult` with `outcome` one of `found`, `not-covered-nation` (Wales, Scotland), `not-covered-ni` (Northern Ireland, `BT`, not loaded), `not-covered-crown-dependency` (Channel Islands, Isle of Man, by the directory's country code), `retired` (with its end date), `unknown`, `not-a-postcode`; `found` carries the point and the area codes. Lookups never log the postcode.

- [ ] **Step 1:** Tests, one per outcome, plus `test_normalise_postcode_case_and_spacing` (" nb1  4xy " → "NB1 4XY") and `test_lookup_postcode_writes_no_log` (capture logging; the postcode never appears). Confirm the directory's country codes and county field on the ONS user guide for the edition in use, and cite it in the test file.
- [ ] **Step 2:** fail. **Step 3:** implement; the adapter loads England, Wales and Scotland rows and the Crown Dependencies' country codes only (no Northern Ireland rows). **Step 4:** pass. **Step 5:** Commit `feat: our own postcode lookup (DA-06)`.

### Task 8: Walking times (DA-08), Sheffield first
**Files:** Create `.github/workflows/walking-times.yml`, `tools/walking_times/` (graph build and matrix scripts), `sources/walking_times.py`; Test `tests/test_sources_walking_times.py`, `tools/tests/test_tools_walking_times.py`.

**Interfaces:**
- Workflow: `workflow_dispatch` only, input `area` (`sheffield` or `england`), `permissions: contents: read` (uploading an artifact needs no extra permission; use the repository's pinned `actions/upload-artifact`); no database credential; Valhalla's official image pinned by digest; uploads `walking-times-<area>-<osm-date>.csv.gz` and its SHA-256 as an artifact; `persist-credentials: false`, no caches. Founder merge.
- Rows: `postcode`, `category`, `place_id`, `place_source`, `minutes` (null unless `status = ok`), `status` (`ok`|`no_route`|`not_computed`), `osm_date`, `method` ("Valhalla pedestrian, default walking speed").
- `sources/walking_times.py`: an `Adapter` whose `fetch` downloads the artifact through GitHub's API with the server's fine-grained token and checks the SHA-256.

- [ ] **Step 1:** Tests: `test_walking_times_no_route_has_null_minutes`; `test_walking_times_beyond_five_km_is_not_computed`; `test_walking_times_checksum_mismatch_fails`; `test_tools_walking_times_nearest_ten_per_category_within_five_km` (worked example on a hand-made grid of 12 places).
- [ ] **Step 2:** fail. **Step 3:** implement; destinations come from official datasets where they exist (schools from DfE, stops from NaPTAN), everyday places and parks from OpenStreetMap; each edition's table is published under ODbL as a release asset with "© OpenStreetMap contributors".
- [ ] **Step 4:** Run the Sheffield build once by hand; record build time, artifact size, rows and the share of `no_route` and `not_computed` in `docs/reviews/<date>-walking-times-sheffield-trial.md`; **stop and bring the numbers to the founder** before running England (0061: "the agent comes back to the founder if 5 km proves too costly").
- [ ] **Step 5:** Commit `feat: walking times build, Sheffield trial (DA-08)`.

### Task 9: Dagster (stop point: the memory check)
**Stop point:** start only when group A's Task 9 has measured at least about 1.5 GB free on the server. Otherwise do not build this task: tell the founder, and plan the fallback (systemd timers and a VPN-only admin page with a canvas board and specification first).

**Files:** Create `packages/vestagraph-dagster/` (`definitions.py`, `assets.py`, `schedules.py`, `jobs.py`), `deploy/dagster.Dockerfile`, a `dagster` service in `deploy/compose.yml`; Test `packages/vestagraph-dagster/tests/test_dagster_definitions.py`.

**Interfaces:** one asset per register source with a blocking asset check that calls `run_checks`; schedules from each record's `cadence`; a `rollback_job` with config `{source, edition}` calling `rollback`; a `dispatch_walking_times` sensor that starts the GitHub workflow when Geofabrik's England extract date changes; run storage SQLite on a server volume; telemetry off; the webserver bound only to the WireGuard interface address (never `0.0.0.0`).

- [ ] **Step 1:** Tests: `test_dagster_definitions_load_one_asset_per_cleared_source`; `test_dagster_rollback_job_calls_rollback` (in process, as the spike did); `test_dagster_schedules_follow_register_cadence`.
- [ ] **Step 2:** fail. **Step 3:** implement; confirm on Dagster's deployment documentation that the webserver and daemon can share SQLite storage, otherwise run both in one container. **Step 4:** pass. **Step 5:** Commit `feat: Dagster runs the pipeline (VPN-only dashboard)`.

### Task 10: Infrastructure (the private infrastructure repository)
Written as a phase plan in that repository, under its own rules; nothing from it comes back here.
- [ ] The R2 bucket (EU) and a token limited to it; the GitHub fine-grained token (this repository, Actions read and write, with an expiry); both in SOPS.
- [ ] The Dagster container on the WireGuard interface only; checked from outside the VPN (direct and through Cloudflare) that it cannot be reached.
- [ ] The uptime workflow checks `/healthz/data` (served by the API from the state file) and alerts on `late` or `failing`; a deliberately late source has raised an alert (launch blocker 3).

## After this plan
Each other pilot source is its own ticket in Task 6's pattern, taken from `docs/references/data-sources.md` and the register, starting with the bus timetable inputs (a GitHub build like Task 8). The API (#93) serves `/healthz/data` and About the data from the register and the live editions (0061).
