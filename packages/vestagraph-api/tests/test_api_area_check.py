"""POST /api/area-check: the three answers, bad bodies, the body limit and the closed state."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from vestagraph_api.main import create_app
from vestagraph_api.settings import Settings

pytestmark = pytest.mark.anyio

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"
SCHEMA_BASE = "https://vestagraph.invalid/schema/"


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
    app = create_app(Settings(_env_file=None, app_env="test", area_check_open=True))
    async for client in _client(app):
        yield client


def _validator(schema_file: str, definition: str) -> Draft202012Validator:
    registry: Registry[Any] = Registry()
    for path in (FIXTURES / "schema").glob("*.schema.json"):
        document = json.loads(path.read_text(encoding="utf-8"))
        registry = registry.with_resource(
            document["$id"], Resource.from_contents(document, DRAFT202012)
        )
    return Draft202012Validator(
        {"$ref": f"{SCHEMA_BASE}{schema_file}#/$defs/{definition}"}, registry=registry
    )


def _generated(postcode: str) -> dict[str, Any]:
    document = json.loads((FIXTURES / "generated" / "area-result.json").read_text("utf-8"))
    return next(p for p in document["postcodes"] if p["postcode"] == postcode)


def _file_records(postcode: str) -> list[dict[str, Any]]:
    document = json.loads((FIXTURES / "data" / "postcode-area.json").read_text("utf-8"))
    return [r for r in document["area"] if r["postcode"] == postcode]


@pytest.mark.parametrize("postcode", ["NB1 4XY", "NB7 1RR"])
async def test_area_check_found_equals_generated_result(
    client: httpx.AsyncClient, postcode: str
) -> None:
    response = await client.post("/api/area-check", json={"postcode": postcode})
    assert response.status_code == 200
    body = response.json()
    assert body["state"] == "found"
    assert body["postcode"] == postcode
    assert body["nation"] == "england"
    assert body["result"] == _generated(postcode)
    _validator("generated-area-result.schema.json", "postcode").validate(body["result"])
    assert body["records"], "a found postcode quotes its records"
    assert body["records"] == _file_records(postcode)
    record_validator = _validator("postcode-area.schema.json", "postcodeAreaItem")
    for record in body["records"]:
        assert record["postcode"] == postcode
        record_validator.validate(record)


async def test_area_check_typed_loosely_returns_the_datas_spelling(
    client: httpx.AsyncClient,
) -> None:
    response = await client.post("/api/area-check", json={"postcode": "nb14xy"})
    assert response.json()["postcode"] == "NB1 4XY"


async def test_area_check_unknown_returns_not_found(client: httpx.AsyncClient) -> None:
    response = await client.post("/api/area-check", json={"postcode": "NB9 9ZZ"})
    assert response.status_code == 200
    assert response.json() == {"state": "notFound"}


async def test_area_check_wales_returns_not_covered(client: httpx.AsyncClient) -> None:
    response = await client.post("/api/area-check", json={"postcode": "ZZ1 0AA"})
    assert response.status_code == 200
    assert response.json() == {"state": "notCovered", "nation": "wales"}


def test_openapi_not_covered_nation_is_one_of_the_other_nations() -> None:
    app = create_app(Settings(_env_file=None, app_env="test"))
    nation = app.openapi()["components"]["schemas"]["NotCovered"]["properties"]["nation"]
    assert nation["enum"] == ["wales", "scotland", "northern-ireland"]


@pytest.mark.parametrize(
    "content",
    [b"not json at all QWERTY", b'{"postcode": 12}', b"{}", b'{"postcode": "ABCDEFGHIJKLMNOPQ"}'],
    ids=["not-json", "number", "missing", "too-long"],
)
async def test_area_check_bad_body_returns_422_without_input(
    client: httpx.AsyncClient, content: bytes
) -> None:
    response = await client.post(
        "/api/area-check", content=content, headers={"content-type": "application/json"}
    )
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    for secret in ("QWERTY", "ABCDEFGHIJKLMNOPQ", "12"):
        if secret.encode() in content:
            assert secret not in response.text


async def test_area_check_body_over_limit_returns_413(client: httpx.AsyncClient) -> None:
    content = json.dumps({"postcode": "N" * 17_000}).encode()
    response = await client.post(
        "/api/area-check", content=content, headers={"content-type": "application/json"}
    )
    assert response.status_code == 413
    assert "NNNN" not in response.text


async def test_area_check_closed_returns_503_and_logs_no_postcode(
    capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture
) -> None:
    app = create_app(Settings(_env_file=None, app_env="test"))
    async for client in _client(app):
        response = await client.post("/api/area-check", json={"postcode": "NB1 4XY"})
        assert response.status_code == 503
        assert response.json()["title"] == "Not available yet"
        assert "NB1 4XY" not in response.text
    assert "NB1 4XY" not in capsys.readouterr().out + caplog.text


async def test_area_check_closed_problem_type_is_under_our_domain_and_has_no_instance() -> None:
    app = create_app(Settings(_env_file=None, app_env="test"))
    async for client in _client(app):
        body = (await client.post("/api/area-check", json={"postcode": "NB1 4XY"})).json()
        assert body["type"] == "https://vestagraph.com/problems/not-available-yet"
        assert "instance" not in body


@pytest.mark.parametrize("log_json", [True, False], ids=["json", "console"])
async def test_area_check_crash_with_postcode_in_message_logs_no_postcode(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    log_json: bool,
) -> None:
    def explode(*_args: object) -> dict[str, Any]:
        try:
            raise KeyError("inner NB1 4XY")
        except KeyError as inner:
            raise RuntimeError("no record for postcode NB1 4XY") from inner

    monkeypatch.setattr("vestagraph_api.area.postcode_result", explode)
    app = create_app(
        Settings(_env_file=None, app_env="test", area_check_open=True, log_json=log_json)
    )
    async for client in _client(app):
        response = await client.post("/api/area-check", json={"postcode": "NB1 4XY"})
        assert response.status_code == 500
        assert response.headers["content-type"].startswith("application/problem+json")
        assert "NB1 4XY" not in response.text
    logged = capsys.readouterr().out + caplog.text
    assert "NB1 4XY" not in logged
    assert "no record for postcode" not in logged
    # What stays: the exception types and where they were raised.
    assert "RuntimeError" in logged
    assert "KeyError" in logged
    assert "explode" in logged


async def test_validation_problem_has_no_instance(client: httpx.AsyncClient) -> None:
    response = await client.post("/api/area-check", json={})
    assert response.status_code == 422
    assert "instance" not in response.json()


async def test_area_check_closed_ignores_the_body() -> None:
    app = create_app(Settings(_env_file=None, app_env="test"))
    async for client in _client(app):
        for content in (b"not json", b"{}", b""):
            response = await client.post(
                "/api/area-check", content=content, headers={"content-type": "application/json"}
            )
            assert response.status_code == 503


async def test_area_check_open_logs_no_postcode(
    client: httpx.AsyncClient,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    await client.post("/api/area-check", json={"postcode": "NB1 4XY"})
    await client.post("/api/area-check", json={"postcode": "NB9 9ZZ"})
    logged = capsys.readouterr().out + caplog.text
    assert "/api/area-check" in logged
    assert "NB1 4XY" not in logged
    assert "NB9 9ZZ" not in logged


def test_settings_defaults_area_check_closed_and_body_limit_16_kib() -> None:
    settings = Settings(_env_file=None)
    assert settings.area_check_open is False
    assert settings.max_request_bytes == 16 * 1024


def test_settings_defaults_fixtures_dir_is_the_repository_fixtures() -> None:
    settings = Settings(_env_file=None)
    assert settings.fixtures_dir == FIXTURES
    assert (settings.fixtures_dir / "data" / "postcode-area.json").is_file()
