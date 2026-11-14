"""Shared helpers for the area tests: paths, and building registry and area values from JSON."""

import json
from pathlib import Path
from typing import Any

from vestagraph_area.records import AreaRecord, PostcodeArea, Registry, Topic


def repository_root() -> Path:
    for folder in Path(__file__).resolve().parents:
        if (folder / "packages" / "fixtures" / "data").is_dir():
            return folder
    message = "The repository root was not found above the tests."
    raise RuntimeError(message)


def fixtures_directory() -> Path:
    return repository_root() / "packages" / "fixtures"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def make_topic(
    key: str,
    *,
    counted: bool = True,
    record_topics: tuple[str, ...] = ("thing",),
    record_subtypes: tuple[str, ...] = (),
    gap_template: str | None = "Gap question about {subject}",
) -> Topic:
    return Topic(
        key=key,
        name=key.capitalize(),
        kind="places",
        counted=counted,
        record_topics=record_topics,
        record_subtypes=record_subtypes,
        gap_question_template=gap_template,
        check_in_person=(f"Visit {key}",),
        official_route=None,
        review_status="draft",
    )


def make_record(
    record_id: str, status: str, *, topic: str = "thing", postcode: str = "ZZ1 1AA"
) -> AreaRecord:
    return AreaRecord(
        id=record_id,
        postcode=postcode,
        topic=topic,
        subtype=None,
        status=status,
        label=f"Label {record_id}",
        value=None,
    )


def make_registry(*topics: Topic, subtype_names: dict[str, str] | None = None) -> Registry:
    return Registry(nation="england", subtype_names=subtype_names or {}, topics=topics)


def make_area(*records: AreaRecord) -> PostcodeArea:
    return PostcodeArea(postcodes=("ZZ1 1AA",), unknown_postcodes=(), records=records)
