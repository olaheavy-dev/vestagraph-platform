"""The readers: what they return from the committed data, and what they refuse."""

import json
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from area_support import fixtures_directory, read_json
from vestagraph_area.records import (
    InvalidAreaDataError,
    read_postcode_area,
    read_registry,
    read_sample_priorities,
    records_of,
)

DATA = fixtures_directory() / "data"


def _write(tmp_path: Path, name: str, value: Any) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_read_registry_committed_data_returns_every_topic() -> None:
    registry = read_registry(DATA / "pilot-topics.json")

    raw = read_json(DATA / "pilot-topics.json")
    assert registry.nation == "england"
    assert [t.key for t in registry.topics] == [t["key"] for t in raw["topics"]]
    family = next(t for t in registry.topics if t.key == "family-view")
    assert family.counted is False
    assert "childcare" in family.record_subtypes
    noise = next(t for t in registry.topics if t.key == "noise")
    assert noise.official_route is not None


def test_read_postcode_area_committed_data_returns_postcodes_and_records() -> None:
    area = read_postcode_area(DATA / "postcode-area.json")

    assert area.postcodes == ("NB1 4XY", "NB7 1RR")
    assert area.unknown_postcodes == ("NB9 9ZZ",)
    assert len(area.records) == 56
    childcare = next(r for r in area.records if r.id == "NB1-4XY-AREA-AMENITY-6")
    assert (childcare.subtype, childcare.status, childcare.value) == (
        "childcare",
        "no-record-in-source",
        None,
    )


def test_read_sample_priorities_committed_data_returns_exact_limits() -> None:
    priorities = read_sample_priorities(DATA / "sample-priorities.json")

    rail = next(p for p in priorities if p.id == "SAMPLE-PRIORITY-RAIL")
    assert (rail.filter_field, rail.filter_equals, rail.measure) == (
        "stopType",
        "rail-station",
        "distance",
    )
    assert (str(rail.limit_value), rail.limit_unit) == ("3/2", "miles")
    assert len(priorities) == 6


def test_read_postcode_area_bus_departures_unknown_stop_raises_invalid_area_data(
    tmp_path: Path,
) -> None:
    data = read_json(DATA / "postcode-area.json")
    bus = next(r for r in data["area"] if r["topic"] == "bus-departures" and "value" in r)
    bus["value"]["stopItemId"] = "NB1-4XY-AREA-TRANSPORT-STOP-99"

    with pytest.raises(InvalidAreaDataError, match="TRANSPORT-STOP-99"):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))


def test_read_postcode_area_bus_departures_stop_of_other_postcode_raises_invalid_area_data(
    tmp_path: Path,
) -> None:
    data = read_json(DATA / "postcode-area.json")
    bus = next(r for r in data["area"] if r["topic"] == "bus-departures" and "value" in r)
    bus["value"]["stopItemId"] = "NB7-1RR-AREA-TRANSPORT-STOP-1"

    with pytest.raises(InvalidAreaDataError, match="NB7-1RR-AREA-TRANSPORT-STOP-1"):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))


def test_read_sample_priorities_unknown_topic_key_raises_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(DATA / "sample-priorities.json")
    data["priorities"][0]["topicKey"] = "no-such-topic"
    path = _write(tmp_path, "sample-priorities.json", data)

    with pytest.raises(InvalidAreaDataError, match="no-such-topic"):
        read_sample_priorities(path, read_registry(DATA / "pilot-topics.json"))


def test_read_postcode_area_not_json_raises_invalid_area_data(tmp_path: Path) -> None:
    path = tmp_path / "postcode-area.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(InvalidAreaDataError):
        read_postcode_area(path)


def test_read_postcode_area_record_missing_status_raises_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(DATA / "postcode-area.json")
    del data["area"][0]["status"]

    with pytest.raises(InvalidAreaDataError, match="status"):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))


# --- Reader hardening: what the JSON parser itself must refuse (final review item 6) ---


def _write_text(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_read_sample_priorities_non_finite_constant_raises_invalid_area_data(
    tmp_path: Path, constant: str
) -> None:
    path = _write_text(tmp_path, "sample-priorities.json", f'{{"priorities": [], "x": {constant}}}')

    with pytest.raises(InvalidAreaDataError, match=constant.lstrip("-")):
        read_sample_priorities(path)


def test_read_postcode_area_number_with_exponent_raises_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(DATA / "postcode-area.json")
    text = json.dumps(data).replace('"distanceMetres": 120,', '"distanceMetres": 1.2e2,', 1)
    assert "1.2e2" in text

    with pytest.raises(InvalidAreaDataError, match="exponent"):
        read_postcode_area(_write_text(tmp_path, "postcode-area.json", text))


def test_read_registry_five_thousand_digit_integer_raises_invalid_area_data(
    tmp_path: Path,
) -> None:
    path = _write_text(tmp_path, "pilot-topics.json", '{"nation": ' + "9" * 5000 + "}")

    with pytest.raises(InvalidAreaDataError):
        read_registry(path)


def test_read_registry_bad_utf8_raises_invalid_area_data(tmp_path: Path) -> None:
    path = tmp_path / "pilot-topics.json"
    path.write_bytes(b'{"nation": "\xff\xfe"}')

    with pytest.raises(InvalidAreaDataError, match="UTF-8"):
        read_registry(path)


def test_read_registry_duplicate_key_raises_invalid_area_data(tmp_path: Path) -> None:
    path = _write_text(tmp_path, "pilot-topics.json", '{"nation": "england", "nation": "wales"}')

    with pytest.raises(InvalidAreaDataError, match="nation"):
        read_registry(path)


def test_read_registry_deeply_nested_json_raises_invalid_area_data(tmp_path: Path) -> None:
    path = _write_text(tmp_path, "pilot-topics.json", "[" * 200_000 + "]" * 200_000)

    with pytest.raises(InvalidAreaDataError):
        read_registry(path)


def test_read_registry_missing_file_raises_os_error(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_registry(tmp_path / "pilot-topics.json")


# --- Reader validation: statuses and bus departures (final review item 7) ---


def test_read_postcode_area_unknown_status_raises_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(DATA / "postcode-area.json")
    data["area"][0]["status"] = "verified"

    with pytest.raises(InvalidAreaDataError, match="verified"):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("routeNumber", 12),
        ("destination", None),
        ("departures", "08:00"),
        ("departures", ["08:00", 830]),
        ("stopItemId", ["NB1-4XY-AREA-TRANSPORT-STOP-1"]),
    ],
)
def test_read_postcode_area_bus_departures_bad_value_shape_raises_invalid_area_data(
    tmp_path: Path, field: str, bad: Any
) -> None:
    data = read_json(DATA / "postcode-area.json")
    bus = next(r for r in data["area"] if r["topic"] == "bus-departures" and "value" in r)
    bus["value"][field] = bad

    with pytest.raises(InvalidAreaDataError, match=field):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))


def test_read_postcode_area_bus_departures_missing_route_number_raises_invalid_area_data(
    tmp_path: Path,
) -> None:
    data = read_json(DATA / "postcode-area.json")
    bus = next(r for r in data["area"] if r["topic"] == "bus-departures" and "value" in r)
    del bus["value"]["routeNumber"]

    with pytest.raises(InvalidAreaDataError, match="routeNumber"):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))


# --- Strict limit numbers (final review item 8) ---


@pytest.mark.parametrize("bad", ["1/3", "-5", " 2 ", "1e3", "\u0661\u0665", "5\n", "", "1.", ".5"])
def test_read_sample_priorities_limit_not_a_plain_decimal_raises_invalid_area_data(
    tmp_path: Path, bad: str
) -> None:
    data = read_json(DATA / "sample-priorities.json")
    data["priorities"][0]["limit"]["value"] = bad

    with pytest.raises(InvalidAreaDataError, match="limit value"):
        read_sample_priorities(_write(tmp_path, "sample-priorities.json", data))


@pytest.mark.parametrize(("text", "expected"), [("15", Fraction(15)), ("0.5", Fraction(1, 2))])
def test_read_sample_priorities_plain_decimal_limit_is_exact(
    tmp_path: Path, text: str, expected: Fraction
) -> None:
    data = read_json(DATA / "sample-priorities.json")
    data["priorities"][0]["limit"]["value"] = text

    priorities = read_sample_priorities(_write(tmp_path, "sample-priorities.json", data))

    assert priorities[0].limit_value == expected


# --- Reader rejections the security review found untested (final review item 18) ---


@pytest.mark.parametrize("reader", [read_registry, read_postcode_area, read_sample_priorities])
def test_read_file_not_an_object_raises_invalid_area_data(
    tmp_path: Path, reader: Callable[[Path], object]
) -> None:
    path = _write(tmp_path, "file.json", [1, 2])

    with pytest.raises(InvalidAreaDataError, match="JSON object"):
        reader(path)


@pytest.mark.parametrize(
    ("field", "bad"),
    [("counted", "yes"), ("name", 3), ("recordTopics", "school"), ("checkInPerson", [1])],
)
def test_read_registry_topic_field_of_wrong_type_raises_invalid_area_data(
    tmp_path: Path, field: str, bad: Any
) -> None:
    data = read_json(DATA / "pilot-topics.json")
    data["topics"][0][field] = bad

    with pytest.raises(InvalidAreaDataError, match=field):
        read_registry(_write(tmp_path, "pilot-topics.json", data))


@pytest.mark.parametrize("bad", ["gov.uk", {"url": "https://example.invalid"}, {"label": 5}])
def test_read_registry_bad_official_route_raises_invalid_area_data(
    tmp_path: Path, bad: Any
) -> None:
    data = read_json(DATA / "pilot-topics.json")
    noise = next(t for t in data["topics"] if t["key"] == "noise")
    noise["officialRoute"] = bad

    with pytest.raises(InvalidAreaDataError, match="noise"):
        read_registry(_write(tmp_path, "pilot-topics.json", data))


def test_read_registry_non_string_subtype_name_raises_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(DATA / "pilot-topics.json")
    data["subtypeNames"]["childcare"] = 7

    with pytest.raises(InvalidAreaDataError, match="subtypeNames"):
        read_registry(_write(tmp_path, "pilot-topics.json", data))


def test_read_registry_duplicate_topic_keys_raise_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(DATA / "pilot-topics.json")
    data["topics"][1]["key"] = data["topics"][0]["key"]

    with pytest.raises(InvalidAreaDataError, match="unique"):
        read_registry(_write(tmp_path, "pilot-topics.json", data))


def test_read_postcode_area_duplicate_record_ids_raise_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(DATA / "postcode-area.json")
    data["area"][1]["id"] = data["area"][0]["id"]

    with pytest.raises(InvalidAreaDataError, match="unique"):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))


def test_read_postcode_area_record_value_not_an_object_raises_invalid_area_data(
    tmp_path: Path,
) -> None:
    data = read_json(DATA / "postcode-area.json")
    data["area"][0]["value"] = [120]

    with pytest.raises(InvalidAreaDataError, match="value"):
        read_postcode_area(_write(tmp_path, "postcode-area.json", data))


def test_read_sample_priorities_non_string_limit_value_raises_invalid_area_data(
    tmp_path: Path,
) -> None:
    data = read_json(DATA / "sample-priorities.json")
    data["priorities"][0]["limit"]["value"] = 15

    with pytest.raises(InvalidAreaDataError, match="value"):
        read_sample_priorities(_write(tmp_path, "sample-priorities.json", data))


def test_read_sample_priorities_non_object_filter_raises_invalid_area_data(tmp_path: Path) -> None:
    data = read_json(DATA / "sample-priorities.json")
    data["priorities"][0]["filter"] = "rail-station"

    with pytest.raises(InvalidAreaDataError, match="filter"):
        read_sample_priorities(_write(tmp_path, "sample-priorities.json", data))


# --- One record selector for a topic, and priorities that fit their topic (final review item 5) ---


def test_records_of_reads_record_topics_and_only_listed_subtypes() -> None:
    registry = read_registry(DATA / "pilot-topics.json")
    area = read_postcode_area(DATA / "postcode-area.json")
    worship = next(t for t in registry.topics if t.key == "places-of-worship")
    nb1 = [r for r in area.records if r.postcode == "NB1 4XY"]

    found = records_of(worship, nb1)

    # By hand from postcode-area.json: the three place-of-worship amenities of NB1 4XY, and no
    # other amenity (supermarket, park, pharmacy, ...).
    assert [r.id for r in found] == [
        "NB1-4XY-AREA-AMENITY-7",
        "NB1-4XY-AREA-AMENITY-8",
        "NB1-4XY-AREA-AMENITY-9",
    ]


def test_records_of_topic_without_subtypes_reads_every_record_of_its_record_topics() -> None:
    registry = read_registry(DATA / "pilot-topics.json")
    area = read_postcode_area(DATA / "postcode-area.json")
    flood = next(t for t in registry.topics if t.key == "flood")

    found = records_of(flood, [r for r in area.records if r.postcode == "NB7 1RR"])

    assert [r.id for r in found] == [
        "NB7-1RR-AREA-FLOOD-1",
        "NB7-1RR-AREA-FLOOD-RISK-POSTCODE-1",
    ]


@pytest.mark.parametrize(
    ("index", "subtype"),
    [(0, "place-of-worship"), (0, "bakery")],
)
def test_read_sample_priorities_subtype_not_in_topic_raises_invalid_area_data(
    tmp_path: Path, index: int, subtype: str
) -> None:
    data = read_json(DATA / "sample-priorities.json")
    data["priorities"][index]["subtype"] = subtype  # SAMPLE-PRIORITY-GP, everyday-places

    with pytest.raises(InvalidAreaDataError, match=subtype):
        read_sample_priorities(
            _write(tmp_path, "sample-priorities.json", data),
            read_registry(DATA / "pilot-topics.json"),
        )


def test_read_sample_priorities_subtype_on_topic_without_subtypes_raises_invalid_area_data(
    tmp_path: Path,
) -> None:
    data = read_json(DATA / "sample-priorities.json")
    broadband = next(p for p in data["priorities"] if p["topicKey"] == "broadband")
    broadband["subtype"] = "full-fibre"

    with pytest.raises(InvalidAreaDataError, match="full-fibre"):
        read_sample_priorities(
            _write(tmp_path, "sample-priorities.json", data),
            read_registry(DATA / "pilot-topics.json"),
        )


@pytest.mark.parametrize(
    ("topic_key", "measure", "unit"),
    [
        ("broadband", "distance", "miles"),
        ("crime", "walking-minutes", "minutes"),
        ("everyday-places", "download-mbps", "mbps"),
        ("everyday-places", "walking-km", "minutes"),
    ],
)
def test_read_sample_priorities_measure_that_cannot_apply_to_topic_raises_invalid_area_data(
    tmp_path: Path, topic_key: str, measure: str, unit: str
) -> None:
    data = read_json(DATA / "sample-priorities.json")
    priority = data["priorities"][0]
    priority.pop("subtype", None)
    priority["topicKey"] = topic_key
    priority["measure"] = measure
    priority["limit"]["unit"] = unit

    with pytest.raises(InvalidAreaDataError, match=measure):
        read_sample_priorities(
            _write(tmp_path, "sample-priorities.json", data),
            read_registry(DATA / "pilot-topics.json"),
        )


def test_read_sample_priorities_committed_data_fits_the_registry() -> None:
    registry = read_registry(DATA / "pilot-topics.json")

    assert len(read_sample_priorities(DATA / "sample-priorities.json", registry)) == 6
