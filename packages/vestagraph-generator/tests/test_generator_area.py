"""The generator writes ``area-result.json`` beside ``costs.json``."""

import io
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from generator_support import copy_data_to, fixtures_directory, read_json, write_json
from vestagraph_area.records import InvalidAreaDataError
from vestagraph_generator.__main__ import main
from vestagraph_generator.area_generator import generate_area, json_number
from vestagraph_generator.costs_generator import run


def test_run_writes_costs_and_area_result_and_keeps_both(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    generated = fixtures / "generated"
    generated.mkdir()
    (generated / "old.json").write_text("{}", encoding="utf-8")

    exit_code = run(fixtures, io.StringIO())

    assert exit_code == 0
    assert (generated / "costs.json").is_file()
    written = (generated / "area-result.json").read_bytes()
    assert written == generate_area(fixtures).encode("utf-8")
    assert written[:3] != b"\xef\xbb\xbf"
    assert written.endswith(b"\n")
    assert not (generated / "old.json").exists()
    run(fixtures, io.StringIO())
    assert (generated / "area-result.json").is_file()
    assert (generated / "costs.json").is_file()


def test_run_area_result_twice_is_byte_identical(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "generated" / "area-result.json"

    run(fixtures, io.StringIO())
    first = path.read_bytes()
    run(fixtures, io.StringIO())

    assert path.read_bytes() == first


def test_run_area_data_with_missing_topic_exits_two_and_writes_nothing(tmp_path: Path) -> None:
    copy_data_to(tmp_path)
    path = tmp_path / "packages" / "fixtures" / "data" / "postcode-area.json"
    document = read_json(path)
    document["area"] = [r for r in document["area"] if r["topic"] != "broadband"]
    write_json(path, document)
    out, err = io.StringIO(), io.StringIO()

    exit_code = main([str(tmp_path)], out, err, tmp_path)

    assert exit_code == 2
    assert "broadband" in err.getvalue()
    assert not (tmp_path / "packages" / "fixtures" / "generated").exists()


def _real_output() -> dict[str, Any]:
    parsed: dict[str, Any] = json.loads(generate_area(fixtures_directory()))
    return parsed


def _postcode(code: str) -> dict[str, Any]:
    found: dict[str, Any] = next(p for p in _real_output()["postcodes"] if p["postcode"] == code)
    return found


def test_generate_area_postcodes_are_the_sample_postcodes_sorted() -> None:
    codes = [p["postcode"] for p in _real_output()["postcodes"]]

    assert codes == sorted(codes)
    assert "NB9 9ZZ" not in codes
    assert "NB1 4XY" in codes


def test_generate_area_bus_hours_count_the_listed_departures() -> None:
    buses = _postcode("NB1 4XY")["busesPerHour"]

    route12 = {
        b["hour"]: b["count"]
        for b in buses
        if b["routeNumber"] == "12" and b["stopItemId"].endswith("STOP-1")
    }
    # Route 12 lists 08:00, 08:15, 08:30, 08:59 and 12:10, 12:40, 12:59 (07:59, 09:00, 13:00
    # are outside the hours), counted by hand from postcode-area.json.
    assert route12 == {8: 4, 12: 3}


def test_generate_area_distance_has_display_from_metres() -> None:
    distances = {d["recordId"]: d for d in _postcode("NB1 4XY")["distances"]}

    stop = distances["NB1-4XY-AREA-TRANSPORT-STOP-1"]
    assert stop["metres"] == 120
    assert stop["walkingMinutes"] == 2
    assert stop["display"] == "120 m"


def test_generate_area_priorities_are_sorted_by_id_and_have_null_nearest_when_none() -> None:
    priorities = _postcode("NB1 4XY")["priorities"]

    assert [p["priorityId"] for p in priorities] == sorted(p["priorityId"] for p in priorities)
    assert all("nearestRecordId" in p for p in priorities)


def test_generate_area_missing_priority_topic_raises(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "data" / "sample-priorities.json"
    document = read_json(path)
    document["priorities"][0]["topicKey"] = "no-such-topic"
    write_json(path, document)

    with pytest.raises(InvalidAreaDataError, match="no-such-topic"):
        generate_area(fixtures)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Fraction(120), 120),
        (120, 120),
        (Fraction(3, 2), "1.5"),
        (Fraction(-3, 2), "-1.5"),
        (Fraction(1, 20), "0.05"),
        (Fraction("1609.344"), "1609.344"),
    ],
)
def test_json_number_whole_is_an_integer_and_other_is_a_decimal_string(
    value: Fraction | int, expected: int | str
) -> None:
    assert json_number(value) == expected


def test_json_number_without_a_short_decimal_form_raises() -> None:
    with pytest.raises(InvalidAreaDataError):
        json_number(Fraction(1, 3))


def test_generate_area_priority_reads_only_its_topics_subtypes(tmp_path: Path) -> None:
    # Worked by hand from postcode-area.json: NB1 4XY's places of worship are AMENITY-7 (600 m),
    # AMENITY-8 (950 m) and AMENITY-9 (1,300 m), all recorded. Limit 500 m: none is within it,
    # the limit is under the 5,000 m search limit, each has a distance and none failed, so
    # rule 6 gives misses, nearest AMENITY-7 (600 m). The pharmacy (250 m) and supermarket
    # (400 m) are everyday places and must not be read for this topic.
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "data" / "sample-priorities.json"
    document = read_json(path)
    document["priorities"].append(
        {
            "id": "SAMPLE-PRIORITY-WORSHIP-TEST",
            "topicKey": "places-of-worship",
            "measure": "distance",
            "limit": {"value": "500", "unit": "metres"},
            "synthetic": True,
        }
    )
    write_json(path, document)

    output = json.loads(generate_area(fixtures))
    nb1 = next(p for p in output["postcodes"] if p["postcode"] == "NB1 4XY")
    worship = next(
        p for p in nb1["priorities"] if p["priorityId"] == "SAMPLE-PRIORITY-WORSHIP-TEST"
    )

    assert worship == {
        "priorityId": "SAMPLE-PRIORITY-WORSHIP-TEST",
        "outcome": "misses",
        "nearestRecordId": "NB1-4XY-AREA-AMENITY-7",
    }
