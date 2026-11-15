"""Council tax band amounts, proved by hand-worked cases in council-tax.json."""

from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.council_records import Council, read_council_area
from vestagraph_area.council_tax import band_monthly, band_yearly
from vestagraph_area.records import InvalidAreaDataError
from vestagraph_engine.pence import Pence

CASES: list[dict[str, Any]] = read_json(fixtures_directory() / "test-cases" / "council-tax.json")[
    "cases"
]
AREA = read_council_area(fixtures_directory() / "data" / "council-area.json")
COUNCILS: dict[str, Council] = {c.code: c for c in AREA.councils}
BAND_CASES = [c for c in CASES if "band" in c["inputs"]]
YEARLY_ONLY_CASES = [c for c in CASES if "band" not in c["inputs"]]


def _expected(value: int | None) -> Pence | None:
    return None if value is None else Pence(value)


@pytest.mark.parametrize("case", BAND_CASES, ids=[c["id"] for c in BAND_CASES])
def test_band_yearly_returns_the_published_amount_for_each_band(case: dict[str, Any]) -> None:
    council = COUNCILS[case["inputs"]["councilCode"]]

    assert band_yearly(council.bands, case["inputs"]["band"]) == _expected(
        case["expected"]["yearlyPence"]
    )


def test_band_yearly_unknown_band_raises() -> None:
    with pytest.raises(InvalidAreaDataError, match="not a council tax band"):
        band_yearly(COUNCILS["E06999001"].bands, "I")


def test_band_yearly_unknown_band_raises_even_for_a_gap() -> None:
    with pytest.raises(InvalidAreaDataError, match="not a council tax band"):
        band_yearly(COUNCILS["E07999002"].bands, "Z")


def test_band_yearly_gap_returns_none_not_zero() -> None:
    gap = COUNCILS["E07999002"].bands

    assert gap.status == "no-record-in-source"
    assert band_yearly(gap, "D") is None


@pytest.mark.parametrize("case", BAND_CASES, ids=[c["id"] for c in BAND_CASES])
def test_band_monthly_worked_cases_match_expected(case: dict[str, Any]) -> None:
    council = COUNCILS[case["inputs"]["councilCode"]]
    yearly = band_yearly(council.bands, case["inputs"]["band"])

    if case["expected"]["monthlyPence"] is None:
        assert yearly is None
    else:
        assert yearly is not None
        assert band_monthly(yearly) == Pence(case["expected"]["monthlyPence"])


@pytest.mark.parametrize("case", YEARLY_ONLY_CASES, ids=[c["id"] for c in YEARLY_ONLY_CASES])
def test_band_monthly_exact_half_penny_rounds_away_from_zero(case: dict[str, Any]) -> None:
    assert band_monthly(Pence(case["inputs"]["yearlyPence"])) == Pence(
        case["expected"]["monthlyPence"]
    )


DATA_CASES = [c for c in CASES if "councilCode" in c["inputs"]]


@pytest.mark.parametrize("case", DATA_CASES, ids=[c["id"] for c in DATA_CASES])
def test_worked_case_yearly_input_equals_the_value_read_from_council_area_json(
    case: dict[str, Any],
) -> None:
    given = case["inputs"]
    read = band_yearly(COUNCILS[given["councilCode"]].bands, given["band"])

    # A gap council has no yearly input in the case: both sides are "no figure" (None).
    assert read == _expected(given.get("yearlyPence"))
