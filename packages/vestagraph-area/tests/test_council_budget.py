"""Budget check, proved by hand-worked cases in council-budget.json."""

from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.budget import BudgetCheck, budget_check
from vestagraph_area.rent_or_buy import BuySide, RentOrBuy
from vestagraph_engine.pence import Pence

CASES: list[dict[str, Any]] = read_json(
    fixtures_directory() / "test-cases" / "council-budget.json"
)["cases"]


def _pence(value: int | None) -> Pence | None:
    return None if value is None else Pence(value)


def _buy_side(product: str, figure: int | None) -> BuySide:
    return BuySide(product, _pence(figure), None, None, None, None, None)


def _rent_or_buy(rent_side: int | None, figures: dict[str, int | None]) -> RentOrBuy:
    sides = tuple(_buy_side(product, figure) for product, figure in figures.items())
    return RentOrBuy(_pence(rent_side), sides, None)


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_budget_check_worked_cases_match_expected(case: dict[str, Any]) -> None:
    given = case["inputs"]
    expected = case["expected"]
    sides = RentOrBuy(
        _pence(given["rentSidePence"]),
        tuple(_buy_side(s["product"], s["buySidePence"]) for s in given["buySides"]),
        given["rentOrBuyProblem"],
    )

    result = budget_check(Pence(given["budgetMonthlyPence"]), sides)

    assert result == BudgetCheck(expected["rent"], expected["buy"], expected["problem"])


def test_budget_check_equal_to_budget_is_within() -> None:
    result = budget_check(Pence(150000), _rent_or_buy(150000, {"2-year-fixed": 150000}))

    assert result.rent == "within"
    assert result.buy == {"2-year-fixed": "within"}


def test_budget_check_one_penny_over_budget_is_above() -> None:
    result = budget_check(Pence(150000), _rent_or_buy(150001, {"2-year-fixed": 150001}))

    assert result.rent == "above"
    assert result.buy == {"2-year-fixed": "above"}


def test_budget_check_missing_side_is_none_not_within() -> None:
    result = budget_check(Pence(150000), _rent_or_buy(None, {"2-year-fixed": None}))

    assert result.rent is None
    assert result.buy == {"2-year-fixed": None}
    assert result.problem is None


def test_budget_check_budget_not_positive_is_a_problem() -> None:
    result = budget_check(Pence(0), _rent_or_buy(100, {"2-year-fixed": 100}))

    assert result == BudgetCheck(None, {}, "budget-not-positive")
