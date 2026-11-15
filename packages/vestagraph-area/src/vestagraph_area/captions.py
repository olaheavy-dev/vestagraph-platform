"""Plain-words caption values for council trends (City Explorer).

A caption carries **values and a pattern key, never a finished sentence**: the wording is approved
by the founder later and quotes these values. Every figure comes from the series, so none is typed
by hand (AGENTS rule 2), and no ``float`` is made anywhere.

The change is between the latest period and the same month a year earlier (the previous year for a
yearly ``YYYY`` series). It is ``None`` when it cannot be worked out honestly (rule 7): the series
is a gap, either end point is missing or not published, or the method changed between the two
(a ``methodBreakBefore`` on any point after the start point, up to and including the end point).
A provisional end point still allows a trend; provisional points in the latest twelve months are
counted so the wording can say so. Money in ``values`` is whole pounds (pence rounded once,
halves away from zero); percents and ratio amounts are one decimal place, also half away from zero.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Final, Literal

from vestagraph_engine.pence import Pence, round_ratio

from vestagraph_area.council_records import Series, SeriesPoint

Direction = Literal["rose", "fell", "unchanged"]
CaptionKind = Literal["trend", "single-point", "missing", "not-comparable"]
_PENCE_PER_POUND: Final = 100


@dataclass(frozen=True, slots=True)
class Change:
    """The change between two end points. ``amount`` is ``to - from`` and keeps its sign.

    The amount is ``Pence`` for a money series and an exact ``Fraction`` for a ratio series.
    ``percent`` is ``amount / from x 100`` (exact), and ``None`` for a ratio series.
    ``direction`` is ``unchanged`` when the amount rounds to 0 pounds (money) or 0.0 (ratio).
    """

    from_period: str
    to_period: str
    from_value: Pence | Fraction
    to_value: Pence | Fraction
    amount: Pence | Fraction
    percent: Fraction | None
    direction: Direction
    provisional_months: int


@dataclass(frozen=True, slots=True)
class Caption:
    """What to say about a topic: a kind and the values (strings) the wording quotes."""

    kind: CaptionKind
    values: dict[str, str]


@dataclass(frozen=True, slots=True)
class _Outcome:
    kind: CaptionKind
    change: Change | None = None
    reason: str = ""
    from_period: str = ""
    to_period: str = ""
    end_point: SeriesPoint | None = None


def _whole(value: object) -> int:
    """The whole pence of a money value (a plain ``int`` point value or ``Pence``)."""
    if isinstance(value, Pence):
        return value.value
    if type(value) is int:
        return value
    message = "A money series needs whole-pence values."
    raise TypeError(message)


def _exact(value: object) -> Fraction:
    """The exact value of a ratio series point or amount."""
    if isinstance(value, Fraction):
        return value
    message = "A ratio series needs exact decimal values."
    raise TypeError(message)


def _key(period: str) -> tuple[int, int]:
    if len(period) == 4 and period.isascii() and period.isdigit():
        return int(period), 0
    if (
        len(period) == 7
        and period[4] == "-"
        and period[:4].isascii()
        and period[:4].isdigit()
        and period[5:].isascii()
        and period[5:].isdigit()
        and 1 <= int(period[5:]) <= 12
    ):
        return int(period[:4]), int(period[5:])
    message = f"Period {period!r} is not YYYY or YYYY-MM."
    raise ValueError(message)


def _a_year_earlier(period: str) -> str:
    year, month = _key(period)
    return f"{year - 1:04d}" if month == 0 else f"{year - 1:04d}-{month:02d}"


def _scaled(value: Fraction, places: int) -> int:
    """``value`` x 10^places, rounded once: nearest, exact halves away from zero."""
    return round_ratio(value.numerator * 10**places, value.denominator).value


def _decimal_text(value: Fraction, places: int) -> str:
    scaled = _scaled(abs(value), places)
    whole, part = divmod(scaled, 10**places)
    return f"{whole}.{part:0{places}d}"


def _pounds_text(pence: int) -> str:
    return str(round_ratio(abs(pence), _PENCE_PER_POUND).value)


def _assess(series: Series, latest_period: str) -> _Outcome:
    end_key = _key(latest_period)
    start_period = _a_year_earlier(latest_period)
    start_key = _key(start_period)
    if series.status != "recorded":
        return _Outcome("missing", reason=series.status)
    by_period = {p.period: p for p in series.points}
    end = by_period.get(latest_period)
    if end is None:
        return _Outcome("missing", reason="end-point-absent")
    if end.value is None:
        return _Outcome("missing", reason="end-point-not-published")
    start = by_period.get(start_period)
    if start is None:
        return _Outcome("single-point", end_point=end)
    if start.value is None:
        return _Outcome("missing", reason="start-point-not-published")
    if any(p.method_break_before and start_key < _key(p.period) <= end_key for p in series.points):
        return _Outcome("not-comparable", from_period=start_period, to_period=latest_period)
    provisional = sum(
        1
        for p in series.points
        if p.status == "provisional" and start_key < _key(p.period) <= end_key
    )
    if series.unit == "ratio":
        change = _ratio_change(start, end, provisional)
    else:
        change = _money_change(start, end, provisional)
    return _Outcome("trend", change=change)


def _money_change(start: SeriesPoint, end: SeriesPoint, provisional: int) -> Change:
    from_pence, to_pence = _whole(start.value), _whole(end.value)
    amount = to_pence - from_pence
    if round_ratio(amount, _PENCE_PER_POUND).value == 0:
        direction: Direction = "unchanged"
    else:
        direction = "rose" if amount > 0 else "fell"
    return Change(
        from_period=start.period,
        to_period=end.period,
        from_value=Pence(from_pence),
        to_value=Pence(to_pence),
        amount=Pence(amount),
        percent=Fraction(amount * 100, from_pence),
        direction=direction,
        provisional_months=provisional,
    )


def _ratio_change(start: SeriesPoint, end: SeriesPoint, provisional: int) -> Change:
    from_value, to_value = _exact(start.value), _exact(end.value)
    amount = to_value - from_value
    if _scaled(amount, 1) == 0:
        direction: Direction = "unchanged"
    else:
        direction = "rose" if amount > 0 else "fell"
    return Change(
        from_period=start.period,
        to_period=end.period,
        from_value=from_value,
        to_value=to_value,
        amount=amount,
        percent=None,
        direction=direction,
        provisional_months=provisional,
    )


def twelve_month_change(series: Series, latest_period: str) -> Change | None:
    """The change from a year before ``latest_period`` to it, or ``None`` if it can't be said.

    Raises ``ValueError`` for a period that is not ``YYYY`` or ``YYYY-MM``.
    """
    return _assess(series, latest_period).change


def _money_values(change: Change) -> dict[str, str]:
    return {
        "fromValue": _pounds_text(_whole(change.from_value)),
        "toValue": _pounds_text(_whole(change.to_value)),
        "amount": _pounds_text(_whole(change.amount)),
    }


def _ratio_values(change: Change) -> dict[str, str]:
    return {
        "fromValue": _decimal_text(_exact(change.from_value), 2),
        "toValue": _decimal_text(_exact(change.to_value), 2),
        "amount": _decimal_text(_exact(change.amount), 1),
    }


def _trend_values(topic: str, change: Change) -> dict[str, str]:
    figures = (
        _ratio_values(change) if isinstance(change.amount, Fraction) else _money_values(change)
    )
    values = {
        "topic": topic,
        "pattern": f"trend-{change.direction}",
        "direction": change.direction,
        "fromPeriod": change.from_period,
        "toPeriod": change.to_period,
        **figures,
    }
    if change.percent is not None and change.direction != "unchanged":
        values["percent"] = _decimal_text(change.percent, 1)
    values["provisionalMonths"] = str(change.provisional_months)
    return values


def _single_point_values(topic: str, series: Series, end: SeriesPoint) -> dict[str, str]:
    if series.unit == "ratio":
        shown = _decimal_text(_exact(end.value), 2)
    else:
        shown = _pounds_text(_whole(end.value))
    return {
        "topic": topic,
        "pattern": "single-point",
        "period": end.period,
        "value": shown,
        "pointStatus": end.status,
    }


def caption_for(topic: str, series: Series, latest_period: str) -> Caption:
    """The caption kind and values for a topic's series at ``latest_period``."""
    outcome = _assess(series, latest_period)
    if outcome.change is not None:
        return Caption("trend", _trend_values(topic, outcome.change))
    if outcome.end_point is not None:
        return Caption("single-point", _single_point_values(topic, series, outcome.end_point))
    if outcome.kind == "not-comparable":
        return Caption(
            "not-comparable",
            {
                "topic": topic,
                "pattern": "not-comparable",
                "fromPeriod": outcome.from_period,
                "toPeriod": outcome.to_period,
            },
        )
    return Caption("missing", {"topic": topic, "pattern": "missing", "reason": outcome.reason})
