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
_PILOT_TOPICS = "packages/fixtures/data/pilot-topics.json"
_POSTCODE_AREA = "packages/fixtures/data/postcode-area.json"
_MAP_LAYERS = "packages/fixtures/data/map-layers.json"
_COUNCIL_AREA = "packages/fixtures/data/council-area.json"
_COUNCIL_RESULT = "packages/fixtures/generated/council-result.json"


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
    topic_keys: frozenset[str]
    map_layers: dict[str, Json]
    topic_map_layers: dict[str, frozenset[str]]
    councils: dict[str, Json]
    council_results: dict[str, Json]
    council_searches: dict[str, Json]


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
    map_layers = {item["id"]: item for item in _read(_MAP_LAYERS)["layers"]}
    topics = _read(_PILOT_TOPICS)["topics"]
    council_result = _read(_COUNCIL_RESULT)
    return _Loaded(
        figures,
        scenarios,
        evidence,
        frozenset(home_records),
        home_records,
        area,
        area_results,
        postcode_records,
        frozenset(item["key"] for item in topics),
        map_layers,
        {item["key"]: frozenset(item.get("mapLayers", [])) for item in topics},
        {item["code"]: item for item in _read(_COUNCIL_AREA)["councils"]},
        {item["code"]: item for item in council_result["councils"]},
        {item["query"]: item for item in council_result["search"]},
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
        """Absent from ``topics`` (registry ``counted`` false) or not-covered: not in the total."""
        assert topic_key in _load().topic_keys, (
            f'Topic "{topic_key}" is not in {_PILOT_TOPICS}. Check the key for a typo.'
        )
        topic = _find(_require_area_result(postcode)["topics"], "key", topic_key)
        assert topic is None or topic["outcome"] == "not-covered", (
            f'Area result "{postcode}" counts topic "{topic_key}" in {_AREA_RESULT}.'
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

    def then_map_layer_has_status(self, layer_id: str, status: str) -> None:
        layer = _load().map_layers.get(layer_id)
        assert layer is not None, (
            f'Map layer "{layer_id}" is not in {_MAP_LAYERS}. '
            "Check the ID against that file; layers are cited by ID and never typed."
        )
        actual = layer.get("status")
        assert actual == status, (
            f'Map layer "{layer_id}" has status "{actual}", not "{status}", in {_MAP_LAYERS}.'
        )

    def then_topic_draws_map_layer(self, topic_key: str, layer_kind: str) -> None:
        layers = _load().topic_map_layers.get(topic_key)
        assert layers is not None, (
            f'Topic "{topic_key}" is not in {_PILOT_TOPICS}. Check the key against that file.'
        )
        assert layer_kind in layers, (
            f'Topic "{topic_key}" does not list map layer "{layer_kind}" in {_PILOT_TOPICS}; '
            f"it lists {sorted(layers)}."
        )

    def then_council_has_field_with_status(self, code: str, field: str, status: str) -> None:
        record = _require_council(code).get(field)
        assert isinstance(record, dict), (
            f'Council "{code}" has no field "{field}" in {_COUNCIL_AREA}. '
            "Check the field name against that file."
        )
        assert record.get("status") == status, (
            f'Council "{code}" field "{field}" has status "{record.get("status")}", '
            f'not "{status}", in {_COUNCIL_AREA}.'
        )

    def then_council_series_marks_method_break(self, code: str, series: str) -> None:
        record = _require_council(code).get(series)
        assert isinstance(record, dict), (
            f'Council "{code}" has no series "{series}" in {_COUNCIL_AREA}.'
        )
        assert any(point.get("methodBreakBefore") for point in record.get("points", [])), (
            f'Council "{code}" series "{series}" marks no method break in {_COUNCIL_AREA}.'
        )

    def then_council_band_has_problem(self, code: str, band: str, problem: str) -> None:
        entry = _require_council_band(code, band)
        assert entry.get("problem") == problem, (
            f'Council "{code}" band "{band}" has problem "{entry.get("problem")}", '
            f'not "{problem}", in {_COUNCIL_RESULT}.'
        )

    def then_council_band_has_no_rent_side(self, code: str, band: str) -> None:
        entry = _require_council_band(code, band)
        assert not {"rentSide", "shownRentSide"} & entry.keys(), (
            f'Council "{code}" band "{band}" has a rent side in {_COUNCIL_RESULT}; '
            "a missing rent is never a figure (rule 7)."
        )

    def then_council_product_has_key(
        self, code: str, band: str, product: str, key: str, value: str
    ) -> None:
        sides = _require_council_band(code, band).get("buySides", [])
        side = _find(sides, "product", product)
        assert side is not None, (
            f'Council "{code}" band "{band}" has no buy side for product "{product}" '
            f"in {_COUNCIL_RESULT}."
        )
        assert side.get(key) == value, (
            f'Council "{code}" band "{band}" product "{product}" has {key} "{side.get(key)}", '
            f'not "{value}", in {_COUNCIL_RESULT}.'
        )

    def then_council_product_has_no_comparison(self, code: str, band: str, product: str) -> None:
        sides = _require_council_band(code, band).get("buySides", [])
        side = _find(sides, "product", product)
        assert side is not None, (
            f'Council "{code}" band "{band}" has no buy side for product "{product}" '
            f"in {_COUNCIL_RESULT}."
        )
        assert not {"comparison", "shownDifference"} & side.keys(), (
            f'Council "{code}" band "{band}" product "{product}" has a comparison in '
            f"{_COUNCIL_RESULT}; a difference needs both sides (rule 7)."
        )

    def then_council_caption_has_key(self, code: str, topic: str, key: str, value: str) -> None:
        council = _load().council_results.get(code)
        assert council is not None, (
            f'Council "{code}" is not in {_COUNCIL_RESULT}. '
            "Check the code against that file; councils are cited by code."
        )
        property_type = None
        if topic.startswith("price:"):
            topic, property_type = "price", topic.removeprefix("price:")
        if property_type is None:
            caption = _find(council["captions"], "topic", topic)
        else:
            caption = _find(council["priceByType"], "propertyType", property_type)
        assert caption is not None, (
            f'Council "{code}" has no caption for "{topic}"'
            f"{'' if property_type is None else f' type {property_type}'} in {_COUNCIL_RESULT}."
        )
        actual = caption["values"].get(key)
        assert actual == value, (
            f'Council "{code}" caption "{topic}" has {key} "{actual}", not "{value}", '
            f"in {_COUNCIL_RESULT}."
        )

    def then_council_search_has_kind(self, query: str, kind: str) -> None:
        search = _require_council_search(query)
        assert search["kind"] == kind, (
            f'Council search "{query}" has kind "{search["kind"]}", not "{kind}", '
            f"in {_COUNCIL_RESULT}."
        )

    def then_council_search_lists_council(
        self, query: str, code: str, note: str | None = None
    ) -> None:
        match = _find(_require_council_search(query)["matches"], "councilCode", code)
        assert match is not None, (
            f'Council search "{query}" does not list council "{code}" in {_COUNCIL_RESULT}.'
        )
        assert note is None or match.get("note") == note, (
            f'Council search "{query}" lists council "{code}" with note "{match.get("note")}", '
            f'not "{note}", in {_COUNCIL_RESULT}.'
        )

    def then_council_neighbourhood_fact_has_status(
        self, code: str, neighbourhood: str, fact: str, status: str
    ) -> None:
        record = _require_neighbourhood_fact(code, neighbourhood, fact)
        assert record.get("status") == status, (
            f'Council "{code}" neighbourhood "{neighbourhood}" fact "{fact}" has status '
            f'"{record.get("status")}", not "{status}", in {_COUNCIL_AREA}.'
        )

    def then_council_neighbourhood_fact_has_level(
        self, code: str, neighbourhood: str, fact: str, level: str
    ) -> None:
        record = _require_neighbourhood_fact(code, neighbourhood, fact)
        actual = record.get("level", {}).get("kind")
        assert actual == level, (
            f'Council "{code}" neighbourhood "{neighbourhood}" fact "{fact}" is at level '
            f'"{actual}", not "{level}", in {_COUNCIL_AREA}.'
        )

    def then_council_lists_neighbourhood_with_label(
        self, code: str, neighbourhood: str, label: str
    ) -> None:
        entry = _find(_require_council_result(code)["neighbourhoods"], "code", neighbourhood)
        assert entry is not None, (
            f'Council "{code}" does not list neighbourhood "{neighbourhood}" in {_COUNCIL_RESULT}.'
        )
        assert entry.get("label") == label, (
            f'Council "{code}" neighbourhood "{neighbourhood}" has label "{entry.get("label")}", '
            f'not "{label}", in {_COUNCIL_RESULT}.'
        )

    def then_council_neighbourhood_has_tenure_shares(self, code: str, neighbourhood: str) -> None:
        entry = _find(_require_council_result(code)["neighbourhoods"], "code", neighbourhood)
        assert entry is not None, (
            f'Council "{code}" does not list neighbourhood "{neighbourhood}" in {_COUNCIL_RESULT}.'
        )
        assert entry.get("tenureShares"), (
            f'Council "{code}" neighbourhood "{neighbourhood}" has no tenure shares in '
            f"{_COUNCIL_RESULT}; missing shares are never shown as zero (rule 7)."
        )

    def then_council_lists_no_neighbourhoods(self, code: str) -> None:
        listed = _require_council_result(code)["neighbourhoods"]
        assert not listed, (
            f'Council "{code}" lists {len(listed)} neighbourhoods in {_COUNCIL_RESULT}; '
            "this step expects none."
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


def _require_council(code: str) -> Json:
    council = _load().councils.get(code)
    assert council is not None, (
        f'Council "{code}" is not in {_COUNCIL_AREA}. '
        "Check the code against that file; councils are cited by code."
    )
    return council


def _require_council_result(code: str) -> Json:
    council = _load().council_results.get(code)
    assert council is not None, (
        f'Council "{code}" is not in {_COUNCIL_RESULT}. '
        "Check the code against that file; councils are cited by code."
    )
    return council


def _require_neighbourhood_fact(code: str, neighbourhood: str, fact: str) -> Json:
    entry = _find(_require_council(code)["neighbourhoods"], "code", neighbourhood)
    assert entry is not None, (
        f'Council "{code}" has no neighbourhood "{neighbourhood}" in {_COUNCIL_AREA}. '
        "Neighbourhoods are cited by their LSOA code."
    )
    record = entry["facts"].get(fact)
    assert isinstance(record, dict), (
        f'Neighbourhood "{neighbourhood}" has no fact "{fact}" in {_COUNCIL_AREA}. '
        "Check the fact name against that file."
    )
    return record


def _require_council_band(code: str, band: str) -> Json:
    council = _load().council_results.get(code)
    assert council is not None, (
        f'Council "{code}" is not in {_COUNCIL_RESULT}. '
        "Check the code against that file; councils are cited by code."
    )
    entry = _find(council["rentOrBuy"]["byBand"], "band", band)
    assert entry is not None, f'Council "{code}" has no band "{band}" in {_COUNCIL_RESULT}.'
    return entry


def _require_council_search(query: str) -> Json:
    search = _load().council_searches.get(query)
    assert search is not None, (
        f'Council search "{query}" is not in {_COUNCIL_RESULT}. '
        "Check it against that file; searches are cited as written there."
    )
    return search
