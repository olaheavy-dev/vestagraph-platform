"""Reads the area data, asks ``vestagraph_area`` for every figure and makes ``area-result.json``.

Nothing in the file is typed by hand (AGENTS rule 2). The output depends only on the data files,
never on the clock. There is no ``float`` anywhere: a whole ``Fraction`` is written as an integer
and a non-whole number as an exact decimal string (for example ``"1.5"``).
"""

import json
from pathlib import Path

from vestagraph_area.area_check import json_number, postcode_result
from vestagraph_area.records import read_postcode_area, read_registry, read_sample_priorities

__all__ = ["FILE_NAME", "generate_area", "json_number"]

FILE_NAME = "area-result.json"


def generate_area(fixtures_directory: Path) -> str:
    """The text of ``area-result.json``: two-space indent, LF line endings, one final newline.

    Raises ``OSError`` when a data file is missing and ``InvalidAreaDataError`` when the area data
    holds something the reader does not understand (for example a counted topic with no record).
    """
    data = fixtures_directory / "data"
    registry = read_registry(data / "pilot-topics.json")
    area = read_postcode_area(data / "postcode-area.json")
    priorities = read_sample_priorities(data / "sample-priorities.json", registry)

    postcodes = [
        postcode_result(registry, area, priorities, postcode)
        for postcode in sorted(p for p in area.postcodes if area.nations[p] == "england")
    ]
    document = {
        "$schema": "../schema/generated-area-result.schema.json",
        "formatVersion": 1,
        "postcodes": postcodes,
    }
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"
