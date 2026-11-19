"""Test-side helpers for the AI-03 marking references (AI-03, AI-14).

The 5b runner will own the real marking; these helpers let the set's own tests apply the same
rules (a set that obeys its own rules) and pin the behaviour the README describes.
"""

import json
import re
from typing import Any

from fixtures_support import fixtures_directory

_NUMBER = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")


def normalise_numbers(text: str) -> list[str]:
    """Every number in ``text`` as plain digits: no £, no thousands commas, no % or unit."""
    return [match.replace(",", "") for match in _NUMBER.findall(text)]


def load_forbidden_words() -> dict[str, Any]:
    path = fixtures_directory() / "evaluation" / "forbidden-words.json"
    document: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return document


def forbidden_hits(text: str, where: str) -> list[str]:
    """The forbidden words or phrases in ``text``; none when ``where`` is an allowed place.

    ``where`` is ``answer`` (the model's reply, the only place the list applies) or one of the
    list's ``allowIn`` places, such as ``user-turn`` or ``quoted-source``. A word matches whole
    words only, so "Safestore" and "safety" never match "safe".
    """
    document = load_forbidden_words()
    if where in document["allowIn"]:
        return []
    return [
        word
        for word in document["words"]
        if re.search(rf"\b{re.escape(word)}\b", text, flags=re.IGNORECASE)
    ]
