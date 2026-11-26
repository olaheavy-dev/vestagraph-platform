"""The FastAPI app; `fastapi dev` and `fastapi run` find it through [tool.fastapi].

create_app builds a fresh app (tests build one per test); resources that live as long as the
process are opened and closed in lifespan.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, MutableMapping
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.telemetry import TelemetryConfig

from vestagraph_api import area, health
from vestagraph_api.limits import BodyLimit, SecurityHeaders
from vestagraph_api.log import REQUEST_ID_HEADER, configure_logging, request_context
from vestagraph_api.problems import UnhandledErrors, install_problem_handlers
from vestagraph_api.settings import Settings, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.area = area.load_area_data(app.state.settings.fixtures_dir)
    yield


def _not_health(scope: MutableMapping[str, Any]) -> bool:
    # Probes hit the health routes every few seconds; their spans would drown the real traffic.
    path = str(scope.get("path", ""))
    return path == "/healthz" or path.startswith("/health/")


# Always off, whatever the environment says (an explicit value beats FASTAPI_OTEL_AUTO_CONFIGURE):
# exported spans carry the URL path and query, and no request data may leave the process (0014).
TELEMETRY: TelemetryConfig = {"auto_configure": False, "exclude": _not_health}


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings)
    docs = settings.docs_on
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs" if docs else None,
        redoc_url=None,
        openapi_url="/openapi.json",
        telemetry=TELEMETRY,
    )
    app.state.settings = settings
    app.state.readiness_checks = {}
    install_problem_handlers(app)
    # Registered before request_context, which therefore wraps it: a 413 still gets an access line.
    app.add_middleware(BodyLimit, max_bytes=settings.max_request_bytes)
    app.middleware("http")(request_context)
    # Outside request_context (so it knows the request id), inside CORS and the headers (so an
    # unexpected 500 still carries them).
    app.add_middleware(UnhandledErrors)
    # Outermost, in this order: hosts are checked first, then CORS answers preflights.
    app.add_middleware(SecurityHeaders)
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=[REQUEST_ID_HEADER, "Retry-After"],
        )
    if settings.allowed_hosts != ["*"]:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
    app.include_router(health.router)
    app.include_router(health.root_router)
    app.include_router(area.router)
    return app


app = create_app()
