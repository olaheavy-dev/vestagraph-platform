# The pilot API image (#93). Build from the repository root:
#   docker build -f deploy/api.Dockerfile --build-arg VESTAGRAPH_COMMIT=<sha> .
# Stage 1 installs the API and its workspace dependencies (no dev group) with uv. Stage 2 copies the
# finished environment, so the image holds no uv, no build tools and no tests.
FROM ghcr.io/astral-sh/uv:0.13.7@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 AS uv

FROM python:3.14-slim@sha256:22eafb370920ad8b429e0aec3fff433e0669968519f5d60469d83729c138b28b AS build
COPY --from=uv /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never
WORKDIR /app
COPY pyproject.toml uv.lock ./
# Every workspace member must be present, or uv --locked reports the lock file as stale. The
# .dockerignore keeps out the fixtures and each member's tests; only the API's packages are installed.
COPY packages/ packages/
RUN uv sync --locked --no-dev --no-editable --package vestagraph-api --no-install-project \
    && uv sync --locked --no-dev --no-editable --package vestagraph-api

FROM python:3.14-slim@sha256:22eafb370920ad8b429e0aec3fff433e0669968519f5d60469d83729c138b28b

LABEL org.opencontainers.image.source="https://github.com/olaheavy-dev/vestagraph-platform"

ARG VESTAGRAPH_COMMIT=unknown
ENV VESTAGRAPH_COMMIT=$VESTAGRAPH_COMMIT \
    FIXTURES_DIR=/app/fixtures \
    PATH=/app/.venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=build /app/.venv /app/.venv
COPY packages/fixtures/data/ /app/fixtures/data/

USER 10001:10001
EXPOSE 8080
CMD ["uvicorn", "--factory", "vestagraph_api.main:create_app", "--host", "0.0.0.0", "--port", "8080", "--no-access-log", "--ws", "none"]
