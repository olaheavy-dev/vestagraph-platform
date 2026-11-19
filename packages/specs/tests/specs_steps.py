"""The step bindings for the data scenarios: the wording is the contract in docs/specs/README.md.

Each binding hands over to ``DataSteps`` (``specs_support.py``), which holds the checks and their
failure messages. A step whose wording is not here makes its scenario fail as undefined: add the
step here (with a test) rather than rewording the scenario around it.

A test module that calls ``scenarios()`` imports everything from here with ``import *``: pytest-bdd
finds step definitions and fixtures in the test module's namespace (or in a ``conftest.py``, which
its documentation also describes). The decorators register each step under a generated name
(``pytestbdd_stepdef_...``) that only a star import carries over. This layout keeps the steps
importable by the proof tests' temporary modules, which a ``conftest.py`` here would not reach.
"""

import pytest
from pytest_bdd import given, parsers, then
from specs_support import DataSteps, StoryPosition


@pytest.fixture
def story_position() -> StoryPosition:
    """One per scenario, so every scenario starts with no home or story step."""
    return StoryPosition()


@pytest.fixture
def data_steps(story_position: StoryPosition) -> DataSteps:
    return DataSteps(story_position)


@given(parsers.parse('home "{home_id}" is at story step {step:d}'))
def given_home_is_at_story_step(data_steps: DataSteps, home_id: str, step: int) -> None:
    data_steps.given_home_is_at_story_step(home_id, step)


@then(parsers.parse('figure "{figure_id}" exists'))
def then_figure_exists(data_steps: DataSteps, figure_id: str) -> None:
    data_steps.then_figure_exists(figure_id)


@then(parsers.parse('figure "{figure_id}" has status "{status}"'))
def then_figure_has_status(data_steps: DataSteps, figure_id: str, status: str) -> None:
    data_steps.then_figure_has_status(figure_id, status)


@then(parsers.parse('figure "{figure_id}" shows no amount'))
def then_figure_shows_no_amount(data_steps: DataSteps, figure_id: str) -> None:
    data_steps.then_figure_shows_no_amount(figure_id)


@then(parsers.parse('figure "{figure_id}" cites evidence "{evidence_id}"'))
def then_figure_cites_evidence(data_steps: DataSteps, figure_id: str, evidence_id: str) -> None:
    data_steps.then_figure_cites_evidence(figure_id, evidence_id)


@then(parsers.parse('the total "{total_id}" is partial with reason "{category}"'))
def then_total_is_partial_with_reason(data_steps: DataSteps, total_id: str, category: str) -> None:
    data_steps.then_total_is_partial_with_reason(total_id, category)


@then(parsers.parse('evidence "{evidence_id}" exists'))
def then_evidence_exists(data_steps: DataSteps, evidence_id: str) -> None:
    data_steps.then_evidence_exists(evidence_id)


@then(parsers.parse('area record "{record_id}" has status "{status}"'))
def then_area_record_has_status(data_steps: DataSteps, record_id: str, status: str) -> None:
    data_steps.then_area_record_has_status(record_id, status)


@then(parsers.parse('area record "{record_id}" shows no value'))
def then_area_record_shows_no_value(data_steps: DataSteps, record_id: str) -> None:
    data_steps.then_area_record_shows_no_value(record_id)


@then(parsers.parse('home "{home_id}" has coverage "{coverage}"'))
def then_home_has_coverage(data_steps: DataSteps, home_id: str, coverage: str) -> None:
    data_steps.then_home_has_coverage(home_id, coverage)


@then(parsers.parse('area result "{postcode}" has topic "{topic_key}" with outcome "{outcome}"'))
def then_area_result_has_topic_with_outcome(
    data_steps: DataSteps, postcode: str, topic_key: str, outcome: str
) -> None:
    data_steps.then_area_result_has_topic_with_outcome(postcode, topic_key, outcome)


@then(
    parsers.parse('area result "{postcode}" leaves topic "{topic_key}" out of the coverage total')
)
def then_area_result_leaves_topic_out_of_coverage(
    data_steps: DataSteps, postcode: str, topic_key: str
) -> None:
    data_steps.then_area_result_leaves_topic_out_of_coverage(postcode, topic_key)


@then(parsers.parse('area result "{postcode}" asks the gap question for record "{record_id}"'))
def then_area_result_asks_gap_question(
    data_steps: DataSteps, postcode: str, record_id: str
) -> None:
    data_steps.then_area_result_asks_gap_question(postcode, record_id)


@then(
    parsers.parse('area result "{postcode}" has priority "{priority_id}" with outcome "{outcome}"')
)
def then_area_result_has_priority_with_outcome(
    data_steps: DataSteps, postcode: str, priority_id: str, outcome: str
) -> None:
    data_steps.then_area_result_has_priority_with_outcome(postcode, priority_id, outcome)


@then(
    parsers.parse(
        'area result "{postcode}" has priority "{priority_id}" with nearest record "{record_id}"'
    )
)
def then_area_result_has_priority_with_nearest_record(
    data_steps: DataSteps, postcode: str, priority_id: str, record_id: str
) -> None:
    data_steps.then_area_result_has_priority_with_nearest_record(postcode, priority_id, record_id)


@then(parsers.parse('area result "{postcode}" has a display distance for record "{record_id}"'))
def then_area_result_has_display_distance(
    data_steps: DataSteps, postcode: str, record_id: str
) -> None:
    data_steps.then_area_result_has_display_distance(postcode, record_id)


@then(
    parsers.parse(
        'area result "{postcode}" counts buses for stop "{stop_id}" '
        'on route "{route}" at hour {hour:d}'
    )
)
def then_area_result_counts_buses(
    data_steps: DataSteps, postcode: str, stop_id: str, route: str, hour: int
) -> None:
    data_steps.then_area_result_counts_buses(postcode, stop_id, route, hour)


@then(parsers.parse('postcode record "{record_id}" has status "{status}"'))
def then_postcode_record_has_status(data_steps: DataSteps, record_id: str, status: str) -> None:
    data_steps.then_postcode_record_has_status(record_id, status)


@then(parsers.parse('map layer "{layer_id}" has status "{status}"'))
def then_map_layer_has_status(data_steps: DataSteps, layer_id: str, status: str) -> None:
    data_steps.then_map_layer_has_status(layer_id, status)


@then(parsers.parse('topic "{topic_key}" draws map layer "{layer_kind}"'))
def then_topic_draws_map_layer(data_steps: DataSteps, topic_key: str, layer_kind: str) -> None:
    data_steps.then_topic_draws_map_layer(topic_key, layer_kind)


@then(parsers.parse('council "{code}" has field "{field}" with status "{status}"'))
def then_council_has_field_with_status(
    data_steps: DataSteps, code: str, field: str, status: str
) -> None:
    data_steps.then_council_has_field_with_status(code, field, status)


@then(parsers.parse('council "{code}" series "{series}" marks a method break'))
def then_council_series_marks_method_break(data_steps: DataSteps, code: str, series: str) -> None:
    data_steps.then_council_series_marks_method_break(code, series)


@then(parsers.parse('council "{code}" at band "{band:w}" has problem "{problem}"'))
def then_council_band_has_problem(
    data_steps: DataSteps, code: str, band: str, problem: str
) -> None:
    data_steps.then_council_band_has_problem(code, band, problem)


@then(parsers.parse('council "{code}" at band "{band:w}" has no rent side'))
def then_council_band_has_no_rent_side(data_steps: DataSteps, code: str, band: str) -> None:
    data_steps.then_council_band_has_no_rent_side(code, band)


@then(
    parsers.parse(
        'council "{code}" at band "{band:w}" for product "{product}" has problem "{problem}"'
    )
)
def then_council_product_has_problem(
    data_steps: DataSteps, code: str, band: str, product: str, problem: str
) -> None:
    data_steps.then_council_product_has_key(code, band, product, "problem", problem)


@then(
    parsers.parse(
        'council "{code}" at band "{band:w}" for product "{product}" has comparison "{comparison}"'
    )
)
def then_council_product_has_comparison(
    data_steps: DataSteps, code: str, band: str, product: str, comparison: str
) -> None:
    data_steps.then_council_product_has_key(code, band, product, "comparison", comparison)


@then(parsers.parse('council "{code}" caption "{topic}" has pattern "{pattern}"'))
def then_council_caption_has_pattern(
    data_steps: DataSteps, code: str, topic: str, pattern: str
) -> None:
    data_steps.then_council_caption_has_key(code, topic, "pattern", pattern)


@then(parsers.parse('council "{code}" caption "{topic}" has reason "{reason}"'))
def then_council_caption_has_reason(
    data_steps: DataSteps, code: str, topic: str, reason: str
) -> None:
    data_steps.then_council_caption_has_key(code, topic, "reason", reason)


@then(parsers.parse('council search "{query}" has kind "{kind}"'))
def then_council_search_has_kind(data_steps: DataSteps, query: str, kind: str) -> None:
    data_steps.then_council_search_has_kind(query, kind)


@then(parsers.parse('council search "{query}" lists council "{code:w}"'))
def then_council_search_lists_council(data_steps: DataSteps, query: str, code: str) -> None:
    data_steps.then_council_search_lists_council(query, code)


@then(parsers.parse('council search "{query}" lists council "{code}" with note "{note}"'))
def then_council_search_lists_council_with_note(
    data_steps: DataSteps, query: str, code: str, note: str
) -> None:
    data_steps.then_council_search_lists_council(query, code, note)


@then(
    parsers.parse('council "{code}" at band "{band:w}" for product "{product}" has no comparison')
)
def then_council_product_has_no_comparison(
    data_steps: DataSteps, code: str, band: str, product: str
) -> None:
    data_steps.then_council_product_has_no_comparison(code, band, product)


@then(
    parsers.parse(
        'council "{code}" neighbourhood "{neighbourhood}" has fact "{fact}" with status "{status}"'
    )
)
def then_council_neighbourhood_fact_has_status(
    data_steps: DataSteps, code: str, neighbourhood: str, fact: str, status: str
) -> None:
    data_steps.then_council_neighbourhood_fact_has_status(code, neighbourhood, fact, status)


@then(
    parsers.parse(
        'council "{code}" neighbourhood "{neighbourhood}" has fact "{fact}" at level "{level}"'
    )
)
def then_council_neighbourhood_fact_has_level(
    data_steps: DataSteps, code: str, neighbourhood: str, fact: str, level: str
) -> None:
    data_steps.then_council_neighbourhood_fact_has_level(code, neighbourhood, fact, level)


@then(parsers.parse('council "{code}" lists neighbourhood "{neighbourhood}" with label "{label}"'))
def then_council_lists_neighbourhood_with_label(
    data_steps: DataSteps, code: str, neighbourhood: str, label: str
) -> None:
    data_steps.then_council_lists_neighbourhood_with_label(code, neighbourhood, label)


@then(parsers.parse('council "{code}" neighbourhood "{neighbourhood}" has tenure shares'))
def then_council_neighbourhood_has_tenure_shares(
    data_steps: DataSteps, code: str, neighbourhood: str
) -> None:
    data_steps.then_council_neighbourhood_has_tenure_shares(code, neighbourhood)


@then(parsers.parse('council "{code}" has tenure shares'))
def then_council_has_tenure_shares(data_steps: DataSteps, code: str) -> None:
    data_steps.then_council_has_tenure_shares(code)


@then(parsers.parse('council "{code}" lists no neighbourhoods'))
def then_council_lists_no_neighbourhoods(data_steps: DataSteps, code: str) -> None:
    data_steps.then_council_lists_no_neighbourhoods(code)


@then(parsers.parse('topic "{topic_key}" is route-only and not counted'))
def then_topic_is_route_only(data_steps: DataSteps, topic_key: str) -> None:
    data_steps.then_topic_is_route_only(topic_key)


@then(parsers.parse('topic "{topic_key}" opens the Vestagraph page "{route}"'))
def then_topic_opens_vestagraph_page(data_steps: DataSteps, topic_key: str, route: str) -> None:
    data_steps.then_topic_opens_vestagraph_page(topic_key, route)


@then(parsers.parse('energy certificate "{number}" has outcome "{outcome}"'))
def then_energy_certificate_has_outcome(data_steps: DataSteps, number: str, outcome: str) -> None:
    data_steps.then_energy_certificate_has_outcome(number, outcome)


@then(parsers.parse('energy certificate "{number}" is more than 10 years old'))
def then_energy_certificate_is_old(data_steps: DataSteps, number: str) -> None:
    data_steps.then_energy_certificate_age(number, True)


@then(parsers.parse('energy certificate "{number}" is not more than 10 years old'))
def then_energy_certificate_is_not_old(data_steps: DataSteps, number: str) -> None:
    data_steps.then_energy_certificate_age(number, False)


@then(parsers.parse('energy certificate "{number}" has status line "{status}"'))
def then_energy_certificate_has_status_line(
    data_steps: DataSteps, number: str, status: str
) -> None:
    data_steps.then_energy_certificate_has_status_line(number, status)


@then(parsers.parse('energy certificate "{number}" shows "{field}" as missing'))
def then_energy_certificate_shows_missing(data_steps: DataSteps, number: str, field: str) -> None:
    data_steps.then_energy_certificate_shows_missing(number, field)


@then(parsers.parse('energy certificate "{number}" shows no ratings, costs, parts or improvements'))
def then_energy_certificate_shows_no_facts(data_steps: DataSteps, number: str) -> None:
    data_steps.then_energy_certificate_shows_no_facts(number)


@then(
    parsers.parse('energy certificate "{number}" lists improvements in its own order with no total')
)
def then_energy_certificate_improvements_in_order(data_steps: DataSteps, number: str) -> None:
    data_steps.then_energy_certificate_improvements_in_order_no_total(number)


@then(parsers.parse('energy certificate "{number}" has an inspection date'))
def then_energy_certificate_has_inspection_date(data_steps: DataSteps, number: str) -> None:
    data_steps.then_energy_certificate_has_inspection_date(number)


@then(parsers.parse('energy certificate "{number}" has a registration date'))
def then_energy_certificate_has_registration_date(data_steps: DataSteps, number: str) -> None:
    data_steps.then_energy_certificate_has_registration_date(number)


@then(parsers.parse('energy certificate "{number}" has a valid until date'))
def then_energy_certificate_has_valid_until(data_steps: DataSteps, number: str) -> None:
    data_steps.then_energy_certificate_has_valid_until(number, True)


@then(parsers.parse('energy certificate "{number}" has no valid until date'))
def then_energy_certificate_has_no_valid_until(data_steps: DataSteps, number: str) -> None:
    data_steps.then_energy_certificate_has_valid_until(number, False)
