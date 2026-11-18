"""Energy certificate rules: pure functions, standard library only."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from fractions import Fraction
from pathlib import Path
from typing import Any, Final

from vestagraph_area.records import InvalidAreaDataError, _get, _load, _objects

VALIDITY_YEARS: Final = 10


def valid_until(start: date) -> date:
    """Last valid day: the same day and month ``VALIDITY_YEARS`` on.

    ``start`` is the registration date (regulation 9(2)(a), 2012 Regulations).
    29 February becomes 28 February when the target year has no such day.
    """
    year = start.year + VALIDITY_YEARS
    if start.month == 2 and start.day == 29 and not _is_leap(year):
        return date(year, 2, 28)
    return date(year, start.month, start.day)


def is_more_than_ten_years_old(start: date, today: date) -> bool:
    """True when ``today`` is after the last valid day."""
    return today > valid_until(start)


def _is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# ---------------------------------------------------------------------------------------------
# Readers: the normalised sample certificates and the code tables (DA-09). A fact the certificate
# does not hold is ``None``, never zero or blank (rule 7).
# ---------------------------------------------------------------------------------------------

_COST_PARTS: Final = ("heating", "hotWater", "lighting")


@dataclass(frozen=True, slots=True)
class Rating:
    band: str
    score: int


@dataclass(frozen=True, slots=True)
class CostPair:
    """Yearly running-cost estimates in whole pence."""

    current_pence: int
    potential_pence: int


@dataclass(frozen=True, slots=True)
class Part:
    part: str
    description: str
    stars: int


@dataclass(frozen=True, slots=True)
class Improvement:
    sequence: int
    code: int
    indicative_cost: str
    typical_saving_pence: int


@dataclass(frozen=True, slots=True)
class Certificate:
    number: str
    country: str
    kind: str
    status: str
    registration_date: date
    inspection_date: date
    current_rating: Rating | None
    potential_rating: Rating | None
    property_type_code: str | None
    built_form_code: str | None
    floor_area: int | Fraction | None
    costs: dict[str, CostPair] | None
    parts: tuple[Part, ...] | None
    improvements: tuple[Improvement, ...] | None


@dataclass(frozen=True, slots=True)
class CodeTables:
    property_type: dict[int, str]
    built_form: dict[int, str]
    improvement: dict[int, str]


def decode(code: int, table: Mapping[int, str]) -> str | None:
    """The words for ``code``; ``None`` when the table does not hold it (never the raw code)."""
    return table.get(code)


def _fact(raw: dict[str, Any], key: str, where: str) -> Any | None:
    """The fact's value, or ``None`` when the certificate marks it missing."""
    fact = _get(raw, key, dict, where)
    if fact.get("status") == "missing":
        return None
    if "value" not in fact:
        message = f"{where}: '{key}' has neither a value nor a missing status."
        raise InvalidAreaDataError(message)
    return fact["value"]


def _whole(obj: dict[str, Any], key: str, where: str) -> int:
    value = obj.get(key)
    if type(value) is not int:
        message = f"{where}: '{key}' must be a whole number."
        raise InvalidAreaDataError(message)
    return value


def _date(raw: dict[str, Any], key: str, where: str) -> date:
    try:
        return date.fromisoformat(_get(raw, key, str, where))
    except ValueError as error:
        message = f"{where}: '{key}' is not a date: {error}"
        raise InvalidAreaDataError(message) from error


def _rating(raw: dict[str, Any], key: str, where: str) -> Rating | None:
    value = _fact(raw, key, where)
    if value is None:
        return None
    return Rating(_get(value, "band", str, where), _whole(value, "score", where))


def _code(raw: dict[str, Any], key: str, where: str) -> str | None:
    value = _fact(raw, key, where)
    if value is not None and not isinstance(value, str):
        message = f"{where}: '{key}' must be text."
        raise InvalidAreaDataError(message)
    return value


def _pence_of(raw: dict[str, Any], key: str, where: str) -> int:
    return _whole(_get(raw, key, dict, where), "pence", where)


def _costs(raw: dict[str, Any], where: str) -> dict[str, CostPair] | None:
    value = _fact(raw, "costs", where)
    if value is None:
        return None
    return {
        part: CostPair(
            _pence_of(_get(value, part, dict, where), "current", where),
            _pence_of(_get(value, part, dict, where), "potential", where),
        )
        for part in _COST_PARTS
    }


def _parts(raw: dict[str, Any], where: str) -> tuple[Part, ...] | None:
    value = _fact(raw, "parts", where)
    if value is None:
        return None
    return tuple(
        Part(
            _get(p, "part", str, where),
            _get(p, "description", str, where),
            _whole(p, "stars", where),
        )
        for p in value
    )


def _improvements(raw: dict[str, Any], where: str) -> tuple[Improvement, ...] | None:
    value = _fact(raw, "improvements", where)
    if value is None:
        return None
    return tuple(
        Improvement(
            _whole(i, "sequence", where),
            _whole(i, "improvementCode", where),
            _get(i, "indicativeCost", str, where),
            _pence_of(i, "typicalSaving", where),
        )
        for i in value
    )


def _certificate(raw: dict[str, Any]) -> Certificate:
    where = f"certificate {raw.get('number')}"
    area = _fact(raw, "totalFloorAreaSquareMetres", where)
    if area is not None and (type(area) is bool or not isinstance(area, (int, Fraction))):
        message = f"{where}: the floor area must be a number."
        raise InvalidAreaDataError(message)
    return Certificate(
        number=_get(raw, "number", str, where),
        country=_get(raw, "country", str, where),
        kind=_get(raw, "kind", str, where),
        status=_get(raw, "status", str, where),
        registration_date=_date(raw, "registrationDate", where),
        inspection_date=_date(raw, "inspectionDate", where),
        current_rating=_rating(raw, "currentRating", where),
        potential_rating=_rating(raw, "potentialRating", where),
        property_type_code=_code(raw, "propertyTypeCode", where),
        built_form_code=_code(raw, "builtFormCode", where),
        floor_area=area,
        costs=_costs(raw, where),
        parts=_parts(raw, where),
        improvements=_improvements(raw, where),
    )


def read_certificates(path: Path) -> tuple[Certificate, ...]:
    """Read ``energy-certificates.json``; refuse a repeated certificate number."""
    data = _load(path)
    certificates = tuple(_certificate(raw) for raw in _objects(data, "certificates", path.name))
    numbers = [c.number for c in certificates]
    if len(set(numbers)) != len(numbers):
        message = f"{path.name}: a certificate number appears twice."
        raise InvalidAreaDataError(message)
    return certificates


def _table(tables: dict[str, Any], name: str, where: str) -> dict[int, str]:
    raw = _get(tables, name, dict, where)
    found: dict[int, str] = {}
    for key, words in raw.items():
        if not key.isascii() or not key.isdigit() or not isinstance(words, str):
            message = f"{where}: table '{name}' has an entry that is not a code and words."
            raise InvalidAreaDataError(message)
        found[int(key)] = words
    return found


def read_code_tables(path: Path) -> CodeTables:
    """Read ``reference/energy-code-tables.json`` (codes become whole numbers)."""
    data = _load(path)
    tables = _get(data, "tables", dict, path.name)
    return CodeTables(
        property_type=_table(tables, "propertyType", path.name),
        built_form=_table(tables, "builtForm", path.name),
        improvement=_table(tables, "improvement", path.name),
    )
