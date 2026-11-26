"""The per-postcode area result and the typed-postcode lookup."""

import json

import pytest
from area_support import fixtures_directory
from vestagraph_area.area_check import check_postcode, postcode_result
from vestagraph_area.records import (
    PostcodeArea,
    read_postcode_area,
    read_registry,
    read_sample_priorities,
)


@pytest.mark.parametrize("postcode", ["NB1 4XY", "NB7 1RR"])
def test_postcode_result_each_sample_equals_generated_entry(postcode: str) -> None:
    fixtures = fixtures_directory()
    registry = read_registry(fixtures / "data" / "pilot-topics.json")
    area = read_postcode_area(fixtures / "data" / "postcode-area.json")
    priorities = read_sample_priorities(fixtures / "data" / "sample-priorities.json", registry)
    generated = json.loads((fixtures / "generated" / "area-result.json").read_text("utf-8"))
    expected = next(p for p in generated["postcodes"] if p["postcode"] == postcode)
    assert postcode_result(registry, area, priorities, postcode) == expected


def _area() -> PostcodeArea:
    return read_postcode_area(fixtures_directory() / "data" / "postcode-area.json")


def test_check_postcode_case_and_spaces_found() -> None:
    lookup = check_postcode(_area(), "nb1  4xy")
    assert lookup.state == "found"
    assert lookup.postcode == "NB1 4XY"


def test_check_postcode_unknown_is_not_found() -> None:
    lookup = check_postcode(_area(), "NB9 9ZZ")
    assert (lookup.state, lookup.postcode, lookup.nation) == ("notFound", None, None)


def test_check_postcode_any_text_is_not_found() -> None:
    assert check_postcode(_area(), "hello").state == "notFound"


def test_check_postcode_wales_is_not_covered() -> None:
    lookup = check_postcode(_area(), "zz1 0aa")
    assert lookup.state == "notCovered"
    assert lookup.nation == "wales"
