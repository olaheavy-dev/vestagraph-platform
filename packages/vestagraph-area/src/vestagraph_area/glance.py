"""At a glance counts for one postcode (FE-38, FE-39, FE-41).

Only counted topics take part in the counts; ``counted: false`` topics (the family view,
route-only topics) are never counted. Every record of the postcode must belong to exactly one
counted topic (a record that only an uncounted grouping reads is allowed). Questions to ask come
from gap records, one per (topic, question text). Check in person lists every counted topic,
whatever its outcome, and every route-only topic, in registry order; the lists are never counted
(FE-41). The counts are derived from record statuses, never typed by hand (AGENTS rule 2).
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from vestagraph_area.records import (
    AreaRecord,
    InvalidAreaDataError,
    PostcodeArea,
    Registry,
    Topic,
    records_of,
)

TopicOutcome = Literal["found", "not-known", "not-covered"]

_FOUND_STATUSES = frozenset({"recorded", "stale", "no-record-in-source"})
_QUESTION_STATUSES = frozenset({"no-record-in-source", "source-failed", "not-covered"})


@dataclass(frozen=True, slots=True)
class Question:
    """A question to ask about one record that is a gap."""

    topic_key: str
    record_id: str
    text: str


@dataclass(frozen=True, slots=True)
class CheckItem:
    """A topic's check-in-person list (no count is shown, FE-41)."""

    topic_key: str
    topic_name: str
    items: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Glance:
    """The At a glance figures: counts, questions, check-in-person lists, each topic's outcome."""

    found: int
    not_known: int
    questions: tuple[Question, ...]
    check_in_person: tuple[CheckItem, ...]
    coverage_found: int
    coverage_total: int
    outcomes: dict[str, TopicOutcome]


def topic_outcome(topic: Topic, records: Sequence[AreaRecord]) -> TopicOutcome:
    """``found`` if any record is recorded, stale or no-record-in-source; else ``not-covered``
    when every record is not-covered; else ``not-known``. The caller passes at least one record.
    """
    if any(r.status in _FOUND_STATUSES for r in records):
        return "found"
    if all(r.status == "not-covered" for r in records):
        return "not-covered"
    return "not-known"


def _check_ownership(registry: Registry, records: Sequence[AreaRecord]) -> None:
    """Each record is read by exactly one counted topic, or only by uncounted groupings."""
    for record in records:
        owners = [t.key for t in registry.topics if t.counted and records_of(t, [record])]
        if len(owners) > 1:
            message = (
                f"Record '{record.id}' is read by more than one counted topic: {', '.join(owners)}."
            )
            raise InvalidAreaDataError(message)
        if not owners and not any(records_of(t, [record]) for t in registry.topics):
            message = f"Record '{record.id}' belongs to no topic in the registry."
            raise InvalidAreaDataError(message)


def _gap_question(registry: Registry, topic: Topic, record: AreaRecord) -> str:
    """The topic's gap template; its {subject} is a plain name, never the record's label."""
    template = topic.gap_question_template
    if template is None:
        message = f"Topic '{topic.key}' has no gapQuestionTemplate."
        raise InvalidAreaDataError(message)
    subject = registry.subtype_names.get(record.subtype or "", topic.name.lower())
    return template.replace("{subject}", subject)


def at_a_glance(registry: Registry, area: PostcodeArea, postcode: str) -> Glance:
    """The At a glance figures for one postcode.

    Raises ``InvalidAreaDataError`` when a counted topic has no record for the postcode, or a
    record of the postcode belongs to no topic or to more than one counted topic.
    """
    postcode_records = [r for r in area.records if r.postcode == postcode]
    _check_ownership(registry, postcode_records)
    outcomes: dict[str, TopicOutcome] = {}
    questions: list[Question] = []
    check_in_person: list[CheckItem] = []
    for topic in registry.topics:
        if topic.kind == "route-only":
            check_in_person.append(CheckItem(topic.key, topic.name, topic.check_in_person))
        if not topic.counted:
            continue
        records = records_of(topic, postcode_records)
        if not records:
            message = f"Topic '{topic.key}' has no record for postcode {postcode}."
            raise InvalidAreaDataError(message)
        outcomes[topic.key] = topic_outcome(topic, records)
        asked: set[str] = set()
        for record in records:
            if record.status not in _QUESTION_STATUSES:
                continue
            text = _gap_question(registry, topic, record)
            if text not in asked:
                asked.add(text)
                questions.append(Question(topic.key, record.id, text))
        check_in_person.append(CheckItem(topic.key, topic.name, topic.check_in_person))
    found = sum(1 for o in outcomes.values() if o == "found")
    not_known = sum(1 for o in outcomes.values() if o == "not-known")
    return Glance(
        found=found,
        not_known=not_known,
        questions=tuple(questions),
        check_in_person=tuple(check_in_person),
        coverage_found=found,
        coverage_total=found + not_known,
        outcomes=outcomes,
    )
