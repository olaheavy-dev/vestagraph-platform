"""The fixtures' JSON Schemas, made self-contained for the OpenAPI description.

The schemas in ``packages/fixtures/schema/`` stay the single source of the shapes. This module
loads them and replaces every ``$ref`` with the schema it points to, so the OpenAPI document
has no reference to a file on disk (the web app's types are generated from it, #95). Nothing
is copied by hand.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_DIR = Path(__file__).resolve().parents[3] / "fixtures" / "schema"
_DROPPED = frozenset({"$schema", "$id"})


def _load(name: str) -> dict[str, Any]:
    document: dict[str, Any] = json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))
    return document


def _follow(document: dict[str, Any], pointer: str) -> Any:
    node: Any = document
    for part in pointer.removeprefix("#").split("/")[1:]:
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def _inline(node: Any, document: dict[str, Any], file_name: str) -> Any:
    if isinstance(node, list):
        return [_inline(item, document, file_name) for item in node]
    if not isinstance(node, dict):
        return node
    if "$ref" in node:
        target, _, pointer = str(node["$ref"]).partition("#")
        other_name = target or file_name
        other = document if not target else _load(target)
        resolved = _inline(_follow(other, f"#{pointer}"), other, other_name)
        siblings = {k: v for k, v in node.items() if k != "$ref"}
        return {**resolved, **_inline(siblings, document, file_name)} if siblings else resolved
    return {k: _inline(v, document, file_name) for k, v in node.items() if k not in _DROPPED}


def definition(file_name: str, name: str) -> dict[str, Any]:
    """``$defs/<name>`` of one schema file, with every reference followed."""
    document = _load(file_name)
    resolved: dict[str, Any] = _inline(document["$defs"][name], document, file_name)
    return resolved
