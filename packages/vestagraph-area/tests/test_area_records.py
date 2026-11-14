"""The readers: what they return from the committed data, and what they refuse."""

import json
from pathlib import Path
from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.records import (
    InvalidAreaDataError,
    read_postcode_area,
    read_registry,
    read_sample_priorities,
)

DATA = fixtures_directory() / "data"


def _write(tmp_path: Path, name: str, value: Any) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_read_registry_committed_data_returns_every_topic() -> None:
    registry = read_registry(DATA / "pilot-topics.json")

    raw = read_json(DATA / "pilot-topics.json")
    assert registry.nation == "england"
    assert [t.key for t in registry.topics] == [t["key"] for t in raw["topics"]]
    family = next(t for t in registry.topics if t.key == "family-view")
    assert family.counted is False
    assert "childcare" in family.record_subtypes
    noise = next(t for t in registry.topics if t.key == "noise")
    assert noise.official_route is not None


def test_read_postcode_area_committed_data_returns_postcodes_and_records() -> None:
    area = read_postcode_area(DATA / "postcode-area.json")

    assert area.postcodes == ("NB1 4XY", "NB7 1RR")
    assert area.unknown_postcodes == ("NB9 9ZZ",)
    assert len(area.records) == 56
    childcare = next(r for r in area.records if r.id == "NB1-4XY-AREA-AMENITY-6")
    assert (childcare.subtype, childcare.status, childcare.value) == (
        "childcare",
        "no-record-in-source",
        None,
    )


def test_read_sample_priorities_committed_data_returns_exact_limits() -> None:
    priorities = read_sample_priorities(DATA / "sample-priorities.json")

    rail = next(p for p in priorities if p.id == "SAMPLE-PRIORITY-RAIL")
    assert (rail.filter_field, rail.filter_equals, rail.measure) == (
        "stopType",
        "rail-station",
        "distance",
    )
    assert (str(rail.limit_value), rail.limit_unit) == ("3/2", "miles")
    assert len(priorities) == 6


def test_read_postcode_area_bus_departures_unknown_stop_raises_invalid_area_data(
    tmp_path: Path,
) -> None:
    data = read_json(DATA / "postcode-area.json")
    bus = next(r for r in data["area"] if r["topic"] == "bus-departures" and "value" in r)
    bus["value"]["stopItemId"] = "NB1-4XY-AREA-TRANSPORT-STOP-99"

    with pytest.raises(InvalidAreaDataError, match="TRANSPORT-STOP-99"):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))


def test_read_postcode_area_bus_departures_stop_of_other_postcode_raises_invalid_area_data(
    tmp_path: Path,
) -> None:
    data = read_json(DATA / "postcode-area.json")
    bus = next(r for r in data["area"] if r["topic"] == "bus-departures" and "value" in r)
    bus["value"]["stopItemId"] = "NB7-1RR-AREA-TRANSPORT-STOP-1"

    with pytest.raises(InvalidAreaDataError, match="NB7-1RR-AREA-TRANSPORT-STOP-1"):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))


def test_read_sample_priorities_unknown_topic_key_raises_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(DATA / "sample-priorities.json")
    data["priorities"][0]["topicKey"] = "no-such-topic"
    path = _write(tmp_path, "sample-priorities.json", data)

    with pytest.raises(InvalidAreaDataError, match="no-such-topic"):
        read_sample_priorities(path, read_registry(DATA / "pilot-topics.json"))


def test_read_postcode_area_not_json_raises_invalid_area_data(tmp_path: Path) -> None:
    path = tmp_path / "postcode-area.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(InvalidAreaDataError):
        read_postcode_area(path)


def test_read_postcode_area_record_missing_status_raises_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(DATA / "postcode-area.json")
    del data["area"][0]["status"]

    with pytest.raises(InvalidAreaDataError, match="status"):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))
