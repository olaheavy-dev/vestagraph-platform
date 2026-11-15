"""council-result.json: whole-pound siblings for every pence amount a board shows, and the
per-property-type price captions, proved by hand-worked cases."""

import json
from typing import Any

import pytest
from generator_support import fixtures_directory, read_json
from vestagraph_generator.council_generator import generate_council

CASES: list[dict[str, Any]] = read_json(
    fixtures_directory() / "test-cases" / "council-shown-pounds.json"
)["cases"]
BAND_CASES = [
    c for c in CASES if "councilCode" in c["inputs"] and c["expected"]["shownYearly"] is not None
]
TYPE_CASES: list[dict[str, Any]] = [
    c
    for c in read_json(fixtures_directory() / "test-cases" / "council-property-types.json")["cases"]
    if "councilCode" in c["inputs"]
]
TYPES = ("detached", "semiDetached", "terraced", "flat")


def _document() -> dict[str, Any]:
    parsed: dict[str, Any] = json.loads(generate_council(fixtures_directory()))
    return parsed


def _council(code: str) -> dict[str, Any]:
    found: dict[str, Any] = next(c for c in _document()["councils"] if c["code"] == code)
    return found


def _by_band(council: dict[str, Any], band: str) -> dict[str, Any]:
    found: dict[str, Any] = next(b for b in council["rentOrBuy"]["byBand"] if b["band"] == band)
    return found


@pytest.mark.parametrize("case", BAND_CASES, ids=[c["id"] for c in BAND_CASES])
def test_generate_council_band_list_has_shown_yearly_and_monthly_council_tax(
    case: dict[str, Any],
) -> None:
    council = _council(case["inputs"]["councilCode"])
    band = next(b for b in council["bands"] if b["band"] == case["inputs"]["band"])

    assert band["shownYearly"] == case["expected"]["shownYearly"]
    assert band["shownCouncilTax"] == case["expected"]["shownCouncilTax"]


@pytest.mark.parametrize("case", BAND_CASES, ids=[c["id"] for c in BAND_CASES])
def test_generate_council_rent_or_buy_band_has_shown_council_tax_beside_its_pence(
    case: dict[str, Any],
) -> None:
    council = _council(case["inputs"]["councilCode"])
    band = _by_band(council, case["inputs"]["band"])
    monthly = next(b for b in council["bands"] if b["band"] == case["inputs"]["band"])["monthly"]

    assert band["councilTax"] == monthly
    assert band["shownCouncilTax"] == case["expected"]["shownCouncilTax"]


def test_generate_council_northbridge_two_year_repayment_has_shown_repayment() -> None:
    case = next(c for c in CASES if c["id"] == "generator-northbridge-band-d")
    band = _by_band(_council("E06999001"), "D")

    side = next(s for s in band["buySides"] if s["product"] == case["inputs"]["product"])

    assert side["repayment"] == 158247
    assert side["shownRepayment"] == case["expected"]["shownRepayment"]


def test_generate_council_missing_amounts_have_no_shown_sibling() -> None:
    case = next(c for c in CASES if c["id"] == "generator-westmere-gap-has-no-shown-figures")
    westmere = _council(case["inputs"]["councilCode"])

    assert westmere["bands"] == []
    for band in westmere["rentOrBuy"]["byBand"]:
        assert "councilTax" not in band
        assert "shownCouncilTax" not in band
        assert "shownRentSide" not in band
        assert band["buySides"] == []


def test_generate_council_a_buy_side_without_a_repayment_has_no_shown_repayment() -> None:
    sides = [s for b in _council("E06999001")["rentOrBuy"]["byBand"] for s in b["buySides"]]
    missing = [s for s in sides if "repayment" not in s]

    assert missing
    assert all("shownRepayment" not in s for s in missing)
    assert all("shownRepayment" in s for s in sides if "repayment" in s)


def test_generate_council_every_shown_figure_is_its_pence_rounded_once() -> None:
    def rounded(pence: int) -> int:
        # Independent of the code: round half away from zero with integer arithmetic.
        sign = -1 if pence < 0 else 1
        return sign * ((abs(pence) * 2 + 100) // 200)

    for council in _document()["councils"]:
        for band in council["bands"]:
            assert band["shownYearly"] == rounded(band["yearly"])
            assert band["shownCouncilTax"] == rounded(band["monthly"])
        monthly = {b["band"]: b["monthly"] for b in council["bands"]}
        for entry in council["rentOrBuy"]["byBand"]:
            if "councilTax" in entry:
                assert entry["councilTax"] == monthly[entry["band"]]
                assert entry["shownCouncilTax"] == rounded(entry["councilTax"])
            for side in entry["buySides"]:
                if "repayment" in side:
                    assert side["shownRepayment"] == rounded(side["repayment"])


@pytest.mark.parametrize("case", TYPE_CASES, ids=[c["id"] for c in TYPE_CASES])
def test_generate_council_price_by_type_caption_matches_the_worked_case(
    case: dict[str, Any],
) -> None:
    council = _council(case["inputs"]["councilCode"])

    entry = next(
        e for e in council["priceByType"] if e["propertyType"] == case["inputs"]["propertyType"]
    )

    assert entry["kind"] == case["expected"]["caption"]["kind"]
    assert entry["values"] == case["expected"]["caption"]["values"]


def test_generate_council_every_council_has_one_caption_per_property_type_in_order() -> None:
    for council in _document()["councils"]:
        assert [e["propertyType"] for e in council["priceByType"]] == list(TYPES)
        assert all(e["values"]["propertyType"] == e["propertyType"] for e in council["priceByType"])


def test_generate_council_gap_property_types_get_missing_captions_not_zero() -> None:
    eastmere = next(e for e in _council("E07999001")["priceByType"] if e["propertyType"] == "flat")
    westmere = _council("E07999002")["priceByType"]

    assert eastmere["kind"] == "missing"
    assert "value" not in eastmere["values"]
    assert all(e["kind"] == "missing" and "value" not in e["values"] for e in westmere)


def test_generate_council_type_captions_never_compare_types_or_councils() -> None:
    for council in _document()["councils"]:
        for entry in council["priceByType"]:
            assert set(entry) == {"propertyType", "kind", "values"}
            assert entry["values"].get("topic") == "price"
            assert not {"otherType", "otherCouncil", "comparedWith"} & set(entry["values"])


def test_generate_council_existing_captions_and_rent_or_buy_price_are_unchanged() -> None:
    council = _council("E06999001")
    price = next(c for c in council["captions"] if c["topic"] == "price")

    assert [c["topic"] for c in council["captions"]] == ["rent", "price", "affordability", "tenure"]
    assert "propertyType" not in price["values"]
    assert council["rentOrBuy"]["pricePeriod"] == "2026-08"
    assert council["rentOrBuy"]["pricePointStatus"] == "provisional"


def test_generate_council_rent_or_buy_figures_match_the_independently_worked_cases() -> None:
    rent_cases = read_json(fixtures_directory() / "test-cases" / "rent-or-buy.json")["cases"]
    worked = next(c for c in rent_cases if c["id"] == "northbridge-deposit-10-percent")
    tax_cases = read_json(fixtures_directory() / "test-cases" / "council-tax.json")["cases"]
    monthly = {
        c["inputs"]["band"]: c["expected"]["monthlyPence"]
        for c in tax_cases
        if c["inputs"].get("councilCode") == "E06999001"
    }
    rent = worked["inputs"]["rentMonthlyPence"]
    northbridge = _council("E06999001")["rentOrBuy"]["byBand"]

    # Every band: the rent side is the worked rent plus the worked monthly council tax.
    assert len(monthly) == 8
    for entry in northbridge:
        assert entry["rentSide"] == rent + monthly[entry["band"]]
        assert entry["councilTax"] == monthly[entry["band"]]
    # Band D is the worked 10% deposit case, line by line (the 5-year product has no band).
    band_d = next(b for b in northbridge if b["band"] == "D")
    assert band_d["rentSide"] == worked["expected"]["rentSidePence"]
    assert band_d["shownRentSide"] == worked["expected"]["shownRentSide"]
    for want in worked["expected"]["buySides"]:
        side = next(s for s in band_d["buySides"] if s["product"] == want["product"])
        assert side.get("buySide") == want["buySidePence"]
        assert side.get("repayment") == want["repaymentPence"]
        assert side.get("difference") == want["differencePence"]
        assert side.get("comparison") == want["comparison"]
        assert side.get("shownBuySide") == want["shownBuySide"]
        assert side.get("shownDifference") == want["shownDifference"]
        assert side.get("problem") == want["problem"]
