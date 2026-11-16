# Design pass Task 6a: sample data for the new topics (plan)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development or superpowers:executing-plans, with test-driven-development and the project's test-first skill. Steps use checkbox (`- [ ]`) syntax.

**Goal:** add the synthetic inputs that the design pass's boards (Task 6b of [`2026-11-16-benchmark-design-pass.md`](2026-11-16-benchmark-design-pass.md)) need for the topics the founder marked "add" (register lines DA-22, DA-23, DA-24, DA-27, DA-28, DA-29), so that no board types a figure by hand (rule 2).

**Founder's answers (16 Nov 2026, prompt window):**
- Radon: "Its own 'Radon' topic (Recommended)".
- Council rent: "Inside Housing affordability (Recommended)".
- Broadband: "Replace it now" (over the agent's recommendation to keep the old predicted-speed record for the speed priority). The old predicted-speed broadband record and the broadband speed priority are removed from the pilot's postcode sample data and priorities.

**Architecture:** quoted inputs only, with no new calculation code. Three new record topics go in `postcode-area.json` (`radon`, `broadband-coverage`, `council-rent`). Map outlines go in a new `map-layers.json`, which no counted topic reads. One new counted topic, "Radon", goes in `pilot-topics.json`. The existing tested code regenerates `area-result.json`. No new packages.

**Research and rules:** [`docs/reviews/2026-11-16-data-gaps-research.md`](../../reviews/2026-11-16-data-gaps-research.md); rules 1, 2, 3 and 7; DA-14 (levels), DA-30 (council-wide figures come from `council-area.json`), FE-38, FE-39 (approved wording), FE-41 (counts).

## 1. Data contract

### 1.1 Constraints from the existing code
- **Places have no coordinates.** Places carry only `distanceMetres` from the postcode centre.
- **Every record needs exactly one topic.** `vestagraph_area/glance.py` `_check_ownership` stops if a `postcode-area.json` record belongs to no topic or to two counted topics, and a counted topic with no record for a postcode also stops it. So map layers live in their own file.
- **New values must not be picked up as distances.** `area_generator._distances` reads any value with `distanceMetres`, and the new values have none.
- **Northbridge's rent is already calculated.** `council-area.json` maps NB1 4XY to E06999001, and `council-result.json` already holds that council's rent caption (`captions[topic=rent].values.toValue`, `toPeriod`) and `rentOrBuy.rentPointStatus`.

### 1.2 `postcode-area.json`: new records
**Schema (`schema/postcode-area.schema.json`):**
- Add `radon`, `broadband-coverage` and `council-rent` to the topic enum.
- Add a level kind `grid-square` with a required integer `squareMetres` (minimum 1).
- Add three value definitions, each with `additionalProperties: false` and one `if`/`then` per topic:
  - `radonValue`: required `classLabel` (string, at least 1 character, as published) and `edition` (`^\d{4}$`). No measured-level or per-home field.
  - `broadbandCoverageValue`: required `gigabitCapablePercent` (a decimal string), `premises` (`all` or `residential`) and `snapshot` (`^\d{4}-\d{2}$`). No `technology` or full-fibre field.
  - `councilRentValue`: required `councilCode` (the council code pattern). A link only: no pence, period or figure.
- **Remove** `broadband` from the topic enum and its predicted-availability value shape, in line with the founder's "Replace it now". Keep any definition `area.schema.json` (the home-keyed file, used later) still needs.

**Pattern for every record:** `source.origin: "official-dataset"`, `synthetic: true` and `date: "2026-10-23"`. Each `source.label` reads "Synthetic sample, shaped like …":
- radon: "the BGS and UKHSA Indicative Atlas of Radon";
- broadband coverage: "the Ofcom Connected Nations postcode data";
- council rent: "the ONS Price Index of Private Rents".

| id | topic | status | level | value |
|---|---|---|---|---|
| `NB1-4XY-AREA-RADON-1` | radon | recorded | grid-square, 1000 | `classLabel` "Class 2 (synthetic example)", `edition` "2022"; link to the UKradon address search; a `note` that class names are to be confirmed from the download |
| `NB7-1RR-AREA-RADON-1` | radon | source-failed | grid-square, 1000 | none; label "Radon lookup failed; not known right now" |
| `NB1-4XY-AREA-BROADBAND-COVERAGE-1` | broadband-coverage | recorded | postcode | `gigabitCapablePercent` "86", `premises` "all", `snapshot` "2026-01"; a `note` that column names are to be confirmed |
| `NB7-1RR-AREA-BROADBAND-COVERAGE-1` | broadband-coverage | no-record-in-source | postcode | none |
| `NB1-4XY-AREA-COUNCIL-RENT-1` | council-rent | recorded | local-authority, "Northbridge (synthetic)" | `councilCode` "E06999001"; label "Average private rent, Northbridge (synthetic)" |
| `NB7-1RR-AREA-COUNCIL-RENT-1` | council-rent | no-record-in-source | local-authority, "Fellshire Council (synthetic)" | none |

**Remove** the old `broadband` records (`NB1-4XY-AREA-BROADBAND-…`, `NB7-1RR-AREA-BROADBAND-…`) from `postcode-area.json`.

**Limit text (`doesNotEstablish`).** Each uses the register phrases word for word; the rest is proposed wording and is listed in section 3.
- **Radon (DA-23):** "Indicative, not definitive: the class is the highest found anywhere in this 1 km square, not a test of this home. Only a measurement in the home gives its radon level. A low class does not mean no radon."
- **Broadband coverage (DA-28):** "The share of premises in this postcode where providers say gigabit-capable broadband is available. It can't say whether a home has full fibre or a working connection, or what speed you would get."
- **Council rent (DA-29):** "A council-wide average, not this street. It does not say what any one home would rent for."

**How the boards quote the rent:**
1. Read the record.
2. If it is recorded, take the figure from `council-result.json` (`councils[code == value.councilCode]`): the rent caption's `toValue` and `toPeriod`, and `rentOrBuy.rentPointStatus`.
3. If that caption's kind is `missing`, or the record is a gap, show "Not known".

The figure is never copied (DA-30).

### 1.3 `map-layers.json` and `schema/map-layers.schema.json` (new)
**File:** `{ "$schema", "frame": "metres-from-postcode-centre" (const), "layers": [...] }`. Positions are `[metresEast, metresNorth]` as whole numbers (`prefixItems` of two integers, `items: false`). An outline is an array of at least 4 positions, closed.

**Layer fields:**
- **Required:** `id` (pattern `…-LAYER-…-n`, for example `NB1-4XY-LAYER-FLOOD-ZONES-1`), `postcode`, `layer`, `status` (the area statuses), `label`, `caption` (1 to 120 characters), `period`, `level` (`{kind: radius, radiusMetres}`), `coverage`, `doesNotEstablish` and `source`.
- **Optional:** `note`, `link` and `features`.
- **`layer` values:** `flood-zones`, `surface-water`, `listed-buildings`, `conservation-areas`, `road-noise`, `rail-noise`.
- **Features:** a recorded or stale layer must have `features`; any other status must not (rule 7). Each feature shape has `additionalProperties: false`:
  - `flood-zones`: `{zone: "2" | "3", outline}`;
  - `surface-water`: `{band, outline}`;
  - `listed-buildings`: `{name, grade: "I" | "II*" | "II", point}`;
  - `conservation-areas`: `{name, outline}`;
  - `road-noise` and `rail-noise`: `{metric: "Lden", band, outline}`.

| layer | NB1 4XY | NB7 1RR | period | caption |
|---|---|---|---|---|
| flood-zones | recorded: one Zone 3 and one Zone 2 outline | no-record-in-source | 2026-10 | "Describes an area, not one property; ignores flood defences" |
| surface-water | recorded: two bands | source-failed | 2026-10 | "Describes an area, not one property" |
| listed-buildings | recorded: 2 points (II, II*) | no-record-in-source | 2026-10 | "No result does not mean no constraint; a listing point, not the protected extent" |
| conservation-areas | recorded: 1 outline | not-covered | 2026-10 | "No result does not mean no constraint" |
| road-noise | recorded: 2 Lden bands | source-failed | 2021 | "Modelled for 2021, not measured" |
| rail-noise | no-record-in-source | no-record-in-source | 2021 | "Modelled for 2021, not measured" |

**Windows and sources:** every window is 500 m. Each source label reads "Synthetic sample, shaped like …":
- flood zones: the Environment Agency Flood Map for Planning (Flood Zones 2 and 3);
- surface water: the EA Risk of Flooding from Surface Water map;
- listed buildings and conservation areas: the Planning Data Platform's listed building and conservation area datasets;
- road and rail noise: the Defra strategic noise maps, round 4.

**What boards may quote:** a layer's status, label, caption, period and source; feature names, grades, zones and bands; and the shapes.

**What boards never show:** whether a home or the postcode centre is inside an outline, a count or area, one noise figure for a home, or "no outline" worded as "no risk" or "no constraint".

### 1.4 `pilot-topics.json` and its schema
**Schema:**
- Add `radon`, `broadband-coverage` and `council-rent` to the `recordTopics` enum, and remove `broadband` if it is no longer a record topic.
- Add an optional `mapLayers` property: an array of the six layer kinds, unique, at least one.

**Data:**
- **New counted topic** `radon`, named "Radon", of kind `area-figures`, `counted: true`, with `recordTopics: ["radon"]`, placed after `air-quality`. Its gap question and check-in lines are in section 3, and its `reviewStatus` stays `draft` until the founder approves.
- **Changed topics:**
  - `broadband.recordTopics` becomes `["broadband-coverage"]` (replacing the old record);
  - `housing-affordability.recordTopics` becomes `["affordability", "council-rent"]`.
- **Map layers:**
  - `flood`: flood-zones, surface-water;
  - `planning-nearby`: listed-buildings, conservation-areas;
  - `noise`: road-noise, rail-noise.
- **Unchanged:** `noise`, `mobile-by-network` and `ground-and-mining` stay route-only.

**Counts:** 16 counted topics and 20 check-in lists. For NB1 4XY: found 16, not known 0, 16 of 16. For NB7 1RR: radon is not known and adds a question, and broadband coverage is not known and adds a question. The rent gap is deduplicated with the affordability gap.

### 1.5 The broadband speed priority is removed ("Replace it now")
- **Sample data:** remove `SAMPLE-PRIORITY-BROADBAND` from `sample-priorities.json`, and the `download-mbps` measure from `priorities.py`'s measure table, `records.py` and `sample-priorities.schema.json`.
- **Tests:** update `test-cases/priority-results.json` (worked examples) and `vestagraph-area` tests.
- **Specification:** in `docs/specs/pilot/area-priorities.feature`, remove the broadband lines from the priority scenarios (lines near 46 and 52). If a scenario loses its point, withdraw it with the `withdrawn` tag and a dated note.
- **Leave alone:** `area.json` (the home-keyed file, used later) keeps its broadband record. The B1 counterpart test (`test_postcode_area_sample_every_allowed_b1_topic_has_a_counterpart_with_equal_values`) drops `broadband` from its allowed topics, with a comment citing this plan.
- **Old plans:** dated plans that mention the speed priority stay as written.

### 1.6 Calculated or quoted
Everything new is quoted. `area-result.json` changes only because the existing tested code reruns. The test-first step is to redo the worked expected counts in `test-cases/area-glance.json` and `priority-results.json` before regenerating (rule 2).

## 2. Tasks
One branch (`feat/design-pass-topic-data`), one PR, with `make check` green after each task.

### Task 1: Schema groundwork
- [ ] **Tests first**, in the rejection-test files, each breaking one thing:
  - radon is accepted;
  - radon without an edition is rejected;
  - a radon measured-level field is rejected;
  - a grid-square level without `squareMetres` is rejected;
  - broadband coverage is accepted;
  - a full-fibre field on broadband coverage is rejected;
  - a broadband percent given as a number is rejected;
  - a snapshot without a month is rejected;
  - council rent with pence is rejected;
  - council rent without a council code is rejected;
  - a council rent gap with a value is rejected;
  - an unknown map layer in `pilot-topics` is rejected;
  - map layers on a route-only topic are accepted.

  Name each test `test_validate_instance_<file>_<condition>_<result>`.
- [ ] Then change the schemas. Existing data must still validate.

### Task 2: Radon
- [ ] Rework `area-glance.json` for NB1 (16, 0, 16 of 16) and NB7 (radon not known, plus its question), showing the working and citing FE-38, FE-39 and FE-41.
- [ ] Add the radon topic and its two records, then run `make generate`.
- [ ] Update the record counts in `test_area_records.py`, `_NEW_TOPIC_LEVEL_KINDS` (`radon: grid-square`) and the GLANCE-01, 03 and 04 scenarios in `docs/specs/pilot/area-glance.feature`.
- [ ] Add these tests:
  - `test_postcode_area_radon_square_is_one_kilometre`;
  - `test_postcode_area_radon_limit_says_indicative_not_definitive`;
  - `test_read_registry_committed_data_returns_every_topic` (radon is counted).

### Task 3: Broadband replaced (DA-28)
- [ ] Rework `area-glance.json` and `priority-results.json` first.
- [ ] Replace the records, remove the speed priority end to end (1.5), regenerate, and update the PRIO and GLANCE scenarios.
- [ ] Add these tests:
  - `test_postcode_area_broadband_coverage_percent_is_at_most_100`;
  - `test_postcode_area_broadband_coverage_limit_says_not_full_fibre`;
  - a test that no priority measure reads a broadband record.

### Task 4: Council rent by council link (DA-29)
- [ ] Add the records, and `council-rent` to `housing-affordability`.
- [ ] Extend `test_fixtures_council_consistency.py`:
  - rent is included in the real-file check and the guard;
  - a different council code is reported;
  - a status that differs from `rentSeries.status` is reported;
  - recorded rent for an unmapped postcode is reported;
  - recorded rent's council has a rent caption value in `council-result.json`.
- [ ] The `area-glance.json` notes show NB7's rent gap being deduplicated.

### Task 5: Map layers (DA-22, DA-24, DA-27)
- [ ] Add the new schema and data file, and `mapLayers` on three topics.
- [ ] **Schema rejection tests:**
  - a valid layer is accepted;
  - a recorded layer without features is rejected;
  - a gap layer with features is rejected;
  - decimal metres are rejected;
  - three numbers in a position are rejected;
  - an outline of three positions is rejected;
  - a "contains postcode centre" field is rejected;
  - a risk field is rejected;
  - flood Zone 1 is rejected;
  - noise decibels are rejected;
  - a listed building with an outline is rejected;
  - an unknown frame is rejected;
  - a missing caption is rejected.
- [ ] **Data tests:**
  - every outline is closed;
  - every position is inside its window;
  - windows are 500 m;
  - positions are whole metres;
  - each sample postcode has every layer once;
  - gap statuses include no-record, source-failed and not-covered;
  - noise is 2021 and "modelled, not measured";
  - the flood caption says "area, not one property";
  - the planning caption says "no result is not no constraint";
  - sources are synthetic and "shaped like";
  - IDs are unique and start with their postcode;
  - postcodes are listed;
  - each layer kind belongs to exactly one topic;
  - no safe, unsafe, verified or approved wording appears.

### Task 6: Documents and close-out
- [ ] **READMEs:** in `packages/fixtures/README.md`, add a map-layers section, the new topics, `grid-square` and the rent quoting path, and the DA-30 note on rent.
- [ ] **Register (`docs/decisions/README.md`):** DA-31 (this data contract and the founder's three answers), plus "as built" notes on DA-22, DA-23, DA-24, DA-27, DA-28 and DA-29.
- [ ] **Status file:** update `docs/planning/status.md`.
- [ ] **Pre-flight:** search for "15 topics", "15 of 15", `predictedMaxDownloadMbps`, `download-mbps`, `SAMPLE-PRIORITY-BROADBAND` and the DA IDs; fix anything stale in live documents.
- [ ] **Checks:** `make check`, the pre-push Opus review, then Codex.

## 3. New wording for founder approval (FE-39)
1. **Radon topic.**
   - Name: "Radon".
   - Gap question: "Has radon been measured in the home, and what was the result?"
   - Check in person: "Ask the owner or landlord whether radon has been measured in the home, and ask to see the result." and "Ask whether anything has been fitted to reduce radon, such as a sump or extra underfloor ventilation."
2. **Radon record.**
   - Label: "Radon potential, the 1 km square around this postcode (synthetic)".
   - Link text: "Get a radon report for an address from UKradon (paid)".
   - The limit text beyond the DA-23 phrase.
3. **Broadband coverage.**
   - Label: "Premises with gigabit-capable broadband available, this postcode (synthetic)".
   - The limit text beyond DA-28.
4. **Council rent:** the label and the limit text beyond DA-29.
5. **Map layers:** the six layer labels, and the caption and limit text beyond the register phrases.

These are marked `draft` and are asked for in the design pass's founder review (Task 7).
