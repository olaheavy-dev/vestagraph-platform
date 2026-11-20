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
            kind=t.get("kind", "places"),
            counted=t["counted"],
            record_topics=tuple(t["recordTopics"]),
            record_subtypes=tuple(t.get("recordSubtypes", ())),
            gap_question_template=t.get("gapQuestionTemplate"),
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
            subtype=r.get("subtype"),
            status=r["status"],
            label=r["label"],
            value=None,
        )
        for r in inputs["records"]
    )
    return (
        Registry(
            nation="england", subtype_names=dict(inputs.get("subtypeNames", {})), topics=topics
        ),
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
    # beta owns R1, so the only problem is that alpha has no record.
    registry = make_registry(
        make_topic("alpha", record_topics=("missing-kind",)), make_topic("beta")
    )
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


def test_at_a_glance_energy_route_only_topic_not_counted() -> None:
    data = fixtures_directory() / "data"
    registry = read_registry(data / "pilot-topics.json")
    area = read_postcode_area(data / "postcode-area.json")

    glance = at_a_glance(registry, area, "NB1 4XY")

    counted = [t for t in registry.topics if t.counted]
    assert "energy-certificate-home" not in glance.outcomes
    assert glance.coverage_total == len(counted)
    assert all(q.topic_key != "energy-certificate-home" for q in glance.questions)


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


def test_at_a_glance_gap_question_never_contains_the_record_label() -> None:
    registry, area, _ = _inputs({"dataPostcode": "NB7 1RR"})
    labels = {r.id: r.label for r in area.records}

    glance = at_a_glance(registry, area, "NB7 1RR")

    # Worked by hand from postcode-area.json after the flood warning record was removed (0061):
    # NB7 1RR has 12 gap records (not recorded and not stale): amenity 1, bus-departures 1,
    # school-demand 1, flood-risk-postcode 1, sold-price 1, broadband-coverage 1, air-quality 1,
    # radon 1, affordability 1, council-rent 1, transport-connectivity 1, green-space 1.
    # One pair shares a (topic, text): affordability with council-rent, so 12 - 1 = 11 questions
    # (hand-worked in area-glance.json, nb7-1rr-sparse step 9).
    assert len(glance.questions) == 11
    for question in glance.questions:
        assert labels[question.record_id] not in question.text
        assert "(synthetic)" not in question.text
        assert "{" not in question.text


def test_at_a_glance_gap_question_subject_uses_subtype_name_then_topic_name() -> None:
    registry = make_registry(
        make_topic("alpha Topic", record_topics=("a",)),
        subtype_names={"gp-surgery": "GP surgery"},
    )
    with_subtype = AreaRecord("R1", "ZZ1 1AA", "a", "gp-surgery", "no-record-in-source", "L1", None)
    without = AreaRecord("R2", "ZZ1 1AA", "a", None, "source-failed", "L2", None)
    area = PostcodeArea(("ZZ1 1AA",), (), (with_subtype, without))

    glance = at_a_glance(registry, area, "ZZ1 1AA")

    assert [q.text for q in glance.questions] == [
        "Gap question about GP surgery",
        "Gap question about alpha topic",
    ]


# --- Every record belongs to exactly one counted topic (final review item 4) ---


def test_at_a_glance_record_read_by_no_topic_raises_invalid_area_data() -> None:
    registry = make_registry(make_topic("alpha"))
    area = make_area(make_record("R1", "recorded"), make_record("R2", "recorded", topic="stray"))

    with pytest.raises(InvalidAreaDataError, match="R2"):
        at_a_glance(registry, area, "ZZ1 1AA")


def test_at_a_glance_record_of_an_unlisted_subtype_raises_invalid_area_data() -> None:
    registry = make_registry(
        make_topic("alpha", record_topics=("amenity",), record_subtypes=("park",))
    )
    park = AreaRecord("R1", "ZZ1 1AA", "amenity", "park", "recorded", "L1", None)
    bakery = AreaRecord("R2", "ZZ1 1AA", "amenity", "bakery", "recorded", "L2", None)

    with pytest.raises(InvalidAreaDataError, match="R2"):
        at_a_glance(registry, PostcodeArea(("ZZ1 1AA",), (), (park, bakery)), "ZZ1 1AA")


def test_at_a_glance_record_read_by_two_counted_topics_raises_invalid_area_data() -> None:
    registry = make_registry(make_topic("alpha"), make_topic("beta"))
    area = make_area(make_record("R1", "recorded"))

    with pytest.raises(InvalidAreaDataError, match=r"R1.*alpha.*beta"):
        at_a_glance(registry, area, "ZZ1 1AA")


def test_at_a_glance_record_read_only_by_an_uncounted_grouping_is_allowed() -> None:
    registry = make_registry(
        make_topic("alpha"), make_topic("group", counted=False, record_topics=("extra",))
    )
    area = make_area(make_record("R1", "recorded"), make_record("R2", "recorded", topic="extra"))

    glance = at_a_glance(registry, area, "ZZ1 1AA")

    assert glance.outcomes == {"alpha": "found"}


def test_at_a_glance_records_of_other_postcodes_are_not_checked_for_ownership() -> None:
    registry = make_registry(make_topic("alpha"))
    area = make_area(
        make_record("R1", "recorded"), make_record("R2", "recorded", topic="stray", postcode="X")
    )

    assert at_a_glance(registry, area, "ZZ1 1AA").found == 1


# --- Check in person (final review item 2) ---


def test_at_a_glance_check_in_person_includes_route_only_topics_with_their_lists() -> None:
    registry, area, postcode = _inputs({"dataPostcode": "NB1 4XY"})

    glance = at_a_glance(registry, area, postcode)

    noise = next(c for c in glance.check_in_person if c.topic_key == "noise")
    mobile = next(c for c in glance.check_in_person if c.topic_key == "mobile-by-network")
    topics = {t.key: t for t in registry.topics}
    assert noise.items == topics["noise"].check_in_person
    assert mobile.items == topics["mobile-by-network"].check_in_person
    assert "family-view" not in {c.topic_key for c in glance.check_in_person}


def test_at_a_glance_check_in_person_lists_are_neutral() -> None:
    registry = read_registry(fixtures_directory() / "data" / "pilot-topics.json")
    banned = ("safe", "unsafe", "verified", "approved", "good", "bad", "risky")

    for topic in registry.topics:
        assert topic.check_in_person, topic.key
        for item in topic.check_in_person:
            words = {w.strip(".,;:()").lower() for w in item.split()}
            assert not words & set(banned), (topic.key, item)
