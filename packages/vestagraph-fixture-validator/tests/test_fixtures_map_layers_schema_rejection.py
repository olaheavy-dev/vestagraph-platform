"""The map-layers schema must refuse bad data (design pass Task 6a, register DA-22, DA-24, DA-27).

Each test starts from a valid layer built here, breaks one thing, and expects the schema to
complain about that thing.
"""

import copy

from fixtures_support import Json, mentions, schema_directory
from vestagraph_fixture_validator.validator import FixtureProblem, validate_instance

_OUTLINE = [[-100, -100], [100, -100], [100, 100], [-100, 100], [-100, -100]]


def _layer(kind: str = "flood-zones") -> Json:
    features: dict[str, Json] = {
        "flood-zones": {"zone": "3", "outline": _OUTLINE},
        "surface-water": {"band": "High", "outline": _OUTLINE},
        "listed-buildings": {"name": "Test hall (synthetic)", "grade": "II", "point": [10, -20]},
        "conservation-areas": {"name": "Test area (synthetic)", "outline": _OUTLINE},
        "road-noise": {"metric": "Lden", "band": "60.0-64.9", "outline": _OUTLINE},
        "rail-noise": {"metric": "Lden", "band": "60.0-64.9", "outline": _OUTLINE},
    }
    return {
        "id": f"NB1-4XY-LAYER-{kind.upper()}-1",
        "postcode": "NB1 4XY",
        "layer": kind,
        "status": "recorded",
        "label": "Test layer (synthetic)",
        "caption": "Describes an area, not one property",
        "period": "2026-10",
        "level": {"kind": "radius", "radiusMetres": 500},
        "coverage": "England",
        "doesNotEstablish": "A synthetic test layer.",
        "source": {
            "origin": "official-dataset",
            "label": "Synthetic sample, shaped like a test source",
            "date": "2026-10-23",
            "synthetic": True,
        },
        "features": [copy.deepcopy(features[kind])],
    }


def _problems(layer: Json) -> list[FixtureProblem]:
    file = {"frame": "metres-from-postcode-centre", "layers": [copy.deepcopy(layer)]}
    return validate_instance(file, "map-layers.schema.json", schema_directory())


def test_validate_instance_map_layers_valid_layer_is_accepted() -> None:
    assert _problems(_layer()) == []


def test_validate_instance_map_layers_every_layer_kind_with_its_feature_is_accepted() -> None:
    for kind in (
        "flood-zones",
        "surface-water",
        "listed-buildings",
        "conservation-areas",
        "road-noise",
        "rail-noise",
    ):
        assert _problems(_layer(kind)) == [], kind


def test_validate_instance_map_layers_recorded_layer_without_features_is_rejected() -> None:
    layer = _layer()
    del layer["features"]
    assert mentions(_problems(layer), "features")


def test_validate_instance_map_layers_gap_layer_with_features_is_rejected() -> None:
    layer = _layer()
    layer["status"] = "no-record-in-source"
    assert mentions(_problems(layer), "features")


def test_validate_instance_map_layers_gap_layer_without_features_is_accepted() -> None:
    layer = _layer()
    layer["status"] = "source-failed"
    del layer["features"]
    assert _problems(layer) == []


def test_validate_instance_map_layers_decimal_metres_are_rejected() -> None:
    layer = _layer()
    layer["features"][0]["outline"][1] = [100.5, -100]
    assert mentions(_problems(layer), "is not of type 'integer'")


def test_validate_instance_map_layers_three_numbers_in_a_position_are_rejected() -> None:
    layer = _layer()
    layer["features"][0]["outline"][1] = [100, -100, 5]
    assert mentions(_problems(layer), "is too long")


def test_validate_instance_map_layers_outline_of_three_positions_is_rejected() -> None:
    layer = _layer()
    layer["features"][0]["outline"] = [[0, 0], [100, 0], [0, 0]]
    assert mentions(_problems(layer), "is too short")


def test_validate_instance_map_layers_contains_postcode_centre_field_is_rejected() -> None:
    layer = _layer()
    layer["features"][0]["containsPostcodeCentre"] = True
    assert mentions(_problems(layer), "containsPostcodeCentre")


def test_validate_instance_map_layers_risk_field_is_rejected() -> None:
    layer = _layer()
    layer["features"][0]["risk"] = "low"
    assert mentions(_problems(layer), "risk")


def test_validate_instance_map_layers_flood_zone_one_is_rejected() -> None:
    layer = _layer()
    layer["features"][0]["zone"] = "1"
    assert mentions(_problems(layer), "zone")


def test_validate_instance_map_layers_noise_decibels_are_rejected() -> None:
    layer = _layer("road-noise")
    layer["features"][0]["decibels"] = 62
    assert mentions(_problems(layer), "decibels")


def test_validate_instance_map_layers_noise_metric_other_than_lden_is_rejected() -> None:
    layer = _layer("rail-noise")
    layer["features"][0]["metric"] = "Lnight"
    assert mentions(_problems(layer), "metric")


def test_validate_instance_map_layers_listed_building_with_an_outline_is_rejected() -> None:
    layer = _layer("listed-buildings")
    layer["features"][0]["outline"] = _OUTLINE
    assert mentions(_problems(layer), "outline")


def test_validate_instance_map_layers_listed_building_grade_unknown_is_rejected() -> None:
    layer = _layer("listed-buildings")
    layer["features"][0]["grade"] = "III"
    assert mentions(_problems(layer), "grade")


def test_validate_instance_map_layers_feature_of_the_wrong_layer_kind_is_rejected() -> None:
    layer = _layer("flood-zones")
    layer["features"] = _layer("listed-buildings")["features"]
    assert mentions(_problems(layer), "zone") or mentions(_problems(layer), "grade")


def test_validate_instance_map_layers_unknown_frame_is_rejected() -> None:
    file = {"frame": "british-national-grid", "layers": [_layer()]}
    problems = validate_instance(file, "map-layers.schema.json", schema_directory())
    assert mentions(problems, "frame")


def test_validate_instance_map_layers_missing_caption_is_rejected() -> None:
    layer = _layer()
    del layer["caption"]
    assert mentions(_problems(layer), "'caption' is a required property")


def test_validate_instance_map_layers_caption_over_120_characters_is_rejected() -> None:
    layer = _layer()
    layer["caption"] = "x" * 121
    assert mentions(_problems(layer), "caption")


def test_validate_instance_map_layers_unknown_layer_kind_is_rejected() -> None:
    layer = _layer()
    layer["layer"] = "crime"
    assert mentions(_problems(layer), "'crime' is not one of")


def test_validate_instance_map_layers_level_without_radius_is_rejected() -> None:
    layer = _layer()
    layer["level"] = {"kind": "radius"}
    assert mentions(_problems(layer), "radiusMetres")


def test_validate_instance_map_layers_id_without_layer_marker_is_rejected() -> None:
    layer = _layer()
    layer["id"] = "NB1-4XY-AREA-FLOOD-ZONES-1"
    assert mentions(_problems(layer), "id")
