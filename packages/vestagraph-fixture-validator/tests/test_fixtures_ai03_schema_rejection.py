"""The AI-03 evaluation case contract must refuse a malformed case (AI-03, AI-14).

Each test starts from the real ``evaluation/ai-03-set.json``, breaks one thing and expects the
schema to complain about that thing.
"""

import copy
import json
from pathlib import Path

from fixtures_support import (
    Json,
    copy_fixture_folders,
    fixtures_directory,
    mentions,
    read_file,
    schema_directory,
)
from vestagraph_fixture_validator.validator import (
    FixtureProblem,
    validate_fixtures,
    validate_instance,
)

SCHEMA = "ai-03-set.schema.json"


def _problems(document: Json) -> list[FixtureProblem]:
    return validate_instance(document, SCHEMA, schema_directory())


def _document() -> Json:
    return copy.deepcopy(read_file(fixtures_directory() / "evaluation" / "ai-03-set.json"))


def _case(document: Json, shape: str) -> Json:
    """The first rule case of this shape that has a must-include list (a stable choice)."""
    matches = [
        c
        for c in document["cases"]
        if c["shape"] == shape and c["kind"] == "rule" and c["expect"].get("mustInclude")
    ]
    assert matches, shape
    return matches[0]


def test_validate_instance_ai03_set_real_file_is_accepted() -> None:
    assert _problems(_document()) == []


def test_validate_instance_ai03_set_unknown_measure_is_rejected() -> None:
    document = _document()
    _case(document, "model")["measures"] = ["vibes"]
    assert mentions(_problems(document), "/cases/")


def test_validate_instance_ai03_set_one_run_on_a_rule_case_is_rejected() -> None:
    document = _document()
    case = _case(document, "model")
    assert case["kind"] == "rule"
    case["runs"] = 1
    assert mentions(_problems(document), "/runs")


def test_validate_instance_ai03_set_model_case_without_conversation_is_rejected() -> None:
    document = _document()
    del _case(document, "model")["conversation"]
    assert mentions(_problems(document), "conversation")


def test_validate_instance_ai03_set_tool_output_case_without_tool_input_is_rejected() -> None:
    document = _document()
    del _case(document, "tool-output")["toolInput"]
    assert mentions(_problems(document), "toolInput")


def test_validate_instance_ai03_set_stub_without_synthetic_is_rejected() -> None:
    document = _document()
    _case(document, "model")["stubs"] = [{"channel": "tool-result", "text": "x"}]
    assert mentions(_problems(document), "synthetic")


def test_validate_instance_ai03_set_stub_not_marked_synthetic_true_is_rejected() -> None:
    document = _document()
    _case(document, "model")["stubs"] = [
        {"channel": "tool-result", "text": "x", "synthetic": False}
    ]
    assert mentions(_problems(document), "synthetic")


def test_validate_instance_ai03_set_unknown_stub_channel_is_rejected() -> None:
    document = _document()
    _case(document, "model")["stubs"] = [{"channel": "email", "text": "x", "synthetic": True}]
    assert mentions(_problems(document), "channel")


def test_validate_instance_ai03_set_valid_stub_is_accepted() -> None:
    document = _document()
    _case(document, "model")["stubs"] = [
        {"channel": "chat-title", "text": "A synthetic title", "synthetic": True}
    ]
    assert _problems(document) == []


def test_validate_instance_ai03_set_group_26_is_rejected() -> None:
    document = _document()
    _case(document, "model")["group"] = 26
    assert mentions(_problems(document), "/group")


def test_validate_instance_ai03_set_group_0_is_rejected() -> None:
    document = _document()
    _case(document, "model")["group"] = 0
    assert mentions(_problems(document), "/group")


def test_validate_instance_ai03_set_extra_property_is_rejected() -> None:
    document = _document()
    _case(document, "model")["verdict"] = "safe"
    assert mentions(_problems(document), "verdict")


def test_validate_instance_ai03_set_bad_case_id_is_rejected() -> None:
    document = _document()
    _case(document, "model")["id"] = "lower-case"
    assert mentions(_problems(document), "/id")


def test_validate_instance_ai03_set_quality_case_with_three_runs_is_rejected() -> None:
    document = _document()
    case = _case(document, "model")
    case["kind"] = "quality"
    case["runs"] = 3
    assert mentions(_problems(document), "/runs")


def test_validate_instance_ai03_set_empty_tests_is_rejected() -> None:
    document = _document()
    _case(document, "model")["tests"] = []
    assert mentions(_problems(document), "/tests")


def test_validate_fixtures_evaluation_folder_is_checked_against_its_schema(tmp_path: Path) -> None:
    root = copy_fixture_folders(tmp_path / "fixtures", ("schema", "data", "evaluation"))
    assert validate_fixtures(root) == []
    path = root / "evaluation" / "ai-03-set.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["cases"][0]["group"] = 26
    path.write_text(json.dumps(document), encoding="utf-8")
    assert mentions(validate_fixtures(root), "ai-03-set.json: /cases/0/group")


def test_validate_instance_ai03_set_tool_output_case_with_conversation_is_rejected() -> None:
    document = _document()
    _case(document, "tool-output")["conversation"] = [{"role": "user", "text": "hello"}]
    assert mentions(_problems(document), "conversation")


def test_validate_instance_ai03_set_model_case_with_tool_input_is_rejected() -> None:
    document = _document()
    _case(document, "model")["toolInput"] = {"tool": "find-area", "arguments": {}}
    assert mentions(_problems(document), "toolInput")


def test_validate_instance_ai03_set_must_include_free_text_source_is_rejected() -> None:
    document = _document()
    _case(document, "model")["expect"]["mustInclude"][0]["from"] = "the council's website"
    assert mentions(_problems(document), "/from")


def test_validate_instance_ai03_set_must_include_known_source_forms_are_accepted() -> None:
    for source in ("NB1-4XY-AREA-CRIME-1", "WCHAT-22", "stubs/0", "generated/area-result.json#/x"):
        document = _document()
        _case(document, "model")["expect"]["mustInclude"][0]["from"] = source
        assert _problems(document) == [], source


def test_validate_instance_ai03_set_must_not_include_plain_string_is_rejected() -> None:
    document = _document()
    _case(document, "model")["expect"]["mustNotInclude"] = ["a verdict"]
    assert mentions(_problems(document), "mustNotInclude")


def test_validate_instance_ai03_set_must_not_literal_without_value_is_rejected() -> None:
    document = _document()
    _case(document, "model")["expect"]["mustNotInclude"] = [{"match": "literal", "why": "x"}]
    assert mentions(_problems(document), "value")


def test_validate_instance_ai03_set_must_not_forbidden_words_with_value_is_rejected() -> None:
    document = _document()
    _case(document, "model")["expect"]["mustNotInclude"] = [
        {"match": "forbidden-words", "value": "safe", "why": "x"}
    ]
    assert mentions(_problems(document), "mustNotInclude")


def test_validate_instance_ai03_set_must_not_unknown_match_is_rejected() -> None:
    document = _document()
    _case(document, "model")["expect"]["mustNotInclude"] = [
        {"match": "vibes", "value": "x", "why": "x"}
    ]
    assert mentions(_problems(document), "match")


def test_validate_instance_ai03_set_must_not_without_why_is_rejected() -> None:
    document = _document()
    _case(document, "model")["expect"]["mustNotInclude"] = [{"match": "literal", "value": "x"}]
    assert mentions(_problems(document), "why")


def test_validate_instance_ai03_set_tool_result_stub_in_tool_output_case_is_rejected() -> None:
    document = _document()
    _case(document, "tool-output")["stubs"] = [
        {"channel": "tool-result", "text": "x", "synthetic": True}
    ]
    assert mentions(_problems(document), "channel")


def test_validate_instance_ai03_set_store_record_stub_in_tool_output_case_is_accepted() -> None:
    document = _document()
    _case(document, "tool-output")["stubs"] = [
        {"channel": "store-record", "text": "x", "synthetic": True}
    ]
    assert _problems(document) == []
