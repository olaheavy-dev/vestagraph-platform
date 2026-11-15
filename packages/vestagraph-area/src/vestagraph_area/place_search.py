"""Find councils by place name (City Explorer).

Matching is on exact names after trimming, collapsing runs of spaces and ignoring case. There is
no fuzzy matching and no punctuation stripping. The search looks at council names, former
council names (note ``former-name``), counties, regions and place names. One match gives
``council``; several give ``choose`` and the search never picks one for the visitor. A place
outside England gives ``not-covered``; if the same name also matches England, the English
matches are listed with ``choose`` and the non-English one is added with note ``not-covered``
(a judgement call). Matches are listed by council name, then county.

The sample places are synthetic. Real data (stage 5b) will come from OS Open Names joined to
councils through a tested name table.
"""

from dataclasses import dataclass
from typing import Literal

from vestagraph_area.council_records import Council, CouncilArea

SearchKind = Literal["council", "choose", "not-found", "not-covered"]
MatchNote = Literal["former-name", "not-covered"]
ENGLAND = "england"


@dataclass(frozen=True, slots=True)
class Match:
    """One council the query could mean, with the label to show the visitor."""

    council_code: str
    label: str
    note: MatchNote | None


@dataclass(frozen=True, slots=True)
class SearchResult:
    """The kind of answer and its matches (empty for ``not-found`` and ``not-covered``)."""

    kind: SearchKind
    matches: tuple[Match, ...]


def _normalise(text: str) -> str:
    return " ".join(text.split()).casefold()


def _council_label(council: Council) -> str:
    return council.name if council.county is None else f"{council.name}, {council.county}"


def find_councils(query: str, area: CouncilArea) -> SearchResult:
    """Councils that the place name ``query`` could mean."""
    wanted = _normalise(query)
    if not wanted:
        return SearchResult("not-found", ())
    by_code = {c.code: c for c in area.councils}
    found: dict[str, tuple[str, str, Match]] = {}  # council code -> (sort name, county, match)
    outside: Match | None = None

    def add(council: Council, label: str, note: MatchNote | None) -> None:
        if council.code not in found:
            found[council.code] = (
                council.name,
                council.county or "",
                Match(council.code, label, note),
            )

    for council in area.councils:
        if _normalise(council.name) == wanted:
            if council.nation == ENGLAND:
                add(council, _council_label(council), None)
            else:
                outside = Match(council.code, f"{council.name} (not yet covered)", "not-covered")
    for council in area.councils:
        if council.nation == ENGLAND and any(_normalise(n) == wanted for n in council.former_names):
            add(council, _council_label(council), "former-name")
    for council in area.councils:
        if council.nation == ENGLAND and council.county and _normalise(council.county) == wanted:
            add(council, _council_label(council), None)
    for place in area.places:
        if wanted not in (_normalise(place.name), _normalise(place.region)):
            continue
        if place.nation != ENGLAND:
            outside = Match(
                place.council_codes[0],
                f"{place.name}, {place.county} (not yet covered)",
                "not-covered",
            )
            continue
        for code in place.council_codes:
            council = by_code[code]
            label = f"{place.name}, {place.county}"
            if len(place.council_codes) > 1:
                label = f"{label} ({council.name})"
            add(council, label, None)

    ordered = [m for _, _, m in sorted(found.values(), key=lambda item: (item[0], item[1]))]
    if outside is not None and not ordered:
        return SearchResult("not-covered", ())
    if outside is not None:
        ordered.append(outside)
    if not ordered:
        return SearchResult("not-found", ())
    if len(ordered) == 1:
        return SearchResult("council", tuple(ordered))
    return SearchResult("choose", tuple(ordered))


def council_for_postcode(postcode: str, area: CouncilArea) -> str | None:
    """Council code for a sample postcode (case and spaces ignored), or ``None``."""
    wanted = "".join(postcode.split()).casefold()
    for entry in area.postcodes:
        if "".join(entry.postcode.split()).casefold() == wanted:
            return entry.council_code
    return None
