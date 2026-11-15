"""The council-result schema must pair each shown figure with its pence amount and pin the
property-type captions. Each test starts from the real generated file and breaks one thing."""

import copy
import json
from typing import Any

import pytest
from fixtures_support import fixtures_directory, schema_directory
from vestagraph_fixture_validator.validator import validate_instance

_SCHEMA = "generated-council-result.schema.json"


def _document() -> dict[str, Any]:
    text = (fixtures_directory() / "generated" / "council-result.json").read_text(encoding="utf-8")
    parsed: dict[str, Any] = json.loads(text)
    return parsed


def _problems(document: dict[str, Any]) -> list[str]:
    found = validate_instance(document, _SCHEMA, schema_directory())
    return [problem.message for problem in found]


def _band(document: dict[str, Any]) -> dict[str, Any]:
    found: dict[str, Any] = document["councils"][0]["rentOrBuy"]["byBand"][0]
    return found


def _side(document: dict[str, Any]) -> dict[str, Any]:
    found: dict[str, Any] = next(
        s
        for b in document["councils"][0]["rentOrBuy"]["byBand"]
        for s in b["buySides"]
        if "repayment" in s
    )
    return found


def test_validate_instance_real_council_result_is_accepted() -> None:
    assert _problems(_document()) == []


def test_validate_instance_shown_council_tax_without_council_tax_is_refused() -> None:
    document = _document()
    del _band(document)["councilTax"]

    assert _problems(document) != []


def test_validate_instance_council_tax_without_shown_council_tax_is_refused() -> None:
    document = _document()
    del _band(document)["shownCouncilTax"]

    assert _problems(document) != []


def test_validate_instance_shown_repayment_without_repayment_is_refused() -> None:
    document = _document()
    del _side(document)["repayment"]

    assert _problems(document) != []


def test_validate_instance_repayment_without_shown_repayment_is_refused() -> None:
    document = _document()
    del _side(document)["shownRepayment"]

    assert _problems(document) != []


def test_validate_instance_shown_rent_side_without_rent_side_is_refused() -> None:
    document = _document()
    del _band(document)["rentSide"]

    assert _problems(document) != []


def test_validate_instance_price_by_type_in_the_wrong_order_is_refused() -> None:
    document = _document()
    items = document["councils"][0]["priceByType"]
    items[0], items[1] = items[1], items[0]

    assert _problems(document) != []


def test_validate_instance_price_by_type_repeating_a_type_is_refused() -> None:
    document = _document()
    items = document["councils"][0]["priceByType"]
    items[1] = copy.deepcopy(items[0])

    assert _problems(document) != []


def test_validate_instance_price_by_type_values_naming_another_type_is_refused() -> None:
    document = _document()
    document["councils"][0]["priceByType"][0]["values"]["propertyType"] = "flat"

    assert _problems(document) != []


@pytest.mark.parametrize("count", [3, 5])
def test_validate_instance_price_by_type_with_the_wrong_number_of_items_is_refused(
    count: int,
) -> None:
    document = _document()
    items = document["councils"][0]["priceByType"]
    document["councils"][0]["priceByType"] = (items * 2)[:count]

    assert _problems(document) != []
