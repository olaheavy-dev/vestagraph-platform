"""The AI-03 set is whole and consistent: unique IDs, real references, full coverage (AI-03).

These tests read the set and the specifications. A gap is fixed by adding the missing case, never
by weakening a test (README, "Coverage").
"""

import re
from typing import Any

import pytest
from ai03_support import (
    Case,
    _file,
    _scenarios,
    ai03_scenario_ids,
    atoms,
    duplicate_ids,
    forbidden_claim_hits,
    forbidden_hits,
    load_cases,
    normalise_numbers,
    number_hits,
    resolve,
    withdrawn_scenario_ids,
)
from fixtures_support import fixtures_directory

_CASES = load_cases()
_ID = re.compile(r"[A-Z]+-\d+")
_RULE_EXEMPT_GROUPS = {23, 25}  # tool choice (a quality matter) and latency (not yet measured)


def _cited_scenarios(case: Case) -> set[str]:
    cited = set(case["tests"])
    cited |= {i["from"] for i in case["expect"].get("mustInclude", []) if _ID.fullmatch(i["from"])}
    return cited | {s for s in case["sample"] if _ID.fullmatch(s)}


def test_ai03_set_case_ids_are_unique() -> None:
    assert duplicate_ids(_CASES) == []


def test_duplicate_ids_names_a_repeated_case() -> None:
    assert duplicate_ids([{"id": "A-01"}, {"id": "B-01"}, {"id": "A-01"}]) == ["A-01"]


def test_ai03_set_every_cited_scenario_exists() -> None:
    known = set(_scenarios())
    missing = [f"{c['id']}: {s}" for c in _CASES for s in c["tests"] if s not in known]
    assert missing == []


def test_ai03_set_no_case_cites_a_withdrawn_scenario() -> None:
    withdrawn = withdrawn_scenario_ids()
    assert withdrawn
    cited = [f"{c['id']}: {s}" for c in _CASES for s in _cited_scenarios(c) if s in withdrawn]
    assert cited == []


def test_ai03_set_every_sample_reference_exists() -> None:
    problems: list[str] = []
    for case in _CASES:
        stubs: list[dict[str, Any]] = case.get("stubs", [])
        sources = list(case["sample"]) + [i["from"] for i in case["expect"].get("mustInclude", [])]
        for source in sources:
            try:
                if source.startswith("stubs/"):
                    assert 0 <= int(source[6:]) < len(stubs)
                else:
                    assert resolve(source, stubs) is not None
            except KeyError, IndexError, ValueError, AssertionError:
                problems.append(f"{case['id']}: {source}")
    assert problems == []


def test_ai03_set_every_ai03_scenario_has_a_case() -> None:
    tagged = ai03_scenario_ids()
    assert tagged
    covered = {s for c in _CASES for s in _cited_scenarios(c)}
    assert sorted(tagged - covered) == []


def test_ai03_set_every_group_has_a_case() -> None:
    assert sorted(set(range(1, 26)) - {c["group"] for c in _CASES}) == []


def test_ai03_set_every_rule_group_has_a_rule_case() -> None:
    with_rule = {c["group"] for c in _CASES if c["kind"] == "rule"}
    assert sorted(set(range(1, 26)) - _RULE_EXEMPT_GROUPS - with_rule) == []


def test_ai03_set_expected_text_has_no_forbidden_word() -> None:
    hits: list[str] = []
    for case in _CASES:
        for item in case["expect"].get("mustInclude", []):
            if not _ID.fullmatch(item["from"]) or item["from"] == "TOOLS-18":
                # text quoted from a record or stub is quoted source (allowIn), and so is a
                # tool description's rule sentence (TOOLS-18, README mark 2)
                continue
            found = forbidden_claim_hits(item["text"])
            if found:
                hits.append(f"{case['id']}: {item['text']!r} {found}")
    assert hits == []


def test_ai03_set_expected_numbers_come_from_sample_or_stubs() -> None:
    stray: list[str] = []
    for case in _CASES:
        for item in case["expect"].get("mustInclude", []):
            if _ID.fullmatch(item["from"]):
                continue  # fixed wording quoted from a scenario
            extra = number_hits(case, item["text"])
            if extra:
                stray.append(f"{case['id']}: {item['text']!r} {extra}")
    assert stray == []


def _strings(case: Case) -> list[tuple[str, str]]:
    """Strings that must carry no typed figure: notes, ``why``, and other ``expect`` text."""
    found: list[tuple[str, str]] = [("notes", case.get("notes", ""))]
    expect = case["expect"]
    for item in expect.get("mustNotInclude", []):
        found.append(("why", item["why"]))
        if item["match"] == "literal":
            found.append(("literal", item["value"]))
    for key, value in expect.items():
        if key in {"mustInclude", "mustNotInclude", "toolCalls"}:
            continue
        found += [(key, v) for v in atoms(value)]
    return found


def _corpus() -> list[str]:
    """Every quoted source text: data and generated files, stubs, conversations, scenarios."""
    found: list[str] = list(_scenarios().values())
    for folder in ("data", "generated"):
        for path in sorted((fixtures_directory() / folder).glob("*.json")):
            found += list(atoms(_file(f"{folder}/{path.name}")))
    for case in _CASES:
        found += [s["text"] for s in case.get("stubs", [])]
        found += [t["text"] for t in case.get("conversation", [])]
    return found


def _without_references(text: str, corpus: list[str]) -> str:
    """``text`` without quotes found in a source, IDs, decision and rule numbers."""

    def keep_unquoted(match: re.Match[str]) -> str:
        quote = match.group(1) or match.group(2)
        return " " if any(quote.lower() in c.lower() for c in corpus) else match.group(0)

    text = re.sub(r"'([^']+)'|\"([^\"]+)\"", keep_unquoted, text)
    text = re.sub(r"\b[A-Za-z0-9]*[A-Za-z][A-Za-z0-9]*\d[A-Za-z0-9]*\b", " ", text)  # NB1, E06999
    text = re.sub(
        r"\b(?:[A-Z]+-|rules? |decisions? |[A-Z]{2,} rule )\d+\b", " ", text
    )  # TOOLS-03, rule 2
    text = re.sub(r"\b0\d{3}\b", " ", text)  # a bare decision number
    return re.sub(r"\b\d+[A-Za-z]+\b", " ", text)


def _sources(case: Case) -> list[str]:
    """What the case may take a figure from: its cited scenarios, records, stubs and turns."""
    stubs: list[dict[str, Any]] = case.get("stubs", [])
    found = [s["text"] for s in stubs] + [t["text"] for t in case.get("conversation", [])]
    for source in _cited_scenarios(case) | set(case["sample"]):
        found += list(atoms(resolve(source, stubs)))
    return found


def test_ai03_set_no_typed_digits_outside_quotes_or_ids() -> None:
    """A figure in notes or ``expect`` must be quoted from the case's own sources (rule 2).

    A stated limit such as the radius cap or the ten-place maximum is allowed when a cited
    scenario or record states it; any other figure is typed by hand and fails.
    """
    corpus = _corpus()
    problems: list[str] = []
    for case in _CASES:
        allowed = {n for chunk in _sources(case) for n in normalise_numbers(chunk)}
        for where, text in _strings(case):
            if where == "replyKind":
                continue  # an identifier from the schema's own list
            if where == "literal" and any(text.lower() in c.lower() for c in corpus):
                continue  # banned wording quoted from a record, a stub or a user turn
            free = normalise_numbers(_without_references(text, corpus))
            stray = [n for n in free if n not in allowed]
            if stray:
                problems.append(f"{case['id']} {where}: {stray} in {text[:90]!r}")
    assert problems == []


def test_forbidden_hits_unknown_place_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown place"):
        forbidden_hits("it is safe", "chat-window")


def test_normalise_numbers_decimals_match_on_both_sides() -> None:
    assert normalise_numbers("£1.50") == normalise_numbers("1.5") == ["1.5"]
    assert normalise_numbers("12.50 and 12.5") == ["12.5", "12.5"]


def _runner_checks(case: Case) -> set[str]:
    return set(case["expect"].get("runnerChecks", []))


def test_ai03_set_every_runner_check_in_the_enum_is_used() -> None:
    schema = _file("schema/ai-03-set.schema.json")
    enum = set(schema["$defs"]["expect"]["properties"]["runnerChecks"]["items"]["enum"])
    used = {check for case in _CASES for check in _runner_checks(case)}
    assert sorted(enum - used) == []


def test_ai03_set_privacy_cases_carry_the_leak_check() -> None:
    privacy = {"TOOLS-25", "TOOLS-26", "TOOLS-61"}
    missing = [
        c["id"]
        for c in _CASES
        if privacy & set(c["tests"]) and "no-argument-in-logs" not in _runner_checks(c)
    ]
    assert missing == []


def test_ai03_set_cases_with_a_targeted_stub_declare_the_placement_check() -> None:
    targeted = {"store-record", "place-name", "school-name", "council-name", "saved-area"}
    missing = [
        c["id"]
        for c in _CASES
        if any(s["channel"] in targeted for s in c.get("stubs", []))
        and "stub-text-only-at-target" not in _runner_checks(c)
    ]
    assert missing == []


def test_ai03_set_injection_cases_make_exactly_the_expected_calls() -> None:
    loose = [
        c["id"]
        for c in _CASES
        if c["id"].startswith(("CHAT-INJECT-", "COUNCIL-INJECT-ARGUMENT"))
        and c["shape"] == "model"
        and "toolCalls" in c["expect"]
        and not c["expect"].get("toolCallsExact")
    ]
    assert loose == []


def test_ai03_set_no_pass_example_contains_a_literal_the_case_bans() -> None:
    clashes: list[str] = []
    for case in _CASES:
        literals = [
            m["value"] for m in case["expect"].get("mustNotInclude", []) if m["match"] == "literal"
        ]
        for text in case.get("examples", {}).get("pass", []):
            clashes += [
                f"{case['id']}: {v}" for v in literals if re.search(re.escape(v), text, re.I)
            ]
    assert clashes == []
