"""The committed openapi.json is the API contract (decision 0060, BE-02)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vestagraph_api.main import create_app
from vestagraph_api.settings import Settings

PACKAGE = Path(__file__).resolve().parents[1]
GENERATED_SCHEMA = (
    Path(__file__).resolve().parents[2]
    / "fixtures"
    / "schema"
    / "generated-area-result.schema.json"
)


def _openapi() -> dict[str, Any]:
    app = create_app(Settings(_env_file=None, app_env="test"))
    document: dict[str, Any] = app.openapi()
    return document


def test_openapi_file_matches_app() -> None:
    expected = json.dumps(_openapi(), indent=2, ensure_ascii=False) + "\n"
    assert (PACKAGE / "openapi.json").read_text(encoding="utf-8") == expected


def test_openapi_found_result_has_the_generated_schemas_required_keys() -> None:
    found = _openapi()["components"]["schemas"]["Found"]["properties"]["result"]
    generated = json.loads(GENERATED_SCHEMA.read_text(encoding="utf-8"))["$defs"]["postcode"]
    assert found["required"] == generated["required"]
    assert {"glance", "topics", "distances", "busesPerHour", "priorities"} <= set(found["required"])


def test_openapi_found_records_items_have_the_record_shape() -> None:
    items = _openapi()["components"]["schemas"]["Found"]["properties"]["records"]["items"]
    assert {"postcode", "level"} <= set(items["required"])


def test_openapi_document_has_no_refs_to_files() -> None:
    text = json.dumps(_openapi())
    assert ".schema.json" not in text
    assert '"$id"' not in text


def test_openapi_422_response_does_not_mention_input() -> None:
    response = _openapi()["paths"]["/api/area-check"]["post"]["responses"]["422"]
    assert "application/problem+json" in response["content"]
    assert "input" not in json.dumps(response)


def test_openapi_503_response_is_problem_details_titled_not_available_yet() -> None:
    response = _openapi()["paths"]["/api/area-check"]["post"]["responses"]["503"]
    assert "application/problem+json" in response["content"]
    assert "Not available yet" in json.dumps(response)
