"""Budget check (City Explorer): is each monthly figure within the user's monthly budget?

"Within" includes a figure equal to the budget (founder decision 23 Oct 2026 (b)). A side whose
figure is missing gives ``None``, never "within" (AGENTS rule 7). There is one answer for the
rent side and one for each buy side, keyed by product. A budget of zero or below is a problem and
nothing is compared. Whole pence only; no ``float`` (rule 2).
"""

from dataclasses import dataclass
from typing import Final

from vestagraph_engine.pence import Pence

from vestagraph_area.rent_or_buy import RentOrBuy

WITHIN: Final = "within"
ABOVE: Final = "above"
BUDGET_NOT_POSITIVE: Final = "budget-not-positive"


@dataclass(frozen=True, slots=True)
class BudgetCheck:
    """``rent`` and each ``buy[product]`` are "within", "above" or ``None`` (no figure)."""

    rent: str | None
    buy: dict[str, str | None]
    problem: str | None


def budget_check(budget_monthly: Pence, rent_or_buy: RentOrBuy) -> BudgetCheck:
    """Compare the rent side and every buy side with the monthly budget."""
    if budget_monthly.value <= 0:
        return BudgetCheck(None, {}, BUDGET_NOT_POSITIVE)
    return BudgetCheck(
        _verdict(budget_monthly, rent_or_buy.rent_side),
        {side.product: _verdict(budget_monthly, side.buy_side) for side in rent_or_buy.buy_sides},
        None,
    )


def _verdict(budget_monthly: Pence, figure: Pence | None) -> str | None:
    if figure is None:
        return None
    return WITHIN if figure.value <= budget_monthly.value else ABOVE
