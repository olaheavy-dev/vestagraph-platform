"""The pilot API's web layer: health, docs switch, security headers and the access log."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from vestagraph_api.main import create_app
from vestagraph_api.settings import Settings

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


async def _client(app: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    async with LifespanManager(app) as manager:
        transport = httpx.ASGITransport(app=manager.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    app = create_app(Settings(_env_file=None, app_env="test", vestagraph_commit="abc"))
    async for client in _client(app):
        yield client


async def test_healthz_returns_status_and_commit(client: httpx.AsyncClient) -> None:
    response = await client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "commit": "abc"}


async def test_health_live_returns_ok(client: httpx.AsyncClient) -> None:
    response = await client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_create_app_production_hides_docs() -> None:
    app = create_app(Settings(_env_file=None, app_env="production"))
    async for client in _client(app):
        assert (await client.get("/docs")).status_code == 404
        assert (await client.get("/redoc")).status_code == 404
        assert (await client.get("/openapi.json")).status_code == 200


async def test_responses_carry_security_headers(client: httpx.AsyncClient) -> None:
    for path in ("/healthz", "/nowhere"):
        headers = (await client.get(path)).headers
        assert headers["x-content-type-options"] == "nosniff"
        assert headers["referrer-policy"] == "no-referrer"
        assert headers["x-frame-options"] == "DENY"
        assert headers["cache-control"] == "no-store"


async def test_access_log_has_route_not_path(
    client: httpx.AsyncClient, capsys: pytest.CaptureFixture[str]
) -> None:
    await client.get("/healthz?x=secret")
    out = capsys.readouterr().out
    assert "/healthz" in out
    assert "secret" not in out
    assert "127.0.0.1" not in out
    assert "testclient" not in out


async def test_create_app_telemetry_cannot_be_switched_on_by_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("FASTAPI_OTEL_AUTO_CONFIGURE", "true")
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
    seen: list[bool] = []

    def record(config: dict[str, object]) -> None:
        seen.append(bool(config["auto_configure"]))

    monkeypatch.setattr("fastapi.telemetry._runtime._configure_from_environment", record)
    app = create_app(Settings(_env_file=None, app_env="test"))
    async for client in _client(app):
        await client.get("/healthz")
    assert seen == [False]


def test_settings_env_file_empty_ignores_dotenv_in_working_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".env").write_text("VESTAGRAPH_COMMIT=from-dotenv\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("VESTAGRAPH_COMMIT", raising=False)
    assert Settings().vestagraph_commit == "unknown"
