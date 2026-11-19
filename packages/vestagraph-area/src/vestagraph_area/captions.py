"""Plain-words caption values for council trends (City Explorer).

A caption carries **values and a pattern key, never a finished sentence**: the wording is approved
by the founder later and quotes these values. Every figure comes from the series, so none is typed
by hand (AGENTS rule 2), and no ``float`` is made anywhere.

The change is between the latest period and the same month a year earlier (the previous year for a
yearly ``YYYY`` series). It is ``None`` when it cannot be worked out honestly (rule 7): the series
is a gap, either end point is missing or not published, or the method changed between the two
(a ``methodBreakBefore`` on any point after the start point, up to and including the end point).
A provisional end point still allows a trend; provisional points in the latest twelve months are
counted so the wording can say so. Money in ``values`` is whole pounds: each figure is rounded
once (halves away from zero) and the shown amount is the difference of those two rounded figures
(register line BE-14), so the numbers add up on screen; the percent is worked from the exact pence
to one decimal place, or is ``less than 0.1`` when a real change would print as 0.0. A ratio is
shown as published (two places) and its amount is exact. When there is no change,
the latest figure is still carried in a ``missing`` caption.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Final, Literal

from vestagraph_engine.pence import Pence, round_ratio

from vestagraph_area.council_records import (
    PROPERTY_TYPES,
    TENURE_KEYS,
    Fact,
    Series,
    SeriesPoint,
    period_key,
)
from vestagraph_area.tenure import share_text, tenure_shares_for_fact

Direction = Literal["rose", "fell", "unchanged"]
CaptionKind = Literal["trend", "missing", "not-comparable", "single-point"]
_PENCE_PER_POUND: Final = 100
LESS_THAN_A_TENTH: Final = "less than 0.1"


@dataclass(frozen=True, slots=True)
class Change:
    """The change between two end points. ``amount`` is ``to - from`` and keeps its sign.

    The amount is ``Pence`` for a money series and an exact ``Fraction`` for a ratio series.
    ``percent`` is ``amount / from x 100`` (exact), and ``None`` for a ratio series.
    ``direction`` is ``unchanged`` when the two figures shown in whole pounds are equal (money,
    each rounded once, register line BE-14) or when the two published values are equal (ratio).
    """

    from_period: str
    to_period: str
    from_value: Pence | Fraction
    to_value: Pence | Fraction
    amount: Pence | Fraction
    percent: Fraction | None
    direction: Direction
    provisional_points: int


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


def _a_year_earlier(period: str) -> str:
    year, month = period_key(period)
    return f"{year - 1:04d}" if month == 0 else f"{year - 1:04d}-{month:02d}"


def _scaled(value: Fraction, places: int) -> int:
    """``value`` x 10^places, rounded once: nearest, exact halves away from zero."""
    return round_ratio(value.numerator * 10**places, value.denominator).value


def _decimal_text(value: Fraction, places: int) -> str:
    scaled = _scaled(abs(value), places)
    whole, part = divmod(scaled, 10**places)
    return f"{whole}.{part:0{places}d}"


def _pounds(pence: int) -> int:
    """Whole pounds, rounded once: nearest, exact halves away from zero."""
    return round_ratio(pence, _PENCE_PER_POUND).value


def _assess(series: Series, latest_period: str) -> _Outcome:
    end_key = period_key(latest_period)
    start_period = _a_year_earlier(latest_period)
    start_key = period_key(start_period)
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
        return _Outcome("missing", reason="start-point-absent", end_point=end)
    if start.value is None:
        return _Outcome("missing", reason="start-point-not-published", end_point=end)
    if any(
        p.method_break_before and start_key < period_key(p.period) <= end_key for p in series.points
    ):
        return _Outcome("not-comparable", from_period=start_period, to_period=latest_period)
    provisional = sum(
        1
        for p in series.points
        if p.status == "provisional" and start_key < period_key(p.period) <= end_key
    )
    if series.unit == "ratio":
        change = _ratio_change(start, end, provisional)
    else:
        change = _money_change(start, end, provisional)
    return _Outcome("trend", change=change)


def _money_change(start: SeriesPoint, end: SeriesPoint, provisional: int) -> Change:
    from_pence, to_pence = _whole(start.value), _whole(end.value)
    amount = to_pence - from_pence
    shown = _pounds(to_pence) - _pounds(from_pence)
    if shown == 0:
        direction: Direction = "unchanged"
    else:
        direction = "rose" if shown > 0 else "fell"
    return Change(
        from_period=start.period,
        to_period=end.period,
        from_value=Pence(from_pence),
        to_value=Pence(to_pence),
        amount=Pence(amount),
        percent=Fraction(amount * 100, from_pence),
        direction=direction,
        provisional_points=provisional,
    )


def _ratio_change(start: SeriesPoint, end: SeriesPoint, provisional: int) -> Change:
    from_value, to_value = _exact(start.value), _exact(end.value)
    amount = to_value - from_value
    if amount == 0:
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
        provisional_points=provisional,
    )


def twelve_month_change(series: Series, latest_period: str) -> Change | None:
    """The change from a year before ``latest_period`` to it, or ``None`` if it can't be said.

    Raises ``ValueError`` for a period that is not ``YYYY`` or ``YYYY-MM``.
    """
    return _assess(series, latest_period).change


def _money_values(change: Change) -> dict[str, str]:
    shown_from, shown_to = _pounds(_whole(change.from_value)), _pounds(_whole(change.to_value))
    return {
        "fromValue": str(shown_from),
        "toValue": str(shown_to),
        "amount": str(abs(shown_to - shown_from)),
    }


def _ratio_values(change: Change) -> dict[str, str]:
    return {
        "fromValue": _decimal_text(_exact(change.from_value), 2),
        "toValue": _decimal_text(_exact(change.to_value), 2),
        "amount": _decimal_text(_exact(change.amount), 2),
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
        values["percent"] = _percent_text(change.percent)
    values["provisionalPoints"] = str(change.provisional_points)
    return values


def _percent_text(percent: Fraction) -> str:
    """The percent to one decimal place, without a sign (the direction says rose or fell).

    A change that is not zero but would print as ``0.0`` (under 0.05%) is ``less than 0.1``
    instead, so a real rise or fall never reads as no change (proposed wording).
    """
    if percent != 0 and _scaled(abs(percent), 1) == 0:
        return LESS_THAN_A_TENTH
    return _decimal_text(percent, 1)


def _latest_values(series: Series, end: SeriesPoint) -> dict[str, str]:
    if series.unit == "ratio":
        shown = _decimal_text(_exact(end.value), 2)
    else:
        shown = str(_pounds(_whole(end.value)))
    return {"period": end.period, "value": shown, "pointStatus": end.status}


def caption_for(topic: str, series: Series, latest_period: str) -> Caption:
    """The caption kind and values for a topic's series at ``latest_period``."""
    outcome = _assess(series, latest_period)
    if outcome.change is not None:
        return Caption("trend", _trend_values(topic, outcome.change))
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
    values = {"topic": topic, "pattern": "missing", "reason": outcome.reason}
    if outcome.end_point is not None:
        values.update(_latest_values(series, outcome.end_point))
    return Caption("missing", values)


def series_caption(topic: str, series: Series) -> Caption:
    """The caption for a topic's series at its latest point, whatever the series holds.

    A series with no points (a gap status) has no latest period, so it gets a ``missing`` caption
    whose reason is the gap status; every other series goes through ``caption_for``.
    """
    if not series.points:
        return Caption("missing", {"topic": topic, "pattern": "missing", "reason": series.status})
    return caption_for(topic, series, series.points[-1].period)


def property_type_caption(property_type: str, series: Series) -> Caption:
    """The price caption for one property type's series, carrying that type.

    It is the ordinary ``price`` caption for the series at its latest point (a trend only when
    both end points are published and the method did not change between them, rule 7), with the
    property type added to its values. It looks at this one series only: a caption never
    compares two types or two councils.

    Raises ``ValueError`` for a name that is not one of ``PROPERTY_TYPES``.
    """
    if property_type not in PROPERTY_TYPES:
        message = f"{property_type!r} is not a property type; use {', '.join(PROPERTY_TYPES)}."
        raise ValueError(message)
    caption = series_caption("price", series)
    return Caption(caption.kind, {**caption.values, "propertyType": property_type})


def tenure_caption(fact: Fact) -> Caption:
    """The caption for a tenure fact: its shares as published, or a ``missing`` caption.

    One Census period has no change over time, so a recorded fact is a ``single-point`` caption
    carrying each share to one decimal place (never a trend). A gap status is a ``missing``
    caption whose reason is that status (rule 7).
    """
    shares = tenure_shares_for_fact(fact)
    if shares is None:
        return Caption("missing", {"topic": "tenure", "pattern": "missing", "reason": fact.status})
    values = {"topic": "tenure", "pattern": "single-point", "period": fact.source.period}
    values.update({key: share_text(shares[key]) for key in TENURE_KEYS})
    return Caption("single-point", values)
