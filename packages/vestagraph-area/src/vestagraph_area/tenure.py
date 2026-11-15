"""Tenure shares (City Explorer): each tenure's percent of households, to one decimal place.

A share is ``count / total x 100`` worked exactly with ``Fraction`` (no ``float``, AGENTS rule 2),
then rounded to one decimal place, halves away from zero. The rounded shares are not forced to
add to 100; the board says "shares may not add to 100% because of rounding". A total of zero
households is refused rather than divided (``InvalidAreaDataError``). A tenure fact with a gap
status has no shares at all: the answer is ``None``, never shares of zero (rule 7).
"""

from collections.abc import Mapping
from fractions import Fraction

from vestagraph_area.council_records import Fact
from vestagraph_area.records import InvalidAreaDataError

TenureCounts = Mapping[str, int]

_HUNDRED = Fraction(100)
_TEN = Fraction(10)
_HALF = Fraction(1, 2)


def _round_to_tenth(percent: Fraction) -> Fraction:
    """Round a non-negative percent to one decimal place, halves up (away from zero)."""
    scaled = percent * _TEN + _HALF
    return Fraction(scaled.numerator // scaled.denominator) / _TEN


def share_text(share: Fraction) -> str:
    """A share already rounded to one decimal place, as text with that one decimal ("35.0").

    The one place the text is made, so the shares and the caption values always agree. Raises
    ``ValueError`` for a share that is not a multiple of a tenth.
    """
    scaled = share * _TEN
    if scaled.denominator != 1:
        message = "A tenure share is a multiple of 0.1."
        raise ValueError(message)
    whole, tenths = divmod(scaled.numerator, 10)
    return f"{whole}.{tenths}"


def tenure_shares(counts: TenureCounts) -> dict[str, Fraction]:
    """Percent share of each tenure, one decimal place; counts are whole households."""
    if any(count < 0 for count in counts.values()):
        message = "A tenure count cannot be negative."
        raise InvalidAreaDataError(message)
    total = sum(counts.values())
    if total <= 0:
        message = "Tenure counts must total at least one household."
        raise InvalidAreaDataError(message)
    return {
        key: _round_to_tenth(Fraction(count, total) * _HUNDRED) for key, count in counts.items()
    }


def tenure_shares_for_fact(fact: Fact) -> dict[str, Fraction] | None:
    """Shares for a recorded tenure fact; ``None`` for any gap status."""
    if fact.status != "recorded":
        return None
    counts: TenureCounts = fact.value
    return tenure_shares(counts)
