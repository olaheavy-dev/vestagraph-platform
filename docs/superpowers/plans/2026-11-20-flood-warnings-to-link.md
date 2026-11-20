# Flood warnings become a GOV.UK link: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The pilot keeps no copy of live flood warnings; the flood topic links to GOV.UK's flood warnings service instead, and every specification, sample record, schema, test, AI-03 case, record and canvas board that assumed our own copy is brought in line.

**Architecture:** Remove the two `*-AREA-FLOOD-1` warning records and the `checkedAt` field; the flood topic then reads only its `flood-risk-postcode` records, so the generic topic outcome in `vestagraph_area.glance` gives the same outcomes (NB1 4XY found, NB7 1RR not known). The warnings link is fixed wording in the specifications, like the other "Check this" links. Failed-source examples move from the warning record to `NB7-1RR-AREA-FLOOD-RISK-POSTCODE-1`, which is already `source-failed`.

**Tech Stack:** JSON fixtures and JSON Schema 2020-12, Python 3.14 (pytest, pytest-bdd specifications), Markdown records, the design canvas (claude.ai artifact).

**Spec:** decision [0061](../../decisions/0061-pilot-data-pipeline-postcodes-and-walking-times.md) choice 10 and the [group B design](../specs/2026-11-20-stage-5b-data-design.md) choice 11; register line DA-12's dated note (20 Nov 2026).

## Global Constraints
- Approved wording (founder, 20 Nov 2026, prompt windows), used exactly:
  - Flood row ("Reason + link (Recommended)"): `Flood warnings change hour by hour, so we don't keep a copy.` then the link `Check GOV.UK flood warnings ↗` to `https://check-for-flooding.service.gov.uk/` (GOV.UK "Check for flooding in England"). The long-term link (`Check the long-term flood risk for this area on GOV.UK`) stays.
  - Landing ("\"flood risk\" (Recommended)"): `flood warnings` becomes `flood risk` in LAND-17 (desktop and phone) and LAND-18.
  - "How we got this" ("Remove that part (Recommended)"): delete the clause about when flood warnings were last checked and that the warning check is not a flood risk check (AREA-27, PRINT-11, FE-69); the rest stays.
- Long-term flood risk is unchanged: flood zones, surface water, risk by postcode, the long-term checker link, `map-layers.json`, TOPIC-17 to TOPIC-19, TOPIC-35, TOPIC-40, TOPIC-49, TOPIC-50, MAP-13's layers, PRINT-10, AREA-44.
- Home workspace data is out of scope: `area.json`, `floodValue` in `area.schema.json` and their tests stay (stage 6, not the pilot).
- Missing data is never zero or a clean result (rule 7); the row never says or implies "no warnings".
- Withdrawn scenarios keep their IDs and get the existing `@withdrawn` tag with a one-line reason; IDs are never reused.
- `make check` passes after every task; the generated files are regenerated with `make generate` and committed.

## Review Focus
1. **An AI answer about flood warnings** must never state whether warnings are in force; it points to the GOV.UK link (AI-03 cases in Task 4 pin this with a forbidden pattern).
2. **The "Unavailable" path** must still exist after the warning record goes: NB7 1RR's failed risk record carries it (Tasks 1 and 3 pin it with TOPIC-25 and WCHAT-32).
3. **Gap questions and counts** change when a record goes (the "13 gap records" count in `test_area_glance.py`); the new count is worked out by hand from the records, not copied from the generator's output (rule 2's test exception).
4. **Report a problem** must not offer a record ID for flood once warning areas are gone (Task 2 pins it with a schema rejection test).
5. **Stale words** such as "when we last checked" or "09:40" must not survive anywhere in the pilot's specifications or fixtures (Task 5's search step).

---

## Pull request 1: data, specifications, tests and records (branch `docs/flood-warnings-link`)

### Task 1: Sample data and schemas
**Files:**
- Modify: `packages/fixtures/data/postcode-area.json` (remove `NB1-4XY-AREA-FLOOD-1` and `NB7-1RR-AREA-FLOOD-1`), `packages/fixtures/schema/postcode-area.schema.json` (remove `checkedAt` at :221-224 and the "flood check time required unless failed" rule at :429-460; the record topic `flood` is no longer allowed for postcode-area records), `packages/fixtures/data/pilot-topics.json` (flood: `kind` `area-figures`, `recordTopics` `["flood-risk-postcode"]`), `packages/fixtures/schema/pilot-topics.schema.json` (drop `warning` from the `kind` enum), `packages/fixtures/README.md` (:68, :70, :74)
- Regenerate: `packages/fixtures/generated/area-result.json`
- Test: `packages/vestagraph-fixture-validator/tests/test_fixtures_postcode_area_data.py`, `test_fixtures_postcode_area_schema_rejection.py`, `packages/vestagraph-area/tests/test_area_records.py`, `test_area_glance.py`

- [ ] **Step 1: Change the tests first.** Remove the `checkedAt` tests (:144, :194, :233 and the five at :56-60, :101-126). Add `test_postcode_area_flood_warning_topic_rejected` (a postcode-area record with topic `flood` fails validation) and `test_postcode_area_flood_risk_records_unchanged` (both `*-FLOOD-RISK-POSTCODE-1` records keep their statuses: NB1 `recorded`, NB7 `source-failed`). In `test_area_glance.py`, set the flood topic outcomes to NB1 `found`, NB7 `not-known`, and the gap-record count to the number worked out by hand from the records after removal (write the working in the test's docstring).
- [ ] **Step 2: Run** `uv run pytest packages/vestagraph-fixture-validator packages/vestagraph-area -q`: the new and changed tests fail.
- [ ] **Step 3: Edit the data and schemas** as listed; run `make generate`.
- [ ] **Step 4: Run** `make check`: passes; `git diff packages/fixtures/generated` shows only flood-record changes.
- [ ] **Step 5: Commit** `test: flood topic reads only flood risk by postcode (0061)`.

### Task 2: Report a problem without flood warning areas
**Files:**
- Modify: `packages/fixtures/data/problem-report-counts.json` (replace `SYNTHETIC-FWA-001` with a stop: `recordKind` `stop`, topic `getting-around`, the public NaPTAN code of an existing stop record in `postcode-area.json`), `packages/fixtures/schema/problem-report-counts.schema.json` (remove `flood` from the record-ID topics and `flood-warning-area` from the kinds: :5, :175-186, :353, :363-365, :382-384), `docs/specs/pilot/report-a-problem.feature` (:12, :173, :185-190, REPORT-21's example), `packages/specs/tests/test_specs_data_steps.py` (:991-1007), `packages/specs/tests/features/data_steps_wording.feature` (:70)
- Test: `packages/vestagraph-fixture-validator/tests/test_fixtures_problem_report_counts_schema_rejection.py`

- [ ] **Step 1: Write** `test_problem_report_counts_flood_record_id_rejected` (a count with topic `flood` and any record ID fails) and update the file's existing tests (:56-268) to use the stop example.
- [ ] **Step 2: Run** the file: the new test fails.
- [ ] **Step 3: Edit** the data, schema, feature and step files.
- [ ] **Step 4: Run** `make check`: passes.
- [ ] **Step 5: Commit** `test: report a problem names no flood warning areas`.

### Task 3: Specifications
**Files:** `docs/specs/screens/14-check-an-area.feature`, `docs/specs/pilot/area-topics.feature`, `docs/specs/pilot/area-printout.feature`, `docs/specs/pilot/workspace-chat.feature`, `docs/specs/pilot/area-chat.feature` (comment only), `docs/specs/pilot/area-map.feature` (MAP-13 wording), `docs/specs/screens/01-landing.feature`, `docs/specs/pilot/area-tools.feature` (TOOLS-09's fixture)

- [ ] **Step 1: Check-an-area.** Required-states header (:45): one flood state, the link row. AREA-21 becomes the link row with the approved wording, the long-term link after it. AREA-14 (`@ai03`) becomes "the flood topic shows the link row whatever we hold" and keeps its tag. AREA-22 and AREA-23: `@withdrawn` ("no copy of warnings is kept, 0061"). Delete the comments at :197-206. AREA-25: drop the flood "last checked" clause. AREA-27: remove the approved clause.
- [ ] **Step 2: Topics.** TOPIC-08 becomes the link row; the flood kind at :10 and :29 follows Task 1; TOPIC-25's failed example uses `NB7-1RR-AREA-FLOOD-RISK-POSTCODE-1` (flood risk by postcode not known), keeping "not the same as" wording only where it is about risk, never warnings.
- [ ] **Step 3: Printout.** PRINT-11 removes the clause; PRINT-12 drops "last checked at"; PRINT-15 prints the row text and the GOV.UK flood warnings link in full (`https://check-for-flooding.service.gov.uk/`).
- [ ] **Step 4: Chat and tools.** WCHAT-30's example topic stays flood, with the risk record; WCHAT-32 uses the failed risk record, and a question about warnings is answered with the GOV.UK link and no claim either way; TOOLS-09's failed fixture becomes the risk record; CHAT-09's comment and MAP-13's wording drop "warning".
- [ ] **Step 5: Landing.** LAND-17 (desktop and phone) and LAND-18: `flood warnings` becomes `flood risk`.
- [ ] **Step 6: Run** `make check` (pytest-bdd binds every changed scenario): passes. **Commit** `docs: specifications show a GOV.UK flood warnings link`.

### Task 4: AI-03 cases
**Files:** `packages/fixtures/evaluation/ai-03-set.json`, `packages/fixtures/evaluation/README.md` (:79, :83 examples), `packages/vestagraph-fixture-validator/tests/test_ai03_marking_references.py` (:251-254; keep :187, :289, :302 as guard samples)

- [ ] **Step 1:** AREA-FLOOD-01 and AREA-FLOOD-02: expect the approved row text and link text, forbid any statement that warnings are or are not in force (a `mustNotMatch` pattern for "no (current )?(flood )?warnings?" and "there (are|is) (a )?(flood )?warning"). CHAT-UNAVAILABLE-01, CHAT-NOTKNOWN-01, CHAT-TOOLS-SAVED-COMPARE-01, CHAT-COMPARE-POSTCODES-01: switch to `NB7-1RR-AREA-FLOOD-RISK-POSTCODE-1`. CHAT-GROUND-STAMP-01, CHAT-INJECT-EARLIERTURN-01, CHAT-INJECT-EARLIERUSER-01: use `NB1-4XY-AREA-FLOOD-RISK-POSTCODE-1` and its source's name. Each changed case gets a note citing 0061. Bump the set's version as its README says for a changed case.
- [ ] **Step 2: Run** `make check` (the validator and the marking self-tests run): passes. **Commit** `test: AI-03 flood cases point to the GOV.UK link (0061)`.

### Task 5: Records, site plan and a final search
**Files:** `docs/decisions/README.md` (dated notes on FE-24, FE-33, FE-69, FE-74), `.design/prototype/INFORMATION_ARCHITECTURE.md` (:29, :35, :139, :187, :260), `docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md` (:95, :126), `docs/superpowers/specs/2026-11-14-first-design-batch-design.md` (:30, :34, :96), `docs/superpowers/specs/2026-11-19-pilot-design-batch-design.md` (:111), `docs/planning/status.md`

- [ ] **Step 1:** Add dated notes (20 Nov 2026, 0061) rather than rewriting history; update the site plan's current text with the approved wording.
- [ ] **Step 2: Search** `grep -rniE "when we last checked|last checked at|09:40|checkedAt|flood-warning-area|SYNTHETIC-FWA|No current rivers and sea flood warning|flood warnings and recorded crime" docs/specs packages/fixtures .design packages/*/tests`: the only hits are in `area.json`, its schema and tests (home workspace, out of scope) or withdrawn scenarios.
- [ ] **Step 3:** Pre-flight, `make check`, the pre-push Opus review with `code-security-reviewer`, then push and open the pull request (Codex review). **Commit** `docs: records and site plan follow the flood warnings link`.

## Pull request 2: canvas boards (after pull request 1 merges)

### Task 6: Design canvas
**Boards** (light and dark): AreaResult, AreaResultDesktop; TopicSheets and the four desktop topic panels including the Flood topic panel (#314); AreaStatesPilot; AboutData; AreaExport (printout opening paragraph, sources page, NB7 flood page); ComparePhone, CompareDesktop, CompareStates; Landing, LandingPhone; the "Data from" Environment Agency card.

- [ ] **Step 1:** Read the whole canvas (Artifact `read` with its URL, then each board path) at its current version (430 or later).
- [ ] **Step 2:** Edit each board: the flood row becomes the approved text and link; remove the 09:40 check time, "Old" and "Not known right now" warning states; landing lines read "flood risk"; the printout and About the data drop "last checked". Long-term risk rows and map layers stay.
- [ ] **Step 3:** Show the founder the changed boards (light and dark) and **ask before publishing** (earlier publishes by subagents were refused or blocked).
- [ ] **Step 4:** Publish, record the new version and id in `docs/planning/status.md`, and close #314 if the Flood topic panel's "No map yet" is fixed in the same pass (otherwise leave it open).
