"""Reads the area data files into this package's own types.

The files are checked against their schemas by ``make validate``. Anything this reader does not
understand, including the cross-references a schema cannot express, is an
``InvalidAreaDataError`` rather than a guess; a missing file is an ``OSError``. Decimals are read
as exact ``Fraction`` values, so no ``float`` is ever made (AGENTS rule 2); ``NaN``, ``Infinity``,
numbers with an exponent, duplicate keys, bad UTF-8 and JSON nested too deeply are refused, as
the cost generator's reader does.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from vestagraph_area.json_reader import (
    PLAIN_DECIMAL,
    get_field,
    load_json_object,
    object_list,
    optional_string,
    string_list,
)
from vestagraph_area.json_reader import (
    InvalidAreaDataError as InvalidAreaDataError,
)

KNOWN_STATUSES = frozenset(
    {"recorded", "stale", "no-record-in-source", "source-failed", "not-covered"}
)
# The record topics that carry each priority measure; sibling records (school-demand, ...) never
# carry one.
MEASURE_RECORD_TOPICS: dict[str, tuple[str, ...]] = {
    "walking-minutes": ("transport-stop", "school", "amenity"),
    "distance": ("transport-stop", "school", "amenity"),
}


@dataclass(frozen=True, slots=True)
class OfficialRoute:
    """Where to look it up officially; ``url`` is ``None`` when none is recorded yet."""

    label: str
    url: str | None


@dataclass(frozen=True, slots=True)
class Topic:
    """One topic of the pilot registry (``pilot-topics.json``)."""

    key: str
    name: str
    kind: str
    counted: bool
    record_topics: tuple[str, ...]
    record_subtypes: tuple[str, ...]
    gap_question_template: str | None
    check_in_person: tuple[str, ...]
    official_route: OfficialRoute | None
    review_status: str
    vestagraph_route: str | None = None


@dataclass(frozen=True, slots=True)
class Registry:
    """The topics of one nation, and a plain name for each record subtype."""

    nation: str
    subtype_names: dict[str, str]
    topics: tuple[Topic, ...]


@dataclass(frozen=True, slots=True)
class AreaRecord:
    """One area record; ``value`` is ``None`` for the gap statuses."""

    id: str
    postcode: str
    topic: str
    subtype: str | None
    status: str
    label: str
    value: dict[str, Any] | None


@dataclass(frozen=True, slots=True)
class PostcodeArea:
    """The sample postcodes, the postcodes known to be unknown, and the records."""

    postcodes: tuple[str, ...]
    unknown_postcodes: tuple[str, ...]
    records: tuple[AreaRecord, ...]


@dataclass(frozen=True, slots=True)
class Priority:
    """A sample priority; the limit stays exact and in the unit it was typed in."""

    id: str
    topic_key: str
    subtype: str | None
    filter_field: str | None
    filter_equals: str | None
    measure: str
    limit_value: Fraction
    limit_unit: str


def records_of(topic: Topic, records: Sequence[AreaRecord]) -> list[AreaRecord]:
    """The records a topic reads: its record topics; a topic's subtypes narrow only its
    ``amenity`` records (the only record topic whose records carry place subtypes)."""
    return [
        r
        for r in records
        if r.topic in topic.record_topics
        and (
            r.topic != "amenity" or not topic.record_subtypes or r.subtype in topic.record_subtypes
        )
    ]


def _topic(raw: dict[str, Any]) -> Topic:
    key = get_field(raw, "key", str, "topic")
    where = f"topic '{key}'"
    route_raw = raw.get("officialRoute")
    route: OfficialRoute | None = None
    if route_raw is not None:
        if not isinstance(route_raw, dict):
            message = f"{where}: 'officialRoute' must be an object."
            raise InvalidAreaDataError(message)
        route = OfficialRoute(
            label=get_field(route_raw, "label", str, where),
            url=optional_string(route_raw, "url", where),
        )
    counted = get_field(raw, "counted", bool, where)
    gap_template = optional_string(raw, "gapQuestionTemplate", where)
    if counted and gap_template is None:
        message = f"{where}: a counted topic needs a 'gapQuestionTemplate'."
        raise InvalidAreaDataError(message)
    return Topic(
        key=key,
        name=get_field(raw, "name", str, where),
        kind=get_field(raw, "kind", str, where),
        counted=counted,
        record_topics=string_list(raw, "recordTopics", where, required=True),
        record_subtypes=string_list(raw, "recordSubtypes", where, required=False),
        gap_question_template=gap_template,
        check_in_person=string_list(raw, "checkInPerson", where, required=True),
        official_route=route,
        review_status=get_field(raw, "reviewStatus", str, where),
        vestagraph_route=optional_string(raw, "vestagraphRoute", where),
    )


def read_registry(path: Path) -> Registry:
    """Read ``pilot-topics.json``."""
    data = load_json_object(path)
    topics = tuple(_topic(raw) for raw in object_list(data, "topics", path.name))
    keys = [t.key for t in topics]
    if len(set(keys)) != len(keys):
        message = f"{path.name}: topic keys must be unique."
        raise InvalidAreaDataError(message)
    names = get_field(data, "subtypeNames", dict, path.name)
    if not all(isinstance(k, str) and isinstance(v, str) for k, v in names.items()):
        message = f"{path.name}: 'subtypeNames' must map subtype keys to plain names."
        raise InvalidAreaDataError(message)
    return Registry(
        nation=get_field(data, "nation", str, path.name), subtype_names=dict(names), topics=topics
    )


def _record(raw: dict[str, Any]) -> AreaRecord:
    record_id = get_field(raw, "id", str, "record")
    where = f"record '{record_id}'"
    value = raw.get("value")
    if value is not None and not isinstance(value, dict):
        message = f"{where}: 'value' must be an object."
        raise InvalidAreaDataError(message)
    status = get_field(raw, "status", str, where)
    if status not in KNOWN_STATUSES:
        message = f"{where}: unknown status '{status}'."
        raise InvalidAreaDataError(message)
    topic = get_field(raw, "topic", str, where)
    if topic == "bus-departures" and value is not None:
        _check_departures_value(value, where)
    return AreaRecord(
        id=record_id,
        postcode=get_field(raw, "postcode", str, where),
        topic=topic,
        subtype=optional_string(raw, "subtype", where),
        status=status,
        label=get_field(raw, "label", str, where),
        value=value,
    )


def _check_departures_value(value: dict[str, Any], where: str) -> None:
    """A bus-departures value names its stop, route and destination, and lists HH:MM strings."""
    for key in ("stopItemId", "routeNumber", "destination"):
        get_field(value, key, str, where)
    string_list(value, "departures", where, required=True)


def _check_bus_stops(records: tuple[AreaRecord, ...]) -> None:
    """A bus-departures record names a transport-stop record of the same postcode."""
    stops = {r.id: r.postcode for r in records if r.topic == "transport-stop"}
    for record in records:
        if record.topic != "bus-departures" or record.value is None:
            continue
        stop_id = record.value.get("stopItemId")
        if stop_id not in stops or stops[stop_id] != record.postcode:
            message = (
                f"record '{record.id}': stopItemId '{stop_id}' is not a transport-stop "
                f"record of postcode {record.postcode}."
            )
            raise InvalidAreaDataError(message)


def read_postcode_area(path: Path) -> PostcodeArea:
    """Read ``postcode-area.json``."""
    data = load_json_object(path)
    where = path.name
    postcodes = tuple(
        get_field(p, "postcode", str, "postcode entry")
        for p in object_list(data, "postcodes", where)
    )
    records = tuple(_record(raw) for raw in object_list(data, "area", where))
    ids = [r.id for r in records]
    if len(set(ids)) != len(ids):
        message = f"{where}: record ids must be unique."
        raise InvalidAreaDataError(message)
    _check_bus_stops(records)
    return PostcodeArea(
        postcodes=postcodes,
        unknown_postcodes=string_list(data, "unknownPostcodes", where, required=True),
        records=records,
    )


def _priority(raw: dict[str, Any]) -> Priority:
    priority_id = get_field(raw, "id", str, "priority")
    where = f"priority '{priority_id}'"
    limit = get_field(raw, "limit", dict, where)
    limit_text = get_field(limit, "value", str, where)
    if PLAIN_DECIMAL.fullmatch(limit_text) is None:
        message = f"{where}: limit value {limit_text!r} is not a plain decimal number."
        raise InvalidAreaDataError(message)
    limit_value = Fraction(limit_text)
    flt = raw.get("filter")
    if flt is not None and not isinstance(flt, dict):
        message = f"{where}: 'filter' must be an object."
        raise InvalidAreaDataError(message)
    return Priority(
        id=priority_id,
        topic_key=get_field(raw, "topicKey", str, where),
        subtype=optional_string(raw, "subtype", where),
        filter_field=None if flt is None else get_field(flt, "field", str, where),
        filter_equals=None if flt is None else get_field(flt, "equals", str, where),
        measure=get_field(raw, "measure", str, where),
        limit_value=limit_value,
        limit_unit=get_field(limit, "unit", str, where),
    )


def _check_priority_fits(priority: Priority, topic: Topic) -> None:
    """The priority's subtype is one its topic reads, and its measure is carried by a record
    topic its topic reads."""
    where = f"priority '{priority.id}'"
    if priority.subtype is not None and priority.subtype not in topic.record_subtypes:
        message = f"{where}: subtype '{priority.subtype}' is not a subtype of topic '{topic.key}'."
        raise InvalidAreaDataError(message)
    carriers = MEASURE_RECORD_TOPICS.get(priority.measure, ())
    if not set(carriers) & set(topic.record_topics):
        message = f"{where}: measure '{priority.measure}' cannot apply to topic '{topic.key}'."
        raise InvalidAreaDataError(message)


def read_sample_priorities(path: Path, registry: Registry | None = None) -> tuple[Priority, ...]:
    """Read ``sample-priorities.json``. With a registry, every ``topicKey`` must name a topic,
    a ``subtype`` must be one of that topic's subtypes, and the measure must be one its records
    carry."""
    data = load_json_object(path)
    priorities = tuple(_priority(raw) for raw in object_list(data, "priorities", path.name))
    if registry is not None:
        topics = {t.key: t for t in registry.topics}
        for priority in priorities:
            if priority.topic_key not in topics:
                message = (
                    f"priority '{priority.id}': topicKey '{priority.topic_key}' is not a "
                    "topic in the registry."
                )
                raise InvalidAreaDataError(message)
            _check_priority_fits(priority, topics[priority.topic_key])
    return priorities
