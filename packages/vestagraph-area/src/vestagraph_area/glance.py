"""At a glance counts for one postcode (FE-38, FE-39, FE-41).

Only counted topics take part; ``counted: false`` topics (the family view, route-only topics) are
ignored. The counts are derived from record statuses, never typed by hand (AGENTS rule 2).
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from vestagraph_area.records import AreaRecord, InvalidAreaDataError, PostcodeArea, Registry, Topic

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


def _records_of(topic: Topic, records: Sequence[AreaRecord]) -> list[AreaRecord]:
    return [
        r
        for r in records
        if r.topic in topic.record_topics
        and (not topic.record_subtypes or r.subtype in topic.record_subtypes)
    ]


def at_a_glance(registry: Registry, area: PostcodeArea, postcode: str) -> Glance:
    """The At a glance figures for one postcode.

    Raises ``InvalidAreaDataError`` when a counted topic has no record for the postcode.
    """
    postcode_records = [r for r in area.records if r.postcode == postcode]
    outcomes: dict[str, TopicOutcome] = {}
    questions: list[Question] = []
    check_in_person: list[CheckItem] = []
    asked: set[str] = set()
    for topic in registry.topics:
        if not topic.counted:
            continue
        records = _records_of(topic, postcode_records)
        if not records:
            message = f"Topic '{topic.key}' has no record for postcode {postcode}."
            raise InvalidAreaDataError(message)
        outcome = topic_outcome(topic, records)
        outcomes[topic.key] = outcome
        for record in records:
            if record.status in _QUESTION_STATUSES and record.id not in asked:
                asked.add(record.id)
                text = topic.question_template.replace("{label}", record.label)
                questions.append(Question(topic.key, record.id, text))
        if outcome != "not-covered":
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
