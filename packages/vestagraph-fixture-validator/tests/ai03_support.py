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


_ONES = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}
_TENS = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}
_MEASURE = (
    r"(?=[- ]?(?:minutes?|mins?|hours?|miles?|km|kilometres?|metres?|meters?|percent|per cent"
    r"|pounds?|out of|years?)\b)"
)
_NUMBER_WORD = re.compile(
    r"\b(?:("
    + "|".join(_TENS)
    + r")(?:[- ]("
    + "|".join(list(_ONES)[1:10])
    + r"))?|("
    + "|".join(_ONES)
    + r"))\b"
    + _MEASURE,
    re.IGNORECASE,
)
_HALF = re.compile(r"\bhalf(?= an? (?:mile|hour|kilometre|minute)\b)", re.IGNORECASE)


def number_words_to_digits(text: str) -> str:
    """Number words that state a measure or a score become digits (WCHAT-70).

    "seven out of ten" is 7 out of ten and "a ten-minute stroll" is 10; a count in running prose
    such as "two councils match" is left alone, so a correct list is not read as a figure.
    """

    def convert(match: re.Match[str]) -> str:
        tens, ones, plain = match.group(1), match.group(2), match.group(3)
        if plain:
            return str(_ONES[plain.lower()])
        value = _TENS[tens.lower()] + (_ONES[ones.lower()] if ones else 0)
        return str(value)

    return _HALF.sub("0.5", _NUMBER_WORD.sub(convert, text))


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
    return [_canonical(match) for match in _NUMBER.findall(number_words_to_digits(text))]


def load_forbidden_words() -> dict[str, Any]:
    path = fixtures_directory() / "evaluation" / "forbidden-words.json"
    document: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return document


def mask_phrases(text: str, phrases: list[str]) -> str:
    """``text`` with every occurrence of each phrase removed (case-insensitive, longest first)."""
    for phrase in sorted({p for p in phrases if len(p) >= 3}, key=len, reverse=True):
        text = re.sub(re.escape(phrase), " ", text, flags=re.IGNORECASE)
    return text


def mask_runs(text: str, source: str, min_words: int = 4) -> str:
    """``text`` without any run of ``min_words`` or more words copied verbatim from ``source``."""
    words = source.split()
    for start in range(len(words)):
        for end in range(len(words), start + min_words - 1, -1):
            phrase = " ".join(words[start:end])
            if re.search(re.escape(phrase), text, flags=re.IGNORECASE):
                text = mask_phrases(text, [phrase])
                break
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


_CLAUSE = re.compile(r"[.!?;\n]+|\b(?:but|though|although|however|yet|whereas|while)\b|—|:", re.I)
_NEGATION = re.compile(
    r"\bno\b(?!,)|\b(?:not|never|neither|nor|no one|nobody|cannot|won't|can't|don't|doesn't"
    r"|isn't|aren't|wouldn't|shouldn't)\b|n't\b|n\N{RIGHT SINGLE QUOTATION MARK}t\b",
    re.I,
)
_FRAME = re.compile(r"\b(?:whether|if)\b", re.I)


def claim_word_hits(text: str, words: list[str], window: int = 10) -> list[str]:
    """Forbidden words that no negation in the same clause governs (README mark 2).

    A negation excuses only words after it in its own clause, within ``window`` words. A clause
    ends at a full stop, ``;``, ``:``, a dash or a contrast word (but, though, however...), and a
    ``whether`` or ``if`` frame ends at a comma. So "I can't say it is safe" and "Neither is
    better or worse" pass, and "It isn't perfect, but the area is safe" fails.
    """
    pattern = re.compile(r"(?i)\b(" + "|".join(re.escape(w) for w in words) + r")\b")
    hits: list[str] = []
    for clause in _CLAUSE.split(text):
        for match in pattern.finditer(clause or ""):
            before = clause[: match.start()]
            if _NEGATION.search(" ".join(before.split()[-window:])):
                continue
            if _FRAME.search(before.split(",")[-1]):
                continue
            hits.append(match.group(1))
    return hits


def forbidden_claim_hits(text: str) -> list[str]:
    """The forbidden-word list applied to a model answer: claims only, negations excused."""
    document = load_forbidden_words()
    return claim_word_hits(mask_phrases(text, document.get("allowPhrases", [])), document["words"])


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


_PENCE_UNITS = {"pence", "pence-per-month"}


def pence_amounts(value: Any, in_pence: bool = False) -> Iterator[int]:
    """Whole numbers in pence fields: a series with a pence unit, ``bands`` and ``*Pence`` keys."""
    if isinstance(value, dict):
        in_pence = in_pence or value.get("unit") in _PENCE_UNITS
        for key, item in value.items():
            marked = in_pence or key == "bands" or key.endswith("Pence")
            if isinstance(item, int) and not isinstance(item, bool) and marked and key != "unit":
                yield item
            else:
                yield from pence_amounts(item, marked)
    elif isinstance(value, list):
        for item in value:
            yield from pence_amounts(item, in_pence)
    elif isinstance(value, int) and not isinstance(value, bool) and in_pence:
        yield value


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
        allowed.update(normalise_numbers(chunk))
    for record in _records(case):
        for amount in pence_amounts(record):
            if amount % 100 == 0:
                allowed.add(str(amount // 100))
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
    plain = text
    if model:
        plain = mask_phrases(text, _stub_texts(case) + _quoted(case, limits_only=False))
        for stub in _stub_texts(case):
            plain = mask_runs(plain, stub)
    for_rules = plain if model else mask_phrases(text, _quoted(case, limits_only=True))
    for_words = plain if model else mask_phrases(text, _quoted(case, limits_only=False))
    for item in case["expect"].get("mustNotInclude", []):
        if item["match"] == "forbidden-words":
            hits = forbidden_claim_hits(for_words) if model else forbidden_hits(for_words, "answer")
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
