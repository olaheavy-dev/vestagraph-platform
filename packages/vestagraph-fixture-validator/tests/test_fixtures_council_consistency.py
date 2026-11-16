"""Council-wide figures agree across the two sample files (issue 299).

`council-area.json` (City Explorer) is the source for a council's figures. `postcode-area.json`
repeats two of them for a postcode in that council: the council tax charge for each band and the
house price to earnings ratio. It also links the postcode to the council for the average private
rent (register DA-29, DA-30): the link carries a council code and no figure, and the rent itself is
read from `council-result.json`. For every postcode that `council-area.json` maps to a council, the
postcode file's copies must equal the council's, and name the council the same way, so the
signed-in chat never shows two answers for one council (rules 1 and 7).

Nothing is calculated here: band charges are compared as pounds against pence (x 100), and the
ratio as the same decimal value.
"""

import copy
from decimal import Decimal

from fixtures_support import Json, fixtures_directory, load, read_file

_COUNCIL_TOPICS = {"council-tax", "affordability", "council-rent"}


def _council_records(postcode_area: Json, council_area: Json) -> list[tuple[Json, Json]]:
    """Each council-level postcode record paired with the council its postcode is mapped to."""
    councils = {c["code"]: c for c in council_area["councils"]}
    pairs: list[tuple[Json, Json]] = []
    for link in council_area["postcodes"]:
        council = councils[link["councilCode"]]
        pairs += [
            (item, council)
            for item in postcode_area["area"]
            if item["postcode"] == link["postcode"] and item["topic"] in _COUNCIL_TOPICS
        ]
    return pairs


def _council_result() -> Json:
    return read_file(fixtures_directory() / "generated" / "council-result.json")


def _mismatches(
    postcode_area: Json, council_area: Json, council_result: Json | None = None
) -> list[str]:
    """Each way a postcode's council-level record differs from its council's figures."""
    result = council_result if council_result is not None else _council_result()
    found: list[str] = _unmapped_rent(postcode_area, council_area)
    links = {link["postcode"]: link["councilCode"] for link in council_area["postcodes"]}
    for item, council in _council_records(postcode_area, council_area):
        name = council["name"]
        if item["topic"] == "council-tax":
            source_status = council["bands"]["status"]
        elif item["topic"] == "council-rent":
            source_status = council["rentSeries"]["status"]
        else:
            source_status = _ratio_point(item, council).get("status", "missing")
        if item["status"] != source_status:
            found.append(f"{item['id']}: status {item['status']}, council has {source_status}")
            continue
        if item["status"] != "recorded":
            continue
        if item["topic"] == "council-tax":
            found += _council_tax_mismatches(item, council)
        elif item["topic"] == "council-rent":
            found += _rent_mismatches(item, links[item["postcode"]], result)
        else:
            found += _affordability_mismatches(item, council)
        if item["level"]["areaName"] != name:
            found.append(f"{item['id']}: level areaName is not {name!r}")
        if name not in item["label"]:
            found.append(f"{item['id']}: label does not name {name!r}")
    return found


def _unmapped_rent(postcode_area: Json, council_area: Json) -> list[str]:
    """A recorded rent link for a postcode that council-area.json maps to no council."""
    mapped = {link["postcode"] for link in council_area["postcodes"]}
    return [
        f"{item['id']}: recorded rent for postcode {item['postcode']}, which has no council link"
        for item in postcode_area["area"]
        if item["topic"] == "council-rent"
        and item["status"] == "recorded"
        and item["postcode"] not in mapped
    ]


def _rent_mismatches(item: Json, linked_code: str, council_result: Json) -> list[str]:
    found: list[str] = []
    code = item["value"]["councilCode"]
    if code != linked_code:
        found.append(f"{item['id']}: councilCode {code}, the postcode is linked to {linked_code}")
    council = next((c for c in council_result["councils"] if c["code"] == code), None)
    captions = [] if council is None else [c for c in council["captions"] if c["topic"] == "rent"]
    if not captions or captions[0]["kind"] == "missing":
        found.append(f"{item['id']}: council {code} has no rent caption value in council-result")
    return found


def _council_tax_mismatches(item: Json, council: Json) -> list[str]:
    value = item["value"]
    found: list[str] = []
    if value["authorityName"] != council["name"]:
        found.append(f"{item['id']}: authorityName is not {council['name']!r}")
    expected = council["bands"]["value"]
    shown = {b["band"]: Decimal(b["annualCharge"]) * 100 for b in value["bands"]}
    if set(shown) != set(expected):
        found.append(f"{item['id']}: bands {sorted(shown)} are not {sorted(expected)}")
    for band, pence in expected.items():
        if band in shown and shown[band] != pence:
            found.append(f"{item['id']}: band {band} is {shown[band]} pence, council has {pence}")
    return found


def _ratio_point(item: Json, council: Json) -> Json:
    """The council's ratio for the record's year; empty when there is not exactly one."""
    year = str(item["value"]["year"]) if "value" in item else None
    points = [p for p in council["affordabilitySeries"]["points"] if p["period"] == year]
    return points[0] if len(points) == 1 else {}


def _affordability_mismatches(item: Json, council: Json) -> list[str]:
    value = item["value"]
    found: list[str] = []
    if value["areaName"] != council["name"]:
        found.append(f"{item['id']}: areaName is not {council['name']!r}")
    point = _ratio_point(item, council)
    if Decimal(value["ratio"]) != Decimal(point["value"]):
        year, council_ratio = value["year"], point["value"]
        found.append(
            f"{item['id']}: ratio {value['ratio']} for {year}, council has {council_ratio}"
        )
    return found


def test_council_figures_real_files_postcode_records_match_their_council() -> None:
    assert _mismatches(load("postcode-area"), load("council-area")) == []


def test_council_figures_real_files_compare_both_northbridge_records() -> None:
    # Guards the check above from passing because nothing was compared.
    pairs = _council_records(load("postcode-area"), load("council-area"))
    compared = {item["id"] for item, _ in pairs if item["status"] == "recorded"}
    assert {
        "NB1-4XY-AREA-COUNCIL-TAX-1",
        "NB1-4XY-AREA-AFFORDABILITY-1",
        "NB1-4XY-AREA-COUNCIL-RENT-1",
    } <= compared


def _broken(item_id: str) -> tuple[Json, Json]:
    postcode_area = copy.deepcopy(load("postcode-area"))
    item = next(i for i in postcode_area["area"] if i["id"] == item_id)
    return postcode_area, item


def test_council_figures_band_d_differs_is_reported() -> None:
    postcode_area, item = _broken("NB1-4XY-AREA-COUNCIL-TAX-1")
    next(b for b in item["value"]["bands"] if b["band"] == "D")["annualCharge"] = "2118.15"
    found = _mismatches(postcode_area, load("council-area"))
    assert found == ["NB1-4XY-AREA-COUNCIL-TAX-1: band D is 211815.00 pence, council has 216000"]


def test_council_figures_band_missing_is_reported() -> None:
    postcode_area, item = _broken("NB1-4XY-AREA-COUNCIL-TAX-1")
    item["value"]["bands"] = [b for b in item["value"]["bands"] if b["band"] != "H"]
    found = _mismatches(postcode_area, load("council-area"))
    assert len(found) == 1
    assert "bands" in found[0]


def test_council_figures_ratio_differs_is_reported() -> None:
    postcode_area, item = _broken("NB1-4XY-AREA-AFFORDABILITY-1")
    item["value"]["ratio"] = "7.9"
    found = _mismatches(postcode_area, load("council-area"))
    assert found == ["NB1-4XY-AREA-AFFORDABILITY-1: ratio 7.9 for 2025, council has 8.44"]


def test_council_figures_ratio_year_not_published_is_reported() -> None:
    postcode_area, item = _broken("NB1-4XY-AREA-AFFORDABILITY-1")
    item["value"]["year"] = 2010
    found = _mismatches(postcode_area, load("council-area"))
    assert found == ["NB1-4XY-AREA-AFFORDABILITY-1: status recorded, council has missing"]


def test_council_figures_council_named_differently_is_reported() -> None:
    postcode_area, item = _broken("NB1-4XY-AREA-COUNCIL-TAX-1")
    item["value"]["authorityName"] = "Northbridge City Council (synthetic)"
    item["level"]["areaName"] = "Northbridge City Council (synthetic)"
    found = _mismatches(postcode_area, load("council-area"))
    assert len(found) == 2
    assert all("is not 'Northbridge (synthetic)'" in line for line in found)


def test_council_figures_postcode_record_not_recorded_is_reported() -> None:
    postcode_area, item = _broken("NB1-4XY-AREA-AFFORDABILITY-1")
    item["status"] = "no-record-in-source"
    found = _mismatches(postcode_area, load("council-area"))
    assert found == [
        "NB1-4XY-AREA-AFFORDABILITY-1: status no-record-in-source, council has recorded"
    ]


def test_council_figures_label_names_council_differently_is_reported() -> None:
    postcode_area, item = _broken("NB1-4XY-AREA-COUNCIL-TAX-1")
    item["label"] = "Council tax charges by band, Northbridge City Council (synthetic)"
    found = _mismatches(postcode_area, load("council-area"))
    assert found == ["NB1-4XY-AREA-COUNCIL-TAX-1: label does not name 'Northbridge (synthetic)'"]


def test_council_figures_rent_link_a_different_council_code_is_reported() -> None:
    postcode_area, item = _broken("NB1-4XY-AREA-COUNCIL-RENT-1")
    item["value"]["councilCode"] = "E06999002"
    found = _mismatches(postcode_area, load("council-area"))
    assert found == [
        "NB1-4XY-AREA-COUNCIL-RENT-1: councilCode E06999002, the postcode is linked to E06999001"
    ]


def test_council_figures_rent_status_differs_from_rent_series_is_reported() -> None:
    postcode_area, item = _broken("NB1-4XY-AREA-COUNCIL-RENT-1")
    item["status"] = "no-record-in-source"
    del item["value"]
    found = _mismatches(postcode_area, load("council-area"))
    assert found == [
        "NB1-4XY-AREA-COUNCIL-RENT-1: status no-record-in-source, council has recorded"
    ]


def test_council_figures_recorded_rent_for_an_unmapped_postcode_is_reported() -> None:
    postcode_area, item = _broken("NB7-1RR-AREA-COUNCIL-RENT-1")
    item["status"] = "recorded"
    item["value"] = {"councilCode": "E06999001"}
    found = _mismatches(postcode_area, load("council-area"))
    assert found == [
        "NB7-1RR-AREA-COUNCIL-RENT-1: recorded rent for postcode NB7 1RR, which has no council link"
    ]


def test_council_figures_rent_council_without_a_rent_caption_value_is_reported() -> None:
    # Eastmere (E07999001) has a rent series with no record, so its rent caption is "missing".
    postcode_area, item = _broken("NB1-4XY-AREA-COUNCIL-RENT-1")
    council_area = copy.deepcopy(load("council-area"))
    next(link for link in council_area["postcodes"] if link["postcode"] == "NB1 4XY")[
        "councilCode"
    ] = "E07999001"
    item["value"]["councilCode"] = "E07999001"
    eastmere = next(c for c in council_area["councils"] if c["code"] == "E07999001")
    eastmere["rentSeries"]["status"] = "recorded"
    item["level"]["areaName"] = eastmere["name"]
    item["label"] = f"Average private rent, {eastmere['name']}"
    # Re-linking the postcode also makes its tax and ratio records disagree; only rent matters here.
    found = [
        line
        for line in _mismatches(postcode_area, council_area)
        if line.startswith("NB1-4XY-AREA-COUNCIL-RENT-1")
    ]
    assert found == [
        "NB1-4XY-AREA-COUNCIL-RENT-1: council E07999001 has no rent caption value in council-result"
    ]


def test_council_figures_rent_gap_for_an_unmapped_postcode_is_accepted() -> None:
    _, item = _broken("NB7-1RR-AREA-COUNCIL-RENT-1")
    assert item["status"] == "no-record-in-source"
    assert _mismatches(load("postcode-area"), load("council-area")) == []
