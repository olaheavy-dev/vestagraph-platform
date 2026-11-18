"""Reads the sample energy certificates and makes ``energy-certificate-result.json`` (DA-09).

The page quotes this file. Every figure is a sample input copied with its meaning, or a
calculated output from ``vestagraph_area.energy_certificate`` (rule 2): no total or saving of
our own is made. "Today" is the snapshot date, never the clock. A code is shown as words from
the code tables; a fact the certificate lacks, or a code the table lacks, is
``{"status": "missing", "text": "Not on this certificate"}``, never zero, blank or a raw code
(rule 7). England only (rule 6): a Welsh certificate has outcome ``not-yet-covered`` and a
non-domestic one ``not-domestic``; neither carries facts. No address, postcode or post town is
ever read or written.
"""

import json
from datetime import date
from pathlib import Path
from typing import Any

from vestagraph_area.energy_certificate import (
    Certificate,
    CodeTables,
    Rating,
    decode,
    is_more_than_ten_years_old,
    read_certificates,
    read_code_tables,
    valid_until,
)
from vestagraph_area.records import InvalidAreaDataError, _get, _load

from vestagraph_generator.area_generator import json_number

FILE_NAME = "energy-certificate-result.json"

MISSING: dict[str, str] = {"status": "missing", "text": "Not on this certificate"}

# What the page says under a certificate the register no longer treats as current.
_STATUS_LINES = {
    "superseded": "A newer certificate has replaced this one.",
    "cancelled": "The register has cancelled this certificate.",
}


def _snapshot_date(fixtures_directory: Path) -> date:
    """The boards' "today": ``snapshotDate`` in ``snapshot.json``."""
    snapshot = _get(
        _load(fixtures_directory / "data" / "snapshot.json"), "snapshot", dict, "snapshot.json"
    )
    try:
        return date.fromisoformat(_get(snapshot, "snapshotDate", str, "snapshot.json"))
    except ValueError as error:
        message = f"snapshot.json: snapshotDate is not a date: {error}"
        raise InvalidAreaDataError(message) from error


def _words(code: str | None, table: dict[int, str]) -> str | dict[str, str]:
    if code is None or not code.isascii() or not code.isdigit():
        return dict(MISSING)
    return decode(int(code), table) or dict(MISSING)


def _rating(rating: Rating | None) -> dict[str, Any]:
    if rating is None:
        return dict(MISSING)
    return {"band": rating.band, "score": rating.score}


def _shown(certificate: Certificate, tables: CodeTables, today: date) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "number": certificate.number,
        "outcome": "shown",
        "validUntil": valid_until(certificate.registration_date).isoformat(),
        "moreThanTenYearsOld": is_more_than_ten_years_old(certificate.registration_date, today),
    }
    if certificate.status in _STATUS_LINES:
        entry["statusLine"] = {
            "status": certificate.status,
            "text": _STATUS_LINES[certificate.status],
        }
    entry["currentRating"] = _rating(certificate.current_rating)
    entry["potentialRating"] = _rating(certificate.potential_rating)
    entry["propertyType"] = _words(certificate.property_type_code, tables.property_type)
    entry["builtForm"] = _words(certificate.built_form_code, tables.built_form)
    entry["totalFloorAreaSquareMetres"] = (
        dict(MISSING) if certificate.floor_area is None else json_number(certificate.floor_area)
    )
    if certificate.costs is None:
        entry["costs"] = dict(MISSING)
    else:
        entry["costs"] = {
            part: {"currentPence": pair.current_pence, "potentialPence": pair.potential_pence}
            for part, pair in certificate.costs.items()
        }
    if certificate.parts is None:
        entry["parts"] = dict(MISSING)
    else:
        entry["parts"] = [
            {"part": p.part, "description": p.description, "stars": p.stars}
            for p in certificate.parts
        ]
    if certificate.improvements is None:
        entry["improvements"] = dict(MISSING)
    else:
        entry["improvements"] = [
            {
                "sequence": i.sequence,
                "description": decode(i.code, tables.improvement) or dict(MISSING),
                "indicativeCost": i.indicative_cost,
                "typicalSavingPence": i.typical_saving_pence,
            }
            for i in sorted(certificate.improvements, key=lambda i: i.sequence)
        ]
    return entry


def _certificate(certificate: Certificate, tables: CodeTables, today: date) -> dict[str, Any]:
    if certificate.country != "england":
        return {"number": certificate.number, "outcome": "not-yet-covered"}
    if certificate.kind != "domestic":
        return {"number": certificate.number, "outcome": "not-domestic"}
    return _shown(certificate, tables, today)


def generate_energy(fixtures_directory: Path) -> str:
    """The text of ``energy-certificate-result.json``: two-space indent, LF, one final newline.

    Raises ``OSError`` when a data file is missing and ``InvalidAreaDataError`` when it holds
    something the reader does not understand.
    """
    certificates = read_certificates(fixtures_directory / "data" / "energy-certificates.json")
    tables = read_code_tables(fixtures_directory / "reference" / "energy-code-tables.json")
    today = _snapshot_date(fixtures_directory)
    document = {
        "$schema": "../schema/generated-energy-certificate-result.schema.json",
        "formatVersion": 1,
        "today": today.isoformat(),
        "certificates": [
            _certificate(c, tables, today) for c in sorted(certificates, key=lambda c: c.number)
        ],
    }
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"
