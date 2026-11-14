"""Reads the area data files into this package's own types.

The files are checked against their schemas by ``make validate``. Anything this reader does not
understand, including the cross-references a schema cannot express, is an
``InvalidAreaDataError`` rather than a guess; a missing file is an ``OSError``. Decimals are read
as exact ``Fraction`` values (``parse_float=Fraction``), so no ``float`` is ever made (AGENTS
rule 2).
"""

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


class InvalidAreaDataError(ValueError):
    """A data file holds something the reader does not understand."""


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
    question_template: str
    check_in_person: tuple[str, ...]
    official_route: OfficialRoute | None
    review_status: str


@dataclass(frozen=True, slots=True)
class Registry:
    """The topics of one nation."""

    nation: str
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


def _load(path: Path) -> dict[str, Any]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"), parse_float=Fraction)
    except json.JSONDecodeError as error:
        message = f"{path.name} is not valid JSON: {error}"
        raise InvalidAreaDataError(message) from error
    if not isinstance(parsed, dict):
        message = f"{path.name} must hold a JSON object."
        raise InvalidAreaDataError(message)
    return parsed


def _get(obj: dict[str, Any], key: str, kind: type, where: str) -> Any:
    if key not in obj:
        message = f"{where}: required field '{key}' is missing."
        raise InvalidAreaDataError(message)
    value = obj[key]
    if not isinstance(value, kind) or (kind is int and isinstance(value, bool)):
        message = f"{where}: field '{key}' must be a {kind.__name__}."
        raise InvalidAreaDataError(message)
    return value


def _strings(obj: dict[str, Any], key: str, where: str, *, required: bool) -> tuple[str, ...]:
    if key not in obj and not required:
        return ()
    items = _get(obj, key, list, where)
    if not all(isinstance(item, str) for item in items):
        message = f"{where}: field '{key}' must be a list of strings."
        raise InvalidAreaDataError(message)
    return tuple(items)


def _objects(obj: dict[str, Any], key: str, where: str) -> list[dict[str, Any]]:
    items: list[Any] = _get(obj, key, list, where)
    objects: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            message = f"{where}: every entry of '{key}' must be an object."
            raise InvalidAreaDataError(message)
        objects.append(item)
    return objects


def _optional_string(obj: dict[str, Any], key: str, where: str) -> str | None:
    if key not in obj:
        return None
    return str(_get(obj, key, str, where))


def _topic(raw: dict[str, Any]) -> Topic:
    key = _get(raw, "key", str, "topic")
    where = f"topic '{key}'"
    route_raw = raw.get("officialRoute")
    route: OfficialRoute | None = None
    if route_raw is not None:
        if not isinstance(route_raw, dict):
            message = f"{where}: 'officialRoute' must be an object."
            raise InvalidAreaDataError(message)
        route = OfficialRoute(
            label=_get(route_raw, "label", str, where),
            url=_optional_string(route_raw, "url", where),
        )
    return Topic(
        key=key,
        name=_get(raw, "name", str, where),
        kind=_get(raw, "kind", str, where),
        counted=_get(raw, "counted", bool, where),
        record_topics=_strings(raw, "recordTopics", where, required=True),
        record_subtypes=_strings(raw, "recordSubtypes", where, required=False),
        question_template=_get(raw, "questionTemplate", str, where),
        check_in_person=_strings(raw, "checkInPerson", where, required=True),
        official_route=route,
        review_status=_get(raw, "reviewStatus", str, where),
    )


def read_registry(path: Path) -> Registry:
    """Read ``pilot-topics.json``."""
    data = _load(path)
    topics = tuple(_topic(raw) for raw in _objects(data, "topics", path.name))
    keys = [t.key for t in topics]
    if len(set(keys)) != len(keys):
        message = f"{path.name}: topic keys must be unique."
        raise InvalidAreaDataError(message)
    return Registry(nation=_get(data, "nation", str, path.name), topics=topics)


def _record(raw: dict[str, Any]) -> AreaRecord:
    record_id = _get(raw, "id", str, "record")
    where = f"record '{record_id}'"
    value = raw.get("value")
    if value is not None and not isinstance(value, dict):
        message = f"{where}: 'value' must be an object."
        raise InvalidAreaDataError(message)
    return AreaRecord(
        id=record_id,
        postcode=_get(raw, "postcode", str, where),
        topic=_get(raw, "topic", str, where),
        subtype=_optional_string(raw, "subtype", where),
        status=_get(raw, "status", str, where),
        label=_get(raw, "label", str, where),
        value=value,
    )


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
    data = _load(path)
    where = path.name
    postcodes = tuple(
        _get(p, "postcode", str, "postcode entry") for p in _objects(data, "postcodes", where)
    )
    records = tuple(_record(raw) for raw in _objects(data, "area", where))
    ids = [r.id for r in records]
    if len(set(ids)) != len(ids):
        message = f"{where}: record ids must be unique."
        raise InvalidAreaDataError(message)
    _check_bus_stops(records)
    return PostcodeArea(
        postcodes=postcodes,
        unknown_postcodes=_strings(data, "unknownPostcodes", where, required=True),
        records=records,
    )


def _priority(raw: dict[str, Any]) -> Priority:
    priority_id = _get(raw, "id", str, "priority")
    where = f"priority '{priority_id}'"
    limit = _get(raw, "limit", dict, where)
    try:
        limit_value = Fraction(_get(limit, "value", str, where))
    except (ValueError, ZeroDivisionError) as error:
        message = f"{where}: limit value is not a decimal number."
        raise InvalidAreaDataError(message) from error
    flt = raw.get("filter")
    if flt is not None and not isinstance(flt, dict):
        message = f"{where}: 'filter' must be an object."
        raise InvalidAreaDataError(message)
    return Priority(
        id=priority_id,
        topic_key=_get(raw, "topicKey", str, where),
        subtype=_optional_string(raw, "subtype", where),
        filter_field=None if flt is None else _get(flt, "field", str, where),
        filter_equals=None if flt is None else _get(flt, "equals", str, where),
        measure=_get(raw, "measure", str, where),
        limit_value=limit_value,
        limit_unit=_get(limit, "unit", str, where),
    )


def read_sample_priorities(path: Path, registry: Registry | None = None) -> tuple[Priority, ...]:
    """Read ``sample-priorities.json``; with a registry, every ``topicKey`` must name a topic."""
    data = _load(path)
    priorities = tuple(_priority(raw) for raw in _objects(data, "priorities", path.name))
    if registry is not None:
        keys = {t.key for t in registry.topics}
        for priority in priorities:
            if priority.topic_key not in keys:
                message = (
                    f"priority '{priority.id}': topicKey '{priority.topic_key}' is not a "
                    "topic in the registry."
                )
                raise InvalidAreaDataError(message)
    return priorities
