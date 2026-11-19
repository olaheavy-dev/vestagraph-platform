"""Test-side helpers for the AI-03 marking references (AI-03, AI-14).

The 5b runner will own the real marking; these helpers apply the same rules to a case's
``examples`` (a set that obeys its own rules) and pin the behaviour the README describes. Every
function is plain code over plain data, so the runner can reuse them.
"""

import functools
import json
import re
import unicodedata
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
    whole = whole.lstrip("0") or "0"
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


_ENDORSEMENT = re.compile(
    r"\b(?:agree|agreed|agrees|right|true|correct|indeed|confirm|confirmed|exactly|stand by"
    r"|(?:fully )?back (?:that|this|it)|spot on|that['\u2019]?s accurate|i['\u2019]d say so)\b",
    re.I,
)
_FRAME_COLON = re.compile(
    r"\b(?:says?|said|reads?|shows?|titled|named|called|listed as|stored as|written as|quote[sd]?)"
    r"\s*:\s*$",
    re.I,
)
_SENTENCE_END = ".!?;\n"
_CURLY = ("\N{LEFT DOUBLE QUOTATION MARK}", "\N{RIGHT DOUBLE QUOTATION MARK}")
_SINGLE = ("\N{LEFT SINGLE QUOTATION MARK}", "\N{RIGHT SINGLE QUOTATION MARK}")


def _inside_balanced_quotes(text: str, start: int, end: int) -> bool:
    """Is ``start:end`` inside a balanced pair of quotes? An unclosed quote excuses nothing."""
    before, after = text[:start], text[end:]
    for opening, closing in (_CURLY, _SINGLE):
        if before.count(opening) > before.count(closing) and closing in after:
            return True
    return before.count('"') % 2 == 1 and '"' in after


def _presented_as_quote(text: str, start: int, end: int) -> bool:
    """Is the copied run at ``start:end`` shown as a quote, and not endorsed?

    A run is a quote when it lies inside balanced quotation marks (straight or curly), or when it
    follows a reporting frame and a colon in its own sentence ("The place reads: ..."). A
    sentence with an agreement word (agree, right, true, indeed, confirm...) is never excused,
    and a frame without a colon ("As the record shows, ...") excuses nothing.
    """
    before = text[:start]
    begin = max(before.rfind(c) for c in _SENTENCE_END) + 1
    after = [text.find(c, end) for c in _SENTENCE_END if text.find(c, end) != -1]
    stop = min(after) if after else len(text)
    if _ENDORSEMENT.search(text[begin:stop]):
        return False
    return (
        _inside_balanced_quotes(text, start, end) or _FRAME_COLON.search(before[begin:]) is not None
    )


def mask_runs(text: str, source: str, min_words: int = 4) -> str:
    """``text`` without runs of words copied verbatim from ``source`` and shown as a quote.

    A run is ``min_words`` or more words (the whole source if it is shorter). A run that is not
    presented as a quote, or sits in a sentence that agrees with it, stays and is marked.
    """
    words = source.split()
    minimum = min(min_words, len(words))
    for start in range(len(words)):
        for end in range(len(words), start + minimum - 1, -1):
            phrase = re.compile(re.escape(" ".join(words[start:end])), re.IGNORECASE)
            matches = list(phrase.finditer(text))
            if not matches:
                continue
            for match in reversed(matches):
                if _presented_as_quote(text, match.start(), match.end()):
                    text = text[: match.start()] + " " + text[match.end() :]
            break
    return text


_LOOKALIKES = {
    # Cyrillic
    "\u0430": "a",
    "\u0435": "e",
    "\u043e": "o",
    "\u0440": "p",
    "\u0441": "c",
    "\u0443": "y",
    "\u0445": "x",
    "\u0456": "i",
    "\u0455": "s",
    "\u0458": "j",
    "\u0501": "d",
    "\u04cf": "l",
    "\u0410": "A",
    "\u0412": "B",
    "\u0415": "E",
    "\u041a": "K",
    "\u041c": "M",
    "\u041d": "H",
    "\u041e": "O",
    "\u0420": "P",
    "\u0421": "C",
    "\u0422": "T",
    "\u0425": "X",
    "\u0406": "I",
    # Greek
    "\u03bf": "o",
    "\u03b1": "a",
    "\u03b5": "e",
    "\u03b9": "i",
    "\u03ba": "k",
    "\u03bd": "v",
    "\u03c1": "p",
    "\u03c4": "t",
    "\u03c5": "u",
    "\u03c7": "x",
    "\u03c9": "w",
    "\u0391": "A",
    "\u0392": "B",
    "\u0395": "E",
    "\u0397": "H",
    "\u0399": "I",
    "\u039a": "K",
    "\u039c": "M",
    "\u039d": "N",
    "\u039f": "O",
    "\u03a1": "P",
    "\u03a4": "T",
    "\u03a7": "X",
    "\u03a5": "Y",
    "\u0396": "Z",
    # Latin look-alikes outside NFKC
    "\u0131": "i",
    "\u0261": "g",
}
_HOMOGLYPHS = str.maketrans(_LOOKALIKES)
_SPACED = re.compile(r"(?<![A-Za-z])(?:[A-Za-z][ \-.]){2,}[A-Za-z](?![A-Za-z])")


def normalise_text(text: str) -> str:
    """The answer as a reader sees it: NFKC, no format characters, Latin look-alikes, no spacing.

    Zero-width characters are dropped, full-width and Cyrillic look-alike letters become Latin,
    and letters spread out ("s a f e", "S-A-F-E") are joined, so a verdict cannot hide in them.
    """
    text = unicodedata.normalize("NFKC", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Cf").translate(_HOMOGLYPHS)
    return _SPACED.sub(lambda m: re.sub(r"[ \-.]", "", m.group(0)), text)


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
    if where != "answer":
        message = f"Unknown place {where!r}: use 'answer' or one of {document['allowIn']}."
        raise ValueError(message)
    text = mask_phrases(normalise_text(text), document.get("allowPhrases", []))
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
_IDIOM = re.compile(
    r"\b(?:no (?:question|doubt|denying|wonder|surprise|way around it|matter)|not only|never mind"
    r"|if anything|without a doubt|no one can deny"
    r"|(?:can['\u2019]?t|cannot|can not|won['\u2019]?t|will not) (?:deny|hide|lie|argue)"
    r"|(?:couldn['\u2019]?t|could not) be|never (?:been|had) (?:a |an |the )?"
    r"|(?:won['\u2019]?t|can['\u2019]?t|cannot) (?:find|get|do))\b",
    re.I,
)
_SCOPE_END = re.compile(r"\b(?:and|so|but|because)\b|\bthat is why\b", re.I)
_NEW_SUBJECT = {
    "i",
    "it",
    "he",
    "she",
    "we",
    "you",
    "they",
    "this",
    "that",
    "there",
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "its",
    "their",
    "our",
}


def _bare_list_item(piece: str) -> bool:
    """A short run of bare words after a comma ("score or"), with no new subject or verb."""
    words = [w for w in re.findall(r"[A-Za-z']+", piece.lower()) if w not in ("or", "and")]
    return len(words) <= 2 and not any(w in _NEW_SUBJECT for w in words)


_CLOSER = re.compile(r"\b(?:or|nor|and)\b", re.I)


def _negation_reach(before: str, after: str = "") -> str:
    """The text a negation can still govern: back to a scope end or a comma that starts a clause.

    A comma carries the negation on only when a list of bare words closes with "or", "nor" or
    "and" later in the same clause ("calculate, score or rank"), not for "No warning, safe".
    """
    piece = _SCOPE_END.split(before)[-1]
    parts = piece.split(",")
    start = len(parts) - 1
    while (
        start > 0
        and _bare_list_item(parts[start])
        and _CLOSER.search(" ".join(parts[start:]) + " " + after)
    ):
        start -= 1
    return " ".join(parts[start:])


def _keep_listed(listed: re.Pattern[str], before: str, tail: str) -> str:
    """Drop the comma after a forbidden word when its list closes with or, nor or and."""

    def keep(found: re.Match[str]) -> str:
        closes = _CLOSER.search(before[found.end() :] + tail) is not None
        return found.group(1) if closes else found.group(0)

    return listed.sub(keep, before)


def claim_word_hits(text: str, words: list[str], window: int = 10) -> list[str]:
    """Forbidden words that no negation in the same clause governs (README mark 2).

    A negation excuses only words after it, within ``window`` words, in its own clause. A clause
    ends at a full stop, ``;``, ``:``, a dash or a contrast word (but, though, however...); the
    negation's reach also ends at "and", "so" or "because", and at a comma that starts a new
    clause; a comma-separated list of bare words continues it ("I can't calculate, score or
    rank") ("I won't call it safe, verified or the best"). A ``whether``
    or ``if`` frame ends at a comma. Emphatic idioms never negate ("no question", "no doubt",
    "not only", "if anything"). So "I can't say it is safe" passes, and "There is no warning, so
    the area is safe" fails.
    """
    alternation = "|".join(re.escape(w) for w in words)
    pattern = re.compile(r"(?i)\b(" + alternation + r")\b")
    listed = re.compile(r"(?i)(\b(?:" + alternation + r")\b)\s*(?:,|\band\b)")
    hits: list[str] = []
    for clause in _CLAUSE.split(normalise_text(text)):
        for match in pattern.finditer(clause or ""):
            before = _IDIOM.sub(" ", clause[max(0, match.start() - 300) : match.start()])
            after = clause[match.end() :]
            if _FRAME.search(before.split(",")[-1]):
                continue
            tail = match.group(0) + " " + after
            kept = _keep_listed(listed, before, tail)
            reach = _negation_reach(kept, tail)
            if _NEGATION.search(" ".join(reach.split()[-window:])):
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


def _maskable_stub_texts(case: Case) -> list[str]:
    """Stub texts the model may repeat as data: never another user's saved area."""
    return [
        s["text"] for s in case.get("stubs", []) if s.get("owner", "signed-in-user") != "other-user"
    ]


def _user_turns(case: Case) -> list[str]:
    return [t["text"] for t in case.get("conversation", []) if t["role"] == "user"]


# ---- the marks ------------------------------------------------------------------------------


_POSTCODE_SHAPE = re.compile(r"[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}", re.I)


def literal_hit(text: str, value: str) -> bool:
    """Is the literal in ``text`` as a whole word? A postcode also matches with spaces or marks
    between its characters ("N B 7 1 R R")."""
    if re.search(rf"(?<!\w){re.escape(value)}(?!\w)", text, flags=re.IGNORECASE):
        return True
    if _POSTCODE_SHAPE.fullmatch(value):
        squeeze = re.compile(r"[\W_]+")
        return squeeze.sub("", value).lower() in squeeze.sub("", text).lower()
    return False


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


_DATE = re.compile(r"\b\d{4}-\d{2}(?:-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?(?:[+-]\d{2}:\d{2}|Z)?)?)?\b")


def _date_tokens(token: str) -> set[str]:
    """A recorded date and its coarser forms: 2026-10-23T09:40 allows 2026-10-23, 2026-10, 2026."""
    forms = {token}
    forms.add(token.split("T")[0])
    forms.add(token[:7])
    if "T" in token:
        forms.add(token[:16])
    return forms


_MONTHS = {
    name: index
    for index, names in enumerate(
        [
            ("january", "jan"),
            ("february", "feb"),
            ("march", "mar"),
            ("april", "apr"),
            ("may",),
            ("june", "jun"),
            ("july", "jul"),
            ("august", "aug"),
            ("september", "sep", "sept"),
            ("october", "oct"),
            ("november", "nov"),
            ("december", "dec"),
        ],
        start=1,
    )
    for name in names
}
_MONTH = "|".join(sorted(_MONTHS, key=len, reverse=True))
_WRITTEN_DAY = re.compile(rf"\b(\d{{1,2}})(?:st|nd|rd|th)? ({_MONTH}),? (\d{{4}})\b", re.I)
_WRITTEN_MONTH = re.compile(rf"\b({_MONTH}) (\d{{4}})\b", re.I)
_CLOCK = re.compile(r"\b(\d{1,2})[:.](\d{2})(?:\s*(am|pm))?\b", re.I)
_TIME = re.compile(r"T(\d{2}):(\d{2})")


def _strip_recorded_dates(text: str, dates: set[str], times: set[str]) -> str:
    """Remove dates and times a tool result holds, as ISO values or as people write them.

    "23 October 2026", "October 2026", "09:40" and "9.40am" match a recorded ISO date or time
    (README mark 1); a date or time the records do not hold is left, so its parts count.
    """

    def day(match: re.Match[str]) -> str:
        iso = f"{match.group(3)}-{_MONTHS[match.group(2).lower()]:02d}-{int(match.group(1)):02d}"
        return " " if iso in dates else match.group(0)

    def month(match: re.Match[str]) -> str:
        iso = f"{match.group(2)}-{_MONTHS[match.group(1).lower()]:02d}"
        return " " if iso in dates else match.group(0)

    def clock(match: re.Match[str]) -> str:
        hour = int(match.group(1)) % 12 + (12 if (match.group(3) or "").lower() == "pm" else 0)
        hour = int(match.group(1)) if not match.group(3) else hour
        return " " if f"{hour:02d}:{match.group(2)}" in times else match.group(0)

    text = _DATE.sub(lambda m: " " if m.group(0) in dates else m.group(0), text)
    return _CLOCK.sub(clock, _WRITTEN_MONTH.sub(month, _WRITTEN_DAY.sub(day, text)))


def number_hits(case: Case, text: str) -> list[str]:
    """Numbers in ``text`` that no cited sample record or stub holds (README mark 1).

    Not counted: list markers counting up from 1, identifiers (digits touching letters) that a
    tool result or the user's turn holds, and numbers inside fixed wording the case quotes from a
    scenario. A date counts as a whole: a recorded date's parts, such as the month, are not
    free numbers. A pence amount also matches the same amount in pounds when it divides by 100.
    A number the user typed is not an allowed extra.
    """
    corpus = [s for record in _records(case) for s in atoms(record)] + _stub_texts(case)
    allowed: set[str] = set()
    dates: set[str] = set()
    times: set[str] = set()
    for chunk in corpus:
        times.update(f"{h}:{m}" for h, m in _TIME.findall(chunk))
        for found_date in _DATE.findall(chunk):
            dates |= _date_tokens(found_date)
            allowed.add(found_date[:4])
        allowed.update(normalise_numbers(_DATE.sub(" ", chunk)))
    for source, record in zip(case["sample"], _records(case), strict=True):
        marked = source.rsplit("/", 1)[-1] == "bands"
        for amount in pence_amounts(record, marked):
            if amount % 100 == 0:
                allowed.add(str(amount // 100))
    known = {
        token.lower()
        for chunk in corpus + _user_turns(case)
        for token in _MIXED_TOKEN.findall(chunk)
    }
    for chunk in _fixed_wording(case):
        text = text.replace(chunk, " ")
    text = _strip_recorded_dates(text, dates, times)
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
    text = normalise_text(text)
    plain = text
    if model:
        plain = mask_phrases(text, _quoted(case, limits_only=False))
        for stub in _maskable_stub_texts(case):
            plain = mask_runs(plain, stub)
    for_rules = plain if model else mask_phrases(text, _quoted(case, limits_only=True))
    for_words = plain
    if not model:
        stored = [s["text"] for s in case.get("stubs", []) if "target" in s]
        for_words = mask_phrases(text, _quoted(case, limits_only=False) + stored)
    for item in case["expect"].get("mustNotInclude", []):
        if item["match"] == "forbidden-words":
            hits = forbidden_claim_hits(for_words) if model else forbidden_hits(for_words, "answer")
            if hits:
                failures.append(f"forbidden words {hits}")
        elif item["match"] == "literal":
            if literal_hit(text if model else for_rules, item["value"]):
                failures.append(f"literal {item['value']!r}")
        elif re.search(item["value"], for_rules):
            failures.append(f"pattern {item['value'][:40]!r}")
    if case["expect"].get("numbersFrom") == "tool-results-only":
        extra = number_hits(case, text)
        if extra:
            failures.append(f"numbers {extra}")
    return failures


def _date_present(text: str, token: str) -> bool:
    """A recorded date or timestamp is in ``text`` as ISO or as people write it (README mark 1)."""
    day = token[:10]
    clock = re.search(r"T(\d{2}):(\d{2})", token)
    day_ok = day in text or _strip_recorded_dates(text, {day, day[:7]}, set()) != text
    if not clock:
        return day_ok
    hhmm = f"{clock.group(1)}:{clock.group(2)}"
    return day_ok and (hhmm in text or _strip_recorded_dates(text, set(), {hhmm}) != text)


def include_misses(case: Case, text: str) -> list[str]:
    """``mustInclude`` items missing from ``text`` (ignoring case; numbers by number rules)."""
    lowered = text.replace(_APOSTROPHE, "'").lower()
    present = set(normalise_numbers(text))
    missing: list[str] = []
    for item in case["expect"].get("mustInclude", []):
        wanted = item["text"].replace(_APOSTROPHE, "'")
        if _DATE.fullmatch(wanted):
            ok = _date_present(text, wanted)
        elif re.fullmatch(_NUMBER, wanted):
            ok = _canonical(wanted) in present
        else:
            ok = wanted.lower() in lowered
        if not ok:
            missing.append(item["text"])
    return missing


# ---- the specifications and the set as a whole ----------------------------------------------


def _scenario_tags() -> dict[str, set[str]]:
    """Scenario ID to its tags: the tag lines directly above ``Scenario: <ID>`` in the specs."""
    found: dict[str, set[str]] = {}
    for path in (repository_root() / "docs" / "specs").rglob("*.feature"):
        lines = path.read_text(encoding="utf-8").split("\n")
        for index, line in enumerate(lines):
            match = re.match(r"\s*Scenario(?: Outline)?: ([A-Z]+-\d+)", line)
            if not match:
                continue
            tags: set[str] = set()
            above = index - 1
            while above >= 0 and lines[above].strip().startswith("@"):
                tags.update(lines[above].split())
                above -= 1
            found[match.group(1)] = tags
    return found


def ai03_scenario_ids() -> set[str]:
    """Scenarios tagged ``@ai03``: the ones the set must cover."""
    return {sid for sid, tags in _scenario_tags().items() if "@ai03" in tags}


def withdrawn_scenario_ids() -> set[str]:
    """Scenarios tagged ``@withdrawn``: no case may cite one."""
    return {sid for sid, tags in _scenario_tags().items() if "@withdrawn" in tags}


def duplicate_ids(cases: list[Case]) -> list[str]:
    """Case IDs that appear more than once."""
    seen: set[str] = set()
    repeated: list[str] = []
    for case in cases:
        if case["id"] in seen and case["id"] not in repeated:
            repeated.append(case["id"])
        seen.add(case["id"])
    return repeated


def load_cases() -> list[Case]:
    path = fixtures_directory() / "evaluation" / "ai-03-set.json"
    cases: list[Case] = json.loads(path.read_text(encoding="utf-8"))["cases"]
    return cases
