"""Reads ``council-area.json`` into this package's own types (City Explorer).

The file is checked against its schema by ``make validate``. Like ``records.py``, this reader
refuses anything it does not understand with an ``InvalidAreaDataError``, including the checks a
schema cannot express: unique and increasing series periods, a recorded series with a usable
point, unique rate bands, and place and postcode codes that name a council. Decimals are exact
``Fraction`` values and no ``float`` is ever made (AGENTS rule 2); ``NaN``, ``Infinity``,
exponents, duplicate keys, bad UTF-8 and over-deep nesting are refused by the shared JSON loader.
A gap status never carries a value (rule 7).
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import Any

from vestagraph_area.records import (
    _PLAIN_DECIMAL,
    InvalidAreaDataError,
    _get,
    _load,
    _objects,
    _optional_string,
    _strings,
)

FACT_STATUSES = frozenset({"recorded", "no-record-in-source", "source-failed", "not-covered"})
POINT_STATUSES = frozenset({"recorded", "provisional", "not-published"})
POINT_STATUSES_WITH_VALUE = frozenset({"recorded", "provisional"})
SERIES_UNITS = frozenset({"pence-per-month", "pence", "ratio"})
BAND_LETTERS = ("A", "B", "C", "D", "E", "F", "G", "H")
TENURE_KEYS = ("ownedOutright", "ownedWithMortgage", "socialRented", "privateRented", "other")
NATIONS = frozenset({"england", "wales", "scotland", "northern-ireland"})
PRODUCTS = frozenset({"2-year-fixed", "5-year-fixed"})


@dataclass(frozen=True, slots=True)
class Level:
    """How local the figure is (local authority, neighbourhood, region or country)."""

    kind: str
    name: str


@dataclass(frozen=True, slots=True)
class Source:
    """Where a figure comes from."""

    label: str
    url: str
    edition: str
    period: str
    synthetic: bool


@dataclass(frozen=True, slots=True)
class Fact:
    """A single recorded figure, or a gap. ``value`` is ``None`` for every gap status."""

    status: str
    value: Any
    level: Level
    source: Source


@dataclass(frozen=True, slots=True)
class SeriesPoint:
    """One period of a series. ``value`` is whole pence, or a ``Fraction`` for a ratio."""

    period: str
    status: str
    value: int | Fraction | None
    method_break_before: bool


@dataclass(frozen=True, slots=True)
class Series:
    """A time series; ``points`` is empty for every gap status."""

    status: str
    unit: str
    points: tuple[SeriesPoint, ...]
    level: Level
    source: Source


@dataclass(frozen=True, slots=True)
class Neighbourhood:
    """A neighbourhood (LSOA) and its facts."""

    code: str
    short_code: str
    larger_area_name: str
    connectivity: Fact
    deprivation: Fact
    tenure: Fact


@dataclass(frozen=True, slots=True)
class Council:
    """A council and its facts and series."""

    code: str
    name: str
    nation: str
    tier: str
    county: str | None
    formed_on: str | None
    former_names: tuple[str, ...]
    population: Fact
    bands: Fact
    rent_series: Series
    price_series: Series
    affordability_series: Series
    tenure: Fact
    connectivity: Fact
    neighbourhoods: tuple[Neighbourhood, ...]


@dataclass(frozen=True, slots=True)
class PlaceName:
    """A place name and the councils it falls in."""

    name: str
    county: str
    region: str
    nation: str
    council_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PostcodeEntry:
    """A sample postcode and its council."""

    postcode: str
    council_code: str


@dataclass(frozen=True, slots=True)
class RateBand:
    """A quoted mortgage rate for a product and a loan-to-value ceiling."""

    product: str
    max_loan_to_value_percent: int
    rate_basis_points: int
    month: str
    source: Source


@dataclass(frozen=True, slots=True)
class CouncilArea:
    """The whole file."""

    councils: tuple[Council, ...]
    places: tuple[PlaceName, ...]
    postcodes: tuple[PostcodeEntry, ...]
    rate_bands: tuple[RateBand, ...]


def _whole(obj: dict[str, Any], key: str, where: str, *, minimum: int) -> int:
    value: int = _get(obj, key, int, where)
    if value < minimum:
        message = f"{where}: field '{key}' must be at least {minimum}."
        raise InvalidAreaDataError(message)
    return value


def _dict(obj: dict[str, Any], key: str, where: str) -> dict[str, Any]:
    value: dict[str, Any] = _get(obj, key, dict, where)
    return value


def _exact_keys(obj: dict[str, Any], keys: tuple[str, ...], where: str) -> None:
    if set(obj) != set(keys):
        message = f"{where}: must hold exactly the keys {', '.join(keys)}."
        raise InvalidAreaDataError(message)


def _level(raw: dict[str, Any], where: str) -> Level:
    level = _dict(raw, "level", where)
    return Level(kind=_get(level, "kind", str, where), name=_get(level, "name", str, where))


def _source(raw: dict[str, Any], where: str) -> Source:
    source = _dict(raw, "source", where)
    return Source(
        label=_get(source, "label", str, where),
        url=_get(source, "url", str, where),
        edition=_get(source, "edition", str, where),
        period=_get(source, "period", str, where),
        synthetic=_get(source, "synthetic", bool, where),
    )


def _decimal(text: str, where: str) -> Fraction:
    if _PLAIN_DECIMAL.fullmatch(text) is None:
        message = f"{where}: {text!r} is not a plain decimal number."
        raise InvalidAreaDataError(message)
    return Fraction(text)


def _band_value(value: Any, where: str) -> dict[str, int]:
    if not isinstance(value, dict):
        message = f"{where}: 'value' must be an object."
        raise InvalidAreaDataError(message)
    _exact_keys(value, BAND_LETTERS, where)
    return {letter: _whole(value, letter, where, minimum=1) for letter in BAND_LETTERS}


def _tenure_value(value: Any, where: str) -> dict[str, int]:
    if not isinstance(value, dict):
        message = f"{where}: 'value' must be an object."
        raise InvalidAreaDataError(message)
    _exact_keys(value, TENURE_KEYS, where)
    return {key: _whole(value, key, where, minimum=0) for key in TENURE_KEYS}


def _connectivity_value(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        message = f"{where}: 'value' must be an object."
        raise InvalidAreaDataError(message)
    _exact_keys(value, ("score", "decile"), where)
    decile = _whole(value, "decile", where, minimum=1)
    if decile > 10:
        message = f"{where}: decile must be between 1 and 10."
        raise InvalidAreaDataError(message)
    score = _decimal(_get(value, "score", str, where), where)
    return {"score": score, "decile": decile}


def _deprivation_value(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        message = f"{where}: 'value' must be an object."
        raise InvalidAreaDataError(message)
    _exact_keys(value, ("decile", "rank", "ofAreas", "edition"), where)
    decile = _whole(value, "decile", where, minimum=1)
    if decile > 10:
        message = f"{where}: decile must be between 1 and 10."
        raise InvalidAreaDataError(message)
    return {
        "decile": decile,
        "rank": _whole(value, "rank", where, minimum=1),
        "ofAreas": _whole(value, "ofAreas", where, minimum=1),
        "edition": _get(value, "edition", str, where),
    }


def _population_value(value: Any, where: str) -> int:
    if type(value) is not int or value < 1:
        message = f"{where}: 'value' must be a whole number of at least 1."
        raise InvalidAreaDataError(message)
    return value


def _fact(raw: dict[str, Any], name: str, parse_value: Any, where: str) -> Fact:
    here = f"{where} {name}"
    status = _get(raw, "status", str, here)
    if status not in FACT_STATUSES:
        message = f"{here}: unknown status '{status}'."
        raise InvalidAreaDataError(message)
    value: Any = None
    if status == "recorded":
        if "value" not in raw:
            message = f"{here}: a recorded fact needs a 'value'."
            raise InvalidAreaDataError(message)
        value = parse_value(raw["value"], here)
    elif "value" in raw:
        message = f"{here}: status '{status}' must not carry a value."
        raise InvalidAreaDataError(message)
    return Fact(status=status, value=value, level=_level(raw, here), source=_source(raw, here))


def _period_key(period: str, where: str) -> tuple[int, int]:
    if len(period) == 4 and period.isascii() and period.isdigit():
        return int(period), 0
    if (
        len(period) == 7
        and period[4] == "-"
        and period[:4].isascii()
        and period[:4].isdigit()
        and period[5:].isascii()
        and period[5:].isdigit()
        and 1 <= int(period[5:]) <= 12
    ):
        return int(period[:4]), int(period[5:])
    message = f"{where}: period {period!r} is not YYYY or YYYY-MM."
    raise InvalidAreaDataError(message)


def _point(raw: dict[str, Any], unit: str, where: str) -> SeriesPoint:
    period = _get(raw, "period", str, where)
    here = f"{where} point {period}"
    status = _get(raw, "status", str, here)
    if status not in POINT_STATUSES:
        message = f"{here}: unknown point status '{status}'."
        raise InvalidAreaDataError(message)
    value: int | Fraction | None = None
    if status in POINT_STATUSES_WITH_VALUE:
        if "value" not in raw:
            message = f"{here}: a {status} point needs a 'value'."
            raise InvalidAreaDataError(message)
        if unit == "ratio":
            value = _decimal(_get(raw, "value", str, here), here)
            if value == 0:
                message = f"{here}: a value of zero is refused; say 'not-published' instead."
                raise InvalidAreaDataError(message)
        else:
            value = _whole(raw, "value", here, minimum=1)
    elif "value" in raw:
        message = f"{here}: status '{status}' must not carry a value."
        raise InvalidAreaDataError(message)
    if "methodBreakBefore" in raw and raw["methodBreakBefore"] is not True:
        message = f"{here}: 'methodBreakBefore' can only be true."
        raise InvalidAreaDataError(message)
    return SeriesPoint(
        period=period,
        status=status,
        value=value,
        method_break_before="methodBreakBefore" in raw,
    )


def _series(raw: dict[str, Any], name: str, where: str) -> Series:
    here = f"{where} {name}"
    status = _get(raw, "status", str, here)
    if status not in FACT_STATUSES:
        message = f"{here}: unknown status '{status}'."
        raise InvalidAreaDataError(message)
    unit = _get(raw, "unit", str, here)
    if unit not in SERIES_UNITS:
        message = f"{here}: unknown unit '{unit}'."
        raise InvalidAreaDataError(message)
    points = tuple(_point(p, unit, here) for p in _objects(raw, "points", here))
    if status != "recorded" and points:
        message = f"{here}: status '{status}' must not carry points."
        raise InvalidAreaDataError(message)
    if status == "recorded" and not any(p.status in POINT_STATUSES_WITH_VALUE for p in points):
        message = f"{here}: a recorded series needs at least one recorded or provisional point."
        raise InvalidAreaDataError(message)
    keys = [_period_key(p.period, here) for p in points]
    if any(later <= earlier for earlier, later in pairwise(keys)):
        message = f"{here}: periods must be unique and strictly increasing."
        raise InvalidAreaDataError(message)
    return Series(
        status=status, unit=unit, points=points, level=_level(raw, here), source=_source(raw, here)
    )


def _neighbourhood(raw: dict[str, Any], where: str) -> Neighbourhood:
    code = _get(raw, "code", str, where)
    here = f"{where} neighbourhood {code}"
    facts = _dict(raw, "facts", here)
    _exact_keys(facts, ("connectivity", "deprivation", "tenure"), here)
    return Neighbourhood(
        code=code,
        short_code=_get(raw, "shortCode", str, here),
        larger_area_name=_get(raw, "largerAreaName", str, here),
        connectivity=_fact(
            _dict(facts, "connectivity", here), "connectivity", _connectivity_value, here
        ),
        deprivation=_fact(
            _dict(facts, "deprivation", here), "deprivation", _deprivation_value, here
        ),
        tenure=_fact(_dict(facts, "tenure", here), "tenure", _tenure_value, here),
    )


def _council(raw: dict[str, Any]) -> Council:
    code = _get(raw, "code", str, "council")
    where = f"council {code}"
    nation = _get(raw, "nation", str, where)
    if nation not in NATIONS:
        message = f"{where}: unknown nation '{nation}'."
        raise InvalidAreaDataError(message)
    tier = _get(raw, "tier", str, where)
    if tier not in ("unitary", "district"):
        message = f"{where}: unknown tier '{tier}'."
        raise InvalidAreaDataError(message)
    county = _optional_string(raw, "county", where)
    if tier == "district" and county is None:
        message = f"{where}: a district needs a 'county'."
        raise InvalidAreaDataError(message)
    return Council(
        code=code,
        name=_get(raw, "name", str, where),
        nation=nation,
        tier=tier,
        county=county,
        formed_on=_optional_string(raw, "formedOn", where),
        former_names=_strings(raw, "formerNames", where, required=False),
        population=_fact(_dict(raw, "population", where), "population", _population_value, where),
        bands=_fact(_dict(raw, "bands", where), "bands", _band_value, where),
        rent_series=_series(_dict(raw, "rentSeries", where), "rentSeries", where),
        price_series=_series(_dict(raw, "priceSeries", where), "priceSeries", where),
        affordability_series=_series(
            _dict(raw, "affordabilitySeries", where), "affordabilitySeries", where
        ),
        tenure=_fact(_dict(raw, "tenure", where), "tenure", _tenure_value, where),
        connectivity=_fact(
            _dict(raw, "connectivity", where), "connectivity", _connectivity_value, where
        ),
        neighbourhoods=tuple(
            _neighbourhood(n, where) for n in _objects(raw, "neighbourhoods", where)
        ),
    )


def _place(raw: dict[str, Any]) -> PlaceName:
    name = _get(raw, "name", str, "place")
    where = f"place '{name}'"
    nation = _get(raw, "nation", str, where)
    if nation not in NATIONS:
        message = f"{where}: unknown nation '{nation}'."
        raise InvalidAreaDataError(message)
    return PlaceName(
        name=name,
        county=_get(raw, "county", str, where),
        region=_get(raw, "region", str, where),
        nation=nation,
        council_codes=_strings(raw, "councilCodes", where, required=True),
    )


def _rate_band(raw: dict[str, Any]) -> RateBand:
    product = _get(raw, "product", str, "rate band")
    if product not in PRODUCTS:
        message = f"rate band: unknown product '{product}'."
        raise InvalidAreaDataError(message)
    where = f"rate band {product}"
    ltv = _whole(raw, "maxLoanToValuePercent", where, minimum=1)
    if ltv > 100:
        message = f"{where}: maxLoanToValuePercent must be at most 100."
        raise InvalidAreaDataError(message)
    return RateBand(
        product=product,
        max_loan_to_value_percent=ltv,
        rate_basis_points=_whole(raw, "rateBasisPoints", where, minimum=1),
        month=_get(raw, "month", str, where),
        source=_source(raw, where),
    )


def _check_references(area: CouncilArea, file_name: str) -> None:
    codes = [c.code for c in area.councils]
    if len(set(codes)) != len(codes):
        message = f"{file_name}: council codes must be unique."
        raise InvalidAreaDataError(message)
    known = set(codes)
    for place in area.places:
        if place.nation != "england":
            continue  # Not yet covered: allowed to have no council record.
        for code in place.council_codes:
            if code not in known:
                message = f"{file_name}: place '{place.name}' names unknown council code {code}."
                raise InvalidAreaDataError(message)
    for entry in area.postcodes:
        if entry.council_code not in known:
            message = (
                f"{file_name}: postcode {entry.postcode} names unknown council code "
                f"{entry.council_code}."
            )
            raise InvalidAreaDataError(message)
    bands = [(b.product, b.max_loan_to_value_percent) for b in area.rate_bands]
    if len(set(bands)) != len(bands):
        message = f"{file_name}: rate bands must be unique by product and loan-to-value."
        raise InvalidAreaDataError(message)


def read_council_area(path: Path) -> CouncilArea:
    """Read ``council-area.json``."""
    data = _load(path)
    where = path.name
    area = CouncilArea(
        councils=tuple(_council(raw) for raw in _objects(data, "councils", where)),
        places=tuple(_place(raw) for raw in _objects(data, "places", where)),
        postcodes=tuple(
            PostcodeEntry(
                postcode=_get(raw, "postcode", str, "postcode entry"),
                council_code=_get(raw, "councilCode", str, "postcode entry"),
            )
            for raw in _objects(data, "postcodes", where)
        ),
        rate_bands=tuple(_rate_band(raw) for raw in _objects(data, "rateBands", where)),
    )
    _check_references(area, where)
    return area
