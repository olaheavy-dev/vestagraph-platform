"""Council-wide figures agree across the two sample files (issue 299).

`council-area.json` (City Explorer) is the source for a council's figures. `postcode-area.json`
repeats two of them for a postcode in that council: the council tax charge for each band and the
house price to earnings ratio. For every postcode that `council-area.json` maps to a council, the
postcode file's copies must equal the council's, and name the council the same way, so the
signed-in chat never shows two answers for one council (rules 1 and 7).

Nothing is calculated here: band charges are compared as pounds against pence (x 100), and the
ratio as the same decimal text.
"""

import copy
from decimal import Decimal

from fixtures_support import Json, load


def _mismatches(postcode_area: Json, council_area: Json) -> list[str]:
    """Each way a postcode's council-level record differs from its council's figures."""
    councils = {c["code"]: c for c in council_area["councils"]}
    found: list[str] = []
    for link in council_area["postcodes"]:
        council = councils[link["councilCode"]]
        name = council["name"]
        for item in postcode_area["area"]:
            if item["postcode"] != link["postcode"] or item["status"] != "recorded":
                continue
            if item["topic"] == "council-tax":
                found += _council_tax_mismatches(item, council)
            elif item["topic"] == "affordability":
                found += _affordability_mismatches(item, council)
            else:
                continue
            if item["level"]["areaName"] != name:
                found.append(f"{item['id']}: level areaName is not {name!r}")
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


def _affordability_mismatches(item: Json, council: Json) -> list[str]:
    value = item["value"]
    found: list[str] = []
    if value["areaName"] != council["name"]:
        found.append(f"{item['id']}: areaName is not {council['name']!r}")
    year = str(value["year"])
    points = [p for p in council["affordabilitySeries"]["points"] if p["period"] == year]
    if len(points) != 1:
        found.append(f"{item['id']}: the council has no single ratio for {year}")
    elif Decimal(value["ratio"]) != Decimal(points[0]["value"]):
        found.append(
            f"{item['id']}: ratio {value['ratio']} for {year}, council has {points[0]['value']}"
        )
    return found


def _compared_ids(postcode_area: Json, council_area: Json) -> set[str]:
    linked = {link["postcode"] for link in council_area["postcodes"]}
    return {
        i["id"]
        for i in postcode_area["area"]
        if i["postcode"] in linked and i["topic"] in {"council-tax", "affordability"}
    }


def test_council_figures_real_files_postcode_records_match_their_council() -> None:
    assert _mismatches(load("postcode-area"), load("council-area")) == []


def test_council_figures_real_files_compare_both_northbridge_records() -> None:
    # Guards the check above from passing because nothing was compared.
    compared = _compared_ids(load("postcode-area"), load("council-area"))
    assert {"NB1-4XY-AREA-COUNCIL-TAX-1", "NB1-4XY-AREA-AFFORDABILITY-1"} <= compared


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
    assert found == ["NB1-4XY-AREA-AFFORDABILITY-1: the council has no single ratio for 2010"]


def test_council_figures_council_named_differently_is_reported() -> None:
    postcode_area, item = _broken("NB1-4XY-AREA-COUNCIL-TAX-1")
    item["value"]["authorityName"] = "Northbridge City Council (synthetic)"
    item["level"]["areaName"] = "Northbridge City Council (synthetic)"
    found = _mismatches(postcode_area, load("council-area"))
    assert len(found) == 2
    assert all("is not 'Northbridge (synthetic)'" in line for line in found)
