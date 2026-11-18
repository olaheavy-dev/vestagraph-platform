"""Energy certificate samples and code tables (DA-09, plan task 1).

``reference/`` holds real official data (code-to-words tables); ``validate_fixtures`` checks each
``reference/NAME.json`` against ``schema/NAME.schema.json``. The sample certificates in
``data/energy-certificates.json`` are synthetic and never carry an address (design 2026-11-18).
"""

import copy
import json
from pathlib import Path

import pytest
from fixtures_support import (
    Json,
    copy_fixture_folders,
    fixtures_directory,
    load,
    mentions,
    read_file,
    schema_directory,
)
from vestagraph_fixture_validator.validator import (
    FixtureProblem,
    validate_fixtures,
    validate_instance,
)


def _certificate_problems(document: Json) -> list[FixtureProblem]:
    return validate_instance(document, "energy-certificates.schema.json", schema_directory())


def _sample_a() -> Json:
    return copy.deepcopy(load("energy-certificates")["certificates"][0])


def _wrap(certificate: Json) -> Json:
    document = copy.deepcopy(load("energy-certificates"))
    document["certificates"] = [certificate]
    return document


def _tables() -> Json:
    return read_file(fixtures_directory() / "reference" / "energy-code-tables.json")


def test_validate_fixtures_reference_table_valid_passes() -> None:
    assert validate_fixtures(fixtures_directory()) == []


def test_validate_fixtures_reference_table_wrong_shape_fails(tmp_path: Path) -> None:
    root = copy_fixture_folders(tmp_path / "fixtures", ("data", "schema", "reference"))
    table_file = root / "reference" / "energy-code-tables.json"
    broken = json.loads(table_file.read_text(encoding="utf-8"))
    broken["tables"]["propertyType"]["2"] = ""
    table_file.write_text(json.dumps(broken), encoding="utf-8")
    problems = validate_fixtures(root)
    assert mentions(problems, "energy-code-tables.json")


def test_validate_fixtures_certificate_with_postcode_fails() -> None:
    certificate = _sample_a()
    certificate["postcode"] = "NB1 4XY"
    problems = _certificate_problems(_wrap(certificate))
    assert len(problems) == 1
    assert mentions(problems, "postcode")


def test_validate_fixtures_certificate_with_address_line_fails() -> None:
    certificate = _sample_a()
    certificate["addressLine1"] = "1 Example Street"
    assert mentions(_certificate_problems(_wrap(certificate)), "addressLine1")


def test_validate_fixtures_fact_zero_cost_fails() -> None:
    certificate = _sample_a()
    certificate["costs"]["value"]["heating"]["current"]["pence"] = 0
    assert mentions(_certificate_problems(_wrap(certificate)), "pence")


def test_validate_fixtures_fact_blank_instead_of_missing_fails() -> None:
    certificate = _sample_a()
    certificate["totalFloorAreaSquareMetres"] = {}
    assert _certificate_problems(_wrap(certificate)) != []


def test_validate_fixtures_certificate_number_not_synthetic_fails() -> None:
    certificate = _sample_a()
    certificate["number"] = "1234-5678-1234-5678-1234"
    assert mentions(_certificate_problems(_wrap(certificate)), "number")


def test_validate_fixtures_samples_real_file_covers_every_state() -> None:
    certificates = load("energy-certificates")["certificates"]
    assert [c["number"] for c in certificates] == [
        f"0000-0000-0000-0000-000{n}" for n in range(1, 9)
    ]
    by_letter = dict(zip("ABCDEFGH", certificates, strict=True))
    assert by_letter["C"]["status"] == "superseded"
    assert by_letter["D"]["status"] == "cancelled"
    assert by_letter["E"]["kind"] == "non-domestic"
    assert by_letter["F"]["country"] == "wales"
    assert by_letter["G"]["parts"] == {"status": "missing"}
    assert by_letter["G"]["improvements"] == {"status": "missing"}
    assert by_letter["H"]["registrationDate"] == "2016-02-29"
    assert by_letter["B"]["registrationDate"] == by_letter["B"]["inspectionDate"]
    assert by_letter["H"]["inspectionDate"] == "2016-02-29"
    assert by_letter["A"]["schema"] == "RdSAP-Schema-21.0.1"


@pytest.mark.parametrize(
    ("fact", "table"),
    [("propertyTypeCode", "propertyType"), ("builtFormCode", "builtForm")],
)
def test_validate_fixtures_samples_code_facts_are_in_the_tables(fact: str, table: str) -> None:
    words = _tables()["tables"][table]
    for certificate in load("energy-certificates")["certificates"]:
        if "value" in certificate[fact]:
            assert certificate[fact]["value"] in words


def test_validate_fixtures_samples_improvement_codes_are_in_the_table() -> None:
    words = _tables()["tables"]["improvement"]
    for certificate in load("energy-certificates")["certificates"]:
        if "value" in certificate["improvements"]:
            for improvement in certificate["improvements"]["value"]:
                assert str(improvement["improvementCode"]) in words
