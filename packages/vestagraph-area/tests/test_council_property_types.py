"""House prices by property type: the reader and the per-type trend caption, proved by hand."""

import copy
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.captions import Change, property_type_caption, twelve_month_change
from vestagraph_area.council_records import (
    PROPERTY_TYPES,
    Council,
    Level,
    Series,
    SeriesPoint,
    Source,
    read_council_area,
)
from vestagraph_area.records import InvalidAreaDataError
from vestagraph_engine.pence import Pence

DATA_FILE = fixtures_directory() / "data" / "council-area.json"
CASES: list[dict[str, Any]] = read_json(
    fixtures_directory() / "test-cases" / "council-property-types.json"
)["cases"]
COUNCILS: dict[str, Council] = {c.code: c for c in read_council_area(DATA_FILE).councils}
_LEVEL = Level(kind="local-authority", name="Test")
_SOURCE = Source(label="test", url="https://example.invalid", edition="", period="", synthetic=True)


def _type_series(inputs: dict[str, Any]) -> Series:
    if "councilCode" in inputs:
        return COUNCILS[inputs["councilCode"]].price_by_type[inputs["propertyType"]]
    points = tuple(
        SeriesPoint(
            period=p["period"],
            status=p["status"],
            value=p.get("value"),
            method_break_before=p.get("methodBreakBefore", False),
        )
        for p in inputs["points"]
    )
    return Series(status="recorded", unit="pence", points=points, level=_LEVEL, source=_SOURCE)


def _expected_change(case: dict[str, Any]) -> Change | None:
    raw = case["expected"]["change"]
    if raw is None:
        return None
    return Change(
        from_period=raw["fromPeriod"],
        to_period=raw["toPeriod"],
        from_value=Pence(raw["fromValue"]),
        to_value=Pence(raw["toValue"]),
        amount=Pence(raw["amount"]),
        percent=Fraction(raw["percent"]),
        direction=raw["direction"],
        provisional_points=raw["provisionalPoints"],
    )


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_property_type_caption_worked_cases_match_expected(case: dict[str, Any]) -> None:
    series = _type_series(case["inputs"])

    caption = property_type_caption(case["inputs"]["propertyType"], series)

    assert caption.kind == case["expected"]["caption"]["kind"]
    assert caption.values == case["expected"]["caption"]["values"]


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_twelve_month_change_property_type_worked_cases_match_expected(
    case: dict[str, Any],
) -> None:
    series = _type_series(case["inputs"])
    latest = series.points[-1].period if series.points else "2026-08"

    assert twelve_month_change(series, latest) == _expected_change(case)


def test_property_type_caption_carries_its_own_type_and_never_compares_types() -> None:
    for case in CASES:
        values = property_type_caption(
            case["inputs"]["propertyType"], _type_series(case["inputs"])
        ).values

        assert values["propertyType"] == case["inputs"]["propertyType"]
        assert not {"otherType", "otherCouncil", "comparedWith"} & set(values)


def test_property_type_caption_unknown_type_raises() -> None:
    series = COUNCILS["E06999001"].price_by_type["flat"]

    with pytest.raises(ValueError, match="not a property type"):
        property_type_caption("bungalow", series)


def test_read_council_area_every_council_has_the_four_property_types() -> None:
    assert PROPERTY_TYPES == ("detached", "semiDetached", "terraced", "flat")
    for council in COUNCILS.values():
        assert tuple(council.price_by_type) == PROPERTY_TYPES
        assert all(s.unit == "pence" for s in council.price_by_type.values())


def test_read_council_area_property_type_gaps_are_series_gaps_not_zero() -> None:
    flat = COUNCILS["E07999001"].price_by_type["flat"]

    assert flat.status == "no-record-in-source"
    assert flat.points == ()
    westmere = COUNCILS["E07999002"].price_by_type.values()
    assert all(s.status == "no-record-in-source" and s.points == () for s in westmere)


def test_read_council_area_type_series_keep_the_all_types_periods_and_gaps() -> None:
    southvale = COUNCILS["E06999002"]
    all_types = [(p.period, p.status) for p in southvale.price_series.points]

    for series in southvale.price_by_type.values():
        assert [(p.period, p.status) for p in series.points] == all_types
    assert ("2025-08", "not-published") in all_types
    eastmere = COUNCILS["E07999001"]
    first = eastmere.price_by_type["detached"].points[0].period
    assert first == eastmere.price_series.points[0].period


def test_property_type_series_are_synthetic_and_say_so() -> None:
    for council in COUNCILS.values():
        for series in council.price_by_type.values():
            assert series.source.synthetic is True
            assert series.source.label.startswith("Synthetic sample, shaped like the UK House")
            assert "property type" in series.source.label


def _data() -> dict[str, Any]:
    parsed: dict[str, Any] = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return parsed


def _refused(tmp_path: Path, data: dict[str, Any], match: str) -> None:
    path = tmp_path / "council-area.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(InvalidAreaDataError, match=match):
        read_council_area(path)


def test_read_council_area_missing_property_type_raises(tmp_path: Path) -> None:
    data = _data()
    del data["councils"][0]["priceSeries"]["byType"]["flat"]

    _refused(tmp_path, data, "byType: must hold exactly the keys")


def test_read_council_area_extra_property_type_raises(tmp_path: Path) -> None:
    data = _data()
    by_type = data["councils"][0]["priceSeries"]["byType"]
    by_type["bungalow"] = copy.deepcopy(by_type["flat"])

    _refused(tmp_path, data, "byType: must hold exactly the keys")


def test_read_council_area_missing_by_type_raises(tmp_path: Path) -> None:
    data = _data()
    del data["councils"][0]["priceSeries"]["byType"]

    _refused(tmp_path, data, "byType")


def test_read_council_area_property_type_series_in_wrong_unit_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["priceSeries"]["byType"]["detached"]["unit"] = "pence-per-month"

    _refused(tmp_path, data, "unit must be 'pence'")


def test_read_council_area_property_type_gap_with_points_raises(tmp_path: Path) -> None:
    data = _data()
    flat = data["councils"][2]["priceSeries"]["byType"]["flat"]
    flat["points"] = [{"period": "2026-08", "status": "recorded", "value": 100}]

    _refused(tmp_path, data, "must not carry points")
