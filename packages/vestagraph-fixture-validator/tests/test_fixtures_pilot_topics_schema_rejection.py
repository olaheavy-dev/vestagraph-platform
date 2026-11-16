"""The pilot-topics schema must refuse a bad map layer list (design pass Task 6a, DA-22).

Each test starts from the real ``pilot-topics.json`` data, breaks one thing and expects the schema
to complain about that thing.
"""

import copy

from fixtures_support import Json, load, mentions, schema_directory
from vestagraph_fixture_validator.validator import FixtureProblem, validate_instance


def _problems(document: Json) -> list[FixtureProblem]:
    return validate_instance(document, "pilot-topics.schema.json", schema_directory())


def _topic(document: Json, key: str) -> Json:
    return next(t for t in document["topics"] if t["key"] == key)


def test_validate_instance_pilot_topics_real_file_is_accepted() -> None:
    assert _problems(copy.deepcopy(load("pilot-topics"))) == []


def test_validate_instance_pilot_topics_unknown_map_layer_is_rejected() -> None:
    document = copy.deepcopy(load("pilot-topics"))
    _topic(document, "flood")["mapLayers"] = ["flood-zones", "tidal-surge"]
    assert mentions(_problems(document), "mapLayers")


def test_validate_instance_pilot_topics_duplicate_map_layer_is_rejected() -> None:
    document = copy.deepcopy(load("pilot-topics"))
    _topic(document, "flood")["mapLayers"] = ["flood-zones", "flood-zones"]
    assert mentions(_problems(document), "mapLayers")


def test_validate_instance_pilot_topics_empty_map_layers_is_rejected() -> None:
    document = copy.deepcopy(load("pilot-topics"))
    _topic(document, "flood")["mapLayers"] = []
    assert mentions(_problems(document), "mapLayers")


def test_validate_instance_pilot_topics_map_layers_on_route_only_topic_are_accepted() -> None:
    document = copy.deepcopy(load("pilot-topics"))
    _topic(document, "noise")["mapLayers"] = ["road-noise", "rail-noise"]
    assert _problems(document) == []


def test_validate_instance_pilot_topics_radon_record_topic_is_accepted() -> None:
    document = copy.deepcopy(load("pilot-topics"))
    _topic(document, "flood")["recordTopics"].append("radon")
    assert _problems(document) == []
