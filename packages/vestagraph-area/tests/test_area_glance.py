"""At a glance counts (FE-38, FE-39, FE-41), proved by hand-worked cases in area-glance.json."""

import json
from pathlib import Path
from typing import Any

import pytest
from area_support import (
    fixtures_directory,
    make_area,
    make_record,
    make_registry,
    make_topic,
    read_json,
)
from vestagraph_area.glance import at_a_glance, topic_outcome
from vestagraph_area.records import (
    AreaRecord,
    InvalidAreaDataError,
    PostcodeArea,
    Registry,
    Topic,
    read_postcode_area,
    read_registry,
)

CASES = read_json(fixtures_directory() / "test-cases" / "area-glance.json")["cases"]


def _inputs(inputs: dict[str, Any]) -> tuple[Registry, PostcodeArea, str]:
    data = fixtures_directory() / "data"
    if "dataPostcode" in inputs:
        return (
            read_registry(data / "pilot-topics.json"),
            read_postcode_area(data / "postcode-area.json"),
            str(inputs["dataPostcode"]),
        )
    topics = tuple(
        Topic(
            key=t["key"],
            name=t["name"],
            kind="places",
            counted=t["counted"],
            record_topics=tuple(t["recordTopics"]),
            record_subtypes=(),
            question_template=t["questionTemplate"],
            check_in_person=tuple(t["checkInPerson"]),
            official_route=None,
            review_status="draft",
        )
        for t in inputs["topics"]
    )
    records = tuple(
        AreaRecord(
            id=r["id"],
            postcode="ZZ1 1AA",
            topic=r["topic"],
            subtype=None,
            status=r["status"],
            label=r["label"],
            value=None,
        )
        for r in inputs["records"]
    )
    return (
        Registry(nation="england", topics=topics),
        PostcodeArea(postcodes=("ZZ1 1AA",), unknown_postcodes=(), records=records),
        "ZZ1 1AA",
    )


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_at_a_glance_worked_cases_match_expected(case: dict[str, Any]) -> None:
    registry, area, postcode = _inputs(case["inputs"])
    expected = case["expected"]

    glance = at_a_glance(registry, area, postcode)

    assert glance.found == expected["found"]
    assert glance.not_known == expected["notKnown"]
    assert glance.coverage_found == expected["coverageFound"]
    assert glance.coverage_total == expected["coverageTotal"]
    assert dict(glance.outcomes) == expected["outcomes"]
    assert [
        {"topicKey": q.topic_key, "recordId": q.record_id, "text": q.text} for q in glance.questions
    ] == expected["questions"]
    assert [c.topic_key for c in glance.check_in_person] == expected["checkInPersonTopics"]


def test_at_a_glance_check_in_person_carries_the_topic_list() -> None:
    registry, area, postcode = _inputs({"dataPostcode": "NB7 1RR"})

    glance = at_a_glance(registry, area, postcode)

    flood = next(c for c in glance.check_in_person if c.topic_key == "flood")
    flood_topic = next(t for t in registry.topics if t.key == "flood")
    assert flood.items == flood_topic.check_in_person


def test_topic_outcome_no_record_in_source_is_found() -> None:
    outcome = topic_outcome(make_topic("a"), [make_record("R1", "no-record-in-source")])

    assert outcome == "found"


def test_topic_outcome_all_source_failed_is_not_known() -> None:
    outcome = topic_outcome(
        make_topic("a"), [make_record("R1", "source-failed"), make_record("R2", "source-failed")]
    )

    assert outcome == "not-known"


def test_topic_outcome_all_not_covered_is_left_out() -> None:
    outcome = topic_outcome(make_topic("a"), [make_record("R1", "not-covered")])

    assert outcome == "not-covered"


def test_topic_outcome_stale_is_found() -> None:
    assert topic_outcome(make_topic("a"), [make_record("R1", "stale")]) == "found"


def test_at_a_glance_topic_without_records_raises_invalid_area_data() -> None:
    registry = make_registry(make_topic("alpha", record_topics=("missing-kind",)))
    area = make_area(make_record("R1", "recorded"))

    with pytest.raises(InvalidAreaDataError, match=r"alpha.*ZZ1 1AA"):
        at_a_glance(registry, area, "ZZ1 1AA")


def test_at_a_glance_route_only_topic_is_ignored() -> None:
    registry = make_registry(
        make_topic("alpha"), make_topic("route", counted=False, record_topics=())
    )
    area = make_area(make_record("R1", "recorded"))

    glance = at_a_glance(registry, area, "ZZ1 1AA")

    assert (glance.found, glance.not_known, glance.coverage_total) == (1, 0, 1)
    assert "route" not in glance.outcomes


def test_at_a_glance_other_postcode_records_are_not_counted() -> None:
    registry = make_registry(make_topic("alpha"))
    area = make_area(
        make_record("R1", "recorded", postcode="ZZ2 2BB"),
        make_record("R2", "source-failed"),
    )

    glance = at_a_glance(registry, area, "ZZ1 1AA")

    assert glance.outcomes == {"alpha": "not-known"}


def test_read_registry_topic_missing_key_raises_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(fixtures_directory() / "data" / "pilot-topics.json")
    del data["topics"][0]["key"]
    path = tmp_path / "pilot-topics.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(InvalidAreaDataError):
        read_registry(path)
