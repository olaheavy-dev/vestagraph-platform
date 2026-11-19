"""Every AI-03 case with a literal or pattern must-not proves its marks on examples (AI-03).

A mark that fails a correct answer would fail a correct product 3 runs out of 3. So each such case
carries plausible passing and failing answers, and these tests apply the code marks to them.
"""

import json
import re
from typing import Any

import pytest
from ai03_support import Case, include_misses, mark, resolve
from fixtures_support import fixtures_directory

_CASES: list[Case] = json.loads(
    (fixtures_directory() / "evaluation" / "ai-03-set.json").read_text(encoding="utf-8")
)["cases"]


def _needs_examples(case: Case) -> bool:
    return any(
        item["match"] != "forbidden-words" for item in case["expect"].get("mustNotInclude", [])
    )


def _ids(cases: list[Case]) -> list[str]:
    return [c["id"] for c in cases]


_WITH_EXAMPLES = [c for c in _CASES if "examples" in c]


def test_ai03_cases_with_literal_or_pattern_marks_have_examples() -> None:
    missing = [c["id"] for c in _CASES if _needs_examples(c) and "examples" not in c]
    assert missing == []


@pytest.mark.parametrize("case", _WITH_EXAMPLES, ids=_ids(_WITH_EXAMPLES))
def test_mark_pass_examples_pass_every_code_mark(case: Case) -> None:
    for text in case["examples"]["pass"]:
        assert mark(case, text) == [], text
        assert include_misses(case, text) == [], text


@pytest.mark.parametrize("case", _WITH_EXAMPLES, ids=_ids(_WITH_EXAMPLES))
def test_mark_fail_examples_fail_a_code_mark(case: Case) -> None:
    for text in case["examples"]["fail"]:
        assert mark(case, text) != [], text


def test_ai03_every_must_include_source_is_in_the_cases_sample() -> None:
    gaps: list[str] = []
    for case in _CASES:
        for item in case["expect"].get("mustInclude", []):
            source = item["from"]
            if source.startswith("stubs/") or re.fullmatch(r"[A-Z]+-\d+", source):
                continue
            if not any(
                source == s or source.startswith(s.rstrip("/") + "/") for s in case["sample"]
            ):
                gaps.append(f"{case['id']}: {source}")
    assert gaps == []


def test_ai03_every_sample_and_must_include_quote_resolves() -> None:
    problems: list[str] = []
    for case in _CASES:
        stubs: list[dict[str, Any]] = case.get("stubs", [])
        for source in case["sample"]:
            resolve(source, stubs)
        for item in case["expect"].get("mustInclude", []):
            text = resolve(item["from"], stubs)
            flat = text if isinstance(text, str) else json.dumps(text, ensure_ascii=False)
            if item["text"] not in flat:
                problems.append(f"{case['id']}: {item['text']!r} not in {item['from']}")
    assert problems == []
