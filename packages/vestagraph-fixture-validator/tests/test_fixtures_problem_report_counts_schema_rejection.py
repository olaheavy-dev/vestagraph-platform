"""The Report a problem daily count contract must refuse personal detail (FE-74).

Each test starts from the real ``problem-report-counts.json`` data, breaks one thing and expects
the schema to complain about that thing.
"""

import copy
import json

from fixtures_support import Json, load, mentions, schema_directory
from vestagraph_fixture_validator.validator import FixtureProblem, validate_instance

SCHEMA = "problem-report-counts.schema.json"


def _problems(document: Json) -> list[FixtureProblem]:
    return validate_instance(document, SCHEMA, schema_directory())


def _locations(document: Json) -> set[str]:
    return {p.location for p in _problems(document)}


def _assert_only_at(document: Json, record: Json) -> None:
    """Some problem exists and every problem is inside this one count, nowhere else."""
    prefix = f"/counts/{document['counts'].index(record)}"
    found = _locations(document)
    assert found
    assert all(loc == prefix or loc.startswith(prefix + "/") for loc in found), found


def _record(document: Json, shape: str, key: str | None = None) -> Json:
    """The one sample count picked by shape and key: topic (fact, area) or areaLevel (figure)."""
    matches = [
        c
        for c in document["counts"]
        if (shape == "councilFigure") == ("figure" in c)
        and (shape != "fact" or "factRecordId" in c)
        and (shape != "area" or ("factRecordId" not in c and "topic" in c))
        and (key is None or key in (c.get("topic"), c.get("areaLevel")))
    ]
    assert len(matches) == 1, (shape, key)
    return matches[0]


def _document() -> Json:
    return copy.deepcopy(load("problem-report-counts"))


def test_validate_instance_problem_report_counts_real_file_is_accepted() -> None:
    assert _problems(_document()) == []


def test_validate_instance_problem_report_counts_sample_has_every_shape() -> None:
    document = _document()
    assert _record(document, "fact", "getting-around")
    assert _record(document, "area", "sold-nearby")
    assert _record(document, "councilFigure", "council")
    assert _record(document, "councilFigure", "neighbourhood")


def test_validate_instance_problem_report_counts_postcode_field_is_rejected() -> None:
    document = _document()
    _record(document, "area", "sold-nearby")["postcode"] = "NB1 4XY"
    assert mentions(_problems(document), "postcode")


def test_validate_instance_problem_report_counts_time_field_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "getting-around")["time"] = "09:40"
    assert mentions(_problems(document), "time")


def test_validate_instance_problem_report_counts_unknown_reason_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "getting-around")["reason"] = "offensive"
    assert mentions(_problems(document), "reason")


def test_validate_instance_problem_report_counts_free_text_is_rejected() -> None:
    document = _document()
    _record(document, "councilFigure", "council")["comment"] = "x"
    assert mentions(_problems(document), "comment")


def test_validate_instance_problem_report_counts_sold_prices_with_record_id_is_rejected() -> None:
    document = _document()
    record = _record(document, "area", "sold-nearby")
    record["topic"] = "sold-nearby"
    record["factRecordId"] = "SYNTHETIC-RECORD-1"
    assert mentions(_problems(document), "factRecordId")


def test_validate_instance_problem_report_counts_planning_with_record_id_is_rejected() -> None:
    document = _document()
    record = _record(document, "area", "planning-nearby")
    record["topic"] = "planning-nearby"
    record["factRecordId"] = "SYNTHETIC-RECORD-1"
    assert mentions(_problems(document), "factRecordId")


def test_validate_instance_problem_report_counts_allow_list_topics_exist_in_registry() -> None:
    schema = json.loads((schema_directory() / SCHEMA).read_text(encoding="utf-8"))
    allowed = schema["$defs"]["recordIdTopics"]["enum"]
    keys = {topic["key"] for topic in load("pilot-topics")["topics"]}
    assert allowed
    assert set(allowed) <= keys


def test_validate_instance_problem_report_counts_topic_enum_equals_counted_registry_keys() -> None:
    schema = json.loads((schema_directory() / SCHEMA).read_text(encoding="utf-8"))
    counted = {t["key"] for t in load("pilot-topics")["topics"] if t["counted"]}
    assert set(schema["$defs"]["topicKey"]["enum"]) == counted
    assert set(schema["$defs"]["recordIdTopics"]["enum"]) <= counted


def test_validate_instance_problem_report_counts_record_id_off_the_allow_list_is_rejected() -> None:
    for topic in ("broadband", "crime", "places-of-worship", "transport-connectivity"):
        document = _document()
        record = _record(document, "fact", "getting-around")
        record["topic"] = topic
        record["factRecordId"] = "100001"
        assert _problems(document), topic


def test_validate_instance_problem_report_counts_zero_count_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "getting-around")["count"] = 0
    assert mentions(_problems(document), "count")


def test_validate_instance_problem_report_counts_date_with_time_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "getting-around")["date"] = "2026-11-19T09:40"
    assert mentions(_problems(document), "date")


def test_validate_instance_problem_report_counts_retention_not_90_is_rejected() -> None:
    document = _document()
    document["retentionDays"] = 365
    assert mentions(_problems(document), "retentionDays")


def test_validate_instance_problem_report_counts_sample_topics_exist_in_registry() -> None:
    keys = {topic["key"] for topic in load("pilot-topics")["topics"]}
    used = {c["topic"] for c in _document()["counts"] if "topic" in c}
    assert used <= keys


def test_validate_instance_problem_report_counts_neighbourhood_with_council_code_is_rejected() -> (
    None
):
    document = _document()
    record = _record(document, "councilFigure", "council")
    record["areaLevel"] = "neighbourhood"
    record["areaCode"] = "E06999001"
    _assert_only_at(document, record)


def test_validate_instance_problem_report_counts_council_with_neighbourhood_code_is_rejected() -> (
    None
):
    document = _document()
    record = _record(document, "councilFigure", "neighbourhood")
    record["areaLevel"] = "council"
    _assert_only_at(document, record)


def test_validate_instance_problem_report_counts_postcode_as_record_id_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "getting-around")["factRecordId"] = "NB1 4XY"
    assert mentions(_problems(document), "factRecordId")


def test_validate_instance_problem_report_counts_address_as_figure_is_rejected() -> None:
    document = _document()
    _record(document, "councilFigure", "council")["figure"] = "12 High Street, NB1 4XY"
    assert mentions(_problems(document), "figure")


def test_validate_instance_problem_report_counts_postcode_as_source_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "getting-around")["source"] = "NB1 4XY"
    assert mentions(_problems(document), "source")


def test_validate_instance_problem_report_counts_record_id_containing_postcode_is_rejected() -> (
    None
):
    document = _document()
    record = _record(document, "fact")
    record["factRecordId"] = "NB1-4XY-AREA-FLOOD-1"
    assert mentions(_problems(document), "factRecordId")


def test_validate_instance_problem_report_counts_real_source_codes_are_accepted() -> None:
    for record_id in ("100001", "490000077E", "SYNTHETIC-STOP-001", "E06999001"):
        document = _document()
        _record(document, "fact")["factRecordId"] = record_id
        assert not _problems(document), record_id


def test_problem_report_counts_flood_record_id_rejected() -> None:
    schema = json.loads((schema_directory() / SCHEMA).read_text(encoding="utf-8"))
    assert "flood" not in schema["$defs"]["recordIdTopics"]["enum"]
    assert "flood-warning-area" not in schema["$defs"]["recordKind"]["enum"]
    document = _document()
    record = _record(document, "fact", "getting-around")
    record["topic"] = "flood"
    record["factRecordId"] = "100001"
    assert mentions(_problems(document), "'flood' is not one of")
    record["recordKind"] = "flood-warning-area"
    assert mentions(_problems(document), "flood-warning-area")


def test_validate_instance_problem_report_counts_childcare_record_kind_is_rejected() -> None:
    document = _document()
    record = _record(document, "fact", "getting-around")
    record["topic"] = "everyday-places"
    record["recordKind"] = "childcare"
    assert _problems(document)


def test_validate_instance_problem_report_counts_unknown_record_kind_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "getting-around")["recordKind"] = "home"
    assert _problems(document)


def test_validate_instance_problem_report_counts_record_kind_wrong_for_topic_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "getting-around")["recordKind"] = "school"
    assert _problems(document)


def test_validate_instance_problem_report_counts_known_values_only_are_accepted() -> None:
    for field, value, shape, key in (
        ("figure", "12-high-street-flat-3-jane-doe", "councilFigure", "council"),
        ("factRecordId", "JaneDoe_07700900123", "fact", None),
        ("factRecordId", "12-Acacia-Avenue", "fact", None),
        ("factRecordId", "NB1--4XY", "fact", None),
        ("factRecordId", "1" * 5000, "fact", None),
        ("topic", "nb1-4xy", "fact", None),
        ("topic", "nb1-4xy", "area", "sold-nearby"),
        ("source", "jane-doe", "fact", None),
    ):
        document = _document()
        _record(document, shape, key)[field] = value
        assert _problems(document), (field, value)


def test_validate_instance_problem_report_counts_record_id_over_32_characters_is_rejected() -> None:
    document = _document()
    _record(document, "fact")["factRecordId"] = "1" * 33
    assert mentions(_problems(document), "factRecordId")
    document = _document()
    _record(document, "fact")["factRecordId"] = "1" * 32
    assert not _problems(document)


def test_validate_instance_problem_report_counts_sample_sources_and_figures_are_known() -> None:
    schema = json.loads((schema_directory() / SCHEMA).read_text(encoding="utf-8"))
    sources = set(schema["$defs"]["source"]["enum"])
    figures = set(schema["$defs"]["figure"]["enum"])
    for count in _document()["counts"]:
        assert count["source"] in sources
        assert count.get("figure", next(iter(figures))) in figures


def test_validate_instance_problem_report_counts_identical_rows_are_rejected() -> None:
    document = _document()
    document["counts"].append(copy.deepcopy(document["counts"][0]))
    assert _problems(document)


def test_validate_instance_problem_report_counts_neighbourhood_code_as_council_is_rejected() -> (
    None
):
    for code in ("E01999011", "E00012345"):
        document = _document()
        _record(document, "fact", "getting-around")["localAuthority"] = code
        assert mentions(_problems(document), "localAuthority"), code
