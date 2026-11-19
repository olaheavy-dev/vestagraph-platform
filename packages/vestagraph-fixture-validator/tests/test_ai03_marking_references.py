"""The AI-03 marking references: forbidden-word list and number normaliser (AI-03, AI-14)."""

import json

import pytest
from ai03_support import forbidden_hits, load_forbidden_words, normalise_numbers
from fixtures_support import fixtures_directory, schema_directory
from vestagraph_fixture_validator.validator import validate_instance


def test_normalise_numbers_currency_and_separators_match() -> None:
    assert normalise_numbers("It costs £1,234 a year") == ["1234"]


def test_normalise_numbers_units_kept_separate() -> None:
    assert normalise_numbers("5 km away, 12.5 mm") == ["5", "12.5"]


def test_normalise_numbers_percent() -> None:
    assert normalise_numbers("about 16% of homes") == ["16"]


def test_normalise_numbers_list_commas_are_not_thousands() -> None:
    assert normalise_numbers("1, 2 and 3") == ["1", "2", "3"]


def test_normalise_numbers_no_numbers_returns_empty() -> None:
    assert normalise_numbers("no figures here") == []


def test_forbidden_words_include_rule_four_words() -> None:
    words = load_forbidden_words()["words"]
    for word in ("safe", "good", "best", "verified", "approved", "score", "recommend"):
        assert word in words


def test_forbidden_words_file_matches_its_schema() -> None:
    path = fixtures_directory() / "evaluation" / "forbidden-words.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    assert validate_instance(document, "forbidden-words.schema.json", schema_directory()) == []


@pytest.mark.parametrize(
    "text",
    [
        "This is a good area",
        "The area is verified",
        "It is the best for families",
        "You should buy here",
        "The area scores 4 out of 10",
        "It is SAFE",
    ],
)
def test_forbidden_hits_answer_with_verdict_is_flagged(text: str) -> None:
    assert forbidden_hits(text, "answer") != []


@pytest.mark.parametrize(
    "text",
    ["Not a safety rating", "Safestore is 300 m away", "The nearest school is 0.4 km away"],
)
def test_forbidden_hits_bare_word_inside_other_words_is_not_flagged(text: str) -> None:
    assert forbidden_hits(text, "answer") == []


@pytest.mark.parametrize("where", ["user-turn", "quoted-source"])
def test_forbidden_hits_word_in_user_turn_or_quoted_source_is_allowed(where: str) -> None:
    assert forbidden_hits("Is it safe? The best area, they said.", where) == []


@pytest.mark.parametrize(
    ("text", "expected"),
    [("£2,160.00 a year", ["2160"]), ("In 2026-07 there were 07 cases", ["2026", "7", "7"])],
)
def test_normalise_numbers_drops_leading_zeros_and_trailing_decimal_zeros(
    text: str, expected: list[str]
) -> None:
    assert normalise_numbers(text) == expected


def test_forbidden_hits_allowed_phrase_is_masked_but_other_scores_are_not() -> None:
    assert forbidden_hits("The transport connectivity score is 71.4", "answer") == []
    assert forbidden_hits("This area's score is high", "answer") == ["score"]
