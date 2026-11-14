"""Display distances (FE-27 as amended), proved by hand-worked cases in distance-display.json."""

from fractions import Fraction
from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.distance import display_distance

CASES = read_json(fixtures_directory() / "test-cases" / "distance-display.json")["cases"]


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_display_distance_worked_cases_match_expected(case: dict[str, Any]) -> None:
    metres = Fraction(case["inputs"]["metres"])

    assert display_distance(metres) == case["expected"]["display"]


def test_display_distance_1605_metres_shows_miles_not_1610_metres() -> None:
    assert display_distance(1605) == "1.0 miles"


def test_display_distance_whole_number_input_matches_fraction_input() -> None:
    assert display_distance(1450) == display_distance(Fraction(1450))


def test_display_distance_negative_metres_raises_value_error() -> None:
    with pytest.raises(ValueError, match="negative"):
        display_distance(-1)
