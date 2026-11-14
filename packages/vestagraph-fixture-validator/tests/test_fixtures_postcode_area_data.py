"""The postcode sample data holds the story's rules (issue 216, register DA-14 and DA-12).

Every figure here is a synthetic input mirrored from the home-keyed area.json; nothing is
calculated.
"""

import copy
from typing import Any

from fixtures_support import Json, area_items, load, number

_ALLOWED_TOPICS = {
    "transport-stop",
    "school",
    "school-inspection",
    "crime",
    "flood",
    "sold-price",
    "amenity",
    "broadband",
    "planning",
}
_CENTRE_METHOD = "straight-line from the postcode centre, synthetic"
_ONE_MILE_METRES = "1609.344"


def _items() -> list[Json]:
    items: list[Json] = load("postcode-area")["area"]
    return items


def _for_postcode(postcode: str) -> list[Json]:
    return [i for i in _items() if i["postcode"] == postcode]


def _b1_allowed() -> list[Json]:
    return [i for i in area_items() if i.get("homeId") == "B1" and i["topic"] in _ALLOWED_TOPICS]


def _expected_level(topic: str) -> dict[str, Any]:
    if topic in {"transport-stop", "school", "amenity"}:
        return {"kind": "from-postcode-centre"}
    if topic == "school-inspection":
        return {"kind": "named-place"}
    if topic == "crime":
        return {"kind": "radius", "radiusMetres": number(_ONE_MILE_METRES)}
    if topic in {"sold-price", "planning"}:
        return {"kind": "radius", "radiusMetres": 500}
    return {"kind": "postcode"}


def _counterpart_id(b1_id: str) -> str:
    return "NB1-4XY-" + b1_id.removeprefix("B1-")


def test_postcode_area_sample_every_allowed_b1_topic_has_a_counterpart_with_equal_values() -> None:
    by_id = {i["id"]: i for i in _for_postcode("NB1 4XY")}
    assert len(by_id) == len(_b1_allowed())
    for b1 in _b1_allowed():
        mine = by_id[_counterpart_id(b1["id"])]
        for field in (
            "label",
            "status",
            "subtype",
            "coverage",
            "doesNotEstablish",
            "source",
            "link",
            "note",
        ):
            assert mine.get(field) == b1.get(field), (mine["id"], field)
        expected = copy.deepcopy(b1.get("value"))
        if expected is not None:
            if "distanceMethod" in expected:
                expected["distanceMethod"] = _CENTRE_METHOD
            if "schoolItemId" in expected:
                expected["schoolItemId"] = _counterpart_id(expected["schoolItemId"])
        assert mine.get("value") == expected, mine["id"]


def test_postcode_area_sample_levels_follow_da14_by_topic() -> None:
    for item in _items():
        assert item["level"] == _expected_level(item["topic"]), item["id"]


def test_postcode_area_sample_crime_radius_is_exactly_one_mile() -> None:
    crimes = [i for i in _items() if i["topic"] == "crime"]
    assert crimes
    for item in crimes:
        assert item["level"]["radiusMetres"] == number(_ONE_MILE_METRES)


def test_postcode_area_sample_flood_checked_at_is_09_40_british_summer_time() -> None:
    floods = [i for i in _for_postcode("NB1 4XY") if i["topic"] == "flood"]
    assert floods
    for item in floods:
        assert item["checkedAt"] == "2026-10-23T09:40:00+01:00"


def test_postcode_area_ids_are_unique_across_area_files() -> None:
    ids = [i["id"] for i in area_items()] + [i["id"] for i in _items()]
    assert len(ids) == len(set(ids))


def test_postcode_area_ids_start_with_their_postcode() -> None:
    for item in _items():
        assert item["id"].startswith(item["postcode"].replace(" ", "-") + "-AREA-"), item["id"]


def test_postcode_area_sources_are_all_synthetic() -> None:
    for item in _items():
        assert item["source"]["synthetic"] is True, item["id"]
