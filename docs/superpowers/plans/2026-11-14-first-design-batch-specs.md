# First design batch specifications Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the approved first-design-batch boards (canvas version 178) into Gherkin specifications that the pilot gate checks and the stage 5b build is tested against.

**Architecture:** Four new pilot feature files, one per part of the area result, plus the data steps they need. Data scenarios (no tag) check `packages/fixtures/generated/area-result.json` and run in `make check` now; `@ui` scenarios describe the page and run from stage 5 with playwright-bdd. Existing scenarios in `14-check-an-area.feature` (AREA-25, AREA-27 and the states AREA-04 to AREA-23) are referenced, not duplicated.

**Tech Stack:** Gherkin (decision 0043), pytest-bdd data steps in Python (decision 0049), mypy strict, ruff.

**Spec:** `docs/superpowers/specs/2026-11-14-first-design-batch-design.md` (approved), with the register lines it names and the founder's later decisions of 14 Nov 2026: FE-24, FE-33, FE-34 and DA-12 amended (About the data as one general page with dates only; a short "How we got this" on each result), FE-40 ("Not known beyond 3.1 miles"), FE-42 (map style), DA-20 (gap labels carry no distances). The boards are the visual reference: canvas https://claude.ai/artifact/MpvQNDVYCePp4iWM3j3Jx4, version 178.

## Global Constraints
- `docs/specs/README.md` rules apply in full: every acceptance criterion is a `Scenario:` with a permanent ID; IDs are never reused; one observable outcome per scenario; required states mapped in each feature description.
- Rule 2: no calculated figure typed in a scenario. Counts, distances, buses per hour and coverage are cited by postcode and record ID from `area-result.json`, never as numbers. Inputs are cited by record ID from `postcode-area.json`.
- Rule 4 and README rule 5: no scenario expects "verified", "safe", "approved", a score, a band, a total of priorities or a "better area".
- Rule 7: every gap state is named; none is expected to read as zero, "none", a miss or a clean result.
- IDs: GLANCE-nn (At a glance), PRIO-nn (priorities), TOPIC-nn (topic sheet and panel), DISP-nn (display settings). New states not already in `14-check-an-area.feature` get AREA-28 onwards there.
- Wording on the page is quoted only where a decision fixes it ("Not known beyond 3.1 miles", "We hold no current copy", "Things to check in person →", "Couldn't check this · Try again", "Checking your priorities…"); otherwise scenarios describe the element, not its copy.
- Test names `test_<method>_<condition>_<result>` (decision 0039); new step tests in `packages/specs/tests/test_specs_data_steps.py`.
- No agent attribution in commits or pull requests.

## Review Focus
1. **A postcode with a topic outcome of `not-known`** must never be counted as found: GLANCE-03 (data) pins it for NB7 1RR.
2. **A priority on a `no-record-in-source` record** must be `not-known`, never `misses`: PRIO-04 (data) pins `SAMPLE-PRIORITY-CHILDCARE` for NB1 4XY.
3. **A priority limit beyond the search** must be `not-known-beyond-search`: PRIO-05 (data) pins `SAMPLE-PRIORITY-HOSPITAL`.
4. **A route-only topic** must be left out of the coverage total and still show its official link: GLANCE-05 (data) and TOPIC-12 (`@ui`).
5. **A gap label shown without its radius** breaks B2: TOPIC-09 (`@ui`) requires the radius beside every "no record" gap (DA-20).

---

### Task 1: Data steps for the area result

**Files:**
- Modify: `packages/specs/tests/specs_steps.py`, `packages/specs/tests/specs_support.py` (loader for `area-result.json`)
- Test: `packages/specs/tests/test_specs_data_steps.py`
- Modify: `packages/specs/tests/features/data_steps_wording.feature` (WORD-03 uses every new wording), `docs/specs/README.md` (data steps list)

**Interfaces:**
- Produces these eight step wordings (the contract the feature files use):
  - `Then area result "<postcode>" has topic "<topic key>" with outcome "<found | not-known | not-covered>"`
  - `Then area result "<postcode>" leaves topic "<topic key>" out of the coverage total`
  - `Then area result "<postcode>" asks the gap question for record "<record ID>"`
  - `Then area result "<postcode>" has priority "<priority ID>" with outcome "<meets | misses | not-known | not-known-beyond-search>"`
  - `Then area result "<postcode>" has priority "<priority ID>" with nearest record "<record ID>"`
  - `Then area result "<postcode>" has a display distance for record "<record ID>"`
  - `Then area result "<postcode>" counts buses for stop "<record ID>" on route "<route>" at hour <8 | 12>`
  - `Then postcode record "<record ID>" has status "<recorded | no-record-in-source | stale | source-failed | not-covered>"` (a record in `packages/fixtures/data/postcode-area.json`; the existing `area record` step reads `area.json`)
- Each step fails with a message naming the postcode and ID when the item is missing; an unknown postcode fails naming it.

- [ ] **Step 1: Write failing tests**, one per wording (eight), each with a passing case and a failing case naming the ID, for example `test_then_area_result_priority_outcome_wrong_outcome_fails_naming_the_id` (NB1 4XY, `SAMPLE-PRIORITY-CHILDCARE`, "misses" must fail; "not-known" passes) and `test_then_area_result_topic_left_out_of_coverage_counted_topic_fails` (NB1 4XY, "schools" must fail; "noise" passes).
- [ ] **Step 2: Run** `uv run --locked pytest packages/specs/tests/test_specs_data_steps.py -v`. Expected: FAIL (steps not defined).
- [ ] **Step 3: Implement** the seven steps on `DataSteps`, reading `area-result.json` once through `specs_support`; a topic is left out of the coverage total when it is absent from the postcode's `topics` list (registry `counted` is false, `packages/fixtures/data/pilot-topics.json`) or its outcome is "not-covered".
- [ ] **Step 4: Run** the same command, then `make check`. Expected: PASS, including WORD-03.
- [ ] **Step 5: Commit** `test: data steps for the area result (first design batch specs)`.

### Task 2: At a glance (`docs/specs/pilot/area-glance.feature`)

**Files:** Create `docs/specs/pilot/area-glance.feature`.

**Interfaces:** Consumes Task 1's wordings.

- [ ] **Step 1: Write the feature** with its description (question it answers, fixtures NB1 4XY, NB7 1RR, NB9 9ZZ, required states: all found, some not known, sparse, unknown postcode) and these scenarios:
  - GLANCE-01 (data) NB1 4XY: every counted topic has outcome "found" (one `Then` per counted topic key from `pilot-topics.json`).
  - GLANCE-02 (data) NB1 4XY asks the gap questions for `NB1-4XY-AREA-AMENITY-6` and `NB1-4XY-AREA-FLOOD-1`.
  - GLANCE-03 (data) NB7 1RR: "flood" and "transport-connectivity" have outcome "not-known".
  - GLANCE-04 (data) NB7 1RR asks the gap question for `NB7-1RR-AREA-AMENITY-2`.
  - GLANCE-05 (data) route-only topics "council-tax-band-home", "mobile-by-network", "noise", "ground-and-mining" and the uncounted "family-view" are left out of the coverage total for both postcodes; NB7 1RR's "green-space" has outcome "not-covered" and is left out too.
  - GLANCE-06 `@ui` At a glance comes first: found, not known and questions to ask with their counts from `area-result.json`, "Things to check in person →" with no count (FE-41), the coverage line, and "What matters to you · Set priorities".
  - GLANCE-07 `@ui` each count opens the list of its items, each item opening its topic; a count of zero shows "None to list" and no link.
  - GLANCE-08 `@ui` "Things to check in person" opens the fixed reviewed list per topic from `pilot-topics.json` (FE-39).
  - GLANCE-09 `@ui` at 320 px the tiles stack into one column with no sideways scroll; every tap target is at least 44 px (B15, B17).
- [ ] **Step 2: Run** `make check`. Expected: PASS (data scenarios run, `@ui` collected and skipped).
- [ ] **Step 3: Commit** `docs: At a glance specifications (GLANCE-01 to 09)`.

### Task 3: Priorities (`docs/specs/pilot/area-priorities.feature`)

**Files:** Create `docs/specs/pilot/area-priorities.feature`.

- [ ] **Step 1: Write the feature** (required states: meets, misses with nearest, not known, not known beyond the search, checking, couldn't check, invalid limit) with:
  - PRIO-01 (data) NB1 4XY: `SAMPLE-PRIORITY-GP` meets with nearest record `NB1-4XY-AREA-AMENITY-10`.
  - PRIO-02 (data) NB1 4XY: `SAMPLE-PRIORITY-RAIL` meets, nearest `NB1-4XY-AREA-TRANSPORT-STOP-2`; `SAMPLE-PRIORITY-PRIMARY` meets, nearest `NB1-4XY-AREA-SCHOOL-1`; `SAMPLE-PRIORITY-BROADBAND` meets.
  - PRIO-03 (data) NB7 1RR: `SAMPLE-PRIORITY-PRIMARY` misses with nearest record `NB7-1RR-AREA-SCHOOL-1`; `SAMPLE-PRIORITY-BROADBAND` misses.
  - PRIO-04 (data) `SAMPLE-PRIORITY-CHILDCARE` is "not-known" for both postcodes (Review Focus 2).
  - PRIO-05 (data) `SAMPLE-PRIORITY-HOSPITAL` is "not-known-beyond-search" for both (Review Focus 3).
  - PRIO-06 `@ui` the sheet (phone) and panel (desktop, FE-26) list the ready-made limits: GP surgery, pharmacy, primary school, secondary school, railway station, bus stop, supermarket, park or green space, childcare provider, hospital, broadband speed; each with an editable number and unit and the line saying what it uses (walking time, straight-line distance, predicted speed).
  - PRIO-07 `@ui` an empty or non-numeric limit shows its message under the box and is not sent.
  - PRIO-08 `@ui` each result is listed on its own; no total, count or ranking of priorities appears anywhere (FE-22).
  - PRIO-09 `@ui` a miss shows "Misses your limit · nearest recorded <distance>" from `area-result.json`.
  - PRIO-10 `@ui` a limit past the search reads "Not known beyond 3.1 miles" (FE-40).
  - PRIO-11 `@ui` "Checking your priorities…" while waiting, announced to screen readers; "Couldn't check this · Try again" on failure, never a miss.
  - PRIO-12 `@ui` limits are sent with the postcode only to work out results and are never stored or logged; "Remember these on this device" is off by default and stays in the browser; a shared link never carries them.
  - PRIO-13 `@ui` Escape or the phone's Back closes the sheet and focus returns to "Set priorities" or "Edit".
- [ ] **Step 2: Run** `make check`. Expected: PASS.
- [ ] **Step 3: Commit** `docs: priorities specifications (PRIO-01 to 13)`.

### Task 4: Topic sheet and panel (`docs/specs/pilot/area-topics.feature`)

**Files:** Create `docs/specs/pilot/area-topics.feature`.

- [ ] **Step 1: Write the feature** (one anatomy, four kinds; required states: gap, stale record, failed copy, no map) with:
  - TOPIC-01 `@ui` every topic opens in the same order (B29): title and headline (the row's own line), your priority result if one is set, facts with the area each covers, the map where the topic has places, gaps, what to do next, Explain this, source stamps.
  - TOPIC-02 `@ui` phone: a bottom sheet with Close; Escape or Back closes it; focus returns to the row; the open topic has its own link (B14).
  - TOPIC-03 `@ui` desktop: a panel beside the list in place of the map, one at a time (FE-26); focus moves to its heading.
  - TOPIC-04 `@ui` Schools: each school with its phase, type, distance and walking time from `area-result.json`, its inspection date and framework, and its admissions figures quoted from records `NB1-4XY-AREA-SCHOOL-DEMAND-1` and `-2`; the desktop panel has its own small map.
  - TOPIC-05 (data) postcode record `NB1-4XY-AREA-SCHOOL-INSPECTION-1` has status "stale" (the inspection date is the fact and stays shown).
  - TOPIC-06 `@ui` Recorded crime: counts by month and category for records `NB1-4XY-AREA-CRIME-1` and `-2`, "within 1 mile", the neighbourhood team, and never on a map (B5).
  - TOPIC-07 `@ui` Deprivation: the decile and rank quoted from `NB1-4XY-AREA-DEPRIVATION-RANK-1` in one sentence with which end is most deprived, "compared with other neighbourhoods", and that it describes the neighbourhood, not this street or home (0054, DA-17).
  - TOPIC-08 `@ui` Flood: warnings with "when we last checked, at <time>" from `NB1-4XY-AREA-FLOOD-1`, the long-term risk link, the properties-by-likelihood counts quoted from `NB1-4XY-AREA-FLOOD-RISK-POSTCODE-1`, and no map (FE-25).
  - TOPIC-09 `@ui` a "no record in this source" gap shows its label with the search distance beside it in the display unit (DA-20, B2; Review Focus 5).
  - TOPIC-10 `@ui` What to do next lists the gap question where one exists and every check-in-person item for the topic (FE-39).
  - TOPIC-11 `@ui` Explain this shows the reviewed text when it exists; otherwise "Explanation not yet available" and no "Ask more about this" (AI-12, CHAT-53).
  - TOPIC-12 `@ui` a route-only topic says "Not yet covered" with its official link and no facts (Review Focus 4).
- [ ] **Step 2: Run** `make check`. Expected: PASS.
- [ ] **Step 3: Commit** `docs: topic sheet and panel specifications (TOPIC-01 to 12)`.

### Task 5: States, display settings and cross-links

**Files:** Modify `docs/specs/screens/14-check-an-area.feature`; create `docs/specs/pilot/area-display.feature`; modify `docs/specs/README.md`, `docs/planning/status.md`.

- [ ] **Step 1: Add the states not yet specified** to `14-check-an-area.feature`, each with cause, reassurance and one action (B22): AREA-28 postcode service down ("Try again", never "not found"), AREA-29 area rate limit, AREA-30 offline, AREA-31 all sources down (rows stay, each "Not known right now", one line pointing to About the data), AREA-32 a search crossing the border (places across it may be missing, B9), AREA-33 sparse area (NB7 1RR: the map opens zoomed to its places with the outer ring "3.1 miles", FE-42). Map each in the feature's required-states list.
- [ ] **Step 2: Write `area-display.feature`** with DISP-01 the Display button opens theme (Device, Light, Dark) and text size (Standard, Large, Larger); DISP-02 at Larger the result reflows to one column with no sideways scroll; DISP-03 the choices are not remembered between visits until the PECR check, so nothing is stored (FE-23, B16).
- [ ] **Step 3: Update** the README layout table (the four new pilot files) and the status file (this batch's specs done; next City Explorer).
- [ ] **Step 4: Run** `make check`. Expected: PASS.
- [ ] **Step 5: Commit** `docs: states and display specifications; cross-links`.

### Task 6: Review and pull request
- [ ] Map every board on canvas version 178 to at least one scenario ID (a table in the pull request).
- [ ] Fresh-context Opus review with "Code Review Rules"; fix; push one branch `docs/first-design-batch-specs`; `@codex review`; merge when the conditions in AGENTS.md hold.

## As built
Task 2 has eight steps, not seven. Task 3 ended at PRIO-19 and Task 4 at TOPIC-25 (TOPIC-20 withdrawn), after the final review; the maps' behaviour was added as `area-map.feature` (MAP-01 onwards) from register line FE-42.
