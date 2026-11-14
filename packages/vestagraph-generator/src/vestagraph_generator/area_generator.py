"""Reads the area data, asks ``vestagraph_area`` for every figure and makes ``area-result.json``.

Nothing in the file is typed by hand (AGENTS rule 2). The output depends only on the data files,
never on the clock. There is no ``float`` anywhere: a whole ``Fraction`` is written as an integer
and a non-whole number as an exact decimal string (for example ``"1.5"``).
"""

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from vestagraph_area.buses import buses_in_hour
from vestagraph_area.distance import display_distance
from vestagraph_area.glance import at_a_glance
from vestagraph_area.priorities import priority_result
from vestagraph_area.records import (
    AreaRecord,
    InvalidAreaDataError,
    read_postcode_area,
    read_registry,
    read_sample_priorities,
    records_of,
)

FILE_NAME = "area-result.json"

_HAS_VALUE = ("recorded", "stale")
_BUS_HOURS = (8, 12)
_MAX_PLACES = 12


def json_number(value: Fraction | int) -> int | str:
    """A whole number as an ``int``; any other exact number as a decimal string."""
    fraction = Fraction(value)
    if fraction.denominator == 1:
        return fraction.numerator
    scaled = abs(fraction)
    places = 0
    while scaled.denominator != 1:
        scaled *= 10
        places += 1
        if places > _MAX_PLACES:
            message = f"{fraction} has no short exact decimal form."
            raise InvalidAreaDataError(message)
    text = str(scaled.numerator).rjust(places + 1, "0")
    sign = "-" if fraction < 0 else ""
    return f"{sign}{text[:-places]}.{text[-places:]}"


def _distances(records: list[AreaRecord]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for record in sorted(records, key=lambda r: r.id):
        if record.status not in _HAS_VALUE or record.value is None:
            continue
        metres = record.value.get("distanceMetres")
        if metres is None:
            continue
        entry: dict[str, Any] = {"recordId": record.id, "metres": json_number(metres)}
        walking = record.value.get("walkingMinutes")
        if walking is not None:
            entry["walkingMinutes"] = json_number(walking)
        entry["display"] = display_distance(metres)
        found.append(entry)
    return found


def _buses(records: list[AreaRecord]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for record in records:
        if record.topic != "bus-departures" or record.status not in _HAS_VALUE:
            continue
        if record.value is None:
            continue
        found.extend(
            {
                "stopItemId": record.value["stopItemId"],
                "routeNumber": record.value["routeNumber"],
                "destination": record.value["destination"],
                "hour": hour,
                "count": buses_in_hour(record.value["departures"], hour),
            }
            for hour in _BUS_HOURS
        )
    found.sort(key=lambda b: (b["stopItemId"], b["routeNumber"], b["hour"]))
    return found


def generate_area(fixtures_directory: Path) -> str:
    """The text of ``area-result.json``: two-space indent, LF line endings, one final newline.

    Raises ``OSError`` when a data file is missing and ``InvalidAreaDataError`` when the area data
    holds something the reader does not understand (for example a counted topic with no record).
    """
    data = fixtures_directory / "data"
    registry = read_registry(data / "pilot-topics.json")
    area = read_postcode_area(data / "postcode-area.json")
    priorities = read_sample_priorities(data / "sample-priorities.json", registry)
    topics = {t.key: t for t in registry.topics}

    postcodes: list[dict[str, Any]] = []
    for postcode in sorted(area.postcodes):
        records = [r for r in area.records if r.postcode == postcode]
        glance = at_a_glance(registry, area, postcode)
        postcode_priorities: list[dict[str, Any]] = []
        for priority in sorted(priorities, key=lambda p: p.id):
            result = priority_result(priority, records_of(topics[priority.topic_key], records))
            postcode_priorities.append(
                {
                    "priorityId": priority.id,
                    "outcome": result.outcome,
                    "nearestRecordId": result.nearest_record_id,
                }
            )
        postcodes.append(
            {
                "postcode": postcode,
                "glance": {
                    "found": glance.found,
                    "notKnown": glance.not_known,
                    "coverageFound": glance.coverage_found,
                    "coverageTotal": glance.coverage_total,
                    "questions": [
                        {"recordId": q.record_id, "text": q.text} for q in glance.questions
                    ],
                    "checkInPerson": [
                        {"topicKey": c.topic_key, "text": text}
                        for c in glance.check_in_person
                        for text in c.items
                    ],
                },
                "topics": [
                    {"key": t.key, "outcome": glance.outcomes[t.key]}
                    for t in registry.topics
                    if t.counted
                ],
                "distances": _distances(records),
                "busesPerHour": _buses(records),
                "priorities": postcode_priorities,
            }
        )
    document = {
        "$schema": "../schema/generated-area-result.schema.json",
        "formatVersion": 1,
        "postcodes": postcodes,
    }
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"
