"""Tests for tools/launch_placeholders.json, the launch guard's list of draft strings (OP-06).

The specifications show unfinished text on purpose (SE-07). Every such "before launch" string
must be in the list, so the release's launch guard can find it in the built pages.
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LIST_PATH = REPO_ROOT / "tools" / "launch_placeholders.json"
SPECS_DIR = REPO_ROOT / "docs" / "specs"
QUOTED_BEFORE_LAUNCH = re.compile(r'"([^"\n]*before launch[^"\n]*)"', re.IGNORECASE)


def _load_list() -> list[str]:
    data = json.loads(LIST_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    return [str(entry) for entry in data]


def test_specs_every_before_launch_string_is_in_the_list() -> None:
    listed = set(_load_list())
    missing: list[str] = []
    for feature in sorted(SPECS_DIR.rglob("*.feature")):
        lines = feature.read_text(encoding="utf-8").splitlines()
        missing.extend(
            f'{feature.relative_to(REPO_ROOT)}:{number}: "{found}"'
            for number, line in enumerate(lines, start=1)
            for found in QUOTED_BEFORE_LAUNCH.findall(line)
            if found not in listed
        )
    assert not missing, "Add these draft strings to tools/launch_placeholders.json:\n" + "\n".join(
        missing
    )


def test_specs_contain_at_least_one_before_launch_string() -> None:
    # Guards the test above against a pattern that silently matches nothing.
    texts = (feature.read_text(encoding="utf-8") for feature in SPECS_DIR.rglob("*.feature"))
    assert any(QUOTED_BEFORE_LAUNCH.search(text) for text in texts)


def test_list_entries_are_unique_non_empty_strings() -> None:
    data = json.loads(LIST_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert data
    assert all(isinstance(entry, str) and entry.strip() for entry in data)
    assert len(set(data)) == len(data)


def test_pattern_capital_before_launch_is_matched() -> None:
    assert QUOTED_BEFORE_LAUNCH.findall('says "Before launch, to be written"') == [
        "Before launch, to be written"
    ]
