"""The data steps, one by one.

The first seven were ported from DataStepsTests (issue #193); the area and coverage steps
were added for the screen specifications (#68).

Each failing case checks the message too: the message tells an author which ID to fix.
"""

import pytest
import specs_support as data
from specs_support import DataSteps, StoryPosition

_TOTAL = "B1.from-step-1.monthly.total"
_INSURANCE = "B1.from-step-1.monthly.buildings-insurance"
_SERVICE_CHARGE = "B1.from-step-1.monthly.service-charge"


@pytest.fixture
def position() -> StoryPosition:
    story = StoryPosition()
    story.set("B1", "from-step-1")
    return story


@pytest.fixture
def steps(position: StoryPosition) -> DataSteps:
    return DataSteps(position)


def test_then_figure_exists_unknown_figure_fails_naming_the_id(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_exists("B1.from-step-1.monthly.nope")

    assert "B1.from-step-1.monthly.nope" in str(failure.value)


def test_then_figure_exists_figure_from_another_step_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_exists("B1.from-step-3.monthly.total")

    assert 'figures here start with "B1.from-step-1."' in str(failure.value)


def test_then_figure_exists_known_figure_passes(steps: DataSteps) -> None:
    steps.then_figure_exists(_TOTAL)


def test_then_figure_exists_before_any_given_step_accepts_any_known_figure() -> None:
    DataSteps(StoryPosition()).then_figure_exists("B1.from-step-3.monthly.total")


def test_then_figure_exists_prefix_inside_but_not_at_the_start_of_the_id_fails(
    position: StoryPosition,
) -> None:
    position.set("B1", "from-step")

    with pytest.raises(AssertionError) as failure:
        DataSteps(position).then_figure_exists(_TOTAL)

    assert 'figures here start with "B1.from-step."' in str(failure.value)


def test_then_figure_exists_id_containing_the_prefix_later_fails(
    position: StoryPosition,
) -> None:
    position.set("1", "from-step-1")

    with pytest.raises(AssertionError):
        DataSteps(position).then_figure_exists(_TOTAL)


def test_then_figure_has_status_wrong_status_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_has_status(_INSURANCE, "calculated")

    assert _INSURANCE in str(failure.value)


def test_then_figure_has_status_part_of_the_real_status_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError):
        steps.then_figure_has_status(_INSURANCE, "miss")


def test_then_figure_has_status_correct_status_passes(steps: DataSteps) -> None:
    steps.then_figure_has_status(_INSURANCE, "missing")


def test_then_figure_has_status_total_fails_saying_it_is_a_total(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_has_status(_TOTAL, "calculated")

    assert "has no status (it is a total, not a line)" in str(failure.value)


def test_then_figure_shows_no_amount_line_with_pence_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_shows_no_amount(_SERVICE_CHARGE)

    assert "missing is never shown as zero" in str(failure.value)


def test_then_figure_shows_no_amount_line_without_amount_passes(steps: DataSteps) -> None:
    steps.then_figure_shows_no_amount(_INSURANCE)


def test_then_figure_shows_no_amount_line_with_zero_pence_fails(
    steps: DataSteps, monkeypatch: pytest.MonkeyPatch
) -> None:
    zero = {"id": _INSURANCE, "status": "calculated", "pence": 0}
    monkeypatch.setattr(data, "try_get_figure", lambda _figure_id: zero)

    with pytest.raises(AssertionError) as failure:
        steps.then_figure_shows_no_amount(_INSURANCE)

    assert "has an amount (pence)" in str(failure.value)


def test_then_figure_shows_no_amount_total_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_shows_no_amount(_TOTAL)

    assert "is not a cost line" in str(failure.value)


def test_then_figure_shows_no_amount_budget_with_budget_pence_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError):
        steps.then_figure_shows_no_amount("B1.from-step-1.monthly.budget")


def test_then_figure_cites_evidence_evidence_not_cited_by_figure_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_cites_evidence(_SERVICE_CHARGE, "B1-STAMP-DUTY")

    assert "does not cite evidence" in str(failure.value)


def test_then_figure_cites_evidence_unknown_evidence_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_cites_evidence(_SERVICE_CHARGE, "NO-SUCH-EVIDENCE")

    assert "NO-SUCH-EVIDENCE" in str(failure.value)
    assert "is not in packages/fixtures/data/evidence.json" in str(failure.value)


def test_then_figure_cites_evidence_cited_evidence_passes(steps: DataSteps) -> None:
    steps.then_figure_cites_evidence(_SERVICE_CHARGE, "B1-SC-LISTING")


def test_then_total_is_partial_with_reason_reason_not_listed_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_total_is_partial_with_reason(_TOTAL, "council-tax")

    assert 'not because of "council-tax"' in str(failure.value)


def test_then_total_is_partial_with_reason_partial_flag_not_true_fails(
    steps: DataSteps, monkeypatch: pytest.MonkeyPatch
) -> None:
    odd = {
        "id": _TOTAL,
        "isPartial": "yes",
        "partialReasons": [{"category": "buildings-insurance"}],
    }
    monkeypatch.setattr(data, "try_get_figure", lambda _figure_id: odd)

    with pytest.raises(AssertionError) as failure:
        steps.then_total_is_partial_with_reason(_TOTAL, "buildings-insurance")

    assert "is not partial" in str(failure.value)


def test_then_total_is_partial_with_reason_listed_reason_passes(steps: DataSteps) -> None:
    steps.then_total_is_partial_with_reason(_TOTAL, "buildings-insurance")


def test_then_total_is_partial_with_reason_total_not_partial_fails(position: StoryPosition) -> None:
    not_partial = next(
        figure_id
        for figure_id in sorted(data.figure_ids())
        if figure_id.endswith(".total")
        and (figure := data.try_get_figure(figure_id)) is not None
        and figure.get("isPartial") is False
    )
    home_id, scenario_id = not_partial.split(".")[:2]
    position.set(home_id, scenario_id)

    with pytest.raises(AssertionError) as failure:
        DataSteps(position).then_total_is_partial_with_reason(not_partial, "buildings-insurance")

    assert "is not partial" in str(failure.value)


def test_then_evidence_exists_known_evidence_passes(steps: DataSteps) -> None:
    steps.then_evidence_exists("B1-STAMP-DUTY")


def test_then_evidence_exists_unknown_evidence_fails_naming_the_id(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_evidence_exists("NO-SUCH-EVIDENCE")

    assert "NO-SUCH-EVIDENCE" in str(failure.value)


def test_given_home_is_at_story_step_step_inside_range_sets_the_scenario(
    position: StoryPosition, steps: DataSteps
) -> None:
    steps.given_home_is_at_story_step("B1", 2)

    assert position.scenario_id == "from-step-1"
    assert position.figure_prefix == "B1.from-step-1."


@pytest.mark.parametrize("step", [0, 5])
def test_given_home_is_at_story_step_step_out_of_range_fails(steps: DataSteps, step: int) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.given_home_is_at_story_step("B1", step)

    assert f"at story step {step}" in str(failure.value)


def test_given_home_is_at_story_step_unknown_home_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.given_home_is_at_story_step("NOPE", 1)

    assert '"NOPE"' in str(failure.value)
    assert "packages/fixtures/data/homes.json" in str(failure.value)


def test_story_position_before_any_given_step_has_no_prefix() -> None:
    assert StoryPosition().figure_prefix is None


def test_then_area_record_has_status_unknown_record_fails_naming_the_id(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_record_has_status("B1-AREA-NOPE", "recorded")

    assert "B1-AREA-NOPE" in str(failure.value)
    assert "area.json" in str(failure.value)


def test_then_area_record_has_status_wrong_status_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_record_has_status("R1-AREA-CRIME-2", "recorded")

    assert "source-failed" in str(failure.value)


def test_then_area_record_has_status_correct_status_passes(steps: DataSteps) -> None:
    steps.then_area_record_has_status("R1-AREA-CRIME-2", "source-failed")


def test_then_area_record_shows_no_value_record_with_value_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_record_shows_no_value("B1-AREA-SCHOOL-INSPECTION-1")

    assert "B1-AREA-SCHOOL-INSPECTION-1" in str(failure.value)


def test_then_area_record_shows_no_value_record_without_value_passes(steps: DataSteps) -> None:
    steps.then_area_record_shows_no_value("WALES-1-AREA-FLOOD-1")


def test_then_area_record_shows_no_value_unknown_record_fails_naming_the_id(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_record_shows_no_value("B1-AREA-NOPE")

    assert "B1-AREA-NOPE" in str(failure.value)


def test_then_home_has_coverage_wrong_coverage_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_home_has_coverage("WALES-1", "covered")

    assert "not-yet-covered" in str(failure.value)


def test_then_home_has_coverage_correct_coverage_passes(steps: DataSteps) -> None:
    steps.then_home_has_coverage("WALES-1", "not-yet-covered")


def test_then_home_has_coverage_unknown_home_fails_naming_the_id(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_home_has_coverage("ZZ-9", "covered")

    assert "ZZ-9" in str(failure.value)


# The area result steps (first design batch specifications). The cases use the synthetic
# postcode NB1 4XY; a passing case and a failing case per wording.

_PC = "NB1 4XY"


def test_then_area_result_topic_outcome_matching_outcome_passes(steps: DataSteps) -> None:
    steps.then_area_result_has_topic_with_outcome(_PC, "schools", "found")


def test_then_area_result_topic_outcome_wrong_outcome_fails_naming_the_topic(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_has_topic_with_outcome(_PC, "schools", "not-known")

    assert "schools" in str(failure.value)
    assert _PC in str(failure.value)


def test_then_area_result_topic_outcome_topic_left_out_fails_naming_the_topic(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_has_topic_with_outcome(_PC, "noise", "found")

    assert "noise" in str(failure.value)


def test_then_area_result_topic_outcome_unknown_postcode_fails_naming_it(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_has_topic_with_outcome("ZZ9 9ZZ", "schools", "found")

    assert "ZZ9 9ZZ" in str(failure.value)


def test_then_area_result_topic_left_out_of_coverage_uncounted_topic_passes(
    steps: DataSteps,
) -> None:
    steps.then_area_result_leaves_topic_out_of_coverage(_PC, "noise")


def test_then_area_result_topic_left_out_of_coverage_counted_topic_fails(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_leaves_topic_out_of_coverage(_PC, "schools")

    assert "schools" in str(failure.value)


def test_then_area_result_topic_left_out_of_coverage_not_covered_topic_passes(
    steps: DataSteps,
) -> None:
    steps.then_area_result_leaves_topic_out_of_coverage("NB7 1RR", "green-space")


def test_then_area_result_topic_left_out_of_coverage_unknown_key_fails_naming_the_key(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_leaves_topic_out_of_coverage(_PC, "nosie")

    assert "nosie" in str(failure.value)


def test_then_area_result_gap_question_known_record_passes(steps: DataSteps) -> None:
    steps.then_area_result_asks_gap_question(_PC, "NB1-4XY-AREA-AMENITY-6")


def test_then_area_result_gap_question_record_without_question_fails_naming_the_id(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_asks_gap_question(_PC, "NB1-4XY-AREA-AMENITY-1")

    assert "NB1-4XY-AREA-AMENITY-1" in str(failure.value)


def test_then_area_result_priority_outcome_matching_outcome_passes(steps: DataSteps) -> None:
    steps.then_area_result_has_priority_with_outcome(_PC, "SAMPLE-PRIORITY-CHILDCARE", "not-known")


def test_then_area_result_priority_outcome_wrong_outcome_fails_naming_the_id(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_has_priority_with_outcome(_PC, "SAMPLE-PRIORITY-CHILDCARE", "misses")

    assert "SAMPLE-PRIORITY-CHILDCARE" in str(failure.value)


def test_then_area_result_priority_outcome_unknown_priority_fails_naming_the_id(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_has_priority_with_outcome(_PC, "SAMPLE-PRIORITY-NOPE", "meets")

    assert "SAMPLE-PRIORITY-NOPE" in str(failure.value)


def test_then_area_result_priority_nearest_matching_record_passes(steps: DataSteps) -> None:
    steps.then_area_result_has_priority_with_nearest_record(
        _PC, "SAMPLE-PRIORITY-GP", "NB1-4XY-AREA-AMENITY-10"
    )


def test_then_area_result_priority_nearest_wrong_record_fails_naming_both_ids(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_has_priority_with_nearest_record(
            _PC, "SAMPLE-PRIORITY-GP", "NB1-4XY-AREA-AMENITY-1"
        )

    assert "SAMPLE-PRIORITY-GP" in str(failure.value)
    assert "NB1-4XY-AREA-AMENITY-1" in str(failure.value)


def test_then_area_result_display_distance_known_record_passes(steps: DataSteps) -> None:
    steps.then_area_result_has_display_distance(_PC, "NB1-4XY-AREA-SCHOOL-1")


def test_then_area_result_display_distance_missing_record_fails_naming_the_id(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_has_display_distance(_PC, "NB1-4XY-AREA-NOPE")

    assert "NB1-4XY-AREA-NOPE" in str(failure.value)


def test_then_area_result_buses_known_stop_route_and_hour_passes(steps: DataSteps) -> None:
    steps.then_area_result_counts_buses(_PC, "NB1-4XY-AREA-TRANSPORT-STOP-1", "12", 8)


def test_then_area_result_buses_unknown_route_fails_naming_stop_and_route(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_area_result_counts_buses(_PC, "NB1-4XY-AREA-TRANSPORT-STOP-1", "999", 8)

    assert "NB1-4XY-AREA-TRANSPORT-STOP-1" in str(failure.value)
    assert "999" in str(failure.value)


def test_then_postcode_record_status_matching_status_passes(steps: DataSteps) -> None:
    steps.then_postcode_record_has_status("NB1-4XY-AREA-SCHOOL-INSPECTION-1", "stale")


def test_then_postcode_record_status_wrong_status_fails_naming_the_id(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_postcode_record_has_status("NB1-4XY-AREA-SCHOOL-INSPECTION-1", "recorded")

    assert "NB1-4XY-AREA-SCHOOL-INSPECTION-1" in str(failure.value)


def test_then_postcode_record_status_unknown_record_fails_naming_the_id(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_postcode_record_has_status("NB1-4XY-NOPE", "stale")

    assert "NB1-4XY-NOPE" in str(failure.value)


def test_then_map_layer_has_status_matching_status_passes(steps: DataSteps) -> None:
    steps.then_map_layer_has_status("NB1-4XY-LAYER-FLOOD-ZONES-1", "recorded")


def test_then_map_layer_has_status_wrong_status_fails_naming_the_id(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_map_layer_has_status("NB1-4XY-LAYER-FLOOD-ZONES-1", "not-covered")

    assert "NB1-4XY-LAYER-FLOOD-ZONES-1" in str(failure.value)


def test_then_map_layer_has_status_unknown_layer_fails_naming_the_id(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_map_layer_has_status("NB1-4XY-LAYER-NOPE-1", "recorded")

    assert "NB1-4XY-LAYER-NOPE-1" in str(failure.value)


def test_then_topic_draws_map_layer_listed_layer_passes(steps: DataSteps) -> None:
    steps.then_topic_draws_map_layer("noise", "road-noise")


def test_then_topic_draws_map_layer_layer_of_another_topic_fails_naming_both(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_topic_draws_map_layer("noise", "flood-zones")

    assert "noise" in str(failure.value)
    assert "flood-zones" in str(failure.value)


def test_then_topic_draws_map_layer_unknown_topic_fails_naming_the_key(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_topic_draws_map_layer("no-such-topic", "road-noise")

    assert "no-such-topic" in str(failure.value)


# City Explorer council steps (plan Task 14a): a passing and a failing case per wording, against
# the committed council-area.json and council-result.json.
_NORTH = "E06999001"
_EAST = "E07999001"
_WEST = "E07999002"


def test_then_council_field_status_matching_status_passes(steps: DataSteps) -> None:
    steps.then_council_has_field_with_status(_EAST, "rentSeries", "no-record-in-source")


def test_then_council_field_status_wrong_status_fails_naming_code_and_field(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_has_field_with_status(_EAST, "rentSeries", "recorded")

    assert _EAST in str(failure.value)
    assert "rentSeries" in str(failure.value)


def test_then_council_field_status_unknown_council_fails_naming_the_code(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_has_field_with_status("E06000000", "bands", "recorded")

    assert "E06000000" in str(failure.value)


def test_then_council_field_status_unknown_field_fails_naming_the_field(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_has_field_with_status(_NORTH, "nope", "recorded")

    assert "nope" in str(failure.value)


def test_then_council_series_method_break_marked_passes(steps: DataSteps) -> None:
    steps.then_council_series_marks_method_break(_EAST, "affordabilitySeries")


def test_then_council_series_method_break_unmarked_fails_naming_the_series(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_series_marks_method_break(_NORTH, "affordabilitySeries")

    assert "affordabilitySeries" in str(failure.value)


def test_then_council_band_problem_matching_problem_passes(steps: DataSteps) -> None:
    steps.then_council_band_has_problem(_WEST, "D", "council-tax-missing")


def test_then_council_band_problem_band_without_problem_fails_naming_the_band(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_band_has_problem(_NORTH, "D", "council-tax-missing")

    assert 'band "D"' in str(failure.value)


def test_then_council_band_problem_unknown_band_fails_naming_the_band(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_band_has_problem(_NORTH, "Z", "council-tax-missing")

    assert '"Z"' in str(failure.value)


def test_then_council_band_no_rent_side_missing_rent_passes(steps: DataSteps) -> None:
    steps.then_council_band_has_no_rent_side(_EAST, "D")


def test_then_council_band_no_rent_side_council_with_rent_fails_naming_the_council(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_band_has_no_rent_side(_NORTH, "D")

    assert _NORTH in str(failure.value)


def test_then_council_product_key_matching_problem_passes(steps: DataSteps) -> None:
    steps.then_council_product_has_key(
        _NORTH, "D", "5-year-fixed", "problem", "rate-band-unavailable"
    )


def test_then_council_product_key_matching_comparison_passes(steps: DataSteps) -> None:
    steps.then_council_product_has_key(_NORTH, "D", "2-year-fixed", "comparison", "more")


def test_then_council_product_key_wrong_value_fails_naming_the_product(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_product_has_key(_NORTH, "D", "2-year-fixed", "comparison", "less")

    assert "2-year-fixed" in str(failure.value)


def test_then_council_product_key_unknown_product_fails_naming_the_product(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_product_has_key(_NORTH, "D", "10-year-fixed", "problem", "x")

    assert "10-year-fixed" in str(failure.value)


def test_then_council_caption_pattern_matching_pattern_passes(steps: DataSteps) -> None:
    steps.then_council_caption_has_key(_NORTH, "rent", "pattern", "trend-rose")


def test_then_council_caption_pattern_of_a_property_type_passes(steps: DataSteps) -> None:
    steps.then_council_caption_has_key(_NORTH, "price:terraced", "pattern", "trend-fell")


def test_then_council_caption_reason_matching_reason_passes(steps: DataSteps) -> None:
    steps.then_council_caption_has_key(_EAST, "price:flat", "reason", "no-record-in-source")


def test_then_council_caption_wrong_pattern_fails_naming_the_topic(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_caption_has_key(_NORTH, "rent", "pattern", "trend-fell")

    assert '"rent"' in str(failure.value)


def test_then_council_caption_unknown_topic_fails_naming_the_topic(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_caption_has_key(_NORTH, "nope", "pattern", "x")

    assert "nope" in str(failure.value)


def test_then_council_caption_unknown_council_fails_naming_the_code(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_caption_has_key("E06000000", "rent", "pattern", "x")

    assert "E06000000" in str(failure.value)


def test_then_council_search_kind_matching_kind_passes(steps: DataSteps) -> None:
    steps.then_council_search_has_kind("Capital (synthetic)", "choose")


def test_then_council_search_kind_wrong_kind_fails_naming_the_query(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_search_has_kind("Capital (synthetic)", "council")

    assert "Capital (synthetic)" in str(failure.value)


def test_then_council_search_kind_unknown_query_fails_naming_the_query(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_search_has_kind("Midvale", "not-found")

    assert "Midvale" in str(failure.value)


def test_then_council_search_lists_council_listed_council_passes(steps: DataSteps) -> None:
    steps.then_council_search_lists_council("Capital (synthetic)", _NORTH)


def test_then_council_search_lists_council_note_matching_passes(steps: DataSteps) -> None:
    steps.then_council_search_lists_council(
        "East Westshire Borough (synthetic)", _EAST, "former-name"
    )


def test_then_council_search_lists_council_unlisted_council_fails_naming_the_code(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_search_lists_council("Capital (synthetic)", _EAST)

    assert _EAST in str(failure.value)


def test_then_council_search_lists_council_wrong_note_fails_naming_the_note(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_search_lists_council("Eastmere (synthetic)", _EAST, "former-name")

    assert "former-name" in str(failure.value)


def test_then_council_product_no_comparison_one_side_missing_passes(steps: DataSteps) -> None:
    steps.then_council_product_has_no_comparison(_EAST, "D", "2-year-fixed")


def test_then_council_product_no_comparison_with_a_comparison_fails_naming_the_council(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_product_has_no_comparison(_NORTH, "D", "2-year-fixed")

    assert _NORTH in str(failure.value)


_NORTH_CENTRE = "E01999011"
_EAST_GREEN = "E01999031"


def test_then_council_neighbourhood_fact_status_matching_status_passes(steps: DataSteps) -> None:
    steps.then_council_neighbourhood_fact_has_status(
        _EAST, _EAST_GREEN, "deprivation", "no-record-in-source"
    )


def test_then_council_neighbourhood_fact_status_wrong_status_fails_naming_the_fact(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_neighbourhood_fact_has_status(
            _EAST, _EAST_GREEN, "deprivation", "recorded"
        )

    assert '"deprivation"' in str(failure.value)


def test_then_council_neighbourhood_fact_status_unknown_neighbourhood_fails_naming_it(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_neighbourhood_fact_has_status(_NORTH, "E01000000", "tenure", "recorded")

    assert "E01000000" in str(failure.value)


def test_then_council_neighbourhood_fact_status_unknown_fact_fails_naming_the_fact(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_neighbourhood_fact_has_status(_NORTH, _NORTH_CENTRE, "nope", "recorded")

    assert "nope" in str(failure.value)


def test_then_council_neighbourhood_fact_level_matching_level_passes(steps: DataSteps) -> None:
    steps.then_council_neighbourhood_fact_has_level(
        _NORTH, _NORTH_CENTRE, "connectivity", "neighbourhood"
    )


def test_then_council_neighbourhood_fact_level_wrong_level_fails_naming_the_level(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_neighbourhood_fact_has_level(
            _NORTH, _NORTH_CENTRE, "connectivity", "local-authority"
        )

    assert "local-authority" in str(failure.value)


def test_then_council_lists_neighbourhood_label_matching_label_passes(steps: DataSteps) -> None:
    steps.then_council_lists_neighbourhood_with_label(
        _NORTH, _NORTH_CENTRE, "Northbridge Centre (synthetic) (011A)"
    )


def test_then_council_lists_neighbourhood_label_wrong_label_fails_naming_the_label(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_lists_neighbourhood_with_label(_NORTH, _NORTH_CENTRE, "Millbrook")

    assert "Millbrook" in str(failure.value)


def test_then_council_lists_neighbourhood_label_unlisted_neighbourhood_fails_naming_it(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_lists_neighbourhood_with_label(_NORTH, _EAST_GREEN, "x")

    assert _EAST_GREEN in str(failure.value)


def test_then_council_neighbourhood_tenure_shares_present_passes(steps: DataSteps) -> None:
    steps.then_council_neighbourhood_has_tenure_shares(_NORTH, _NORTH_CENTRE)


def test_then_council_neighbourhood_tenure_shares_unlisted_neighbourhood_fails_naming_it(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_neighbourhood_has_tenure_shares(_NORTH, _EAST_GREEN)

    assert _EAST_GREEN in str(failure.value)


def test_then_council_lists_no_neighbourhoods_empty_list_passes(steps: DataSteps) -> None:
    steps.then_council_lists_no_neighbourhoods("E07999002")


def test_then_council_lists_no_neighbourhoods_council_with_some_fails_naming_the_council(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_council_lists_no_neighbourhoods(_NORTH)

    assert _NORTH in str(failure.value)


def test_then_council_neighbourhood_tenure_shares_empty_shares_fails_naming_the_neighbourhood(
    steps: DataSteps, monkeypatch: pytest.MonkeyPatch
) -> None:
    import specs_support

    council = specs_support._load().council_results[_NORTH]
    entry = council["neighbourhoods"][0]
    monkeypatch.setitem(entry, "tenureShares", None)

    with pytest.raises(AssertionError) as failure:
        steps.then_council_neighbourhood_has_tenure_shares(_NORTH, _NORTH_CENTRE)

    assert _NORTH_CENTRE in str(failure.value)


# Malformed generated data: a descriptive failure naming the council and the key, never a
# KeyError or AttributeError (security review of PR C, P3).
def test_then_council_caption_without_values_fails_naming_council_and_key(
    steps: DataSteps, monkeypatch: pytest.MonkeyPatch
) -> None:
    broken = type("Loaded", (), {"council_results": {"X1": {"captions": [{"topic": "rent"}]}}})
    monkeypatch.setattr(data, "_load", lambda: broken)

    with pytest.raises(AssertionError) as failure:
        steps.then_council_caption_has_key("X1", "rent", "pattern", "trend-rose")

    assert 'Council "X1"' in str(failure.value)
    assert '"values"' in str(failure.value)


def test_then_council_neighbourhood_fact_with_null_level_fails_naming_the_fact(
    steps: DataSteps, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(data, "_require_neighbourhood_fact", lambda *_args: {"level": None})

    with pytest.raises(AssertionError) as failure:
        steps.then_council_neighbourhood_fact_has_level("X1", "LSOA1", "tenure", "neighbourhood")

    assert 'neighbourhood "LSOA1"' in str(failure.value)
    assert '"level"' in str(failure.value)


def test_find_entry_without_the_key_fails_naming_the_key_and_where() -> None:
    with pytest.raises(AssertionError) as failure:
        data._find([{"other": 1}], "topic", "rent", 'council "X1" captions')

    assert '"topic"' in str(failure.value)
    assert 'council "X1" captions' in str(failure.value)


# Energy certificate steps (plan Task 4): a passing and a failing case per wording.
_EPC_A = "0000-0000-0000-0000-0001"
_EPC_B = "0000-0000-0000-0000-0002"
_EPC_C = "0000-0000-0000-0000-0003"
_EPC_E = "0000-0000-0000-0000-0005"
_EPC_G = "0000-0000-0000-0000-0007"


def test_then_topic_route_only_energy_row_passes(steps: DataSteps) -> None:
    steps.then_topic_is_route_only("energy-certificate-home")
    steps.then_topic_opens_vestagraph_page("energy-certificate-home", "/energy-certificate")


def test_then_topic_route_only_counted_topic_fails_naming_the_topic(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_topic_is_route_only("flood")

    assert "flood" in str(failure.value)


def test_then_topic_opens_vestagraph_page_wrong_route_fails_naming_the_route(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_topic_opens_vestagraph_page("energy-certificate-home", "/elsewhere")

    assert "/elsewhere" in str(failure.value)


def test_then_energy_certificate_outcome_age_and_status_matching_passes(steps: DataSteps) -> None:
    steps.then_energy_certificate_has_outcome(_EPC_A, "shown")
    steps.then_energy_certificate_age(_EPC_A, more_than_ten_years=False)
    steps.then_energy_certificate_age(_EPC_B, more_than_ten_years=True)
    steps.then_energy_certificate_has_status_line(_EPC_C, "superseded")
    steps.then_energy_certificate_has_status_line(_EPC_A, "none")


def test_then_energy_certificate_wrong_outcome_fails_naming_the_number(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_energy_certificate_has_outcome(_EPC_A, "not-domestic")

    assert _EPC_A in str(failure.value)


def test_then_energy_certificate_unknown_number_fails_naming_the_number(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_energy_certificate_has_outcome("0000-0000-0000-0000-9999", "shown")

    assert "0000-0000-0000-0000-9999" in str(failure.value)


def test_then_energy_certificate_wrong_age_fails_naming_the_number(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_energy_certificate_age(_EPC_A, more_than_ten_years=True)

    assert _EPC_A in str(failure.value)


def test_then_energy_certificate_missing_fact_marked_missing_passes(steps: DataSteps) -> None:
    steps.then_energy_certificate_shows_missing(_EPC_G, "parts")


def test_then_energy_certificate_recorded_fact_not_missing_fails_naming_the_field(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_energy_certificate_shows_missing(_EPC_A, "parts")

    assert "parts" in str(failure.value)


def test_then_energy_certificate_not_shown_has_no_facts_passes_and_shown_fails(
    steps: DataSteps,
) -> None:
    steps.then_energy_certificate_shows_no_facts(_EPC_E)
    with pytest.raises(AssertionError):
        steps.then_energy_certificate_shows_no_facts(_EPC_A)


def test_then_energy_certificate_improvements_in_order_passes_and_missing_list_fails(
    steps: DataSteps,
) -> None:
    steps.then_energy_certificate_improvements_in_order_no_total(_EPC_A)
    with pytest.raises(AssertionError) as failure:
        steps.then_energy_certificate_improvements_in_order_no_total(_EPC_G)

    assert _EPC_G in str(failure.value)


def test_then_energy_certificate_inspection_date_shown_sample_passes(steps: DataSteps) -> None:
    steps.then_energy_certificate_has_inspection_date(_EPC_A)


def test_then_energy_certificate_inspection_date_not_shown_sample_fails_naming_the_number(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_energy_certificate_has_inspection_date(_EPC_E)

    assert _EPC_E in str(failure.value)


def test_then_report_counts_sample_file_passes_every_shape_check(steps: DataSteps) -> None:
    steps.then_report_counts_keep_days(90)
    steps.then_report_counts_hold_fact_count("flood", "SYNTHETIC-FLOOD-1", "out-of-date")
    steps.then_report_counts_hold_area_count("sold-nearby", "wrong")
    steps.then_report_counts_hold_area_count("planning-nearby", "missing-something")
    steps.then_report_counts_hold_figure_count("council-tax-band-d", "council", "E06999001")
    steps.then_report_counts_hold_figure_count(
        "average-price-for-flats", "neighbourhood", "E01999011"
    )
    steps.then_report_counts_have_no_field("postcode")
    steps.then_report_counts_dates_are_days()
    steps.then_report_counts_reasons_are_fixed()


def test_then_report_counts_missing_count_fails_naming_the_topic(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_report_counts_hold_fact_count("flood", "SYNTHETIC-FLOOD-1", "wrong")
    assert "flood" in str(failure.value)
    with pytest.raises(AssertionError):
        steps.then_report_counts_hold_area_count("flood", "out-of-date")
    with pytest.raises(AssertionError):
        steps.then_report_counts_keep_days(365)


def test_then_report_counts_field_present_in_a_count_fails_naming_the_field(
    steps: DataSteps,
) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_report_counts_have_no_field("topic")

    assert '"topic"' in str(failure.value)
