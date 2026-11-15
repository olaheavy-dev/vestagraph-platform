"""Reads the council data, asks ``vestagraph_area`` for every figure, makes ``council-result.json``.

Nothing in the file is typed by hand (AGENTS rule 2). The published inputs (a band's yearly
council tax, a rate band) are copied from the data with their meaning; every calculated figure
(monthly council tax, repayments, the rent or buy comparison, caption values, tenure shares)
comes from ``vestagraph_area`` and the cost engine. The output depends only on the data files,
never on the clock. A whole number is written as an integer and any other exact number as a
decimal string, never a ``float``. A gap is left out, never written as zero (rule 7).
"""

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from vestagraph_area.captions import property_type_caption, series_caption, tenure_caption
from vestagraph_area.council_records import (
    BAND_LETTERS,
    PROPERTY_TYPES,
    TENURE_KEYS,
    Council,
    CouncilArea,
    Series,
    read_council_area,
)
from vestagraph_area.council_tax import band_monthly, band_yearly
from vestagraph_area.place_search import council_for_postcode, find_councils
from vestagraph_area.records import InvalidAreaDataError
from vestagraph_area.rent_or_buy import BuySide, rent_or_buy, shown_pounds
from vestagraph_area.tenure import share_text, tenure_shares_for_fact
from vestagraph_engine.pence import Pence

from vestagraph_generator.area_generator import json_number

FILE_NAME = "council-result.json"

# The example inputs the design canvas quotes (controller ruling for Task 8): a 10% deposit over
# 25 years and no typed rate, so each product's quoted rate band is used.
_DEPOSIT_PERCENT = Fraction(10)
_TERM_YEARS = 25


def _latest_value(series: Series) -> Any:
    """The series' latest point value; ``None`` when there are no points or it is unpublished."""
    if series.status != "recorded" or not series.points:
        return None
    return series.points[-1].value


def _pence(value: int | Fraction | None) -> Pence | None:
    """Whole pence; anything that is not a whole number is refused, never cut (rule 2)."""
    if value is None:
        return None
    if type(value) is not int:
        message = f"A pence value must be a whole number, not {value}."
        raise InvalidAreaDataError(message)
    return Pence(value)


def _shares(shares: dict[str, Fraction]) -> dict[str, str]:
    # One decimal place as text ("35.0"): the same text the tenure caption quotes.
    return {key: share_text(shares[key]) for key in TENURE_KEYS}


def _buy_side(side: BuySide) -> dict[str, Any]:
    entry: dict[str, Any] = {"product": side.product}
    if side.buy_side is not None:
        entry["buySide"] = side.buy_side.value
    if side.repayment is not None:
        entry["repayment"] = side.repayment.value
    if side.shown_repayment is not None:
        entry["shownRepayment"] = side.shown_repayment
    if side.rate_used is not None:
        entry["rateBand"] = {
            "maxLoanToValuePercent": side.rate_used.max_loan_to_value_percent,
            "rateBasisPoints": side.rate_used.rate_basis_points,
            "month": side.rate_used.month,
        }
    if side.comparison is not None:
        entry["comparison"] = side.comparison
    if side.difference is not None:
        entry["difference"] = side.difference.value
    if side.shown_buy_side is not None:
        entry["shownBuySide"] = side.shown_buy_side
    if side.shown_difference is not None:
        entry["shownDifference"] = side.shown_difference
    if side.problem is not None:
        entry["problem"] = side.problem
    return entry


def _bands(council: Council) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for band in BAND_LETTERS:
        yearly = band_yearly(council.bands, band)
        if yearly is not None:
            monthly = band_monthly(yearly)
            found.append(
                {
                    "band": band,
                    "yearly": yearly.value,
                    "monthly": monthly.value,
                    "shownYearly": shown_pounds(yearly),
                    "shownCouncilTax": shown_pounds(monthly),
                }
            )
    return found


def _label_series(prefix: str, series: Series, into: dict[str, Any]) -> None:
    """Say which month and status a used figure has, or why there is none (never an older month)."""
    if series.status != "recorded":
        into[f"{prefix}MissingReason"] = series.status
        return
    last = series.points[-1]
    if last.value is None:
        into[f"{prefix}MissingReason"] = "latest-not-published"
        return
    into[f"{prefix}Period"] = last.period
    into[f"{prefix}PointStatus"] = last.status


def _rent_or_buy(council: Council, area: CouncilArea) -> dict[str, Any]:
    rent = _pence(_latest_value(council.rent_series))
    price = _pence(_latest_value(council.price_series))
    by_band: list[dict[str, Any]] = []
    for band in BAND_LETTERS:
        yearly = band_yearly(council.bands, band)
        tax = None if yearly is None else band_monthly(yearly)
        outcome = rent_or_buy(
            rent, price, tax, _DEPOSIT_PERCENT, _TERM_YEARS, None, area.rate_bands
        )
        entry: dict[str, Any] = {"band": band}
        if tax is not None:
            entry["councilTax"] = tax.value
            entry["shownCouncilTax"] = shown_pounds(tax)
        if outcome.rent_side is not None:
            entry["rentSide"] = outcome.rent_side.value
        if outcome.shown_rent_side is not None:
            entry["shownRentSide"] = outcome.shown_rent_side
        entry["buySides"] = [_buy_side(s) for s in outcome.buy_sides]
        if outcome.problem is not None:
            entry["problem"] = outcome.problem
        by_band.append(entry)
    result: dict[str, Any] = {}
    _label_series("rent", council.rent_series, result)
    _label_series("price", council.price_series, result)
    if council.bands.status != "recorded":
        result["councilTaxMissingReason"] = council.bands.status
    result["byBand"] = by_band
    return result


def _captions(council: Council) -> list[dict[str, Any]]:
    captions = [
        (topic, series_caption(topic, series))
        for topic, series in (
            ("rent", council.rent_series),
            ("price", council.price_series),
            ("affordability", council.affordability_series),
        )
    ]
    captions.append(("tenure", tenure_caption(council.tenure)))
    return [{"topic": t, "kind": c.kind, "values": c.values} for t, c in captions]


def _price_by_type(council: Council) -> list[dict[str, Any]]:
    """One price caption per property type, in the fixed order; each looks at its own series."""
    found: list[dict[str, Any]] = []
    for property_type in PROPERTY_TYPES:
        caption = property_type_caption(property_type, council.price_by_type[property_type])
        found.append(
            {"propertyType": property_type, "kind": caption.kind, "values": caption.values}
        )
    return found


def _council(council: Council, area: CouncilArea) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "code": council.code,
        "bands": _bands(council),
        "rentOrBuy": _rent_or_buy(council, area),
        "captions": _captions(council),
        "priceByType": _price_by_type(council),
    }
    shares = tenure_shares_for_fact(council.tenure)
    if shares is not None:
        entry["tenureShares"] = _shares(shares)
    neighbourhoods: list[dict[str, Any]] = []
    for hood in sorted(council.neighbourhoods, key=lambda n: n.code):
        item: dict[str, Any] = {
            "code": hood.code,
            "label": f"{hood.larger_area_name} ({hood.short_code})",
        }
        hood_shares = tenure_shares_for_fact(hood.tenure)
        if hood_shares is not None:
            item["tenureShares"] = _shares(hood_shares)
        else:
            item["tenureMissingReason"] = hood.tenure.status
        neighbourhoods.append(item)
    entry["neighbourhoods"] = neighbourhoods
    return entry


def _search(area: CouncilArea) -> list[dict[str, Any]]:
    queries = {p.name for p in area.places}
    for council in area.councils:
        queries.add(council.name)
        queries.update(council.former_names)
    found: list[dict[str, Any]] = []
    for query in sorted(queries):
        result = find_councils(query, area)
        matches = []
        for m in result.matches:
            match: dict[str, Any] = {"councilCode": m.council_code, "label": m.label}
            if m.note is not None:
                match["note"] = m.note
            matches.append(match)
        found.append({"query": query, "kind": result.kind, "matches": matches})
    for entry in sorted(area.postcodes, key=lambda p: p.postcode):
        code = council_for_postcode(entry.postcode, area)
        found.append(
            {
                "query": entry.postcode,
                "kind": "council-for-postcode",
                "matches": [] if code is None else [{"councilCode": code}],
            }
        )
    return found


def generate_council(fixtures_directory: Path) -> str:
    """The text of ``council-result.json``: two-space indent, LF line endings, one final newline.

    Raises ``OSError`` when the data file is missing and ``InvalidAreaDataError`` when it holds
    something the reader does not understand.
    """
    area = read_council_area(fixtures_directory / "data" / "council-area.json")
    document = {
        "$schema": "../schema/generated-council-result.schema.json",
        "formatVersion": 1,
        "exampleInputs": {
            "depositPercent": json_number(_DEPOSIT_PERCENT),
            "termYears": _TERM_YEARS,
        },
        "councils": [_council(c, area) for c in sorted(area.councils, key=lambda c: c.code)],
        "search": _search(area),
    }
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"
