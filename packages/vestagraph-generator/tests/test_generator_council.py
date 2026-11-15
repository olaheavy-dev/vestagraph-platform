"""The generator writes ``council-result.json`` beside ``costs.json`` and ``area-result.json``."""

import io
import json
from pathlib import Path
from typing import Any

from generator_support import copy_data_to, fixtures_directory, read_json, write_json
from vestagraph_generator.__main__ import main
from vestagraph_generator.costs_generator import run
from vestagraph_generator.council_generator import generate_council

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
