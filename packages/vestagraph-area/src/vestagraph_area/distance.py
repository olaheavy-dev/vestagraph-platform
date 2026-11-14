"""Display distances (FE-27 as amended): metres under a mile, miles from there."""

from fractions import Fraction

METRES_PER_MILE = Fraction("1609.344")
_UNDER_TEN = 10
_MILES_FROM = 1610


def _round_half_away(value: Fraction) -> int:
    """Round a non-negative fraction to a whole number, halves away from zero."""
    return int(value + Fraction(1, 2))  # int() floors a non-negative Fraction


def display_distance(metres: Fraction | int) -> str:
    """Return the display text for a stored distance in metres.

    The metres are rounded to the nearest 10 only to choose the unit. Under 10 shows
    "under 10 m", under 1,610 shows metres, otherwise the stored metres are shown in
    miles to one decimal. All rounding is halves away from zero, with exact fractions.
    """
    stored = Fraction(metres)
    if stored < 0:
        raise ValueError(f"a distance cannot be negative: {metres}")
    rounded = _round_half_away(stored / 10) * 10
    if rounded < _UNDER_TEN:
        return "under 10 m"
    if rounded < _MILES_FROM:
        return f"{rounded:,} m"
    tenths = _round_half_away(stored / METRES_PER_MILE * 10)
    return f"{tenths // 10}.{tenths % 10} miles"
