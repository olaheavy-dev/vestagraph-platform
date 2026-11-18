"""Energy certificate rules: pure functions, standard library only."""

from datetime import date
from typing import Final

VALIDITY_YEARS: Final = 10


def valid_until(start: date) -> date:
    """Last valid day: the same day and month ``VALIDITY_YEARS`` on.

    ``start`` is the registration date (regulation 9(2)(a), 2012 Regulations).
    29 February becomes 28 February when the target year has no such day.
    """
    year = start.year + VALIDITY_YEARS
    if start.month == 2 and start.day == 29 and not _is_leap(year):
        return date(year, 2, 28)
    return date(year, start.month, start.day)


def is_more_than_ten_years_old(start: date, today: date) -> bool:
    """True when ``today`` is after the last valid day."""
    return today > valid_until(start)


def _is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
