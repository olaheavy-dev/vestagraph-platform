"""The resolved JSON Schemas the OpenAPI description carries, read from package data.

``contract_schemas.json`` is written by ``make generate`` (see ``schemas.py``) and ships inside
the package, so nothing outside ``vestagraph_api`` is needed to start the app.
"""

from __future__ import annotations

import json
from importlib import resources
from typing import Any


def _load() -> dict[str, dict[str, Any]]:
    text = resources.files("vestagraph_api").joinpath("contract_schemas.json").read_text("utf-8")
    loaded: dict[str, dict[str, Any]] = json.loads(text)
    return loaded


_SCHEMAS = _load()
RESULT_SCHEMA = _SCHEMAS["result"]
RECORD_SCHEMA = _SCHEMAS["record"]
