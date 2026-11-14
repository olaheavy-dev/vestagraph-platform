"""The postcode-area schema must refuse bad data (issue 216).

Each test starts from a valid postcode-level record built here, breaks one thing, and expects the
schema to complain about that thing.
"""

import copy

from fixtures_support import Json, mentions, schema_directory
from vestagraph_fixture_validator.validator import FixtureProblem, validate_instance


def _valid_item() -> Json:
    return {
        "id": "NB1-4XY-AREA-TRANSPORT-STOP-1",
        "postcode": "NB1 4XY",
        "topic": "transport-stop",
        "status": "recorded",
        "label": "Test stop (synthetic)",
        "value": {
            "stopName": "Test stop (synthetic)",
            "stopType": "bus-stop",
            "distanceMetres": 100,
            "distanceMethod": "straight-line from the postcode centre, synthetic",
        },
        "level": {"kind": "from-postcode-centre"},
        "coverage": "England",
        "doesNotEstablish": "A synthetic test record.",
        "source": {
            "origin": "official-dataset",
            "label": "Synthetic test",
            "date": "2026-10-23",
            "synthetic": True,
        },
    }


def _problems(item: Json) -> list[FixtureProblem]:
    """Wrap one record in a complete file shape (the file also needs its postcode lists)."""
    file = {
        "postcodes": [
            {
                "postcode": "NB1 4XY",
                "nation": "england",
                "placeName": "Northbridge (synthetic)",
                "role": "sample",
                "synthetic": True,
            }
        ],
        "unknownPostcodes": [],
        "area": [copy.deepcopy(item)],
    }
    return validate_instance(file, "postcode-area.schema.json", schema_directory())


def _flood_item() -> Json:
    item = _valid_item()
    item["id"] = "NB1-4XY-AREA-FLOOD-1"
    item["topic"] = "flood"
    item["subtype"] = "rivers-and-sea"
    item["status"] = "no-record-in-source"
    del item["value"]
    item["level"] = {"kind": "postcode"}
    return item


def test_validate_instance_postcode_area_valid_item_is_accepted() -> None:
    assert _problems(_valid_item()) == []


def test_validate_instance_postcode_area_item_with_home_id_is_rejected() -> None:
    item = _valid_item()
    item["homeId"] = "B1"
    assert mentions(_problems(item), "homeId")


def test_validate_instance_postcode_area_item_with_no_postcode_is_rejected() -> None:
    item = _valid_item()
    del item["postcode"]
    assert mentions(_problems(item), "postcode")


def test_validate_instance_postcode_area_item_with_no_level_is_rejected() -> None:
    item = _valid_item()
    del item["level"]
    assert mentions(_problems(item), "level")


def test_validate_instance_postcode_area_radius_level_without_metres_is_rejected() -> None:
    item = _valid_item()
    item["level"] = {"kind": "radius"}
    assert mentions(_problems(item), "radiusMetres")


def test_validate_instance_postcode_area_neighbourhood_level_without_name_is_rejected() -> None:
    item = _valid_item()
    item["level"] = {"kind": "neighbourhood"}
    assert mentions(_problems(item), "areaName")


def test_validate_instance_postcode_area_flood_without_checked_at_is_rejected() -> None:
    assert mentions(_problems(_flood_item()), "checkedAt")


def test_validate_instance_postcode_area_checked_at_without_offset_is_rejected() -> None:
    item = _flood_item()
    item["checkedAt"] = "2026-10-23T09:40:00"
    assert mentions(_problems(item), "checkedAt")


def test_validate_instance_postcode_area_flood_with_offset_time_is_accepted() -> None:
    item = _flood_item()
    item["checkedAt"] = "2026-10-23T09:40:00+01:00"
    assert _problems(item) == []


def test_validate_instance_postcode_area_failed_flood_without_checked_at_is_accepted() -> None:
    item = _flood_item()
    item["status"] = "source-failed"
    assert _problems(item) == []


def test_validate_instance_postcode_area_checked_at_on_other_topic_is_rejected() -> None:
    item = _valid_item()
    item["checkedAt"] = "2026-10-23T09:40:00+01:00"
    assert mentions(_problems(item), "checkedAt")


def test_validate_instance_postcode_area_commute_topic_is_rejected() -> None:
    item = _valid_item()
    item["topic"] = "commute"
    assert mentions(_problems(item), "topic")
