"""Council search by place name and postcode, over the synthetic sample places."""

from functools import cache

from area_support import fixtures_directory
from vestagraph_area.council_records import CouncilArea, read_council_area
from vestagraph_area.place_search import Match, council_for_postcode, find_councils

NORTHBRIDGE = "E06999001"
SOUTHVALE = "E06999002"
EASTMERE = "E07999001"
WESTMERE = "E07999002"


@cache
def _area() -> CouncilArea:
    return read_council_area(fixtures_directory() / "data" / "council-area.json")


def test_find_councils_same_name_in_two_counties_is_choose_with_counties() -> None:
    result = find_councils("Newbury (synthetic)", _area())

    assert result.kind == "choose"
    assert result.matches == (
        Match(EASTMERE, "Newbury (synthetic), Westshire (synthetic)", None),
        Match(SOUTHVALE, "Newbury (synthetic), Southshire (synthetic)", None),
    )


def test_find_councils_county_lists_its_districts() -> None:
    result = find_councils("westshire (synthetic)", _area())

    assert result.kind == "choose"
    assert [m.council_code for m in result.matches] == [EASTMERE, WESTMERE]


def test_find_councils_former_name_leads_to_current_with_note() -> None:
    result = find_councils("East Westshire Borough (synthetic)", _area())

    assert result.kind == "council"
    assert result.matches == (
        Match(EASTMERE, "Eastmere (synthetic), Westshire (synthetic)", "former-name"),
    )


def test_find_councils_welsh_place_is_not_covered() -> None:
    result = find_councils("Afonbryn (synthetic)", _area())

    assert result.kind == "not-covered"
    assert result.matches == ()


def test_find_councils_unknown_is_not_found() -> None:
    result = find_councils("Nowhere", _area())

    assert result.kind == "not-found"
    assert result.matches == ()


def test_find_councils_blank_query_is_not_found() -> None:
    assert find_councils("   ", _area()).kind == "not-found"


def test_find_councils_region_lists_several_councils() -> None:
    result = find_councils("Capital (synthetic)", _area())

    assert result.kind == "choose"
    assert [m.council_code for m in result.matches] == [NORTHBRIDGE, SOUTHVALE]


def test_find_councils_place_spanning_two_councils_is_choose() -> None:
    result = find_councils("Eastmere Westmere Fields (synthetic)", _area())

    assert result.kind == "choose"
    assert [m.council_code for m in result.matches] == [EASTMERE, WESTMERE]


def test_find_councils_single_council_name_is_council_and_never_fuzzy() -> None:
    exact = find_councils("  northbridge   (SYNTHETIC) ", _area())
    near = find_councils("Northbrige (synthetic)", _area())

    assert exact.kind == "council"
    assert [m.council_code for m in exact.matches] == [NORTHBRIDGE]
    assert near.kind == "not-found"


def test_find_councils_english_and_welsh_same_name_lists_both_with_not_covered_note() -> None:
    base = _area()
    welsh = next(p for p in base.places if p.nation == "wales")
    clash = type(welsh)(
        "Northbridge (synthetic)", welsh.county, welsh.region, "wales", welsh.council_codes
    )
    area = CouncilArea(base.councils, (*base.places, clash), base.postcodes, base.rate_bands)

    result = find_councils("Northbridge (synthetic)", area)

    assert result.kind == "choose"
    assert [m.note for m in result.matches] == [None, "not-covered"]


def test_council_for_postcode_in_another_council_returns_that_council() -> None:
    assert council_for_postcode("sv2  3ab", _area()) == SOUTHVALE
    assert council_for_postcode("NB1 4XY", _area()) == NORTHBRIDGE


def test_council_for_postcode_unknown_is_none() -> None:
    assert council_for_postcode("ZZ9 9ZZ", _area()) is None
