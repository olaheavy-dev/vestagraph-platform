"""The contract schemas ship as package data; the API never reads the fixtures' schema folder."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from vestagraph_api import schemas

SRC = Path(__file__).resolve().parents[1] / "src" / "vestagraph_api"
FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"
RUNTIME_MODULES = [p for p in SRC.glob("*.py") if p.name != "schemas.py"]


def test_contract_schemas_file_matches_the_fixtures_schemas() -> None:
    assert (SRC / "contract_schemas.json").read_text(encoding="utf-8") == schemas.render()


def test_runtime_modules_do_not_reference_the_fixtures_schema_folder() -> None:
    for path in RUNTIME_MODULES:
        text = path.read_text(encoding="utf-8")
        assert "SCHEMA_DIR" not in text, path.name
        assert '/ "schema"' not in text, path.name
        assert ".schema.json" not in text, path.name


def test_main_imports_without_the_fixtures_schema_folder(tmp_path: Path) -> None:
    shutil.copytree(FIXTURES / "data", tmp_path / "fixtures" / "data")
    env = {**os.environ, "FIXTURES_DIR": str(tmp_path / "fixtures"), "ENV_FILE": ""}
    work = tmp_path / "work"
    work.mkdir()
    result = subprocess.run(
        [sys.executable, "-c", "import vestagraph_api.main as m; m.create_app()"],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
