"""``energy-certificate-result.json``: what the energy certificate page quotes (DA-09).

Expected dates come from the sample data and the hand-worked validity cases (registration date
plus ten years, regulation 9(2)(a) of the 2012 Regulations); nothing is copied from the output.
"""

import json
from pathlib import Path
from typing import Any

from generator_support import copy_data_to, fixtures_directory, read_json, write_json
from vestagraph_generator.energy_generator import generate_energy

MISSING = {"status": "missing", "text": "Not on this certificate"}


def _result(fixtures: Path | None = None) -> dict[str, dict[str, Any]]:
    text = generate_energy(fixtures or fixtures_directory())
    document = json.loads(text)
    return {c["number"]: c for c in document["certificates"]}


def _number(letter: str) -> str:
    return f"0000-0000-0000-0000-000{ord(letter) - ord('A') + 1}"


def test_generate_energy_sample_a_valid_until_2035_04_04() -> None:
    sample = _result()[_number("A")]

    assert sample["outcome"] == "shown"
    assert sample["validUntil"] == "2035-04-04"
    assert sample["moreThanTenYearsOld"] is False
    assert "statusLine" not in sample


def test_generate_energy_sample_a_inspection_date_2025_04_04() -> None:
    sample = _result()[_number("A")]

    assert sample["inspectionDate"] == "2025-04-04"


def test_generate_energy_sample_b_more_than_ten_years_old_true() -> None:
    sample = _result()[_number("B")]

    assert sample["validUntil"] == "2024-06-10"
    assert sample["moreThanTenYearsOld"] is True


def test_generate_energy_sample_h_leap_day_valid_until_28_february() -> None:
    assert _result()[_number("H")]["validUntil"] == "2026-02-28"


def test_generate_energy_superseded_and_cancelled_have_a_status_line() -> None:
    result = _result()

    assert result[_number("C")]["statusLine"]["status"] == "superseded"
    assert result[_number("D")]["statusLine"]["status"] == "cancelled"


def test_generate_energy_sample_g_missing_parts_not_on_this_certificate() -> None:
    sample = _result()[_number("G")]

    assert sample["outcome"] == "shown"
    assert sample["parts"] == MISSING
    assert sample["improvements"] == MISSING
    assert sample["propertyType"] == MISSING
    assert sample["builtForm"] == MISSING


def test_generate_energy_sample_e_outcome_not_domestic() -> None:
    sample = _result()[_number("E")]

    assert sample["outcome"] == "not-domestic"
    assert set(sample) == {"number", "outcome"}


def test_generate_energy_sample_f_outcome_not_yet_covered() -> None:
    sample = _result()[_number("F")]

    assert sample["outcome"] == "not-yet-covered"
    assert set(sample) == {"number", "outcome"}


def test_generate_energy_sample_a_facts_are_words_and_whole_pence() -> None:
    sample = _result()[_number("A")]

    assert sample["propertyType"] == "Flat"
    assert sample["builtForm"] == "Mid-Terrace"
    assert sample["currentRating"] == {"band": "E", "score": 50}
    assert sample["costs"]["heating"] == {"currentPence": 36598, "potentialPence": 25034}
    assert sample["improvements"][0]["description"] == "Low energy lighting for all fixed outlets"
    assert sample["improvements"][0]["typicalSavingPence"] == 13900


def test_generate_energy_unknown_improvement_code_not_on_this_certificate(
    tmp_path: Path,
) -> None:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "data" / "energy-certificates.json"
    document = read_json(path)
    document["certificates"][0]["improvements"]["value"][0]["improvementCode"] = 9999
    write_json(path, document)

    improvement = _result(fixtures)[_number("A")]["improvements"][0]

    assert improvement["description"] == MISSING
    assert "9999" not in json.dumps(improvement)


def _keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {k for v in value.values() for k in _keys(v)}
    if isinstance(value, list):
        return {k for v in value for k in _keys(v)}
    return set()


def test_generate_energy_output_has_no_address_field() -> None:
    document = json.loads(generate_energy(fixtures_directory()))

    for key in _keys(document):
        assert not key.lower().startswith("address")
        assert key.lower() not in {"postcode", "posttown"}
