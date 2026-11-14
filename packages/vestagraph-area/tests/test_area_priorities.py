"""Priority results (FE-40), proved by worked cases in priority-results.json."""

from fractions import Fraction
from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.priorities import (
    SEARCH_LIMIT_METRES,
    PriorityResult,
    limit_in_metres,
    priority_result,
)
from vestagraph_area.records import (
    AreaRecord,
    Priority,
    read_postcode_area,
    read_registry,
    read_sample_priorities,
    records_of,
)

DATA = fixtures_directory() / "data"
CASES = read_json(fixtures_directory() / "test-cases" / "priority-results.json")["cases"]
REGISTRY = read_registry(DATA / "pilot-topics.json")
AREA = read_postcode_area(DATA / "postcode-area.json")
PRIORITIES = {p.id: p for p in read_sample_priorities(DATA / "sample-priorities.json", REGISTRY)}


def _priority(raw: dict[str, Any]) -> Priority:
    flt = raw.get("filter")
    return Priority(
        id="CASE",
        topic_key=raw["topicKey"],
        subtype=raw.get("subtype"),
        filter_field=None if flt is None else flt["field"],
        filter_equals=None if flt is None else flt["equals"],
        measure=raw["measure"],
        limit_value=Fraction(raw["limit"]["value"]),
        limit_unit=raw["limit"]["unit"],
    )


def _record(raw: dict[str, Any]) -> AreaRecord:
    return AreaRecord(
        id=raw["id"],
        postcode="ZZ1 1AA",
        topic=raw["topic"],
        subtype=raw.get("subtype"),
        status=raw["status"],
        label=f"Label {raw['id']}",
        value=raw.get("value"),
    )


def _from_inputs(inputs: dict[str, Any]) -> tuple[Priority, list[AreaRecord]]:
    if "priorityId" in inputs:
        priority = PRIORITIES[inputs["priorityId"]]
        topic = next(t for t in REGISTRY.topics if t.key == priority.topic_key)
        postcode_records = [r for r in AREA.records if r.postcode == inputs["dataPostcode"]]
        return priority, records_of(topic, postcode_records)
    return _priority(inputs["priority"]), [_record(r) for r in inputs["records"]]


def _case(case_id: str) -> dict[str, Any]:
    return next(c for c in CASES if c["id"] == case_id)


def _result(case_id: str) -> PriorityResult:
    return priority_result(*_from_inputs(_case(case_id)["inputs"]))


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_priority_result_worked_cases_match_expected(case: dict[str, Any]) -> None:
    result = priority_result(*_from_inputs(case["inputs"]))

    assert result.outcome == case["expected"]["outcome"]
    assert result.nearest_record_id == case["expected"]["nearestRecordId"]


def test_priority_result_no_record_in_source_is_not_known_never_misses() -> None:
    result = _result("childcare-no-record-in-source-is-not-known")

    assert result == PriorityResult("not-known", None)


def test_priority_result_exactly_at_limit_meets() -> None:
    assert _result("walking-time-exactly-at-limit-meets").outcome == "meets"
    assert _result("distance-exactly-at-metres-limit-meets").outcome == "meets"


def test_priority_result_missing_walking_time_is_not_known_not_straight_line() -> None:
    # 700 m straight-line is well within what 15 minutes could cover; it must not be used.
    assert _result("distance-without-walking-time-is-not-known").outcome == "not-known"


def test_priority_result_one_place_over_limit_one_without_walking_time_is_not_known() -> None:
    assert _result("one-gp-over-limit-one-without-walking-time-is-not-known").outcome == "not-known"


def test_priority_result_limit_beyond_search_with_nothing_found_is_not_known_beyond_search() -> (
    None
):
    case = "limit-beyond-search-with-nothing-found-is-not-known-beyond-search"

    assert _result(case).outcome == "not-known-beyond-search"


def test_priority_result_meets_comes_before_beyond_search() -> None:
    assert _result("limit-beyond-search-recorded-within-limit-meets").outcome == "meets"


def test_priority_result_no_records_at_all_is_not_known() -> None:
    priority = _priority(_case("no-matching-record-is-not-known")["inputs"]["priority"])

    assert priority_result(priority, []) == PriorityResult("not-known", None)


def test_priority_result_over_limit_with_a_failed_lookup_is_not_known() -> None:
    case = "recorded-over-limit-plus-source-failed-record-is-not-known"

    assert _result(case) == PriorityResult("not-known", None)


def test_priority_result_beyond_search_with_no_matching_record_is_not_known_beyond_search() -> None:
    case = "no-matching-record-beyond-search-is-not-known-beyond-search"

    assert _result(case).outcome == "not-known-beyond-search"


def test_priority_result_filter_with_failed_lookup_and_place_over_limit_is_not_known() -> None:
    case = "filter-with-failed-lookup-and-place-over-limit-is-not-known"

    assert _result(case) == PriorityResult("not-known", None)


def test_priority_result_sibling_record_without_the_measure_is_ignored() -> None:
    assert _result("sibling-record-without-the-measure-is-ignored") == PriorityResult(
        "misses", "S-1"
    )


def test_priority_result_subtype_and_filter_keep_a_matching_gap() -> None:
    assert _result("subtype-and-filter-keep-a-matching-gap").outcome == "not-known"


def test_priority_result_recorded_with_null_value_is_not_known() -> None:
    assert _result("recorded-with-null-value-is-not-known").outcome == "not-known"


def test_priority_result_broadband_has_no_nearest_record() -> None:
    assert _result("broadband-above-limit-meets").nearest_record_id is None
    assert _result("broadband-below-limit-misses").nearest_record_id is None


def test_priority_result_search_limit_is_five_thousand_metres() -> None:
    assert Fraction(5000) == SEARCH_LIMIT_METRES


def test_priority_result_unknown_measure_unit_pair_raises() -> None:
    priority = _priority(
        {"topicKey": "x", "measure": "walking-minutes", "limit": {"value": "5", "unit": "miles"}}
    )

    with pytest.raises(ValueError, match="walking-minutes"):
        priority_result(priority, [])


def test_priority_result_unknown_measure_raises() -> None:
    priority = _priority(
        {"topicKey": "x", "measure": "noise", "limit": {"value": "5", "unit": "decibels"}}
    )

    with pytest.raises(ValueError, match="noise"):
        priority_result(priority, [])


def test_limit_in_metres_half_mile_is_exact() -> None:
    assert limit_in_metres(Fraction("0.5"), "miles") == Fraction("804.672")


def test_limit_in_metres_metres_unchanged() -> None:
    assert limit_in_metres(Fraction(1000), "metres") == Fraction(1000)


def test_limit_in_metres_other_unit_raises() -> None:
    with pytest.raises(ValueError, match="minutes"):
        limit_in_metres(Fraction(15), "minutes")


def test_priority_result_family_view_primary_school_distance_meets() -> None:
    """Worked by hand from NB1 4XY in postcode-area.json: the family view reads school records.

    Limit 0.5 miles = 0.5 x 1609.344 = 804.672 m. Millbrook Primary (phase primary) is 450 m
    away, and 450 <= 804.672, so the priority meets, nearest NB1-4XY-AREA-SCHOOL-1. Northbridge
    Academy is secondary (1100 m) and the phase filter leaves it out.
    """
    family = next(t for t in REGISTRY.topics if t.key == "family-view")
    priority = Priority(
        id="FAMILY-PRIMARY",
        topic_key="family-view",
        subtype=None,
        filter_field="phase",
        filter_equals="primary",
        measure="distance",
        limit_value=Fraction("0.5"),
        limit_unit="miles",
    )
    nb1 = [r for r in AREA.records if r.postcode == "NB1 4XY"]

    result = priority_result(priority, records_of(family, nb1))

    assert result == PriorityResult("meets", "NB1-4XY-AREA-SCHOOL-1")
