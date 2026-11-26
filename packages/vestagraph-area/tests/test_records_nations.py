"""The nation each sample postcode belongs to, as the reader returns it."""

import json
from pathlib import Path

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.records import InvalidAreaDataError, read_postcode_area

DATA = fixtures_directory() / "data"


def test_read_postcode_area_nations_reads_each_entry() -> None:
    area = read_postcode_area(DATA / "postcode-area.json")

    assert area.nations["NB1 4XY"] == "england"
    assert area.nations["ZZ1 0AA"] == "wales"


def test_read_postcode_area_unknown_nation_raises(tmp_path: Path) -> None:
    data = read_json(DATA / "postcode-area.json")
    data["postcodes"][0]["nation"] = "mars"
    path = tmp_path / "postcode-area.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(InvalidAreaDataError, match="mars"):
        read_postcode_area(path)
