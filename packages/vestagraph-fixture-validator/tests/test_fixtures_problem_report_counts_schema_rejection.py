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


def _record(document: Json, shape: str) -> Json:
    """The first sample count of one shape: fact, area or councilFigure."""
    marker = {"fact": "factRecordId", "councilFigure": "figure"}
    if shape in marker:
        return next(c for c in document["counts"] if marker[shape] in c)
    return next(c for c in document["counts"] if "factRecordId" not in c and "topic" in c)


def _document() -> Json:
    return copy.deepcopy(load("problem-report-counts"))


def test_validate_instance_problem_report_counts_real_file_is_accepted() -> None:
    assert _problems(_document()) == []


def test_validate_instance_problem_report_counts_sample_has_every_shape() -> None:
    document = _document()
    for shape in ("fact", "area", "councilFigure"):
        assert _record(document, shape) is not None


def test_validate_instance_problem_report_counts_postcode_field_is_rejected() -> None:
    document = _document()
    _record(document, "area")["postcode"] = "NB1 4XY"
    assert mentions(_problems(document), "postcode")


def test_validate_instance_problem_report_counts_time_field_is_rejected() -> None:
    document = _document()
    _record(document, "fact")["time"] = "09:40"
    assert mentions(_problems(document), "time")


def test_validate_instance_problem_report_counts_unknown_reason_is_rejected() -> None:
    document = _document()
    _record(document, "fact")["reason"] = "offensive"
    assert mentions(_problems(document), "reason")


def test_validate_instance_problem_report_counts_free_text_is_rejected() -> None:
    document = _document()
    _record(document, "councilFigure")["comment"] = "x"
    assert mentions(_problems(document), "comment")


def test_validate_instance_problem_report_counts_sold_prices_with_record_id_is_rejected() -> None:
    document = _document()
    record = _record(document, "area")
    record["topic"] = "sold-nearby"
    record["factRecordId"] = "SYNTHETIC-RECORD-1"
    assert mentions(_problems(document), "factRecordId")


def test_validate_instance_problem_report_counts_planning_with_record_id_is_rejected() -> None:
    document = _document()
    record = _record(document, "area")
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
    _record(document, "fact")["count"] = 0
    assert mentions(_problems(document), "count")


def test_validate_instance_problem_report_counts_date_with_time_is_rejected() -> None:
    document = _document()
    _record(document, "fact")["date"] = "2026-11-19T09:40"
    assert mentions(_problems(document), "date")


def test_validate_instance_problem_report_counts_retention_not_90_is_rejected() -> None:
    document = _document()
    document["retentionDays"] = 365
    assert mentions(_problems(document), "retentionDays")
