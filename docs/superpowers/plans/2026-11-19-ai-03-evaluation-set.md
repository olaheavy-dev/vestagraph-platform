# AI-03 evaluation set: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write the pilot's one versioned AI evaluation set (AI-03, AI-14) as schema-checked data files, with tests in `make check` that prove it is complete, cites real scenarios and sample records, and obeys the rules it tests; the runner comes at stage 5b.

**Architecture:** A JSON Schema defines a case (two shapes: tool-output and model). The fixture validator learns an `evaluation/` folder. Scenarios the set must cover are tagged `@ai03` in the feature files. The cases are written in three batches (area tools, council tools, signed-in chat), then integrity and coverage tests close the set.

**Tech Stack:** Python 3.14, uv, pytest, jsonschema and the existing `vestagraph_fixture_validator`; Gherkin tags as registered pytest markers. No new packages.

**Spec:** `docs/superpowers/specs/2026-11-19-ai-03-evaluation-set-design.md` (approved 19 Nov 2026).

## Global Constraints
- Rule cases: marked by code only, `runs: 3`, pass mark 100%. Quality cases: `runs: 1`, judge measures pass at 4 of 5, set-wide 95%. Latency cases: listed, not marked before 5b.
- Measures use Foundry names exactly: `groundedness`, `task_adherence`, `tool_call_accuracy`, `tool_selection`, `tool_input_accuracy`, `intent_resolution`, `relevance`, `response_completeness`, `coherence`, `fluency`.
- Expected figures and phrases are quoted from `packages/fixtures/data/` or `generated/` (rule 2); hostile text, saved areas, chat titles and earlier turns go in a case's `stubs`, marked synthetic, never into shared fixtures.
- Every conversation is written by us; no real personal data (rule 5; 0058 choice 9).
- A case's own expected text contains no verdict word, no calculated figure and no number absent from its `sample` or `stubs`.
- A case may not cite a scenario tagged `@withdrawn`.
- Test names `test_<method>_<condition>_<result>` (0039). Commits `test:`/`docs:`; no attribution lines.

## Review Focus
1. **A case citing a scenario ID that was renamed or withdrawn:** the integrity test fails naming the case; Task 6 pins it.
2. **A forbidden word inside quoted source text or the user's own turn** (for example "safe" in "Is it safe?"): allowed only in the user turn and in quoted source text on the allow-list; Task 3's word-list test pins it.
3. **A number with a unit or separator** ("£1,234", "5 km", "16%"): the number check normalises and still matches the sample; Task 3 pins the normaliser's examples.
4. **Two cases with the same ID across surface files:** the uniqueness test fails; Task 6 pins it.
5. **An `@ai03` scenario with no case:** the coverage test fails naming the scenario; Task 6 pins it.

---

### Task 1: The case schema and the validator's `evaluation/` folder

**Files:**
- Create: `packages/fixtures/schema/ai-03-set.schema.json`, `packages/fixtures/evaluation/ai-03-set.json` (version 1, one example case per shape)
- Modify: `packages/vestagraph-fixture-validator/src/vestagraph_fixture_validator/validator.py` (`validate_fixtures`: add `evaluation` with the name-to-schema rule used for `data/`)
- Test: `packages/vestagraph-fixture-validator/tests/test_fixtures_ai03_schema_rejection.py`, extend `test_fixtures_command_line.py` if it lists folders

**Interfaces:**
- Produces: document `{ "version": 1, "cases": [ ... ] }`; a case has `id` (`^[A-Z0-9]+(-[A-Z0-9]+)+$`), `surface` (`area-tools|council-tools|signed-in-chat`), `group` (1–25), `kind` (`rule|quality|latency`), `shape` (`tool-output|model`), `tests` (scenario IDs, min 1), `measures` (enum above, min 1), `runs` (rule → 3, quality/latency → 1, enforced by if/then), `toolInput` (required when `shape` is `tool-output`), `conversation` (required when `model`: list of `{role: user|assistant, text}`), `sample` (record IDs or `generated/<file>#<pointer>`), `stubs` (optional; every stub has `synthetic: true` and a `channel`: `tool-result|place-name|school-name|council-name|saved-area|chat-title|earlier-turn`), `expect` (`toolCalls`, `mustInclude` [{text, from}], `mustNotInclude`, `numbersFrom: tool-results-only`, `replyKind`), `notes`. `additionalProperties: false` throughout.

- [x] **Step 1:** Write failing tests: `test_validate_instance_ai03_set_real_file_is_accepted`; rejections for: unknown measure, `runs: 1` on a rule case, a model case without `conversation`, a tool-output case without `toolInput`, a stub without `synthetic: true`, an unknown stub channel, group 26, an extra property.
- [x] **Step 2:** `uv run pytest packages/vestagraph-fixture-validator/tests/test_fixtures_ai03_schema_rejection.py -v` → FAIL.
- [x] **Step 3:** Write the schema, the two example cases (one tool-output rule case for group 4 "unknown postcode NB9 9ZZ", one model rule case for group 9 "add up the crimes"), and the validator change.
- [x] **Step 4:** Tests and `make validate` → PASS. Commit `test: AI-03 case schema and the evaluation folder`.

### Task 2: `@ai03` tags in the specifications

**Files:** `pyproject.toml` (marker `ai03: Gherkin tag, a scenario the AI-03 evaluation set must cover`), `docs/specs/pilot/area-tools.feature`, `docs/specs/pilot/workspace-chat.feature`, any other feature whose description lists AI-03 cases (grep "AI-03"), `docs/specs/README.md` (the tag), `docs/planning/backlog.md` row 38f.

- [x] **Step 1:** Tag every scenario the descriptions list for AI-03 (area-tools: the TOOLS list including TOOLS-47, 55, 57–59, 64–72; workspace-chat: WCHAT-19 to 22, 30 to 39, 42, 51, 52, 67 to 70, 73, 78 to 80, 84, 86, 87, 93, 102, 110, and any the description adds); never a `@withdrawn` one. Replace each prose list with "the scenarios tagged `@ai03`".
- [x] **Step 2:** `make test` → PASS (strict markers accept the new tag). Commit `docs: tag the scenarios the AI-03 set must cover`.

### Task 3: Marking references (word list, normaliser examples, rubric, README)

**Files:** Create `packages/fixtures/evaluation/forbidden-words.json` (+ schema), `packages/fixtures/evaluation/README.md` (version, changelog, how cases are marked, the measures table from the design, the 5b runner's contract); Test: `packages/vestagraph-fixture-validator/tests/test_ai03_marking_references.py`.

**Interfaces:**
- Produces: `forbidden-words.json` = `{ "version": 1, "words": [...], "allowIn": ["user-turn", "quoted-source"] }` built from AGENTS rule 4, 0004, 0054 and WCHAT-67 to 80; a test-side helper `normalise_numbers(text: str) -> list[str]` in `packages/vestagraph-fixture-validator/tests/ai03_support.py` (used by Task 6).

- [x] **Step 1:** Failing tests: `test_normalise_numbers_currency_and_separators_match` (`"£1,234"` → `"1234"`), `..._units_kept_separate` (`"5 km"` → `"5"`), `..._percent` (`"16%"` → `"16"`), `test_forbidden_words_include_rule_four_words` (contains `safe`, `good`, `best`, `verified`, `approved`, `score`, `recommend`).
- [x] **Step 2:** Run → FAIL; write the files and helper; run → PASS. Commit `test: AI-03 marking references`.

### Task 4: Area tools cases (audit groups 1–12)

**Files:** `packages/fixtures/evaluation/ai-03-set.json` (append).
- [x] **Step 1:** Write at least one rule case per group 1–12 (group 12 a tool-output rule case: the card's places equal the nearby tool's result), plus quality cases for tool choice; cover each audit example in groups 1–12; injection cases through place and school names and tool text as `stubs`.
- [x] **Step 2:** `make validate` and `make test` → PASS. Commit `test: AI-03 area tools cases`.

### Task 5: Council tools cases (groups 13–19) and signed-in chat cases (groups 20–25)

**Files:** same file (append).
- [x] **Step 1:** Council: each audit example in 13–19 (TOOLS-47, 55, 57–59, 64–72 as model cases through our chat's model; tool-output cases where only the tool result matters). Chat: each example in 20–25; injection through council names, saved areas, chat titles and earlier turns as `stubs`; `list_saved_areas` own-areas as a rule; latency cases for OP-05 as `kind: latency`.
- [x] **Step 2:** `make validate`, `make test` → PASS. Commit `test: AI-03 council tools and signed-in chat cases`.

### Task 6: Integrity and coverage tests

**Files:** Create `packages/vestagraph-fixture-validator/tests/test_ai03_set_integrity.py`; helper in `ai03_support.py`: `ai03_scenario_ids() -> set[str]` and `withdrawn_scenario_ids() -> set[str]` (parse `docs/specs/**/*.feature`: a tag line directly above `Scenario: <ID> …`).
- [x] **Step 1:** Tests: `test_ai03_set_case_ids_are_unique`; `..._every_cited_scenario_exists`; `..._no_case_cites_a_withdrawn_scenario`; `..._every_sample_reference_exists`; `..._every_ai03_scenario_has_a_case` (fails naming the missing IDs); `..._every_group_has_a_case`; `..._every_rule_group_has_a_rule_case` (all groups except tool choice in 23 and latency in 25); `..._expected_text_has_no_forbidden_word`; `..._expected_numbers_come_from_sample_or_stubs`.
- [x] **Step 2:** Run → fix cases until PASS (never weaken a test to pass). Commit `test: AI-03 set integrity and coverage`.

### Task 7: Founder spot-check, records and pull request

**Files:** `docs/decisions/README.md` (AI-03 status "Written (set version 1), runner at 5b"; AI-14 dated note with the four founder answers; a line for the marking rules as agent's calls), `docs/planning/backlog.md` 38f, `docs/planning/status.md` (item 6: set written; next, gate round 2), the design's records.
- [x] **Step 1:** Pick 10 cases (one per group cluster, all three surfaces, both kinds); the controller shows them to the founder in plain language in a prompt window; apply corrections.
- [x] **Step 2:** Records; pre-flight grep for AI-03, AI-14, "evaluation set", "38f", "@ai03".
- [ ] **Step 3:** `make check`; fresh-context review (Code Review Rules) and `code-security-reviewer` (the injection cases); fix; push; PR; `@codex review`.

---

## As built (19 Nov 2026)

All seven tasks done. The set is `packages/fixtures/evaluation/ai-03-set.json`, version 1: 143 cases (131 rule, 10 quality, 2 latency), 78 scenarios tagged `@ai03`. Tests are in `packages/vestagraph-fixture-validator/tests/` (`test_fixtures_ai03_schema_rejection.py`, `test_ai03_marking_references.py`, `test_ai03_examples.py`, `test_ai03_set_integrity.py`, with `ai03_support.py` holding the marking functions); every `@ai03` scenario, group and rule group has a case. Rulings recorded in the design (agent's calls, open to the founder): must-not items are code checks (5), tool-output number and word checks (6), the `store-record` stub (7), the Task 5 review rulings (8, a to n); register AI-15 (marking rules) and FE-82 (the card's places). The founder's spot-check of 10 cases was approved ("Approve (Recommended)"). Step 3 of Task 7 (reviews, push, pull request, Codex) is not ticked: it is the controller's next step.
