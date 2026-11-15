"""The generator writes ``council-result.json`` beside ``costs.json`` and ``area-result.json``."""

import io
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from generator_support import copy_data_to, fixtures_directory, read_json, write_json
from vestagraph_area.records import InvalidAreaDataError
from vestagraph_engine.pence import Pence
from vestagraph_generator.__main__ import main
from vestagraph_generator.costs_generator import run
from vestagraph_generator.council_generator import _pence, generate_council

NAMES = ("area-result.json", "costs.json", "council-result.json")


def test_run_writes_all_three_generated_files_and_keeps_them(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    generated = fixtures / "generated"
    generated.mkdir()
    (generated / "old.json").write_text("{}", encoding="utf-8")

    exit_code = run(fixtures, io.StringIO())

    assert exit_code == 0
    assert sorted(p.name for p in generated.iterdir()) == sorted(NAMES)
    written = (generated / "council-result.json").read_bytes()
    assert written[:3] != b"\xef\xbb\xbf"
    assert written.endswith(b"\n")
    run(fixtures, io.StringIO())
    assert sorted(p.name for p in generated.iterdir()) == sorted(NAMES)


def test_run_council_result_twice_is_byte_identical(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "generated" / "council-result.json"

    run(fixtures, io.StringIO())
    first = path.read_bytes()
    run(fixtures, io.StringIO())

    assert path.read_bytes() == first


def test_run_council_data_invalid_exits_two_and_writes_nothing(tmp_path: Path) -> None:
    copy_data_to(tmp_path)
    path = tmp_path / "packages" / "fixtures" / "data" / "council-area.json"
    document = read_json(path)
    document["postcodes"][0]["councilCode"] = "E00000000"
    write_json(path, document)
    generated = tmp_path / "packages" / "fixtures" / "generated"
    generated.mkdir()
    for name in NAMES:
        (generated / name).write_bytes(b'{"known": "file"}\n')
    out, err = io.StringIO(), io.StringIO()

    exit_code = main([str(tmp_path)], out, err, tmp_path)

    assert exit_code == 2
    assert "council-area.json" in err.getvalue()
    assert sorted(p.name for p in generated.iterdir()) == sorted(NAMES)
    assert all((generated / n).read_bytes() == b'{"known": "file"}\n' for n in NAMES)


def _council(code: str) -> dict[str, Any]:
    document = json.loads(generate_council(fixtures_directory()))
    found: dict[str, Any] = next(c for c in document["councils"] if c["code"] == code)
    return found


def test_generate_council_northbridge_band_d_matches_the_worked_case() -> None:
    cases = read_json(fixtures_directory() / "test-cases" / "rent-or-buy.json")["cases"]
    expected = next(c for c in cases if c["id"] == "northbridge-deposit-10-percent")["expected"]
    two_year = next(s for s in expected["buySides"] if s["product"] == "2-year-fixed")
    band_d = next(b for b in _council("E06999001")["rentOrBuy"]["byBand"] if b["band"] == "D")

    side = next(s for s in band_d["buySides"] if s["product"] == "2-year-fixed")
    assert band_d["rentSide"] == expected["rentSidePence"]
    assert side["buySide"] == two_year["buySidePence"]
    assert side["repayment"] == two_year["repaymentPence"]
    assert side["difference"] == two_year["differencePence"]
    assert side["comparison"] == two_year["comparison"] == "more"
    assert band_d["shownRentSide"] == expected["shownRentSide"]
    assert side["shownBuySide"] == two_year["shownBuySide"]
    assert side["shownDifference"] == two_year["shownDifference"]


def test_generate_council_gaps_are_left_out_and_say_why() -> None:
    westmere = _council("E07999002")
    eastmere = _council("E07999001")

    assert "tenureShares" not in westmere
    assert westmere["rentOrBuy"]["councilTaxMissingReason"] == "no-record-in-source"
    assert all("rentSide" not in b for b in westmere["rentOrBuy"]["byBand"])
    assert eastmere["rentOrBuy"]["rentMissingReason"] == "no-record-in-source"
    assert "rentPeriod" not in eastmere["rentOrBuy"]
    assert eastmere["rentOrBuy"]["pricePointStatus"] in ("recorded", "provisional")
    assert _council("E06999001")["rentOrBuy"]["rentPeriod"] == "2026-10"


def test_generate_council_every_council_has_eight_bands() -> None:
    document = json.loads(generate_council(fixtures_directory()))

    assert all(len(c["rentOrBuy"]["byBand"]) == 8 for c in document["councils"])


def _generate_with(tmp_path: Path, change: Any) -> dict[str, Any]:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "data" / "council-area.json"
    document = read_json(path)
    change(document)
    write_json(path, document)
    parsed: dict[str, Any] = json.loads(generate_council(fixtures))
    return parsed


def _southvale(document: dict[str, Any]) -> dict[str, Any]:
    found: dict[str, Any] = next(c for c in document["councils"] if c["code"] == "E06999002")
    return found


def test_generate_council_latest_price_not_published_gives_no_buy_figure_and_says_why(
    tmp_path: Path,
) -> None:
    def change(document: dict[str, Any]) -> None:
        last = _southvale(document)["priceSeries"]["points"][-1]
        last["status"] = "not-published"
        del last["value"]

    result = _generate_with(tmp_path, change)
    southvale = next(c for c in result["councils"] if c["code"] == "E06999002")["rentOrBuy"]

    assert "pricePeriod" not in southvale
    assert "pricePointStatus" not in southvale
    assert southvale["priceMissingReason"] == "latest-not-published"
    for band in southvale["byBand"]:
        assert all("buySide" not in side and "repayment" not in side for side in band["buySides"])
        assert "rentSide" in band  # Rent is still shown: only the buy side is missing.


def test_generate_council_tenure_gap_gives_a_missing_caption_with_the_gap_status() -> None:
    westmere = _council("E07999002")
    tenure = next(c for c in westmere["captions"] if c["topic"] == "tenure")

    assert tenure == {
        "topic": "tenure",
        "kind": "missing",
        "values": {"topic": "tenure", "pattern": "missing", "reason": "no-record-in-source"},
    }


def test_generate_council_neighbourhood_tenure_gap_says_why(tmp_path: Path) -> None:
    def change(document: dict[str, Any]) -> None:
        tenure = _southvale(document)["neighbourhoods"][0]["facts"]["tenure"]
        tenure["status"] = "source-failed"
        del tenure["value"]

    result = _generate_with(tmp_path, change)
    hood = next(c for c in result["councils"] if c["code"] == "E06999002")["neighbourhoods"][0]

    assert "tenureShares" not in hood
    assert hood["tenureMissingReason"] == "source-failed"


def test_generate_council_tenure_shares_and_caption_use_the_same_one_decimal_text() -> None:
    council = _council("E06999001")
    caption = next(c for c in council["captions"] if c["topic"] == "tenure")["values"]

    for key, text in council["tenureShares"].items():
        assert isinstance(text, str)
        assert text.count(".") == 1
        assert len(text.split(".")[1]) == 1
        assert caption[key] == text


def test_generate_council_example_deposit_is_a_json_number() -> None:
    document = json.loads(generate_council(fixtures_directory()))

    assert document["exampleInputs"]["depositPercent"] == 10
    assert type(document["exampleInputs"]["depositPercent"]) is int


def test_generate_council_postcode_search_kind_is_hyphenated() -> None:
    document = json.loads(generate_council(fixtures_directory()))
    kinds = {case["kind"] for case in document["search"]}

    assert "council-for-postcode" in kinds
    assert "council_for_postcode" not in kinds


def test_pence_whole_number_is_made_into_pence() -> None:
    assert _pence(123) == Pence(123)
    assert _pence(None) is None


def test_pence_refuses_a_value_that_is_not_a_whole_number() -> None:
    # 1200.99 pence must never be silently cut to 1200.
    with pytest.raises(InvalidAreaDataError, match="whole"):
        _pence(Fraction("1200.99"))


def test_generate_council_whole_percent_share_keeps_its_decimal_in_shares_and_caption(
    tmp_path: Path,
) -> None:
    # Counts of 35, 25, 20, 10 and 10 out of 100 households are exactly 35.0, 25.0, 20.0, 10.0 and
    # 10.0 percent (count / 100 x 100), whole numbers that must still read "35.0", not "35".
    def change(document: dict[str, Any]) -> None:
        _southvale(document)["tenure"]["value"] = {
            "ownedOutright": 35,
            "ownedWithMortgage": 25,
            "socialRented": 20,
            "privateRented": 10,
            "other": 10,
        }

    result = _generate_with(tmp_path, change)
    council = next(c for c in result["councils"] if c["code"] == "E06999002")
    caption = next(c for c in council["captions"] if c["topic"] == "tenure")["values"]

    assert council["tenureShares"]["ownedOutright"] == "35.0"
    assert caption["ownedOutright"] == "35.0"
    assert council["tenureShares"]["other"] == "10.0"
