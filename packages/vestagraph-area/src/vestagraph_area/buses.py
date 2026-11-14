"""Buses per hour for one route at one stop (DA-18 as amended, founder, 14 Nov 2026).

Per route, two whole-number counts of timetabled weekday departures (08:00 to 08:59 and 12:00 to
12:59). No stop totals and no averaging. The count is derived from the listed times, never typed
by hand (AGENTS rule 2).
"""

import re
from collections.abc import Sequence

from vestagraph_area.records import InvalidAreaDataError

_TIME = re.compile(r"([01]\d|2[0-3]):[0-5]\d", re.ASCII)


def buses_in_hour(departures: Sequence[str], hour: int) -> int:
    """Count the ``HH:MM`` departures whose hour equals ``hour`` (0 to 23).

    An empty list gives 0 only because the departures record exists and lists no times. A stop
    with no departures record at all is a gap, never 0: the caller must not call this for it
    (Task 7 handles that). Every time is checked, including those outside the hour, so a
    malformed time raises ``InvalidAreaDataError`` rather than being silently skipped. A bad
    ``hour`` is a programming error and raises ``ValueError``.
    """
    if not 0 <= hour <= 23:
        message = f"hour must be 0 to 23, got {hour}."
        raise ValueError(message)
    count = 0
    for time in departures:
        if _TIME.fullmatch(time) is None:
            message = f"A departure time must be HH:MM (00:00 to 23:59), got {time!r}."
            raise InvalidAreaDataError(message)
        if int(time[:2]) == hour:
            count += 1
    return count
