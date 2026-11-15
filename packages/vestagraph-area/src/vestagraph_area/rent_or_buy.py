"""Rent or buy, per month (City Explorer).

Two monthly figures are set side by side for an area's average home: renting (rent plus council
tax) and buying (the mortgage repayment plus council tax), one buy figure per mortgage product.
Every amount is whole pence and nothing here uses a ``float`` (AGENTS rule 2). The repayment comes
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
# Buy and rent within 10 pounds a month are called about the same (the agent's call, for review).
ABOUT_THE_SAME_PENCE: Final = 1000
MIN_TERM_YEARS: Final = 1
MAX_TERM_YEARS: Final = 40
PRODUCT_ORDER: Final = ("2-year-fixed", "5-year-fixed")
_MONTHS_PER_YEAR: Final = 12


@dataclass(frozen=True, slots=True)
class BuySide:
    """The monthly cost of buying with one product (or a typed rate).

    ``buy_side`` is repayment plus council tax; ``comparison`` is the buy side against the rent
    side ("more", "less" or "about-the-same"); ``difference`` is buy side minus rent side.
    """

    product: str
    buy_side: Pence | None
    repayment: Pence | None
    rate_used: RateBand | None
    comparison: str | None
    difference: Pence | None
    problem: str | None


@dataclass(frozen=True, slots=True)
class RentOrBuy:
    """Both sides. ``problem`` hides every buy side; ``None`` means the buying inputs are usable."""

    rent_side: Pence | None
    buy_sides: tuple[BuySide, ...]
    problem: str | None


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
    problem = _buying_problem(deposit_percent, term_years, rate_basis_points)
    if problem is not None:
        return RentOrBuy(rent_side, (), problem)

    loan = None if price is None else _loan(price, deposit_percent)
    if rate_basis_points is not None:
        typed = _side("typed-rate", None, rate_basis_points, loan, term_years, council_tax_monthly)
        return RentOrBuy(rent_side, (_compared(typed, rent_side),), None)

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
    return RentOrBuy(rent_side, sides, None)


def _buying_problem(
    deposit_percent: Fraction, term_years: int, rate_basis_points: int | None
) -> str | None:
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
    return BuySide(product, repayment + council_tax_monthly, repayment, band, None, None, None)


def _repayment(loan: Pence, rate_basis_points: int, term_years: int) -> Pence:
    if rate_basis_points == 0:
        # The engine refuses a 0% rate: the repayment is the loan over the payments, rounded once.
        return round_ratio(loan.value, term_years * _MONTHS_PER_YEAR)
    result = monthly_repayment(loan, rate_basis_points, term_years)
    return result.value.monthly_repayment


def _compared(side: BuySide, rent_side: Pence | None) -> BuySide:
    """Add the comparison with the rent side when both figures exist."""
    if side.buy_side is None or rent_side is None:
        return side
    difference = side.buy_side - rent_side
    if abs(difference.value) < ABOUT_THE_SAME_PENCE:
        comparison = "about-the-same"
    else:
        comparison = "more" if difference.value > 0 else "less"
    return replace(side, comparison=comparison, difference=difference)
