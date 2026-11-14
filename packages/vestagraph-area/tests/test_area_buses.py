"""Buses per hour per route (DA-18 as amended), proved by worked cases in buses-per-hour.json."""

from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.buses import buses_in_hour
from vestagraph_area.records import InvalidAreaDataError, read_postcode_area

CASES = read_json(fixtures_directory() / "test-cases" / "buses-per-hour.json")["cases"]
AREA = read_postcode_area(fixtures_directory() / "data" / "postcode-area.json")


def _departures(inputs: dict[str, Any]) -> list[str]:
    if "dataRecordId" in inputs:
        record = next(r for r in AREA.records if r.id == inputs["dataRecordId"])
        assert record.value is not None
        return list(record.value["departures"])
    return list(inputs["departures"])


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_buses_in_hour_worked_cases_match_expected(case: dict[str, Any]) -> None:
    departures = _departures(case["inputs"])

    assert buses_in_hour(departures, case["inputs"]["hour"]) == case["expected"]["count"]


def test_buses_in_hour_edges_of_the_hour_count_inclusively() -> None:
    times = ["07:59", "08:00", "08:59", "09:00"]

    assert buses_in_hour(times, 8) == 2


@pytest.mark.parametrize(
    "bad",
    [
        "8:5",
        "8:05",
        "08:5",
        "24:00",
        "08:60",
        "0800",
        "08:00:00",
        "",
        "ab:cd",
        " 08:00",
        "\u0660\u0668:\u0660\u0660",
    ],
)
def test_buses_in_hour_malformed_time_raises(bad: str) -> None:
    with pytest.raises(InvalidAreaDataError, match="departure time"):
        buses_in_hour(["08:00", bad], 8)


def test_buses_in_hour_malformed_time_outside_the_hour_still_raises() -> None:
    with pytest.raises(InvalidAreaDataError):
        buses_in_hour(["13:5"], 8)


@pytest.mark.parametrize("hour", [-1, 24, 100])
def test_buses_in_hour_hour_out_of_range_raises_value_error(hour: int) -> None:
    with pytest.raises(ValueError, match="hour"):
        buses_in_hour(["08:00"], hour)
