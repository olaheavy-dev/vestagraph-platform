"""The data steps for the Gherkin specifications in docs/specs/ (decision 0043, SP-03; issue #193).

Ported from the C# ``DataSteps``, ``SpecData`` and ``StoryPosition``. The steps check a
specification's quoted IDs against the committed fixtures and the cost engine's committed
``costs.json``, so a wrong or stale ID fails ``make test``. They never run the engine
(AGENTS.md rule 2: figures are cited by ID, not typed into a specification).
A failed check raises ``AssertionError`` with a message that names the ID to fix.
"""

import json
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

Json = Any

_COSTS = "packages/fixtures/generated/costs.json"
_EVIDENCE = "packages/fixtures/data/evidence.json"
_HOMES = "packages/fixtures/data/homes.json"
_AREA = "packages/fixtures/data/area.json"
_AREA_RESULT = "packages/fixtures/generated/area-result.json"
_POSTCODE_AREA = "packages/fixtures/data/postcode-area.json"


@dataclass(frozen=True)
class _ScenarioRange:
    home_id: str
    scenario_id: str
    from_step: int
    to_step: int


@dataclass(frozen=True)
class _Loaded:
    figures: dict[str, Json]
    scenarios: list[_ScenarioRange]
    evidence: frozenset[str]
    homes: frozenset[str]
    home_records: dict[str, Json]
    area: dict[str, Json]
    area_results: dict[str, Json]
    postcode_records: dict[str, Json]


def repository_root() -> Path:
    for folder in Path(__file__).resolve().parents:
        if (folder / "uv.lock").is_file() and (folder / "docs" / "specs").is_dir():
            return folder
    message = (
        "The repository root (uv.lock and docs/specs) was not found above "
        + str(Path(__file__))
        + "."
    )
    raise RuntimeError(message)


def specs_directory() -> Path:
    """The folder the Gherkin files are loaded from, in place (never copied)."""
    return repository_root() / "docs" / "specs"


def _read(relative_path: str) -> Json:
    return json.loads((repository_root() / relative_path).read_text(encoding="utf-8"))


def _collect_figures(node: Json, figures: dict[str, Json]) -> None:
    """Records every object that has a string ``id``, anywhere in the document."""
    if isinstance(node, dict):
        figure_id = node.get("id")
        if isinstance(figure_id, str):
            figures[figure_id] = node
        for value in node.values():
            _collect_figures(value, figures)
    elif isinstance(node, list):
        for item in node:
            _collect_figures(item, figures)


@cache
def _load() -> _Loaded:
    costs = _read(_COSTS)
    figures: dict[str, Json] = {}
    _collect_figures(costs, figures)
    scenarios = [
        _ScenarioRange(
            home["homeId"], scenario["scenarioId"], scenario["fromStep"], scenario["toStep"]
        )
        for home in costs["homes"]
        for scenario in home["scenarios"]
    ]
    evidence = frozenset(item["id"] for item in _read(_EVIDENCE)["evidence"])
    home_records = {item["id"]: item for item in _read(_HOMES)["homes"]}
    area = {item["id"]: item for item in _read(_AREA)["area"]}
    area_results = {item["postcode"]: item for item in _read(_AREA_RESULT)["postcodes"]}
    postcode_records = {item["id"]: item for item in _read(_POSTCODE_AREA)["area"]}
    return _Loaded(
        figures,
        scenarios,
        evidence,
        frozenset(home_records),
        home_records,
        area,
        area_results,
        postcode_records,
    )


def evidence_ids() -> frozenset[str]:
    return _load().evidence


def home_ids() -> frozenset[str]:
    return _load().homes


def figure_ids() -> frozenset[str]:
    return frozenset(_load().figures)


def try_get_figure(figure_id: str) -> Json | None:
    """Looks a figure up by its ID (case-sensitive); None when costs.json has no such ID."""
    return _load().figures.get(figure_id)


def try_find_scenario(home_id: str, step: int) -> str | None:
    """Finds the calculated scenario that covers a story step (B1 step 2 is "from-step-1")."""
    for item in _load().scenarios:
        if item.home_id == home_id and item.from_step <= step <= item.to_step:
            return item.scenario_id
    return None


def has_scenario_from_step(home_id: str, step: int) -> bool:
    return try_find_scenario(home_id, step) is not None


class StoryPosition:
    """Where a scenario is in the story: the home and the calculated scenario for its step.

    One per scenario (a fixture), so it starts empty each time.
    """

    def __init__(self) -> None:
        self.home_id: str | None = None
        self.scenario_id: str | None = None

    def set(self, home_id: str, scenario_id: str) -> None:
        self.home_id = home_id
        self.scenario_id = scenario_id

    @property
    def figure_prefix(self) -> str | None:
        """The prefix every cited figure ID must start with, or None before a Given step."""
        if self.home_id is None:
            return None
        return f"{self.home_id}.{self.scenario_id}."


class DataSteps:
    """The data steps; the wording that selects each is in ``specs_steps.py``."""

    def __init__(self, position: StoryPosition) -> None:
        self._position = position

    def given_home_is_at_story_step(self, home_id: str, step: int) -> None:
        assert home_id in home_ids(), (
            f'Home "{home_id}" is not in packages/fixtures/data/homes.json.'
        )
        scenario_id = try_find_scenario(home_id, step)
        assert scenario_id is not None, (
            f'{_COSTS} has no scenario for home "{home_id}" at story step {step}.'
        )
        self._position.set(home_id, scenario_id)

    def then_figure_exists(self, figure_id: str) -> None:
        self._require_figure(figure_id)

    def then_figure_has_status(self, figure_id: str, status: str) -> None:
        figure = self._require_figure(figure_id)
        assert "status" in figure, (
            f'Figure "{figure_id}" has no status (it is a total, not a line).'
        )
        assert figure["status"] == status, (
            f'Figure "{figure_id}" has a different status in {_COSTS}: '
            f'expected "{status}", found "{figure["status"]}".'
        )

    def then_figure_shows_no_amount(self, figure_id: str) -> None:
        figure = self._require_figure(figure_id)
        assert "status" in figure, (
            f'Figure "{figure_id}" is not a cost line (it has no status), '
            'so "shows no amount" does not apply to it.'
        )
        amounts = [name for name in figure if name.lower().endswith("pence")]
        assert not amounts, (
            f'Figure "{figure_id}" has an amount ({", ".join(amounts)}), '
            "but this specification expects none "
            "(missing is never shown as zero)."
        )

    def then_figure_cites_evidence(self, figure_id: str, evidence_id: str) -> None:
        figure = self._require_figure(figure_id)
        assert evidence_id in evidence_ids(), (
            f'Evidence "{evidence_id}" is not in packages/fixtures/data/evidence.json.'
        )
        cited = figure.get("evidenceIds", [])
        assert evidence_id in cited, (
            f'Figure "{figure_id}" does not cite evidence "{evidence_id}" in {_COSTS}.'
        )

    def then_total_is_partial_with_reason(self, total_id: str, category: str) -> None:
        total = self._require_figure(total_id)
        assert total.get("isPartial") is True, f'Total "{total_id}" is not partial in {_COSTS}.'
        categories = [reason["category"] for reason in total["partialReasons"]]
        assert category in categories, (
            f'Total "{total_id}" is partial, but not because of "{category}".'
        )

    def then_evidence_exists(self, evidence_id: str) -> None:
        assert evidence_id in evidence_ids(), (
            f'Evidence "{evidence_id}" is not in packages/fixtures/data/evidence.json.'
        )

    def then_area_record_has_status(self, record_id: str, status: str) -> None:
        record = _require_area_record(record_id)
        actual = record.get("status")
        assert actual == status, (
            f'Area record "{record_id}" has status "{actual}", not "{status}", in {_AREA}.'
        )

    def then_area_record_shows_no_value(self, record_id: str) -> None:
        """Rule 7: a gap, a failed source or an uncovered topic carries no value to show."""
        record = _require_area_record(record_id)
        assert "value" not in record, (
            f'Area record "{record_id}" has a value in {_AREA}, so the screen would show one.'
        )

    def then_home_has_coverage(self, home_id: str, coverage: str) -> None:
        home = _load().home_records.get(home_id)
        assert home is not None, f'Home "{home_id}" is not in {_HOMES}.'
        actual = home.get("coverage")
        assert actual == coverage, (
            f'Home "{home_id}" has coverage "{actual}", not "{coverage}", in {_HOMES}.'
        )

    def then_area_result_has_topic_with_outcome(
        self, postcode: str, topic_key: str, outcome: str
    ) -> None:
        topic = _find(_require_area_result(postcode)["topics"], "key", topic_key)
        assert topic is not None, (
            f'Area result "{postcode}" has no topic "{topic_key}" in {_AREA_RESULT} '
            "(an uncounted topic is left out of the list)."
        )
        assert topic["outcome"] == outcome, (
            f'Area result "{postcode}" topic "{topic_key}" has outcome "{topic["outcome"]}", '
            f'not "{outcome}", in {_AREA_RESULT}.'
        )

    def then_area_result_leaves_topic_out_of_coverage(self, postcode: str, topic_key: str) -> None:
        """Uncounted topics (registry ``counted`` false) are absent; not-covered add nothing."""
        topic = _find(_require_area_result(postcode)["topics"], "key", topic_key)
        assert topic is None or topic["outcome"] == "not-covered", (
            f'Area result "{postcode}" counts topic "{topic_key}" '
            f'(outcome "{topic["outcome"] if topic else ""}") in {_AREA_RESULT}, '
            "so it is not left out of the coverage total."
        )

    def then_area_result_asks_gap_question(self, postcode: str, record_id: str) -> None:
        questions = _require_area_result(postcode)["glance"]["questions"]
        assert _find(questions, "recordId", record_id) is not None, (
            f'Area result "{postcode}" asks no gap question for record "{record_id}" '
            f"in {_AREA_RESULT}."
        )

    def then_area_result_has_priority_with_outcome(
        self, postcode: str, priority_id: str, outcome: str
    ) -> None:
        priority = _require_priority(postcode, priority_id)
        assert priority["outcome"] == outcome, (
            f'Area result "{postcode}" priority "{priority_id}" has outcome '
            f'"{priority["outcome"]}", not "{outcome}", in {_AREA_RESULT}.'
        )

    def then_area_result_has_priority_with_nearest_record(
        self, postcode: str, priority_id: str, record_id: str
    ) -> None:
        priority = _require_priority(postcode, priority_id)
        assert priority.get("nearestRecordId") == record_id, (
            f'Area result "{postcode}" priority "{priority_id}" has nearest record '
            f'"{priority.get("nearestRecordId")}", not "{record_id}", in {_AREA_RESULT}.'
        )

    def then_area_result_has_display_distance(self, postcode: str, record_id: str) -> None:
        distance = _find(_require_area_result(postcode)["distances"], "recordId", record_id)
        assert distance is not None, (
            f'Area result "{postcode}" has no distance for record "{record_id}" in {_AREA_RESULT}.'
        )
        display = distance.get("display")
        assert isinstance(display, str), (
            f'Area result "{postcode}" distance for record "{record_id}" has no display text '
            f"in {_AREA_RESULT}."
        )
        assert display, (
            f'Area result "{postcode}" distance for record "{record_id}" has no display text '
            f"in {_AREA_RESULT}."
        )

    def then_area_result_counts_buses(
        self, postcode: str, stop_id: str, route: str, hour: int
    ) -> None:
        counts = [
            item
            for item in _require_area_result(postcode)["busesPerHour"]
            if item["stopItemId"] == stop_id
            and item["routeNumber"] == route
            and item["hour"] == hour
        ]
        assert counts, (
            f'Area result "{postcode}" has no bus count for stop "{stop_id}" on route "{route}" '
            f"at hour {hour} in {_AREA_RESULT}."
        )

    def then_postcode_record_has_status(self, record_id: str, status: str) -> None:
        record = _load().postcode_records.get(record_id)
        assert record is not None, (
            f'Postcode record "{record_id}" is not in {_POSTCODE_AREA}. '
            "Check the ID against that file; records are cited by ID and never typed."
        )
        actual = record.get("status")
        assert actual == status, (
            f'Postcode record "{record_id}" has status "{actual}", not "{status}", '
            f"in {_POSTCODE_AREA}."
        )

    def _require_figure(self, figure_id: str) -> Json:
        figure = try_get_figure(figure_id)
        assert figure is not None, (
            f'Figure "{figure_id}" is not in {_COSTS}. '
            "Check the ID against that file; figures are cited by ID and never typed."
        )
        prefix = self._position.figure_prefix
        assert prefix is None or figure_id.startswith(prefix), (
            f'Figure "{figure_id}" does not belong to this scenario\'s story step: '
            f'figures here start with "{prefix}".'
        )
        return figure


def _require_area_record(record_id: str) -> Json:
    record = _load().area.get(record_id)
    assert record is not None, (
        f'Area record "{record_id}" is not in {_AREA}. '
        "Check the ID against that file; records are cited by ID and never typed."
    )
    return record


def _find(items: list[Json], key: str, value: str) -> Json | None:
    return next((item for item in items if item[key] == value), None)


def _require_area_result(postcode: str) -> Json:
    result = _load().area_results.get(postcode)
    assert result is not None, (
        f'Postcode "{postcode}" is not in {_AREA_RESULT}. '
        "Check it against that file; postcodes are cited as written there."
    )
    return result


def _require_priority(postcode: str, priority_id: str) -> Json:
    priority = _find(_require_area_result(postcode)["priorities"], "priorityId", priority_id)
    assert priority is not None, (
        f'Area result "{postcode}" has no priority "{priority_id}" in {_AREA_RESULT}.'
    )
    return priority
