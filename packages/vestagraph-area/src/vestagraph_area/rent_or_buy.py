"""Rent or buy, per month (City Explorer).

Two monthly figures are set side by side for an area's average home: renting (rent plus council
tax) and buying (the mortgage repayment plus council tax), one buy figure per mortgage product.
Every amount is whole pence and nothing here uses a ``float`` (AGENTS rule 2). Each figure also
has a shown value in whole pounds: each side is rounded once from pence (halves away from zero,
decision 0034), the shown difference is the rounded buy side minus the rounded rent side, and the
comparison is made on those shown pounds so it always agrees with what is on screen. The
repayment comes
from the cost engine's ``monthly_repayment``; only a typed 0% rate, which the engine refuses, is
worked here as the loan divided by the number of payments, rounded once.

The loan is ``price x (100 - deposit) / 100``, rounded once (nearest penny, halves away from zero)
before the engine is called. Missing data is never shown as zero (rule 7): a missing rent or price
leaves that figure ``None``, and a missing council tax hides both sides.
"""

from collections.abc import Sequence
from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Final

from vestagraph_engine.mortgage import monthly_repayment
from vestagraph_engine.pence import Pence, round_ratio

from vestagraph_area.council_records import RateBand

# A typed rate may be at most this (20%); a larger one is refused. The agent's call, for the
# founder to review in pull request A.
MAX_TYPED_RATE_BASIS_POINTS: Final = 2000
# Buy and rent less than 10 pounds a month apart, as shown in whole pounds, are called about the
# same (the agent's call, for review). 10 pounds or more apart is "more" or "less".
ABOUT_THE_SAME_POUNDS: Final = 10
_PENCE_PER_POUND: Final = 100
MIN_TERM_YEARS: Final = 1
MAX_TERM_YEARS: Final = 40
PRODUCT_ORDER: Final = ("2-year-fixed", "5-year-fixed")
_MONTHS_PER_YEAR: Final = 12


@dataclass(frozen=True, slots=True)
class BuySide:
    """The monthly cost of buying with one product (or a typed rate).

    ``buy_side`` is repayment plus council tax; ``comparison`` is the buy side against the rent
    side ("more", "less" or "about-the-same") on the shown whole pounds; ``difference`` is buy
    side minus rent side in pence. ``shown_buy_side`` and ``shown_difference`` are the whole-pound
    values to display (``None`` when there is no figure, never zero); ``shown_repayment`` is the
    repayment in whole pounds, rounded once from its own pence.
    """

    product: str
    buy_side: Pence | None
    repayment: Pence | None
    rate_used: RateBand | None
    comparison: str | None
    difference: Pence | None
    problem: str | None
    shown_buy_side: int | None = None
    shown_difference: int | None = None
    shown_repayment: int | None = None


@dataclass(frozen=True, slots=True)
class RentOrBuy:
    """Both sides. ``problem`` hides every buy side; ``None`` means the buying inputs are usable."""

    rent_side: Pence | None
    buy_sides: tuple[BuySide, ...]
    problem: str | None
    shown_rent_side: int | None = None


@dataclass(frozen=True, slots=True)
class ShownFigures:
    """The whole-pound values to display for a rent side and a buy side, and their comparison.

    A side that does not exist is ``None``; the difference and comparison need both.
    """

    rent_side: int | None
    buy_side: int | None
    difference: int | None
    comparison: str | None


def shown_pounds(pence: Pence | None) -> int | None:
    """Whole pounds, rounded once: nearest, exact halves away from zero (decision 0034).

    The one helper behind every whole-pound figure a council board shows; ``None`` (a missing
    amount) stays ``None``, never zero (rule 7).
    """
    return None if pence is None else round_ratio(pence.value, _PENCE_PER_POUND).value


def shown_figures(rent_side: Pence | None, buy_side: Pence | None) -> ShownFigures:
    """Display values: each side rounded once to whole pounds; difference = shown buy - shown rent.

    The comparison is ``about-the-same`` when the shown difference is less than 10 pounds either
    way, otherwise ``more`` (buying costs more) or ``less``. Exactly 10 pounds apart is not
    about the same.
    """
    shown_rent, shown_buy = shown_pounds(rent_side), shown_pounds(buy_side)
    if shown_rent is None or shown_buy is None:
        return ShownFigures(shown_rent, shown_buy, None, None)
    difference = shown_buy - shown_rent
    if abs(difference) < ABOUT_THE_SAME_POUNDS:
        comparison = "about-the-same"
    else:
        comparison = "more" if difference > 0 else "less"
    return ShownFigures(shown_rent, shown_buy, difference, comparison)


def rate_band_for(
    deposit_percent: Fraction, bands: Sequence[RateBand], product: str
) -> RateBand | None:
    """The product's rate at the loan-to-value band this deposit falls in, or ``None``.

    The loan-to-value is ``100 - deposit_percent``. The band is chosen on the whole grid (the
    ceilings of every product's bands together): the smallest grid band at or above the
    loan-to-value, since a band means "up to X% loan". The product's rate is returned only at
    that same grid band; a band is never borrowed from another band or product. ``None`` when
    the product has no rate there, when the loan-to-value is above the highest band, or when it
    is zero or less.
    """
    loan_to_value = 100 - deposit_percent
    grid = sorted({band.max_loan_to_value_percent for band in bands})
    if loan_to_value <= 0 or not grid or loan_to_value > grid[-1]:
        return None
    grid_band = next(ceiling for ceiling in grid if ceiling >= loan_to_value)
    for band in bands:
        if band.product == product and band.max_loan_to_value_percent == grid_band:
            return band
    return None


def rent_or_buy(
    rent_monthly: Pence | None,
    price: Pence | None,
    council_tax_monthly: Pence | None,
    deposit_percent: Fraction,
    term_years: int,
    rate_basis_points: int | None,
    bands: Sequence[RateBand],
) -> RentOrBuy:
    """Rent and buy, each per month, with a buy side for every product that has a rate."""
    if council_tax_monthly is None:
        return RentOrBuy(None, (), "council-tax-missing")

    rent_side = None if rent_monthly is None else rent_monthly + council_tax_monthly
    shown_rent = shown_pounds(rent_side)
    problem = _buying_problem(deposit_percent, term_years, rate_basis_points)
    if problem is not None:
        return RentOrBuy(rent_side, (), problem, shown_rent)

    loan = None if price is None else _loan(price, deposit_percent)
    if rate_basis_points is not None:
        typed = _side("typed-rate", None, rate_basis_points, loan, term_years, council_tax_monthly)
        return RentOrBuy(rent_side, (_compared(typed, rent_side),), None, shown_rent)

    sides = tuple(
        _compared(
            _side(
                product,
                rate_band_for(deposit_percent, bands, product),
                None,
                loan,
                term_years,
                council_tax_monthly,
            ),
            rent_side,
        )
        for product in PRODUCT_ORDER
    )
    return RentOrBuy(rent_side, sides, None, shown_rent)


def _buying_problem(
    deposit_percent: Fraction, term_years: int, rate_basis_points: int | None
) -> str | None:
    # A bool is an int in Python (True == 1) but is never a real term or rate: refuse it here
    # rather than let the engine raise a TypeError.
    if type(term_years) is not int:
        return "term-out-of-range"
    if rate_basis_points is not None and type(rate_basis_points) is not int:
        return "rate-invalid"
    if deposit_percent < 0:
        return "deposit-negative"
    if deposit_percent >= 100:
        return "deposit-too-large"
    if not MIN_TERM_YEARS <= term_years <= MAX_TERM_YEARS:
        return "term-out-of-range"
    if rate_basis_points is not None and rate_basis_points < 0:
        return "rate-negative"
    if rate_basis_points is not None and rate_basis_points > MAX_TYPED_RATE_BASIS_POINTS:
        return "rate-too-high"
    return None


def _loan(price: Pence, deposit_percent: Fraction) -> Pence:
    """``price x (100 - deposit) / 100`` as an exact fraction of pence, rounded once."""
    share = 100 - deposit_percent
    return round_ratio(price.value * share.numerator, share.denominator * 100)


def _side(
    product: str,
    band: RateBand | None,
    typed_rate_basis_points: int | None,
    loan: Pence | None,
    term_years: int,
    council_tax_monthly: Pence,
) -> BuySide:
    """One buy side, before it is compared with the rent side."""
    if typed_rate_basis_points is None and band is None:
        return BuySide(product, None, None, None, None, None, "rate-band-unavailable")
    if loan is None:
        return BuySide(product, None, None, band, None, None, None)
    if loan.value <= 0:
        return BuySide(product, None, None, band, None, None, "price-not-positive")
    rate = typed_rate_basis_points if band is None else band.rate_basis_points
    assert rate is not None  # noqa: S101 - one of the two is always set here
    repayment = _repayment(loan, rate, term_years)
    return BuySide(
        product,
        repayment + council_tax_monthly,
        repayment,
        band,
        None,
        None,
        None,
        shown_repayment=shown_pounds(repayment),
    )


def _repayment(loan: Pence, rate_basis_points: int, term_years: int) -> Pence:
    if rate_basis_points == 0:
        # The engine refuses a 0% rate: the repayment is the loan over the payments, rounded once.
        return round_ratio(loan.value, term_years * _MONTHS_PER_YEAR)
    result = monthly_repayment(loan, rate_basis_points, term_years)
    # Safe: the engine fails only for a loan, rate or term it refuses, and the callers already
    # guarantee a positive loan, a rate above zero (0 is handled above) and a term of 1 to 40.
    # Were that ever untrue, ``.value`` raises RuntimeError rather than returning a made-up figure.
    return result.value.monthly_repayment


def _compared(side: BuySide, rent_side: Pence | None) -> BuySide:
    """Add the comparison with the rent side when both figures exist."""
    if side.buy_side is None or rent_side is None:
        return replace(side, shown_buy_side=shown_pounds(side.buy_side))
    difference = side.buy_side - rent_side
    shown = shown_figures(rent_side, side.buy_side)
    return replace(
        side,
        comparison=shown.comparison,
        difference=difference,
        shown_buy_side=shown.buy_side,
        shown_difference=shown.difference,
    )
