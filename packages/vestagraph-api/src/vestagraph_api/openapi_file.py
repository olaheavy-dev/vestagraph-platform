"""Writes ``packages/vestagraph-api/openapi.json``: the API's contract (decision 0060, BE-02).

Run with ``python -m vestagraph_api.openapi_file`` (``make generate`` does). The file is
committed, and ``make generated-check`` fails if it is stale.
"""

from __future__ import annotations

import json
from pathlib import Path

from vestagraph_api.main import create_app
from vestagraph_api.settings import Settings

OPENAPI_FILE = Path(__file__).resolve().parents[2] / "openapi.json"


def render() -> str:
    # No .env and no environment-specific values: the description must be the same everywhere.
    app = create_app(Settings(_env_file=None, app_env="test"))
    return json.dumps(app.openapi(), indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    OPENAPI_FILE.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
