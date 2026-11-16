"""The sample map layers hold the design pass's rules (Task 6a; DA-22, DA-24, DA-27, DA-31).

Every expected value below comes from the plan's table (docs/superpowers/plans/
2026-11-16-design-pass-topic-data.md, section 1.3), not from the data. Positions are whole metres
east and north of the postcode centre; nothing is calculated here except an integer square
distance, worked as x squared plus y squared against 500 squared (250,000).
"""

import json
import re
from typing import Any

from fixtures_support import Json, load

_WINDOW_METRES = 500
_KINDS = (
    "flood-zones",
    "surface-water",
    "listed-buildings",
    "conservation-areas",
    "road-noise",
    "rail-noise",
)
# layer -> (status at NB1 4XY, status at NB7 1RR, period), from the plan's table.
_PLAN_TABLE = {
    "flood-zones": ("recorded", "no-record-in-source", "2026-10"),
    "surface-water": ("recorded", "source-failed", "2026-10"),
    "listed-buildings": ("recorded", "no-record-in-source", "2026-10"),
    "conservation-areas": ("recorded", "not-covered", "2026-10"),
    "road-noise": ("recorded", "source-failed", "2021"),
    "rail-noise": ("no-record-in-source", "no-record-in-source", "2021"),
}
# What each layer's recorded features must be at NB1 4XY, from the plan's table.
_PLAN_FEATURE_COUNTS = {
    "flood-zones": 2,  # one Zone 3 and one Zone 2 outline
    "surface-water": 2,  # two bands
    "listed-buildings": 2,  # two points (grade II and II*)
    "conservation-areas": 1,
    "road-noise": 2,  # two Lden bands
}
_FORBIDDEN_WORDS = re.compile(r"\b(safe|unsafe|verified|approved)\b", re.IGNORECASE)


def _layers() -> list[Json]:
    layers: list[Json] = load("map-layers")["layers"]
    return layers


def _layer(postcode: str, kind: str) -> Json:
    found = [lay for lay in _layers() if lay["postcode"] == postcode and lay["layer"] == kind]
    assert len(found) == 1, (postcode, kind)
    return found[0]


def _positions(layer: Json) -> list[list[Any]]:
    found: list[list[Any]] = []
    for feature in layer.get("features", []):
        if "point" in feature:
            found.append(feature["point"])
        found.extend(feature.get("outline", []))
    return found


def test_map_layers_frame_is_metres_from_the_postcode_centre() -> None:
    assert load("map-layers")["frame"] == "metres-from-postcode-centre"


def test_map_layers_each_sample_postcode_has_every_layer_once() -> None:
    for postcode in ("NB1 4XY", "NB7 1RR"):
        kinds = sorted(lay["layer"] for lay in _layers() if lay["postcode"] == postcode)
        assert kinds == sorted(_KINDS), postcode
    assert len(_layers()) == 12


def test_map_layers_statuses_and_periods_follow_the_plan_table() -> None:
    for kind, (nb1, nb7, period) in _PLAN_TABLE.items():
        assert _layer("NB1 4XY", kind)["status"] == nb1, kind
        assert _layer("NB7 1RR", kind)["status"] == nb7, kind
        assert _layer("NB1 4XY", kind)["period"] == period, kind
        assert _layer("NB7 1RR", kind)["period"] == period, kind


def test_map_layers_gap_statuses_include_no_record_source_failed_and_not_covered() -> None:
    statuses = {lay["status"] for lay in _layers()}
    assert {"no-record-in-source", "source-failed", "not-covered"} <= statuses


def test_map_layers_recorded_features_match_the_plan_counts() -> None:
    for kind, count in _PLAN_FEATURE_COUNTS.items():
        assert len(_layer("NB1 4XY", kind)["features"]) == count, kind
    zones = sorted(f["zone"] for f in _layer("NB1 4XY", "flood-zones")["features"])
    assert zones == ["2", "3"]
    grades = sorted(f["grade"] for f in _layer("NB1 4XY", "listed-buildings")["features"])
    assert grades == ["II", "II*"]


def test_map_layers_gap_layers_have_no_features() -> None:
    for lay in _layers():
        if lay["status"] not in {"recorded", "stale"}:
            assert "features" not in lay, lay["id"]


def test_map_layers_every_outline_is_closed() -> None:
    outlines = [
        f["outline"] for lay in _layers() for f in lay.get("features", []) if "outline" in f
    ]
    # Outlines at NB1 4XY: flood zones 2 + surface water 2 + conservation areas 1 + road noise 2
    # = 7; listed buildings are points, and the gap layers have no features.
    assert len(outlines) == 7
    for outline in outlines:
        assert len(outline) >= 4
        assert outline[0] == outline[-1]


def test_map_layers_positions_are_whole_metres() -> None:
    positions = [p for lay in _layers() for p in _positions(lay)]
    assert positions
    for position in positions:
        assert len(position) == 2
        assert all(isinstance(v, int) and not isinstance(v, bool) for v in position), position


def test_map_layers_windows_are_500_metres() -> None:
    for lay in _layers():
        assert lay["level"] == {"kind": "radius", "radiusMetres": _WINDOW_METRES}, lay["id"]


def test_map_layers_every_position_is_inside_its_window() -> None:
    for lay in _layers():
        for east, north in _positions(lay):
            assert east * east + north * north <= _WINDOW_METRES * _WINDOW_METRES, lay["id"]


def test_map_layers_noise_is_2021_and_modelled_not_measured() -> None:
    for kind in ("road-noise", "rail-noise"):
        for postcode in ("NB1 4XY", "NB7 1RR"):
            lay = _layer(postcode, kind)
            assert lay["period"] == "2021"
            assert "Modelled for 2021, not measured" in lay["caption"]


def test_map_layers_flood_caption_says_area_not_one_property() -> None:
    for kind in ("flood-zones", "surface-water"):
        for postcode in ("NB1 4XY", "NB7 1RR"):
            assert "Describes an area, not one property" in _layer(postcode, kind)["caption"]
    assert "ignores flood defences" in _layer("NB1 4XY", "flood-zones")["caption"]


def test_map_layers_planning_captions_say_no_result_is_not_no_constraint() -> None:
    for kind in ("listed-buildings", "conservation-areas"):
        for postcode in ("NB1 4XY", "NB7 1RR"):
            assert "No result does not mean no constraint" in _layer(postcode, kind)["caption"]
    assert "not the protected extent" in _layer("NB1 4XY", "listed-buildings")["caption"]


def test_map_layers_sources_are_synthetic_and_shaped_like() -> None:
    for lay in _layers():
        source = lay["source"]
        assert source["synthetic"] is True, lay["id"]
        assert source["label"].startswith("Synthetic sample, shaped like "), lay["id"]
        assert source["origin"] == "official-dataset", lay["id"]


def test_map_layers_ids_are_unique_and_start_with_their_postcode() -> None:
    ids = [lay["id"] for lay in _layers()]
    assert len(set(ids)) == len(ids)
    for lay in _layers():
        assert lay["id"].startswith(lay["postcode"].replace(" ", "-") + "-LAYER-"), lay["id"]


def test_map_layers_every_postcode_is_listed() -> None:
    listed = {p["postcode"] for p in load("postcode-area")["postcodes"]}
    assert {lay["postcode"] for lay in _layers()} <= listed


def test_map_layers_each_layer_kind_belongs_to_exactly_one_topic() -> None:
    owners: dict[str, list[str]] = {kind: [] for kind in _KINDS}
    for topic in load("pilot-topics")["topics"]:
        for kind in topic.get("mapLayers", []):
            owners[kind].append(topic["key"])
    assert owners == {
        "flood-zones": ["flood"],
        "surface-water": ["flood"],
        "listed-buildings": ["planning-nearby"],
        "conservation-areas": ["planning-nearby"],
        "road-noise": ["noise"],
        "rail-noise": ["noise"],
    }


def test_map_layers_no_counted_topic_reads_a_layer_as_a_record_topic() -> None:
    # Layers live in their own file so the counts (FE-38) never see them.
    record_topics = {rt for t in load("pilot-topics")["topics"] for rt in t["recordTopics"]}
    assert not set(_KINDS) & record_topics
    assert all(i["topic"] not in _KINDS for i in load("postcode-area")["area"])


def test_map_layers_no_safe_unsafe_verified_or_approved_wording() -> None:
    text = json.dumps(load("map-layers"), default=str)
    assert _FORBIDDEN_WORDS.search(text) is None


def test_map_layers_no_gap_layer_says_no_risk() -> None:
    for lay in _layers():
        if lay["status"] in {"recorded", "stale"}:
            continue
        text = f"{lay['label']} {lay['caption']} {lay['doesNotEstablish']}".lower()
        assert "no risk" not in text, lay["id"]
