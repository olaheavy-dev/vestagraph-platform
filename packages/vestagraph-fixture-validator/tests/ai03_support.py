"""Test-side helpers for the AI-03 marking references (AI-03, AI-14).

The 5b runner will own the real marking; these helpers apply the same rules to a case's
``examples`` (a set that obeys its own rules) and pin the behaviour the README describes. Every
function is plain code over plain data, so the runner can reuse them.
"""

import functools
import json
import re
from collections.abc import Iterator
from typing import Any

from fixtures_support import fixtures_directory, repository_root

Case = dict[str, Any]

_APOSTROPHE = "\N{RIGHT SINGLE QUOTATION MARK}"
_NUMBER = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")
_MIXED_TOKEN = re.compile(r"\b(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[A-Za-z])[A-Za-z0-9]+\b")
_LIST_MARKER = re.compile(r"(?m)^[ \t]*(\d{1,2})[.)][ \t]")
_LIMIT_KEYS = {"doesNotEstablish", "note"}
_NAME_KEYS = {"label", "name", "areaName", "largerAreaName", "text", "note", "doesNotEstablish"}


def _canonical(number: str) -> str:
    whole, _, fraction = number.replace(",", "").partition(".")
    whole = str(int(whole))
    fraction = fraction.rstrip("0")
    return f"{whole}.{fraction}" if fraction else whole


def normalise_numbers(text: str) -> list[str]:
    """Every number in ``text`` as plain digits.

    No £, no thousands commas, no % or unit; leading zeros and a trailing ``.0`` or ``.00`` are
    dropped (``07`` is ``7``; ``2,160.00`` is ``2160``). Decimals are kept (``12.5``).
    """
    return [_canonical(match) for match in _NUMBER.findall(text)]


def load_forbidden_words() -> dict[str, Any]:
    path = fixtures_directory() / "evaluation" / "forbidden-words.json"
    document: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return document


def mask_phrases(text: str, phrases: list[str]) -> str:
    """``text`` with every occurrence of each phrase removed (case-insensitive, longest first)."""
    for phrase in sorted({p for p in phrases if len(p) >= 3}, key=len, reverse=True):
        text = re.sub(re.escape(phrase), " ", text, flags=re.IGNORECASE)
    return text


def forbidden_hits(text: str, where: str) -> list[str]:
    """The forbidden words or phrases in ``text``; none when ``where`` is an allowed place.

    ``where`` is ``answer`` (the model's reply, or text a tool returns outside quoted-source
    fields) or one of the list's ``allowIn`` places, such as ``user-turn`` or ``quoted-source``.
    A word matches whole words only, so "Safestore" and "safety" never match "safe". Phrases in
    ``allowPhrases`` (a source's own metric name) are masked first.
    """
    document = load_forbidden_words()
    if where in document["allowIn"]:
        return []
    text = mask_phrases(text, document.get("allowPhrases", []))
    return [
        word
        for word in document["words"]
        if re.search(rf"\b{re.escape(word)}\b", text, flags=re.IGNORECASE)
    ]


# ---- reading the case's sources -------------------------------------------------------------


@functools.cache
def _file(name: str) -> Any:
    return json.loads((fixtures_directory() / name).read_text(encoding="utf-8"))


@functools.cache
def _scenarios() -> dict[str, str]:
    found: dict[str, str] = {}
    for path in (repository_root() / "docs" / "specs").rglob("*.feature"):
        lines = path.read_text(encoding="utf-8").split("\n")
        for index, line in enumerate(lines):
            match = re.match(r"\s*Scenario(?: Outline)?: ([A-Z]+-\d+)", line)
            if not match:
                continue
            block = [line]
            for follow in lines[index + 1 :]:
                if not follow.strip() or follow.strip().startswith(("Scenario", "@")):
                    break
                block.append(follow)
            found[match.group(1)] = "\n".join(block)
    return found


@functools.cache
def _records_by_id() -> dict[str, Any]:
    found: dict[str, Any] = {}

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if isinstance(value.get("id"), str):
                found.setdefault(value["id"], value)
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    for path in sorted((fixtures_directory() / "data").glob("*.json")):
        walk(json.loads(path.read_text(encoding="utf-8")))
    return found


def _pointer(source: str) -> Any:
    name, _, fragment = source.partition("#")
    value = _file(name)
    for part in fragment.split("/")[1:]:
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def resolve(source: str, stubs: list[dict[str, Any]]) -> Any:
    """The record, pointer target, scenario text or stub text a ``from`` or ``sample`` names."""
    if source.startswith("stubs/"):
        return stubs[int(source[6:])]["text"]
    if "#" in source:
        return _pointer(source)
    if source in _records_by_id():
        return _records_by_id()[source]
    return _scenarios()[source]


def atoms(value: Any) -> Iterator[str]:
    """Every string and number inside ``value``, keys left out."""
    if isinstance(value, dict):
        for item in value.values():
            yield from atoms(item)
    elif isinstance(value, list):
        for item in value:
            yield from atoms(item)
    elif isinstance(value, bool) or value is None:
        return
    else:
        yield str(value)


def _keyed(value: Any, keys: set[str]) -> Iterator[str]:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in keys and isinstance(item, str):
                yield item
            else:
                yield from _keyed(item, keys)
    elif isinstance(value, list):
        for item in value:
            yield from _keyed(item, keys)


def _records(case: Case) -> list[Any]:
    stubs = case.get("stubs", [])
    return [resolve(source, stubs) for source in case["sample"]]


def _quoted(case: Case, *, limits_only: bool) -> list[str]:
    """Strings the tool quotes from a source: all of them, or only the limit fields."""
    found: list[str] = []
    for record in _records(case):
        if isinstance(record, str):
            continue
        if isinstance(record, dict) and "topic" in record and "label" in record:
            link = record.get("link") or {}
            found += [record[key] for key in _LIMIT_KEYS if isinstance(record.get(key), str)]
            if link.get("text"):
                found.append(link["text"])
            if not limits_only:
                found.append(record["label"])
                found += [s for s in atoms(record.get("value")) if " " in s.strip()]
        else:
            keys = _LIMIT_KEYS if limits_only else _NAME_KEYS
            found += list(_keyed(record, keys))
    return found


def _stub_texts(case: Case) -> list[str]:
    return [stub["text"] for stub in case.get("stubs", [])]


def _user_turns(case: Case) -> list[str]:
    return [t["text"] for t in case.get("conversation", []) if t["role"] == "user"]


# ---- the marks ------------------------------------------------------------------------------


def literal_hit(text: str, value: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(value)}(?!\w)", text, flags=re.IGNORECASE) is not None


def _fixed_wording(case: Case) -> list[str]:
    return [
        item["text"]
        for item in case["expect"].get("mustInclude", [])
        if re.fullmatch(r"[A-Z]+-\d+", item["from"])
    ]


def number_hits(case: Case, text: str) -> list[str]:
    """Numbers in ``text`` that no cited sample record or stub holds (README mark 1).

    Not counted: list markers counting up from 1, identifiers (digits touching letters) that a
    tool result or the user's turn holds, and numbers inside fixed wording the case quotes from a
    scenario. A pence amount also matches the same amount in pounds when it divides by 100. A
    number the user typed is not an allowed extra.
    """
    corpus = [s for record in _records(case) for s in atoms(record)] + _stub_texts(case)
    allowed: set[str] = set()
    for chunk in corpus:
        for found in normalise_numbers(chunk):
            allowed.add(found)
            if "." not in found and int(found) >= 100 and int(found) % 100 == 0:
                allowed.add(str(int(found) // 100))
    known = {
        token.lower()
        for chunk in corpus + _user_turns(case)
        for token in _MIXED_TOKEN.findall(chunk)
    }
    for chunk in _fixed_wording(case):
        text = text.replace(chunk, " ")
    markers = _LIST_MARKER.findall(text)
    if markers and [int(m) for m in markers] == list(range(1, len(markers) + 1)):
        text = _LIST_MARKER.sub(" ", text)
    text = _MIXED_TOKEN.sub(lambda m: " " if m.group(0).lower() in known else m.group(0), text)
    return [n for n in normalise_numbers(text) if n not in allowed]


def mark(case: Case, text: str) -> list[str]:
    """What fails in ``text`` among the case's code marks (not ``mustInclude``).

    Masking follows the README: for a model answer the runner first masks every verbatim stub
    text and quoted-source field; for a tool result the literal and pattern checks skip the limit
    fields and the forbidden-word check skips every quoted-source field.
    """
    failures: list[str] = []
    model = case["shape"] == "model"
    plain = (
        mask_phrases(text, _stub_texts(case) + _quoted(case, limits_only=False)) if model else text
    )
    for_rules = plain if model else mask_phrases(text, _quoted(case, limits_only=True))
    for_words = plain if model else mask_phrases(text, _quoted(case, limits_only=False))
    for item in case["expect"].get("mustNotInclude", []):
        if item["match"] == "forbidden-words":
            hits = forbidden_hits(for_words, "answer")
            if hits:
                failures.append(f"forbidden words {hits}")
        elif item["match"] == "literal":
            if literal_hit(for_rules, item["value"]):
                failures.append(f"literal {item['value']!r}")
        elif re.search(item["value"], for_rules):
            failures.append(f"pattern {item['value'][:40]!r}")
    if case["expect"].get("numbersFrom") == "tool-results-only":
        extra = number_hits(case, text)
        if extra:
            failures.append(f"numbers {extra}")
    return failures


def include_misses(case: Case, text: str) -> list[str]:
    """``mustInclude`` items missing from ``text`` (ignoring case; numbers by number rules)."""
    lowered = text.replace(_APOSTROPHE, "'").lower()
    present = set(normalise_numbers(text))
    missing: list[str] = []
    for item in case["expect"].get("mustInclude", []):
        wanted = item["text"].replace(_APOSTROPHE, "'")
        if re.fullmatch(_NUMBER, wanted):
            ok = _canonical(wanted) in present
        else:
            ok = wanted.lower() in lowered
        if not ok:
            missing.append(item["text"])
    return missing
