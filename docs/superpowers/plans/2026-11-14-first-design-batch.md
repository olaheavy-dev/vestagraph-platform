# First design batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Anything numeric also follows `.claude/skills/test-first/` (decision 0031).

**Goal:** Give the area result's canvas boards real, tested numbers (At a glance counts, display distances, buses per hour, priority results), then draw the first design batch on the canvas.

**Architecture:** Data contract first: the postcode sample data and its schema gain every pilot topic, and a new topic registry file lists the pilot's topics. A new workspace package, `vestagraph_area`, holds the area rules (pure functions, no I/O beyond reading). The generator calls it and writes a second generated file, `area-result.json`, which the canvas boards quote. Then the boards are drawn on the design canvas.

**Tech Stack:** Python 3.14, uv workspace, pytest, mypy strict, ruff, JSON Schema 2020-12 (jsonschema validator). No new third-party packages. The canvas is the claude.ai design canvas (version 138 onwards).

**Spec:** `docs/superpowers/specs/2026-11-14-first-design-batch-design.md` (approved 14 Nov 2026), with register lines FE-38 to FE-41, DA-17, DA-18 and FE-27 (amended).

## Global Constraints
- Rule 2: no calculated figure typed by hand anywhere (data, boards, docs). Inputs carry a source; outputs come from `vestagraph_area` through `area-result.json`. Test expectations are worked out independently (test-first skill), with their working.
- Rule 7: missing is never zero, "none", a miss or a clean result. A gap status is never turned into a value.
- Sample data stays synthetic: names end "(synthetic)", `source.label` says "Synthetic sample, shaped like …".
- No status word or date on a fact (FE-33); no limit line on rows or sheet tops (FE-34); the flood check time is the one exception (DA-12).
- England distances: under 1 mile in metres to the nearest 10 m, from 1 mile in miles to one decimal, the unit chosen from the rounded value (FE-27 amended); crime keeps "within 1 mile".
- Priorities: never tallied, never stored; "within" includes the limit; comparisons use stored metres or minutes, never display values (FE-40).
- Test names: `test_<method>_<condition>_<result>` (decision 0039). Test files: `test_area_*.py` (unique per package for mypy).
- No agent attribution in commits or pull requests.

## Review Focus
1. **A sample postcode with a topic that has no record at all** must fail generation, not count as left out (spec: "the validator rejects a topic with none"). Test in Task 3.
2. **A distance of 1,605 to 1,609 m** must display "1.0 miles", never "1,610 m". Test in Task 4.
3. **A priority on a `no-record-in-source` or `source-failed` record** must be Not known, never Misses. Test in Task 6.
4. **A limit beyond the 5 km search** with nothing found within 5 km must be "Not known beyond 5 km", not Misses. Test in Task 6.
5. **`generated/` holding both files**: the generator must stop deleting a sibling generated file it now writes (`costs.json` and `area-result.json` both survive a run). Test in Task 7.

## Pull requests
- **PR A (code, Codex review):** Tasks 1 to 8, branch `feat/area-result-data`. Founder-only merge does not apply (no rule tables, no new packages).
- **PR B (canvas record, documentation):** Tasks 9 to 13; the canvas changes plus a status and canvas-version note in the repository.

---

### Task 1: Topic registry and the postcode schema (data contract)

**Files:**
- Create: `packages/fixtures/schema/pilot-topics.schema.json`, `packages/fixtures/data/pilot-topics.json`
- Create: `packages/fixtures/schema/sample-priorities.schema.json`, `packages/fixtures/data/sample-priorities.json`
- Modify: `packages/fixtures/schema/postcode-area.schema.json` (topic enum, value shapes)
- Modify: `packages/fixtures/README.md` (the two new files)
- Test: `make validate` (the validator maps `data/NAME.json` to `schema/NAME.schema.json`)

**Interfaces:**
- Produces: `pilot-topics.json`: `{ "$schema", "nation": "england", "topics": [ { "key", "name", "kind", "recordTopics": [..], "recordSubtypes": [..]?, "questionTemplate", "checkInPerson": [..], "officialRoute"? } ] }`. `kind` is one of `places`, `area-figures`, `official-rank`, `warning`, `route-only`. `recordTopics` lists the `postcode-area.json` topic values this pilot topic reads (for example everyday places reads `amenity` with subtypes `supermarket`, `shop`, `park`, `pharmacy`, `gp-surgery`, `hospital`, `clinic`, `dentist`, `police-station`, `childcare`).
- Produces: `sample-priorities.json`: `{ "$schema", "priorities": [ { "id", "topicKey", "subtype"?, "measure": "walking-minutes"|"distance-metres"|"download-mbps", "limit": <number>, "synthetic": true } ] }`: example limits used only to draw the boards (never a visitor's).
- Produces: postcode topic enum gains `deprivation-rank`, `transport-connectivity`, `green-space`, `air-quality`, `council-tax`, `affordability`, `mobile`, `flood-risk-postcode`, `school-demand`, `bus-departures`. Place values (`transport-stop`, `amenity`, `school`) gain optional `walkingMinutes` (integer) and `walkingMethod` (string, required with it) (DA-18). `bus-departures` value: `{ "stopItemId", "serviceDay": "weekday", "departures": ["HH:MM", ...] }`. `deprivation-rank` value: `{ "decile": 1..10, "rank": int, "ofAreas": int, "edition": "2025", "domain": "overall"|... }` with `level.kind: "neighbourhood"` (DA-14, 0054).

- [ ] **Step 1:** Write the registry with these topics in this order (the B13 list): getting around (`places`: `transport-stop`, `bus-departures`), everyday places (`places`), places of worship (`places`, subtype `place-of-worship`), schools (`places`: `school`, `school-inspection`, `school-demand`), family view (`places`: childcare, schools, parks), planning nearby (`places`), flood (`warning`: `flood`, `flood-risk-postcode`), recorded crime (`area-figures`), sold nearby (`area-figures`), broadband (`area-figures`), mobile (`area-figures`), air quality (`area-figures`), council tax by band (`area-figures`), housing affordability (`area-figures`), deprivation (`official-rank`), transport connectivity (`official-rank`), green space (`official-rank`, the standard), and route-only: council tax band of a home, noise, ground and mining. Each non-route topic has a `questionTemplate` with one `{label}` slot and a `checkInPerson` list (two to four items of things data can't show). Mark every template and list `"reviewStatus": "draft"`; the founder reviews them in PR A.
- [ ] **Step 2:** Extend `postcode-area.schema.json` as above; keep `additionalProperties: false`; gap statuses still carry no `value`.
- [ ] **Step 3:** Run `make validate`. Expected: passes (the new data files are valid, the old records still are).
- [ ] **Step 4:** Commit: `feat: pilot topic registry and postcode schema for every pilot topic`.

### Task 2: Sample records for every pilot topic

**Files:**
- Modify: `packages/fixtures/data/postcode-area.json`
- Modify: `docs/assets/README.md` only if an image is added (none planned)

- [ ] **Step 1:** For **NB1 4XY** add records so every non-route registry topic has at least one: walking minutes on its stops, schools and amenities (DA-18, `walkingMethod: "routing over paths, synthetic"`); `bus-departures` for each bus stop; `school-demand` for both schools (applications and offers as past-year inputs); `flood-risk-postcode` (property counts per category, categories marked "to confirm from the download", DA-16); a `flood` warning count of zero keeps the existing no-record item; `deprivation-rank` (neighbourhood level, `areaName`); `transport-connectivity`, `green-space`, `air-quality`, `council-tax` (per band, local-authority level), `affordability` (local-authority level), `mobile` (`source.label` notes the Ofcom service change on 30 Nov 2026).
- [ ] **Step 2:** For **NB7 1RR** (sparse) add one record per remaining topic, mostly gaps: at least one `source-failed`, one `not-covered`, one `no-record-in-source`, so the states boards have each.
- [ ] **Step 3:** Every value is a synthetic input (never a total, count per hour or ratio we work out). The affordability ratio is the ONS published figure, so it is an input with its source label.
- [ ] **Step 4:** Run `make validate`. Expected: passes.
- [ ] **Step 5:** Commit: `feat: synthetic sample records for every pilot topic`.

### Task 3: `vestagraph_area` package, registry reader and At a glance

**Files:**
- Create: `packages/vestagraph-area/pyproject.toml` (no dependencies), `packages/vestagraph-area/src/vestagraph_area/{__init__.py,py.typed,records.py,glance.py}`
- Modify: root `pyproject.toml` (mypy paths, pytest paths, coverage), `uv.lock` (`uv sync`)
- Create: `packages/fixtures/test-cases/area-glance.json` (worked cases with their working), `packages/vestagraph-area/tests/test_area_glance.py`

**Interfaces:**
- Produces: `records.py`: `read_registry(path: Path) -> Registry`, `read_postcode_area(path: Path) -> PostcodeArea`, raising `InvalidAreaDataError(ValueError)` for anything not understood. Frozen dataclasses `Topic(key, name, kind, record_topics, record_subtypes, question_template, check_in_person)`, `AreaRecord(id, postcode, topic, subtype, status, label, value)`.
- Produces: `glance.py`: `topic_outcome(topic: Topic, records: Sequence[AreaRecord]) -> TopicOutcome` (`found` | `not-known` | `not-covered`), `at_a_glance(registry: Registry, area: PostcodeArea, postcode: str) -> Glance` with `Glance(found: int, not_known: int, questions: tuple[Question, ...], check_in_person: tuple[CheckItem, ...], coverage_found: int, coverage_total: int, outcomes: dict[str, TopicOutcome])`.

Rules (FE-38, FE-39, FE-41): route-only topics are ignored. A topic is `found` when any of its records is `recorded`, `stale` or `no-record-in-source`; `not-known` when it has records and all are `source-failed`; `not-covered` (left out of found, not known and the total) when all are `not-covered`. Records mixing `not-covered` with `source-failed` and nothing found: `not-known`. A topic with **no record** for a postcode raises `InvalidAreaDataError` naming the topic and postcode. Questions: one per record whose status is `no-record-in-source`, `source-failed` or `not-covered`, text from the topic's template with the record's label. Check in person: every found or not-known topic's list (no count is shown, FE-41, but the list is returned). `coverage_total = found + not_known`.

- [ ] **Step 1:** Work the cases in `area-glance.json` by hand from the Task 2 records (inputs, steps, expected), without running code: NB1 4XY full; NB7 1RR sparse; a synthetic case with one topic all `not-covered`; one with mixed `recorded` and `source-failed`.
- [ ] **Step 2:** Write `test_at_a_glance_worked_cases_match_expected` (data-driven from the file), `test_topic_outcome_no_record_in_source_is_found`, `test_topic_outcome_all_source_failed_is_not_known`, `test_topic_outcome_all_not_covered_is_left_out`, `test_at_a_glance_topic_without_records_raises_invalid_area_data`, `test_at_a_glance_route_only_topic_is_ignored`.
- [ ] **Step 3:** Run `uv run pytest packages/vestagraph-area -q`. Expected: FAIL, `vestagraph_area` not importable.
- [ ] **Step 4:** Implement `records.py` and `glance.py` to the signatures above.
- [ ] **Step 5:** Run the tests. Expected: PASS. Run `make check`. Expected: PASS.
- [ ] **Step 6:** Commit: `feat: area package with At a glance counts (FE-38, FE-39, FE-41)`.

### Task 4: Display distances (FE-27 amended)

**Files:**
- Create: `packages/vestagraph-area/src/vestagraph_area/distance.py`, `packages/fixtures/test-cases/distance-display.json`, `packages/vestagraph-area/tests/test_area_distance.py`

**Interfaces:**
- Produces: `display_distance(metres: Fraction | int) -> str`. A mile is exactly 1,609.344 m. Round metres to the nearest 10, halves away from zero; if the rounded value is under 1,610 return `"<n> m"` with a thousands comma; otherwise return miles to one decimal, halves away from zero, `"<x.y> miles"` (always one decimal, "1.0 miles").

- [ ] **Step 1:** Work the cases by hand: 0, 4, 5, 120, 1,445, 1,450, 1,604, 1,605, 1,609, 1,609.344, 1,610, 2,092 (1.3 miles boundary area), 4,600, and the 0.05-mile halves either side of 1.25 miles. Show each working.
- [ ] **Step 2:** Write `test_display_distance_worked_cases_match_expected` and `test_display_distance_1605_metres_shows_miles_not_1610_metres`.
- [ ] **Step 3:** Run. Expected: FAIL, no `display_distance`.
- [ ] **Step 4:** Implement with `Fraction` arithmetic (no float).
- [ ] **Step 5:** Run. Expected: PASS. Commit: `feat: display distances, unit from the rounded value (FE-27)`.

### Task 5: Buses per hour (DA-18)

**Blocked on a founder decision:** which hours are counted (see the hand-over question). Default if the founder picks the recommended option: two whole-number counts per bus stop, timetabled weekday departures between 08:00 and 08:59 and between 12:00 and 12:59, no averaging.

**Files:**
- Create: `packages/vestagraph-area/src/vestagraph_area/buses.py`, cases in `packages/fixtures/test-cases/buses-per-hour.json`, `packages/vestagraph-area/tests/test_area_buses.py`

**Interfaces:**
- Produces: `buses_in_hour(departures: Sequence[str], hour: int) -> int` (counts `HH:MM` strings whose hour equals `hour`; raises `InvalidAreaDataError` for a malformed time).

- [ ] **Step 1:** Work cases: empty list gives 0 only for a stop whose departures record exists (a missing record is a gap, never 0); 07:59 and 09:00 are outside 08:00–08:59; 08:00 and 08:59 inside; a malformed "8:5" raises.
- [ ] **Step 2:** Write `test_buses_in_hour_worked_cases_match_expected`, `test_buses_in_hour_edges_of_the_hour_count_inclusively`, `test_buses_in_hour_malformed_time_raises`.
- [ ] **Step 3:** Run (FAIL, missing function), implement, run (PASS). Commit: `feat: buses per hour from timetabled departures (DA-18)`.

### Task 6: Priority results (FE-40)

**Files:**
- Create: `packages/vestagraph-area/src/vestagraph_area/priorities.py`, cases in `packages/fixtures/test-cases/priority-results.json`, `packages/vestagraph-area/tests/test_area_priorities.py`

**Interfaces:**
- Consumes: `AreaRecord`, `Topic` (Task 3), `display_distance` (Task 4).
- Produces: `priority_result(priority: Priority, records: Sequence[AreaRecord]) -> PriorityResult` with `PriorityResult(outcome: "meets"|"misses"|"not-known"|"not-known-beyond-search", nearest_record_id: str | None)`. `SEARCH_LIMIT_METRES = 5000` (FE-12).

Rules: consider the topic's records with the priority's subtype. If any `recorded` or `stale` record has its measure at or under the limit (≤): meets. Else, if a `recorded` or `stale` record exists with the measure present but over the limit: misses, with that record as nearest. If the measure is missing on the nearest place (no `walkingMinutes`): not-known (never switch to straight-line). If the limit is a distance over 5,000 m and nothing meets: not-known-beyond-search. Records that are `no-record-in-source`, `source-failed` or `not-covered` alone: not-known. Broadband: the recorded predicted download speed at or above the limit meets.

- [ ] **Step 1:** Work cases by hand from Task 2 records: a GP within its walking limit (meets); a station over its limit (misses); childcare `no-record-in-source` (not-known); a place with distance but no walking time against a minutes limit (not-known); exactly at the limit (meets); a 10-mile limit with nothing recorded (not-known-beyond-search); broadband at, above and below.
- [ ] **Step 2:** Write `test_priority_result_worked_cases_match_expected`, `test_priority_result_no_record_in_source_is_not_known_never_misses`, `test_priority_result_exactly_at_limit_meets`, `test_priority_result_missing_walking_time_is_not_known_not_straight_line`, `test_priority_result_limit_beyond_search_with_nothing_found_is_not_known_beyond_search`.
- [ ] **Step 3:** Run (FAIL), implement, run (PASS). Commit: `feat: priority results, meets misses or not known (FE-40)`.

### Task 7: Generator writes `area-result.json`

**Files:**
- Create: `packages/fixtures/schema/generated-area-result.schema.json`, `packages/vestagraph-generator/src/vestagraph_generator/area_generator.py`, `packages/vestagraph-generator/tests/test_generator_area.py`
- Modify: `packages/vestagraph-generator/pyproject.toml` (depend on `vestagraph-area`), `packages/vestagraph-generator/src/vestagraph_generator/costs_generator.py` (stop deleting `area-result.json`), `__main__.py` (run both; exit codes unchanged), `Makefile` comment, AGENTS.md Commands table (`make generate` writes both files), `packages/fixtures/README.md`
- Generated: `packages/fixtures/generated/area-result.json`

**Interfaces:**
- Consumes: Tasks 3 to 6.
- Produces: `area-result.json`: `{ "$schema", "formatVersion": 1, "postcodes": [ { "postcode", "glance": {found, notKnown, coverageFound, coverageTotal, questions: [{recordId, text}], checkInPerson: [{topicKey, text}]}, "topics": [{key, outcome}], "distances": [{recordId, metres, walkingMinutes?, display}], "busesPerHour": [{stopItemId, hour, count}], "priorities": [{priorityId, outcome, nearestRecordId}] } ] }`, sorted by postcode then id, so a rerun is byte-identical.

- [ ] **Step 1:** Write `test_run_writes_costs_and_area_result_and_keeps_both`, `test_run_area_result_twice_is_byte_identical`, `test_run_area_data_with_missing_topic_exits_two_and_writes_nothing`.
- [ ] **Step 2:** Run. Expected: FAIL (no `area-result.json`).
- [ ] **Step 3:** Implement; run `make generate`; commit the generated file.
- [ ] **Step 4:** Run `make check`. Expected: PASS, including generated-check and validate.
- [ ] **Step 5:** Commit: `feat: generator writes area-result.json`.

### Task 8: PR A, review and merge
- [ ] Map each acceptance item (Tasks 3 to 7 rules, Review Focus 1 to 5) to its test name in the PR description, with the test-first slice table.
- [ ] Ask the founder, in the PR, to review the draft question templates and check-in-person lists (`reviewStatus: "draft"` becomes `"reviewed"` on approval).
- [ ] Pre-push Opus review with `code-security-reviewer`; fix; push; `@codex review`; merge per AGENTS "When merging". Update `docs/planning/status.md` in the PR.

### Task 9: Canvas, result boards (light)
Board values come only from `area-result.json` and `postcode-area.json` (quote, never work out). Style: canvas 138 Brand and style sections 7 to 9.
- [ ] Board "Check an area · result" (phone, 390 wide), no priorities set: header with Display button, At a glance (found, not known, questions to ask with counts; "Things to check in person →" without a count; coverage line; "What matters to you · Set priorities"), topic rows in registry order, "Ask about this area" entry with AI badge (FE-13), closed "How we got this".
- [ ] Board "Check an area · result desktop" (1440): At a glance and topic list left, map right with legend, category filters and a place list (B17, B24), "distances measured from the postcode centre" line.
- [ ] Acceptance: no verdict words (B1); every figure has its area or radius beside it (B3); 320 px reflow noted on the board; touch targets ≥ 44 px.
- [ ] Acceptance: quoted source text (for example the NB7 1RR planning description) is shown as quoted and never read as our wording; sold prices show street and property type only, never `addressText` (DA-13).

### Task 10: Canvas, priorities and topic boards (light)
- [ ] Priorities sheet (phone) and panel (desktop, FE-26 one at a time): ready-made limits with editable numbers and units, validation message example, the three outcomes from `area-result.json` priorities, "Checking your priorities…", "Couldn't check this · Try again", "Not known beyond 5 km".
- [ ] Topic sheet (phone) and panel (desktop) for Schools, Recorded crime, Deprivation, Flood, in the anatomy order of the spec; Flood has no map (FE-25); deprivation text in the fact's own words (DA-17); Escape and focus notes on the board.

### Task 11: Canvas, How we got this, About the data, states, display (light)
- [ ] "How we got this" opened (phone): every topic's method and limits, including the counts' and priorities' methods.
- [ ] About the data: each source with date and status (where a stale source shows).
- [ ] States board: every state in the spec's board 7 list, each with cause, reassurance and one action.
- [ ] Display settings: theme (device, light, dark) and text size (standard, large, larger), the phone result at the largest size; a note that choices aren't remembered until the PECR check.
- [ ] Remove the boards these replace (the old Check an area and area-states boards, light and dark) in the same canvas change, and list them.

### Task 12: Founder review, then dark versions
- [ ] Founder reviews the light boards (canvas link, comments); fix.
- [ ] Draw the dark versions (slate ink) of every approved board.

### Task 13: PR B, record and hand over
- [ ] Branch `docs/first-design-batch-canvas`: status file (canvas version, boards added and removed), any register notes the review produced. Fallback documentation rules apply if Codex is unavailable.
- [ ] Next plan: the specifications for this batch (feature files for At a glance, priorities, topic anatomy, states), written after the founder approves the boards.
