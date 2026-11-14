"""Priority results (FE-40): meets, misses or not known, proved by priority-results.json.

The rules run in this order over the records that match the priority's subtype and filter:

1. A recorded or stale record whose measure is at or under the limit: meets (for a download
   speed, at or above the limit).
2. A distance limit over 5,000 m (the search limit, FE-12): not-known-beyond-search, whether or
   not any record matched.
3. No matching record: not-known.
4. A recorded or stale record without the measure (for example no walking time): not-known.
   The straight-line distance is never used instead.
5. A source-failed matching record: not-known (a failed lookup may hide a nearer place).
6. At least one recorded or stale record, all of them over the limit: misses. A
   no-record-in-source or not-covered record does not stop this (data present is not a gap).
7. Anything else: not-known.

All arithmetic is exact (``Fraction``); no float is made (AGENTS rule 2).
"""

from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

from vestagraph_area.distance import METRES_PER_MILE
from vestagraph_area.records import AreaRecord, Priority

SEARCH_LIMIT_METRES = Fraction(5000)

Outcome = Literal["meets", "misses", "not-known", "not-known-beyond-search"]

_HAS_VALUE = ("recorded", "stale")
# measure -> (the field of the record's value, the unit its limit is typed in)
_MEASURES: dict[str, tuple[str, tuple[str, ...]]] = {
    "walking-minutes": ("walkingMinutes", ("minutes",)),
    "distance": ("distanceMetres", ("metres", "miles")),
    "download-mbps": ("predictedMaxDownloadMbps", ("mbps",)),
}


@dataclass(frozen=True, slots=True)
class PriorityResult:
    """The outcome, and the record to quote as the nearest place (``None`` when there is none)."""

    outcome: Outcome
    nearest_record_id: str | None


def limit_in_metres(value: Fraction, unit: str) -> Fraction:
    """Convert a distance limit to metres: 1 mile is exactly 1,609.344 m."""
    if unit == "metres":
        return value
    if unit == "miles":
        return value * METRES_PER_MILE
    message = f"a distance limit is in metres or miles, not '{unit}'"
    raise ValueError(message)


def _matches(priority: Priority, record: AreaRecord) -> bool:
    if priority.subtype is not None and record.subtype != priority.subtype:
        return False
    if priority.filter_field is None:
        return True
    if record.value is None:
        return False
    return bool(record.value.get(priority.filter_field) == priority.filter_equals)


def _measure(record: AreaRecord, field: str) -> Fraction | None:
    if record.status not in _HAS_VALUE or record.value is None:
        return None
    found = record.value.get(field)
    return None if found is None else Fraction(found)


def priority_result(priority: Priority, records: Sequence[AreaRecord]) -> PriorityResult:
    """Say whether a postcode's records of the priority's topic meet its limit."""
    if priority.measure not in _MEASURES:
        message = f"unknown measure '{priority.measure}'"
        raise ValueError(message)
    field, units = _MEASURES[priority.measure]
    if priority.limit_unit not in units:
        message = f"measure '{priority.measure}' cannot have a limit in '{priority.limit_unit}'"
        raise ValueError(message)
    is_speed = priority.measure == "download-mbps"
    is_distance = priority.measure == "distance"
    limit = priority.limit_value
    if is_distance:
        limit = limit_in_metres(limit, priority.limit_unit)

    matching = [r for r in records if _matches(priority, r)]
    measured = [(m, r.id) for r in matching if (m := _measure(r, field)) is not None]
    meeting = [(m, i) for m, i in measured if (m >= limit if is_speed else m <= limit)]
    if meeting:
        return PriorityResult("meets", min(meeting)[1])
    if is_distance and limit > SEARCH_LIMIT_METRES:
        return PriorityResult("not-known-beyond-search", None)
    if not matching:
        return PriorityResult("not-known", None)
    with_value = [r for r in matching if r.status in _HAS_VALUE and r.value is not None]
    if any(_measure(r, field) is None for r in with_value):
        return PriorityResult("not-known", None)
    if any(r.status == "source-failed" for r in matching):
        return PriorityResult("not-known", None)
    if with_value:
        return PriorityResult("misses", min(measured)[1])
    return PriorityResult("not-known", None)
