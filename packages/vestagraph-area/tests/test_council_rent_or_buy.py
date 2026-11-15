"""Rent or buy per month, proved by hand-worked cases in rent-or-buy.json."""

from fractions import Fraction
from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.council_records import RateBand, read_council_area
from vestagraph_area.rent_or_buy import (
    ABOUT_THE_SAME_PENCE,
    MAX_TYPED_RATE_BASIS_POINTS,
    BuySide,
    RentOrBuy,
    rate_band_for,
    rent_or_buy,
)
from vestagraph_engine.pence import Pence

CASES: list[dict[str, Any]] = read_json(fixtures_directory() / "test-cases" / "rent-or-buy.json")[
    "cases"
]
BANDS = read_council_area(fixtures_directory() / "data" / "council-area.json").rate_bands


def _pence(value: int | None) -> Pence | None:
    return None if value is None else Pence(value)


def _run(
    *,
    rent: int | None = 138700,
    price: int | None = 29780000,
    council_tax: int | None = 18000,
    deposit: str = "25",
    term: int = 25,
    rate: int | None = None,
) -> RentOrBuy:
    return rent_or_buy(
        _pence(rent),
        _pence(price),
        _pence(council_tax),
        Fraction(deposit),
        term,
        rate,
        BANDS,
    )


def _side(result: RentOrBuy, product: str) -> BuySide:
    return next(s for s in result.buy_sides if s.product == product)


def _band_summary(side: BuySide) -> tuple[int, int] | None:
    if side.rate_used is None:
        return None
    return side.rate_used.max_loan_to_value_percent, side.rate_used.rate_basis_points


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_rent_or_buy_worked_cases_match_expected(case: dict[str, Any]) -> None:
    given = case["inputs"]
    expected = case["expected"]

    result = rent_or_buy(
        _pence(given["rentMonthlyPence"]),
        _pence(given["pricePence"]),
        _pence(given["councilTaxMonthlyPence"]),
        Fraction(given["depositPercent"]),
        given["termYears"],
        given["rateBasisPoints"],
        BANDS,
    )

    assert result.rent_side == _pence(expected["rentSidePence"])
    assert result.problem == expected["problem"]
    assert [s.product for s in result.buy_sides] == [s["product"] for s in expected["buySides"]]
    for side, want in zip(result.buy_sides, expected["buySides"], strict=True):
        assert side.buy_side == _pence(want["buySidePence"])
        assert side.repayment == _pence(want["repaymentPence"])
        assert side.comparison == want["comparison"]
        assert side.difference == _pence(want["differencePence"])
        assert side.problem == want["problem"]
        if want["rateUsedBasisPoints"] is None:
            assert side.rate_used is None
        else:
            assert _band_summary(side) == (
                want["rateUsedMaxLoanToValuePercent"],
                want["rateUsedBasisPoints"],
            )


def test_rate_band_for_two_year_eighty_percent_loan_takes_eighty_five_band() -> None:
    band = rate_band_for(Fraction(20), BANDS, "2-year-fixed")

    assert band is not None
    assert (band.max_loan_to_value_percent, band.rate_basis_points) == (85, 470)


def test_rate_band_for_five_year_without_a_band_at_the_grid_band_is_none() -> None:
    assert rate_band_for(Fraction(20), BANDS, "5-year-fixed") is None
    assert rate_band_for(Fraction(10), BANDS, "5-year-fixed") is None
    band = rate_band_for(Fraction(25), BANDS, "5-year-fixed")
    assert band is not None
    assert band.rate_basis_points == 450


def test_rate_band_for_loan_above_highest_band_is_none() -> None:
    for deposit in (Fraction(3), Fraction(0), Fraction("4.9"), Fraction(-5), Fraction(100)):
        assert rate_band_for(deposit, BANDS, "2-year-fixed") is None
        assert rate_band_for(deposit, BANDS, "5-year-fixed") is None


def test_rate_band_for_fifty_percent_loan_takes_lowest_band() -> None:
    band = rate_band_for(Fraction(50), BANDS, "2-year-fixed")

    assert band is not None
    assert (band.max_loan_to_value_percent, band.rate_basis_points) == (60, 410)


def test_rate_band_for_loan_exactly_on_a_band_takes_that_band() -> None:
    band = rate_band_for(Fraction(5), BANDS, "2-year-fixed")

    assert band is not None
    assert band.max_loan_to_value_percent == 95


def test_rent_or_buy_returns_one_buy_side_per_product() -> None:
    result = _run()

    assert [s.product for s in result.buy_sides] == ["2-year-fixed", "5-year-fixed"]


def test_rent_or_buy_five_year_unavailable_keeps_two_year_side_and_rent_side() -> None:
    result = _run(deposit="10")

    assert result.rent_side == Pence(156700)
    assert _side(result, "2-year-fixed").buy_side == Pence(176247)
    five = _side(result, "5-year-fixed")
    assert (five.buy_side, five.problem) == (None, "rate-band-unavailable")


def test_rent_or_buy_typed_rate_gives_one_typed_rate_side() -> None:
    result = _run(rate=650)

    assert [s.product for s in result.buy_sides] == ["typed-rate"]
    assert result.buy_sides[0].rate_used is None
    assert result.buy_sides[0].repayment == Pence(150808)


def test_rent_or_buy_deposit_one_hundred_percent_is_deposit_too_large() -> None:
    result = _run(deposit="100")

    assert result.problem == "deposit-too-large"
    assert result.buy_sides == ()
    assert result.rent_side == Pence(156700)


def test_rent_or_buy_missing_rent_has_buy_side_only_and_no_comparison() -> None:
    result = _run(rent=None)

    assert result.rent_side is None
    for side in result.buy_sides:
        assert side.buy_side is not None
        assert side.comparison is None
        assert side.difference is None


def test_rent_or_buy_zero_typed_rate_divides_loan_by_payments() -> None:
    result = _run(deposit="33", rate=0)

    assert result.buy_sides[0].repayment == Pence(66509)
    assert result.problem is None


def test_rent_or_buy_within_ten_pounds_is_about_the_same() -> None:
    assert ABOUT_THE_SAME_PENCE == 1000
    result = _run(rent=122622)

    assert _side(result, "2-year-fixed").comparison == "about-the-same"
    assert _side(result, "2-year-fixed").difference == Pence(-999)


def test_rent_or_buy_missing_council_tax_is_problem_not_zero() -> None:
    result = _run(council_tax=None)

    assert result.problem == "council-tax-missing"
    assert result.rent_side is None
    assert result.buy_sides == ()


def test_rent_or_buy_rate_above_limit_is_rate_too_high() -> None:
    assert MAX_TYPED_RATE_BASIS_POINTS == 2000

    assert _run(rate=2001).problem == "rate-too-high"
    assert _run(rate=2000).problem is None


def test_rent_or_buy_no_rate_band_keeps_rent_side_and_hides_buy_side() -> None:
    result = _run(deposit="3")

    assert result.rent_side == Pence(156700)
    assert result.problem is None
    assert [s.problem for s in result.buy_sides] == ["rate-band-unavailable"] * 2
    assert all(s.buy_side is None and s.comparison is None for s in result.buy_sides)


def test_rent_or_buy_zero_price_reports_the_engine_problem_not_a_figure() -> None:
    result = _run(price=0)

    assert all(s.buy_side is None and s.problem == "price-not-positive" for s in result.buy_sides)


def test_rate_band_for_ignores_bands_of_other_products() -> None:
    only_five: list[RateBand] = [b for b in BANDS if b.product == "5-year-fixed"]

    assert rate_band_for(Fraction(25), only_five, "2-year-fixed") is None
