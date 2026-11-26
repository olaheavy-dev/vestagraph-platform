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


async def test_request_id_from_client_header_is_never_used(
    client: httpx.AsyncClient, capsys: pytest.CaptureFixture[str]
) -> None:
    response = await client.get("/healthz", headers={"X-Request-ID": "SW1A1AA"})
    sent_back = response.headers["x-request-id"]
    assert sent_back != "SW1A1AA"
    assert len(sent_back) == 32
    assert sent_back in capsys.readouterr().out
    assert "SW1A1AA" not in response.text


async def test_not_found_problem_has_no_instance(client: httpx.AsyncClient) -> None:
    response = await client.get("/nowhere/NB1-4XY")
    assert response.status_code == 404
    assert "instance" not in response.json()
    assert "NB1-4XY" not in response.text


async def test_cors_preflight_does_not_allow_credentials() -> None:
    app = create_app(
        Settings(_env_file=None, app_env="test", cors_origins=["https://app.example.com"])
    )
    async for client in _client(app):
        response = await client.options(
            "/healthz",
            headers={
                "Origin": "https://app.example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.headers["access-control-allow-origin"] == "https://app.example.com"
        assert "access-control-allow-credentials" not in response.headers


def test_settings_cors_origins_wildcard_is_refused() -> None:
    with pytest.raises(ValueError, match="CORS_ORIGINS"):
        Settings(_env_file=None, cors_origins=["https://ok.example.com", "*"])


def test_settings_allowed_hosts_read_from_a_json_list_in_the_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ALLOWED_HOSTS", '["vestagraph.com","127.0.0.1"]')
    assert Settings(_env_file=None).allowed_hosts == ["vestagraph.com", "127.0.0.1"]


def test_main_module_has_no_import_time_app() -> None:
    import vestagraph_api.main as main

    assert not hasattr(main, "app")


def test_openapi_info_is_the_apis_own() -> None:
    app = create_app(Settings(_env_file=None, app_env="test"))
    assert app.openapi()["info"] == {"title": "Vestagraph API", "version": "0.1.0"}


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
