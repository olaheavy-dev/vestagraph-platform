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
    assert mentions(_problems(item), "'postcode' is a required property")


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


# Decimal strings are ASCII digits only (final review item 8): "\d" in Python's re also matches
# other scripts' digits, such as Arabic-Indic fifteen (U+0661 U+0665).
_ARABIC_INDIC_FIFTEEN = "\u0661\u0665"


def test_validate_instance_postcode_area_air_quality_non_ascii_digits_are_rejected() -> None:
    item = _valid_item()
    item["id"] = "NB1-4XY-AREA-AIR-QUALITY-1"
    item["topic"] = "air-quality"
    item["value"] = {
        "pollutant": "no2",
        "year": 2024,
        "concentration": "21.4",
        "unit": "µg/m³",
    }
    item["level"] = {"kind": "neighbourhood", "areaName": "Northbridge Central 003 (synthetic)"}
    assert _problems(item) == []

    item["value"]["concentration"] = _ARABIC_INDIC_FIFTEEN

    assert mentions(_problems(item), "concentration")


def test_validate_instance_sample_priorities_non_ascii_digit_limit_is_rejected() -> None:
    priority: Json = {
        "id": "SAMPLE-PRIORITY-TEST",
        "topicKey": "everyday-places",
        "subtype": "gp-surgery",
        "measure": "walking-minutes",
        "limit": {"value": "15", "unit": "minutes"},
        "synthetic": True,
    }
    schema = "sample-priorities.schema.json"
    assert validate_instance({"priorities": [priority]}, schema, schema_directory()) == []

    priority["limit"]["value"] = _ARABIC_INDIC_FIFTEEN

    problems = validate_instance({"priorities": [priority]}, schema, schema_directory())
    assert mentions(problems, "value")


# Flood risk by postcode is published counts per likelihood category and property type, never a
# single verdict (DA-16, final review item 3).
def _flood_risk_item() -> Json:
    item = _valid_item()
    item["id"] = "NB1-4XY-AREA-FLOOD-RISK-POSTCODE-1"
    item["topic"] = "flood-risk-postcode"
    item["value"] = {
        "source": "Rivers and sea (synthetic example)",
        "counts": [
            {
                "category": "Medium (to confirm from the download)",
                "propertyType": "residential (to confirm from the download)",
                "properties": 6,
            }
        ],
    }
    item["level"] = {"kind": "postcode"}
    return item


def test_validate_instance_postcode_area_flood_risk_counts_are_accepted() -> None:
    assert _problems(_flood_risk_item()) == []


def test_validate_instance_postcode_area_flood_risk_yes_no_field_is_rejected() -> None:
    item = _flood_risk_item()
    item["value"]["inAreaAtRisk"] = True

    assert mentions(_problems(item), "inAreaAtRisk")


def test_validate_instance_postcode_area_flood_risk_single_band_is_rejected() -> None:
    item = _flood_risk_item()
    item["value"]["publishedBand"] = "Medium"

    assert mentions(_problems(item), "publishedBand")


def test_validate_instance_postcode_area_flood_risk_without_counts_is_rejected() -> None:
    item = _flood_risk_item()
    del item["value"]["counts"]

    assert mentions(_problems(item), "counts")


def test_validate_instance_postcode_area_flood_risk_decimal_count_is_rejected() -> None:
    item = _flood_risk_item()
    item["value"]["counts"][0]["properties"] = 6.5

    assert mentions(_problems(item), "properties")


# Radon, broadband coverage and council rent (design pass Task 6a, register DA-23, DA-28, DA-29).
def _radon_item() -> Json:
    item = _valid_item()
    item["id"] = "NB1-4XY-AREA-RADON-1"
    item["topic"] = "radon"
    item["value"] = {"classLabel": "Class 2 (synthetic example)", "edition": "2022"}
    item["level"] = {"kind": "grid-square", "squareMetres": 1000}
    return item


def _broadband_coverage_item() -> Json:
    item = _valid_item()
    item["id"] = "NB1-4XY-AREA-BROADBAND-COVERAGE-1"
    item["topic"] = "broadband-coverage"
    item["value"] = {"gigabitCapablePercent": "86", "premises": "all", "snapshot": "2026-01"}
    item["level"] = {"kind": "postcode"}
    return item


def _council_rent_item() -> Json:
    item = _valid_item()
    item["id"] = "NB1-4XY-AREA-COUNCIL-RENT-1"
    item["topic"] = "council-rent"
    item["value"] = {"councilCode": "E06999001"}
    item["level"] = {"kind": "local-authority", "areaName": "Northbridge (synthetic)"}
    return item


def test_validate_instance_postcode_area_radon_is_accepted() -> None:
    assert _problems(_radon_item()) == []


def test_validate_instance_postcode_area_radon_without_edition_is_rejected() -> None:
    item = _radon_item()
    del item["value"]["edition"]
    assert mentions(_problems(item), "edition")


def test_validate_instance_postcode_area_radon_measured_level_field_is_rejected() -> None:
    item = _radon_item()
    item["value"]["measuredBecquerelsPerCubicMetre"] = 120
    assert mentions(_problems(item), "measuredBecquerelsPerCubicMetre")


def test_validate_instance_postcode_area_grid_square_no_square_metres_is_rejected() -> None:
    item = _radon_item()
    item["level"] = {"kind": "grid-square"}
    assert mentions(_problems(item), "squareMetres")


def test_validate_instance_postcode_area_broadband_coverage_is_accepted() -> None:
    assert _problems(_broadband_coverage_item()) == []


def test_validate_instance_postcode_area_broadband_coverage_full_fibre_field_is_rejected() -> None:
    item = _broadband_coverage_item()
    item["value"]["fullFibrePercent"] = "40"
    assert mentions(_problems(item), "fullFibrePercent")


def test_validate_instance_postcode_area_broadband_coverage_number_percent_is_rejected() -> None:
    item = _broadband_coverage_item()
    item["value"]["gigabitCapablePercent"] = 86
    assert mentions(_problems(item), "gigabitCapablePercent")


def test_validate_instance_postcode_area_broadband_coverage_snapshot_no_month_is_rejected() -> None:
    item = _broadband_coverage_item()
    item["value"]["snapshot"] = "2026"
    assert mentions(_problems(item), "snapshot")


def test_validate_instance_postcode_area_council_rent_is_accepted() -> None:
    assert _problems(_council_rent_item()) == []


def test_validate_instance_postcode_area_council_rent_with_pence_is_rejected() -> None:
    item = _council_rent_item()
    item["value"]["rentPence"] = 125000
    assert mentions(_problems(item), "rentPence")


def test_validate_instance_postcode_area_council_rent_without_council_code_is_rejected() -> None:
    item = _council_rent_item()
    del item["value"]["councilCode"]
    assert mentions(_problems(item), "councilCode")


def test_validate_instance_postcode_area_council_rent_gap_with_value_is_rejected() -> None:
    item = _council_rent_item()
    item["status"] = "no-record-in-source"
    assert mentions(_problems(item), "value")
