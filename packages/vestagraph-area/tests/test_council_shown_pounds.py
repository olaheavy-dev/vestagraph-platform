"""Whole pounds shown beside a pence amount, proved by hand-worked cases."""

from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.rent_or_buy import shown_pounds
from vestagraph_engine.pence import Pence

CASES: list[dict[str, Any]] = read_json(
    fixtures_directory() / "test-cases" / "council-shown-pounds.json"
)["cases"]
HELPER_CASES = [c for c in CASES if "pence" in c["inputs"]]


@pytest.mark.parametrize("case", HELPER_CASES, ids=[c["id"] for c in HELPER_CASES])
def test_shown_pounds_worked_cases_match_expected(case: dict[str, Any]) -> None:
    pence = case["inputs"]["pence"]

    result = shown_pounds(None if pence is None else Pence(pence))

    assert result == case["expected"]["shownPounds"]


def test_shown_pounds_missing_amount_is_none_never_zero() -> None:
    assert shown_pounds(None) is None
