"""The council records reader: what it reads, and everything it refuses."""

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from area_support import fixtures_directory
from vestagraph_area.council_records import CouncilArea, read_council_area
from vestagraph_area.records import InvalidAreaDataError

DATA_FILE = fixtures_directory() / "data" / "council-area.json"


def _data() -> dict[str, Any]:
    parsed: dict[str, Any] = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return parsed


def _read(tmp_path: Path, data: dict[str, Any]) -> CouncilArea:
    path = tmp_path / "council-area.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return read_council_area(path)


def _read_text(tmp_path: Path, text: str | bytes) -> CouncilArea:
    path = tmp_path / "council-area.json"
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8")
    return read_council_area(path)


def _refused(tmp_path: Path, data: dict[str, Any], match: str) -> None:
    with pytest.raises(InvalidAreaDataError, match=match):
        _read(tmp_path, data)


def test_read_council_area_committed_file_reads_every_council() -> None:
    area = read_council_area(DATA_FILE)

    assert [c.code for c in area.councils] == ["E06999001", "E06999002", "E07999001", "E07999002"]
    assert area.councils[0].bands.value["A"] == 144000
    assert area.councils[3].bands.value is None


def test_read_council_area_matches_the_committed_file_counts() -> None:
    raw = _data()
    area = read_council_area(DATA_FILE)

    assert len(area.places) == len(raw["places"])
    assert len(area.postcodes) == len(raw["postcodes"])
    assert len(area.rate_bands) == len(raw["rateBands"])
    assert sum(len(c.neighbourhoods) for c in area.councils) == sum(
        len(c["neighbourhoods"]) for c in raw["councils"]
    )


def test_read_council_area_ratio_values_are_exact_fractions() -> None:
    series = read_council_area(DATA_FILE).councils[0].affordability_series

    assert str(series.points[0].value) == "741/100"


def test_read_council_area_gap_with_value_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][3]["bands"]["value"] = copy.deepcopy(data["councils"][0]["bands"]["value"])

    _refused(tmp_path, data, "must not carry a value")


def test_read_council_area_recorded_bands_missing_a_band_raises(tmp_path: Path) -> None:
    data = _data()
    del data["councils"][0]["bands"]["value"]["H"]

    _refused(tmp_path, data, "exactly the keys A, B, C, D, E, F, G, H")


def test_read_council_area_recorded_fact_without_value_raises(tmp_path: Path) -> None:
    data = _data()
    del data["councils"][0]["bands"]["value"]

    _refused(tmp_path, data, "needs a 'value'")


def test_read_council_area_band_amount_of_zero_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["bands"]["value"]["A"] = 0

    _refused(tmp_path, data, "at least 1")


def test_read_council_area_unknown_fact_status_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["bands"]["status"] = "guessed"

    _refused(tmp_path, data, "unknown status")


def test_read_council_area_series_gap_with_points_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][2]["rentSeries"]["points"] = [
        {"period": "2025-07", "value": 1, "status": "recorded"}
    ]

    _refused(tmp_path, data, "must not carry points")


def test_read_council_area_recorded_series_without_usable_point_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["rentSeries"]["points"] = [{"period": "2025-07", "status": "not-published"}]

    _refused(tmp_path, data, "at least one recorded or provisional point")


def test_read_council_area_recorded_series_with_no_points_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["rentSeries"]["points"] = []

    _refused(tmp_path, data, "at least one recorded or provisional point")


def test_read_council_area_duplicate_series_period_raises(tmp_path: Path) -> None:
    data = _data()
    points = data["councils"][0]["rentSeries"]["points"]
    points[1]["period"] = points[0]["period"]

    _refused(tmp_path, data, "unique and strictly increasing")


def test_read_council_area_decreasing_series_period_raises(tmp_path: Path) -> None:
    data = _data()
    points = data["councils"][0]["rentSeries"]["points"]
    points[0], points[1] = points[1], points[0]

    _refused(tmp_path, data, "unique and strictly increasing")


def test_read_council_area_bad_period_text_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["rentSeries"]["points"][0]["period"] = "2024-13"

    _refused(tmp_path, data, "not YYYY or YYYY-MM")


def test_read_council_area_not_published_point_with_value_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["rentSeries"]["points"][0] = {
        "period": "2024-11",
        "value": 5,
        "status": "not-published",
    }

    _refused(tmp_path, data, "must not carry a value")


def test_read_council_area_zero_decimal_string_value_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["affordabilitySeries"]["points"][0]["value"] = "0.00"

    _refused(tmp_path, data, "value of zero is refused")


def test_read_council_area_decimal_string_with_exponent_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["affordabilitySeries"]["points"][0]["value"] = "7.4e1"

    _refused(tmp_path, data, "not a plain decimal")


def test_read_council_area_point_value_wrong_type_for_unit_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["rentSeries"]["points"][0]["value"] = "118000.5"

    _refused(tmp_path, data, "must be a int")


def test_read_council_area_duplicate_rate_band_raises(tmp_path: Path) -> None:
    data = _data()
    data["rateBands"].append(copy.deepcopy(data["rateBands"][0]))

    _refused(tmp_path, data, "rate bands must be unique")


def test_read_council_area_unknown_rate_product_raises(tmp_path: Path) -> None:
    data = _data()
    data["rateBands"][0]["product"] = "tracker"

    _refused(tmp_path, data, "unknown product")


def test_read_council_area_place_with_unknown_council_code_raises(tmp_path: Path) -> None:
    data = _data()
    data["places"][0]["councilCodes"] = ["E06999777"]

    _refused(tmp_path, data, "unknown council code E06999777")


def test_read_council_area_non_england_place_may_have_no_council_record(tmp_path: Path) -> None:
    data = _data()
    data["places"].append(
        {
            "name": "Elsewhere (synthetic)",
            "county": "Elsewhere shire (synthetic)",
            "region": "Elsewhere (synthetic)",
            "nation": "wales",
            "councilCodes": ["W06999001"],
        }
    )

    area = _read(tmp_path, data)

    assert area.places[-1].council_codes == ("W06999001",)


def test_read_council_area_postcode_with_unknown_council_code_raises(tmp_path: Path) -> None:
    data = _data()
    data["postcodes"][0]["councilCode"] = "E06999777"

    _refused(tmp_path, data, "postcode NB1 4XY names unknown council code")


def test_read_council_area_duplicate_council_code_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][1]["code"] = data["councils"][0]["code"]

    _refused(tmp_path, data, "council codes must be unique")


def test_read_council_area_district_without_county_raises(tmp_path: Path) -> None:
    data = _data()
    del data["councils"][2]["county"]

    _refused(tmp_path, data, "needs a 'county'")


def test_read_council_area_unknown_nation_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["nation"] = "atlantis"

    _refused(tmp_path, data, "unknown nation")


def test_read_council_area_neighbourhood_decile_out_of_range_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["neighbourhoods"][0]["facts"]["connectivity"]["value"]["decile"] = 11

    _refused(tmp_path, data, "between 1 and 10")


def test_read_council_area_missing_required_field_raises(tmp_path: Path) -> None:
    data = _data()
    del data["councils"][0]["name"]

    _refused(tmp_path, data, "required field 'name' is missing")


def test_read_council_area_nan_raises(tmp_path: Path) -> None:
    with pytest.raises(InvalidAreaDataError, match="NaN"):
        _read_text(tmp_path, '{"councils": NaN}')


def test_read_council_area_infinity_raises(tmp_path: Path) -> None:
    with pytest.raises(InvalidAreaDataError, match="Infinity"):
        _read_text(tmp_path, '{"councils": Infinity}')


def test_read_council_area_number_with_exponent_raises(tmp_path: Path) -> None:
    with pytest.raises(InvalidAreaDataError, match="exponent"):
        _read_text(tmp_path, '{"councils": 1.5e3}')


def test_read_council_area_duplicate_key_raises(tmp_path: Path) -> None:
    with pytest.raises(InvalidAreaDataError, match="appears twice"):
        _read_text(tmp_path, '{"councils": [], "councils": []}')


def test_read_council_area_bad_utf8_raises(tmp_path: Path) -> None:
    with pytest.raises(InvalidAreaDataError, match="not valid UTF-8"):
        _read_text(tmp_path, b"\xff\xfe{}")


def test_read_council_area_too_deeply_nested_raises(tmp_path: Path) -> None:
    # Raised as "nested too deeply" or as "not a JSON object", depending on the interpreter's
    # recursion limit; either way it is refused, as in the registry reader's test.
    with pytest.raises(InvalidAreaDataError):
        _read_text(tmp_path, "[" * 200_000 + "]" * 200_000)


def test_read_council_area_not_an_object_raises(tmp_path: Path) -> None:
    with pytest.raises(InvalidAreaDataError, match="must hold a JSON object"):
        _read_text(tmp_path, "[]")


def test_read_council_area_missing_file_raises_os_error(tmp_path: Path) -> None:
    with pytest.raises(OSError, match="council-area"):
        read_council_area(tmp_path / "council-area.json")


def test_read_council_area_rent_series_in_ratio_unit_raises(tmp_path: Path) -> None:
    # A rent marked "ratio" would let "1200.99" through and the generator would truncate it.
    data = _data()
    series = data["councils"][0]["rentSeries"]
    series["unit"] = "ratio"
    for point in series["points"]:
        if "value" in point:
            point["value"] = "1200.99"

    _refused(tmp_path, data, "rentSeries: unit must be 'pence-per-month'")


def test_read_council_area_price_series_in_wrong_unit_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["priceSeries"]["unit"] = "pence-per-month"

    _refused(tmp_path, data, "priceSeries: unit must be 'pence'")


def test_read_council_area_affordability_series_in_pence_unit_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["affordabilitySeries"]["unit"] = "pence"

    _refused(tmp_path, data, "affordabilitySeries: unit must be 'ratio'")


def test_read_council_area_over_long_decimal_text_raises_a_data_error(tmp_path: Path) -> None:
    # 5,000 digits would make Fraction raise a bare ValueError (Python's 4,300-digit limit).
    data = _data()
    data["councils"][0]["affordabilitySeries"]["points"][0]["value"] = "1" * 5000 + ".00"

    _refused(tmp_path, data, "too long")


def test_read_council_area_place_with_no_council_codes_raises(tmp_path: Path) -> None:
    # place_search reads council_codes[0] for a place outside England, so an empty list is refused.
    data = _data()
    data["places"].append(
        {
            "name": "Nowhere (synthetic)",
            "county": "Nowhere shire (synthetic)",
            "region": "Nowhere (synthetic)",
            "nation": "wales",
            "councilCodes": [],
        }
    )

    _refused(tmp_path, data, "at least one council code")


def test_read_council_area_pence_above_sixty_four_bits_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["priceSeries"]["points"][0]["value"] = 10**30

    _refused(tmp_path, data, "at most 9223372036854775807")


def test_read_council_area_pence_at_the_sixty_four_bit_limit_is_read(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["priceSeries"]["points"][0]["value"] = 2**63 - 1

    area = _read(tmp_path, data)

    assert area.councils[0].price_series.points[0].value == 2**63 - 1


def test_read_council_area_band_amount_above_sixty_four_bits_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["bands"]["value"]["A"] = 10**30

    _refused(tmp_path, data, "at most 9223372036854775807")


def test_read_council_area_rate_above_twenty_percent_raises(tmp_path: Path) -> None:
    data = _data()
    data["rateBands"][0]["rateBasisPoints"] = 2001

    _refused(tmp_path, data, "at most 2000")


def test_read_council_area_rate_of_exactly_twenty_percent_is_read(tmp_path: Path) -> None:
    data = _data()
    data["rateBands"][0]["rateBasisPoints"] = 2000

    assert _read(tmp_path, data).rate_bands[0].rate_basis_points == 2000


def test_read_council_area_tenure_counts_all_zero_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["tenure"]["value"] = dict.fromkeys(
        data["councils"][0]["tenure"]["value"], 0
    )

    _refused(tmp_path, data, "at least one household")


def test_read_council_area_negative_tenure_count_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["tenure"]["value"]["ownedOutright"] = -1

    _refused(tmp_path, data, "at least 0")


def test_read_council_area_ratio_with_three_decimal_places_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["affordabilitySeries"]["points"][0]["value"] = "7.411"

    _refused(tmp_path, data, "exactly two decimal places")


def test_read_council_area_ratio_with_one_decimal_place_raises(tmp_path: Path) -> None:
    data = _data()
    data["councils"][0]["affordabilitySeries"]["points"][0]["value"] = "7.4"

    _refused(tmp_path, data, "exactly two decimal places")
