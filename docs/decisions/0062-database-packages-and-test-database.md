# 0062: Database packages (psycopg with a licence exception, SQLAlchemy, Alembic) and a real test database

**ID:** BE-40  
**Status:** Accepted (founder, 20 Nov 2026, prompt windows)  
**Date:** 2026-11-20  
**Stage:** 5b (for the group B build, [0061](0061-pilot-data-pipeline-postcodes-and-walking-times.md); the API, #93, uses the same packages)  
**Amends (older records get a dated status note, no other rewrite):** [0027](0027-stage-2-engineering-hardening.md)'s licence allow-list, with one named exception (the three psycopg packages); [0049](0049-back-to-python-final.md)'s note that the FastAPI template's runtime packages are not pre-approved and are approved by the founder at #93: three of them are approved here, earlier, for the pipeline.

## Context
The data pipeline (0061) stores every edition in PostgreSQL on Neon (0060), so it needs a PostgreSQL driver. The founder's FastAPI template, the API's starting point (0049), uses psycopg 3 under SQLAlchemy and Alembic. psycopg is licensed LGPL-3.0, which 0027's allow-list blocks unless the founder records an exception. The pipeline's switch-live and roll-back logic must also be tested against a real database, which `make check` (Python only) cannot do today.

## Options
- **Driver:** psycopg 3 (LGPL-3.0; the most used and most actively maintained of the three: about 222 million downloads in the month to 20 Nov 2026 and 11 releases in the past year, per pypistats.org and PyPI), asyncpg (Apache-2.0; about 148 million, 2 releases; async only), pg8000 (BSD-3; about 56 million, 1 release).
- **Query layer:** SQLAlchemy and Alembic, as the template does; or plain SQL files with a small runner of our own.
- **Test database:** a throwaway PostGIS container started by `make check`, with GitHub's database service in CI; or database tests outside `make check`.

## Decision
The founder's words, 20 Nov 2026 (prompt windows):
1. After asking "which is better used, and popular and well maintained" and "what psycopg used for again": **"psycopg + exception (Recommended)"**; then, when the pre-push review found that the template's install also brings psycopg-binary and psycopg-pool (both LGPL-3.0-only): **"Yes, all three (Recommended)"**.
2. **"Yes, like the template (Recommended)"**: SQLAlchemy and Alembic.
3. **"Docker locally, service in CI (Recommended)"**.

So:
- **psycopg** (3.x, with its `binary` and `pool` extras as the template uses them) is approved, with a **licence exception for psycopg, psycopg-binary and psycopg-pool only** (all LGPL-3.0-only, same maintainers). We use them unmodified. Running them on our own server is not distribution; publishing a container image that contains them is, so any such image carries their licence texts (the GPL and LGPL texts shipped in the wheels) and a pointer to their source (PyPI); the binary wheel also bundles libpq and OpenSSL, whose own licence files come with it. The three are added to the dependency check's `allow-dependencies-licenses` list, with a comment naming this record, in the pull request that first adds them. (This is the agent's summary of the licence, not legal advice.)
- **SQLAlchemy** (2.x) and **Alembic** (1.x), both MIT, are approved. The pipeline uses SQLAlchemy's plain-SQL layer (Core) for bulk loads and view switches; the API uses its ORM. One Alembic migration history serves the pipeline and the API.
- **Test database:** `make check` starts a throwaway PostGIS container (Docker Desktop on the founder's machine) and removes it afterwards; CI uses a PostGIS service container. The same database tests run in both. `make check`'s requirements in `AGENTS.md` gain Docker. The pull request that changes the CI workflow is a founder merge (CI permissions and settings).

## Consequences
- Pipeline and API share one driver, one query layer and one migration history; #93 adds no new database packages.
- **Aspire (0049 item 10, #94)** is for running the whole app locally (API, frontend, Dagster and the database together, with one dashboard). It uses Docker itself and will run the same PostGIS image. The tests do not depend on it: `make check` and CI start their own throwaway database, so they need no Node.js or Aspire CLI. Founder asked: "will aspire not help with docker?" (20 Nov 2026).
- `make check` needs Docker running locally (it already runs for other projects; the founder keeps Docker Desktop running).
- **Revisit if** psycopg's licence changes, its maintenance stops, or a lawyer advises otherwise on the LGPL exception.
