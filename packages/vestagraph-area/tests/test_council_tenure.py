"""Tenure shares, proved by hand-worked cases in council-tenure.json."""

from fractions import Fraction
from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.council_records import Fact, Level, Source
from vestagraph_area.records import InvalidAreaDataError
from vestagraph_area.tenure import tenure_shares, tenure_shares_for_fact

CASES: list[dict[str, Any]] = read_json(
    fixtures_directory() / "test-cases" / "council-tenure.json"
)["cases"]

_LEVEL = Level("local-authority", "Test")
_SOURCE = Source("Test", "https://example.invalid", "2026", "2026", True)


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_tenure_shares_worked_cases_match_expected(case: dict[str, Any]) -> None:
    expected = case["expected"]

    shares = tenure_shares(case["inputs"]["counts"])

    assert shares == {key: Fraction(text) for key, text in expected["shares"].items()}
    assert sum(shares.values(), Fraction(0)) == Fraction(expected["sumOfShares"])


def test_tenure_shares_zero_total_is_refused() -> None:
    counts = dict.fromkeys(
        ("ownedOutright", "ownedWithMortgage", "socialRented", "privateRented", "other"), 0
    )

    with pytest.raises(InvalidAreaDataError):
        tenure_shares(counts)


def test_tenure_shares_for_fact_gap_status_is_none_not_zeros() -> None:
    fact = Fact("no-record-in-source", None, _LEVEL, _SOURCE)

    assert tenure_shares_for_fact(fact) is None


def test_tenure_shares_for_fact_recorded_gives_shares() -> None:
    counts = {"ownedOutright": 1, "ownedWithMortgage": 1, "socialRented": 1}
    counts |= {"privateRented": 0, "other": 0}
    fact = Fact("recorded", counts, _LEVEL, _SOURCE)

    shares = tenure_shares_for_fact(fact)

    assert shares is not None
    assert shares["ownedOutright"] == Fraction("33.3")
