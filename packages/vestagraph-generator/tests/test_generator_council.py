"""The generator writes ``council-result.json`` beside ``costs.json`` and ``area-result.json``."""

import io
from pathlib import Path

from generator_support import copy_data_to, read_json, write_json
from vestagraph_generator.__main__ import main
from vestagraph_generator.costs_generator import run

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
