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
    assert _record(document, "fact", "flood")
    assert _record(document, "area", "sold-nearby")
    assert _record(document, "councilFigure", "council")
    assert _record(document, "councilFigure", "neighbourhood")


def test_validate_instance_problem_report_counts_postcode_field_is_rejected() -> None:
    document = _document()
    _record(document, "area", "sold-nearby")["postcode"] = "NB1 4XY"
    assert mentions(_problems(document), "postcode")


def test_validate_instance_problem_report_counts_time_field_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "flood")["time"] = "09:40"
    assert mentions(_problems(document), "time")


def test_validate_instance_problem_report_counts_unknown_reason_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "flood")["reason"] = "offensive"
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


def test_validate_instance_problem_report_counts_banned_topics_exist_in_registry() -> None:
    schema = json.loads((schema_directory() / SCHEMA).read_text(encoding="utf-8"))
    banned = schema["$defs"]["noRecordIdTopics"]["enum"]
    keys = {topic["key"] for topic in load("pilot-topics")["topics"]}
    assert banned
    assert set(banned) <= keys


def test_validate_instance_problem_report_counts_zero_count_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "flood")["count"] = 0
    assert mentions(_problems(document), "count")


def test_validate_instance_problem_report_counts_date_with_time_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "flood")["date"] = "2026-11-19T09:40"
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
    _record(document, "fact", "flood")["factRecordId"] = "NB1 4XY"
    assert mentions(_problems(document), "factRecordId")


def test_validate_instance_problem_report_counts_address_as_figure_is_rejected() -> None:
    document = _document()
    _record(document, "councilFigure", "council")["figure"] = "12 High Street, NB1 4XY"
    assert mentions(_problems(document), "figure")


def test_validate_instance_problem_report_counts_postcode_as_source_is_rejected() -> None:
    document = _document()
    _record(document, "fact", "flood")["source"] = "NB1 4XY"
    assert mentions(_problems(document), "source")
