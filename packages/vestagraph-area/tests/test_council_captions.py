"""Plain-words caption values for council trends, proved by hand-worked cases."""

from fractions import Fraction
from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.captions import Change, caption_for, twelve_month_change
from vestagraph_area.council_records import (
    Level,
    Series,
    SeriesPoint,
    Source,
    read_council_area,
)
from vestagraph_engine.pence import Pence

CASES: list[dict[str, Any]] = read_json(
    fixtures_directory() / "test-cases" / "council-captions.json"
)["cases"]
BY_ID = {case["id"]: case for case in CASES}
COUNCILS = {
    c.code: c
    for c in read_council_area(fixtures_directory() / "data" / "council-area.json").councils
}
_LEVEL = Level(kind="local-authority", name="Test")
_SOURCE = Source(label="test", url="https://example.invalid", edition="", period="", synthetic=True)


def _value(unit: str, raw: Any) -> int | Fraction:
    return Fraction(raw) if unit == "ratio" else int(raw)


def _series(inputs: dict[str, Any]) -> Series:
    if "councilCode" in inputs:
        council = COUNCILS[inputs["councilCode"]]
        return {
            "rentSeries": council.rent_series,
            "priceSeries": council.price_series,
            "affordabilitySeries": council.affordability_series,
        }[inputs["series"]]
    unit = inputs["unit"]
    points = tuple(
        SeriesPoint(
            period=p["period"],
            status=p["status"],
            value=_value(unit, p["value"]) if "value" in p else None,
            method_break_before=p.get("methodBreakBefore", False),
        )
        for p in inputs["points"]
    )
    return Series(status="recorded", unit=unit, points=points, level=_LEVEL, source=_SOURCE)


def _topic(case: dict[str, Any]) -> str:
    return str(case["expected"]["caption"]["values"]["topic"])


def _expected_change(case: dict[str, Any]) -> Change | None:
    raw = case["expected"]["change"]
    if raw is None:
        return None
    ratio = _series(case["inputs"]).unit == "ratio"

    def number(text: Any) -> Pence | Fraction:
        return Fraction(text) if ratio else Pence(int(text))

    return Change(
        from_period=raw["fromPeriod"],
        to_period=raw["toPeriod"],
        from_value=number(raw["fromValue"]),
        to_value=number(raw["toValue"]),
        amount=number(raw["amount"]),
        percent=None if raw["percent"] is None else Fraction(raw["percent"]),
        direction=raw["direction"],
        provisional_months=raw["provisionalMonths"],
    )


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_twelve_month_change_worked_cases_match_expected(case: dict[str, Any]) -> None:
    series = _series(case["inputs"])
    latest = case["inputs"]["latestPeriod"]
    change = twelve_month_change(series, latest)
    assert change == _expected_change(case)
    if change is not None:
        assert type(change.amount) is type(change.from_value)
    caption = caption_for(_topic(case), series, latest)
    assert caption.kind == case["expected"]["caption"]["kind"]
    assert caption.values == case["expected"]["caption"]["values"]


def test_twelve_month_change_missing_start_point_is_none() -> None:
    case = BY_ID["southvale-price-start-point-not-published"]
    assert twelve_month_change(_series(case["inputs"]), "2026-08") is None
    caption = caption_for("price", _series(case["inputs"]), "2026-08")
    assert caption.kind == "missing"
    assert caption.values["reason"] == "start-point-not-published"
    assert caption.values["value"] == "202550"  # The latest figure is still carried.


def test_caption_for_absent_start_point_is_missing_never_single_point() -> None:
    for case_id in (
        "northbridge-rent-start-point-absent",
        "eastmere-affordability-start-point-absent",
    ):
        case = BY_ID[case_id]
        caption = caption_for(_topic(case), _series(case["inputs"]), case["inputs"]["latestPeriod"])
        assert caption.kind == "missing"
        assert caption.values["reason"] == "start-point-absent"


def test_caption_for_money_amount_is_difference_of_shown_pounds() -> None:
    money = [c for c in CASES if c["expected"]["caption"]["kind"] == "trend"]
    checked = 0
    for case in money:
        values = case["expected"]["caption"]["values"]
        if "." in values["fromValue"]:
            continue
        caption = caption_for(_topic(case), _series(case["inputs"]), case["inputs"]["latestPeriod"])
        shown = abs(int(caption.values["toValue"]) - int(caption.values["fromValue"]))
        assert shown == int(caption.values["amount"])
        checked += 1
    assert checked >= 10


def test_twelve_month_change_across_method_break_is_not_comparable() -> None:
    series = _series(BY_ID["eastmere-affordability-across-method-break"]["inputs"])
    assert twelve_month_change(series, "2023") is None
    assert caption_for("affordability", series, "2023").kind == "not-comparable"
    # The break sits before the start point of 2023 to 2024, so that pair is comparable.
    assert twelve_month_change(series, "2024") is not None


@pytest.mark.parametrize(
    "case_id",
    [
        "inline-rent-rise-just-below-half-is-unchanged",
        "inline-rent-fall-just-below-half-is-unchanged",
        "inline-rent-fall-by-half-a-pound",
        "inline-ratio-equal-values-are-unchanged",
    ],
)
def test_twelve_month_change_rounding_to_zero_is_unchanged(case_id: str) -> None:
    case = BY_ID[case_id]
    change = twelve_month_change(_series(case["inputs"]), case["inputs"]["latestPeriod"])
    assert change is not None
    assert change.direction == "unchanged"
    # The two shown figures are equal; the exact money amount is kept, a ratio's is exactly zero.
    if isinstance(change.amount, Pence):
        assert change.amount != Pence.ZERO
    else:
        assert change.amount == 0


def test_twelve_month_change_bad_latest_period_raises() -> None:
    series = _series(BY_ID["northbridge-rent-rose"]["inputs"])
    with pytest.raises(ValueError, match="YYYY"):
        twelve_month_change(series, "2026-13")
