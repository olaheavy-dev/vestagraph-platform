# Energy certificate by certificate number: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Before the pilot gate, give the "Check an energy certificate" page its data contract, its tested validity rule, its generated sample result, a "Check this" entry on the area result, its specification and its canvas boards (DA-09).

**Architecture:** Data contract first: a synthetic, already-normalised sample (`data/energy-certificates.json`) and real official code tables (`reference/energy-code-tables.json`, a new folder) each get a JSON Schema the validator checks. A pure, tested function in `vestagraph_area` works out each certificate's validity date (rule 2; functional core, BE-39), and the generator writes `generated/energy-certificate-result.json` with codes turned into words. The specification and the canvas boards quote that generated file only. No live register call is built here; the adapter is stage 5b.

**Tech Stack:** Python 3.14, uv, mypy strict, ruff, pytest, pytest-bdd, jsonschema (all existing); the design canvas (https://claude.ai/artifact/MpvQNDVYCePp4iWM3j3Jx4).

**Spec:** `docs/superpowers/specs/2026-11-18-energy-certificate-design.md` (approved 18 Nov 2026).

## Global Constraints
- No address, postcode, post town or address line in any sample, schema, board or scenario; schemas use `"additionalProperties": false` so such fields are rejected (design, anti-goals).
- Certificate numbers in samples are obviously synthetic: 20 digits starting `0000-0000-` (for example `0000-0000-0000-0000-0001`), never a real certificate.
- Money is whole pence (0036); missing facts carry an explicit missing status, never zero or blank (rule 7).
- Every displayed figure is quoted from the sample (an input) or from the generated file (a calculated output); nothing hand-typed (rule 2). No totals or savings sums of our own.
- Never "good", "bad", "safe", "verified", "recommended" in our voice (rule 4); the register's own scale words "A (best) to G (worst)" may be quoted with its source.
- The number never appears in a URL, `#` fragment, query string or log (0014); the page address is `/energy-certificate`.
- England only: a certificate whose country is Wales shows "Wales is not yet covered." (rule 6).
- Test names `test_<method>_<condition>_<result>` (0039); pure functions over frozen dataclasses, I/O only in the generator (BE-39).
- All page wording was proposed, then approved by the founder on 19 Nov 2026 (copy review, "Approve as written (Recommended)"; "Current" over "Now").
- No new packages.

## Review Focus
1. **A certificate dated 29 February:** the validity date must not crash or skip a day; Task 2's leap-day case pins it.
2. **A code with no table entry** (a newer schema adds a code): the result says "Not on this certificate", never the raw code or a blank; Task 3's unknown-code test pins it.
3. **A number typed with spaces or dashes, or 19 or 21 digits:** spaces and dashes are ignored, wrong length is an inline error before any lookup; Task 4's ENERGY scenarios pin it.
4. **An address field slipped into a sample:** the validator rejects it; Task 1's rejection test pins it.
5. **"More than 10 years old" on the boards' date:** decided against the fixtures' snapshot date (23 Oct 2026), not the real clock; Task 3's generator test pins it.

---

### Task 1: Data contract (samples, code tables, schemas, validator)

**Files:**
- Create: `packages/fixtures/data/energy-certificates.json`, `packages/fixtures/schema/energy-certificates.schema.json`
- Create: `packages/fixtures/reference/energy-code-tables.json`, `packages/fixtures/reference/README.md`, `packages/fixtures/schema/energy-code-tables.schema.json`
- Modify: `packages/vestagraph-fixture-validator/src/vestagraph_fixture_validator/validator.py` (`validate_fixtures` also checks `reference/NAME.json` against `schema/NAME.schema.json`), its `__main__.py` docstring, `packages/fixtures/README.md` (the reference folder is real official data, everything else stays invented)
- Test: `packages/vestagraph-fixture-validator/tests/test_validator_reference.py`

**Interfaces:**
- Produces: `data/energy-certificates.json` = `{"$schema", "nation": "england", "certificates": [Certificate]}`. A `Certificate` has `number` (pattern `^0000-0000-\d{4}-\d{4}-\d{4}$`), `schema` (for example `"RdSAP-Schema-21.0.1"`), `country` (`england` | `wales`), `kind` (`domestic` | `non-domestic`), `status` (`entered` | `cancelled` | `superseded`, as the register marks it), `registrationDate`, `inspectionDate` (ISO dates), and the facts, each either `{"value": …, "source": {…}}` or `{"status": "missing"}`: `currentRating`/`potentialRating` (`{"band": "A"–"G", "score": int}`), `propertyTypeCode`, `builtFormCode`, `totalFloorAreaSquareMetres`, `costs` (`heating`, `hotWater`, `lighting`, each `{"current": Money, "potential": Money}`, period `year`), `parts` (list of `{"part": "walls"|"roof"|"windows"|"floor"|"main-heating"|"heating-controls"|"hot-water"|"lighting", "description": str, "stars": 1–5}`), `improvements` (list of `{"sequence": int, "improvementCode": int, "indicativeCost": str, "typicalSaving": Money}`).
- Produces: `reference/energy-code-tables.json` = `{"$schema", "partial": true, "tables": {"propertyType": {code: words}, "builtForm": {…}, "improvement": {code: words}}, "sources": [{"table", "url", "effectiveDate", "checked"}]}`.
- Samples (one each): **A** current RdSAP 21.0.1 home (state 4); **B** registered more than 10 years before 23 Oct 2026 (state 5); **C** `superseded` (state 6); **D** `cancelled` (state 6); **E** `non-domestic` (state 7); **F** `wales` (state 8); **G** older SAP schema with `parts` and `improvements` missing (state 11); **H** registered on 29 Feb 2016 (Review Focus 1).

- [ ] **Step 1:** Fetch the code tables from an official source (the SAP or RdSAP specification, or the register's published lookups; start from the register's [technical documentation](https://get-energy-performance-data.communities.gov.uk/api-technical-documentation) and [JSON samples](https://github.com/communitiesuk/epb-data-warehouse/tree/main/spec/fixtures/json_samples)). Copy only the codes samples A to H use, each table's source URL and effective date. If no official table for improvement codes can be found, stop and report (the design forbids showing raw codes).
- [ ] **Step 2: Write the failing tests** in `test_validator_reference.py`: `test_validate_fixtures_reference_table_valid_passes` (the real file gives no problems); `test_validate_fixtures_certificate_with_postcode_fails` (a copy of sample A with `"postcode": "NB1 4XY"` added gives one problem naming `postcode`); `test_validate_fixtures_fact_zero_cost_fails` (a cost of 0 pence is rejected; missing must be `{"status": "missing"}`).
- [ ] **Step 3:** Run `uv run pytest packages/vestagraph-fixture-validator -k reference -v`. Expected: FAIL.
- [ ] **Step 4:** Write the two schemas, the two data files and the validator change.
- [ ] **Step 5:** Run `make validate` and the tests. Expected: PASS.
- [ ] **Step 6:** Commit `feat: energy certificate sample data and code tables (DA-09)`.

### Task 2: Validity rule (test-first, `test-first` skill)

**Files:**
- Create: `packages/vestagraph-area/src/vestagraph_area/energy_certificate.py`
- Test: `packages/vestagraph-area/tests/test_energy_certificate_validity.py`

**Interfaces:**
- Produces: `valid_until(start: date) -> date` (the same day and month 10 years on; 29 February becomes 28 February); `is_more_than_ten_years_old(start: date, today: date) -> bool` (`today > valid_until(start)`); `VALIDITY_YEARS: Final = 10`.

- [ ] **Step 1:** Confirm on GOV.UK which date the 10 years run from (the certificate's registration or inspection date) and how the official Find an energy certificate service shows "valid until" for a certificate; record the answer and URLs in the test module's docstring and in `reference/energy-code-tables.json` `sources` as the rule line (`"table": "validity"`). If the source is silent on 29 February, keep 28 February and mark it the agent's call in the docstring.
- [ ] **Step 2: Write the failing tests**, each with its working in a comment: `test_valid_until_ordinary_date_adds_ten_years` (2025-04-04 → 2035-04-04); `test_valid_until_leap_day_gives_28_february` (2016-02-29 → 2026-02-28); `test_is_more_than_ten_years_old_on_the_last_valid_day_false` (start 2016-10-23, today 2026-10-23 → False); `test_is_more_than_ten_years_old_day_after_true` (start 2016-10-22, today 2026-10-23 → True); `test_is_more_than_ten_years_old_leap_day_start_on_28_february_false` (2016-02-29, today 2026-02-28 → False).
- [ ] **Step 3:** Run `uv run pytest packages/vestagraph-area/tests/test_energy_certificate_validity.py -v`. Expected: FAIL.
- [ ] **Step 4:** Implement the two functions (pure, standard library only).
- [ ] **Step 5:** Run the tests. Expected: PASS. Then `make mutate` is not needed (the engine is unchanged).
- [ ] **Step 6:** Commit `feat: energy certificate validity rule (rule 2)`.

### Task 3: Generated result

**Files:**
- Create: `packages/vestagraph-generator/src/vestagraph_generator/energy_generator.py`, `packages/fixtures/schema/generated-energy-certificate-result.schema.json`, `packages/fixtures/generated/energy-certificate-result.json`
- Modify: `packages/vestagraph-generator/src/vestagraph_generator/__main__.py` (write the fourth file; nothing written if any fails), `packages/vestagraph-area/src/vestagraph_area/energy_certificate.py` (record readers and `decode`), `packages/fixtures/README.md` (four generated files), `AGENTS.md` Commands table (`make generate` writes four files)
- Test: `packages/vestagraph-generator/tests/test_energy_generator.py`, `packages/vestagraph-area/tests/test_energy_certificate_decode.py`

**Interfaces:**
- Consumes: Task 1's files; Task 2's `valid_until`, `is_more_than_ten_years_old`; `snapshot.json`'s `snapshotDate` as today.
- Produces: `decode(code: int, table: Mapping[int, str]) -> str | None` (None when the code is absent); `generated/energy-certificate-result.json` = per sample number: `outcome` (`shown` | `not-domestic` | `not-yet-covered`), `validUntil`, `moreThanTenYearsOld`, `statusLine` (`entered` → none, `superseded`, `cancelled`), every fact decoded to words or `{"status": "missing", "text": "Not on this certificate"}`, and the money as pence.

- [ ] **Step 1: Write the failing tests:** `test_decode_unknown_code_none`; `test_generate_energy_sample_b_more_than_ten_years_old_true`; `test_generate_energy_sample_a_valid_until_2035_04_04` (or the date Task 2 step 1 confirms); `test_generate_energy_sample_g_missing_parts_not_on_this_certificate`; `test_generate_energy_sample_e_outcome_not_domestic`; `test_generate_energy_sample_f_outcome_not_yet_covered`; `test_generate_energy_unknown_improvement_code_not_on_this_certificate`; `test_generate_energy_output_has_no_address_field` (no key named `address*`, `postcode`, `postTown` anywhere).
- [ ] **Step 2:** Run them. Expected: FAIL.
- [ ] **Step 3:** Implement the readers, `decode` and the generator; run `make generate`.
- [ ] **Step 4:** Run `make check`. Expected: PASS (generated-check, validate and tests).
- [ ] **Step 5:** Commit `feat: generated energy certificate result`.

### Task 4: "Check this" entry and the specification

**Files:**
- Modify: `packages/fixtures/data/pilot-topics.json` (new topic `energy-certificate-home`, kind `route-only`, `counted: false`, name "Energy certificate of a home", `officialRoute` GOV.UK Find an energy certificate, new optional `vestagraphRoute: "/energy-certificate"`), `packages/fixtures/schema/pilot-topics.schema.json`, `packages/vestagraph-area/src/vestagraph_area/records.py` (read `vestagraphRoute`), regenerate `area-result.json`
- Create: `docs/specs/pilot/energy-certificate.feature` (ENERGY-01 onwards)
- Modify: `docs/specs/pilot/area-topics.feature` (TOPIC-41: the energy row opens the page and shows no result), `docs/specs/pilot/area-printout.feature` (PRINT-21: the row is listed under "Not yet covered here"), `docs/specs/screens/01-landing.feature` (LAND-21: the landing link), `packages/specs/tests/specs_steps.py` (data steps for the non-UI scenarios)
- Test: `packages/vestagraph-area/tests/test_area_records.py` (`test_read_registry_vestagraph_route_read`), `packages/vestagraph-area/tests/test_area_glance.py` (`test_glance_energy_route_only_not_counted`)

**Interfaces:**
- Consumes: Task 3's generated file; scenarios quote it by sample number.

- [ ] **Step 1:** Write the two failing unit tests; run them (FAIL); add the registry entry, schema and reader; run them (PASS); `make generate`.
- [ ] **Step 2:** Write `energy-certificate.feature` with a "Required states" header mapping each of the design's 11 states, the printout and the anti-goals to scenarios. It must include: the number is never in the address, fragment, query string or logs (two scenarios, as WCHAT-96/97); spaces and dashes ignored, 19 and 21 digits rejected before any lookup; each sample A to H's outcome quoting the generated file; costs labelled "the certificate's estimates, not your bills"; improvements in the certificate's order with no total; "Not known right now" when the register is unavailable or over its limit (UI, fake adapter); no address or postcode shown or implied (no "for NB1 4XY"); the printout ends with its sources page; display settings and dark mode as the other pilot pages. UI scenarios are tagged `@ui`.
- [ ] **Step 3:** Add TOPIC-41, PRINT-21 and LAND-21; add data steps; run `make test`. Expected: PASS (the `@ui` scenarios are deselected; data scenarios pass).
- [ ] **Step 4:** Commit `docs: energy certificate specification and Check this entry`.

### Task 5: Canvas boards

**Files:** the design canvas (page "Pilot · public area check", a new section "Energy certificate"); generator scripts in the session scratchpad, as in the 16 Nov design pass (`docs/superpowers/plans/2026-11-16-benchmark-design-pass.md`).

- [x] **Step 1:** Read the canvas's current version and the Brand and style boards (FeedbackKit, Craft); keep FE-29 to FE-33, FE-64 and FE-31's slate-ink dark.
- [x] **Step 2:** Draw, light first: `EnergyPhone` and `EnergyDesktop` (sample A found); `EnergyStates` (empty, wrong format, checking skeleton, older than 10 years (B), superseded (C), cancelled (D), not a home certificate (E), Wales (F), not found, Not known right now, Not on this certificate (G)); `EnergyPrint` (sample A, ending with sources); the "Check this" energy row on the result boards and the landing link. Every figure and line is quoted from `energy-certificate-result.json` and `energy-certificate.feature`; each board carries "Sample data".
- [x] **Step 3:** Draw the dark twins of every screen board (not the printout, as FE-31).
- [ ] **Step 4:** Visual review in Chrome at 390 and 1440 px (`visual-reviewer`), fix, re-check; record the canvas version.
- [x] **Step 5:** Note "As drawn" under this task with the canvas version.

**As drawn (19 Nov 2026), Task 5:** steps 1 to 3 and 5; step 4 (the visual review in Chrome) is not done yet. On the canvas page "Pilot · public area check", a new section "Pilot 7 · Energy certificate" sits below everything (title note at y 30200, light boards from y 30500, dark twins in a row below from y 34920). New boards: `EnergyPhone` (390 wide) and `EnergyDesktop` (1440, a fluid page) for sample A found; `EnergyStates` (eleven phone-width cards: empty, wrong format, checking skeleton, older than 10 years (B), replaced (C), cancelled (D), not a home certificate (E), Wales (F), not found, Not known right now, Not on this certificate (G)); `EnergyPrint` (three A4 pages for sample A: rating and running costs, the parts and improvements, then the sources page with the privacy line; no dark twin, FE-31); and the dark twins `EnergyPhoneDark`, `EnergyDesktopDark` and `EnergyStatesDark`. Every figure, date and description is generated from `energy-certificate-result.json` by the scratchpad scripts (money written in pounds from the pence, with pence only where the amount has them); wording is copied from the specification, and every other line is proposed and listed in the Task 5 report for the copy review. Edits to existing boards, light and dark: the "Check this" energy row (TOPIC-41) after "Council tax band of a home" on `AreaResult` and `AreaResultDesktop`, with the same entry in each board's compact "How we got this" list and, on the desktop boards, in the "Check in person" list; the landing link (LAND-21) under the search box on `Landing` and `LandingPhone`; and the printout's "Not yet covered here" entry (PRINT-21) on `AreaExport` page 16, with its contents line and the three sentences that counted the not-yet-covered topics. No older GOV.UK energy row existed, so nothing was replaced. Agent's calls (open to the founder): the A to G strip in neutral tints rather than the usual colour scale (rule 4); an amber warning for cancelled and information notices for older and replaced; "How we got this" drawn open; the certificate number is not printed on the printout. Review fixes (19 Nov 2026): About the data now has the register entry and the energy row (ENERGY-44, both themes); the state cards 4, 5, 6 and 11 carry the Sample data chip; the "EPC register ↗" stamp goes to the search page https://www.gov.uk/find-energy-certificate (controller's ruling: the certificate's own page carries the number, so ENERGY-39 and decision 0014 win; ENERGY-11 amended); frame heights were measured in headless Chrome (content height + 32 px) and the printout text raised to 17 px. Second review fixes: the four landing boards' root height, `$preview` and frame now agree (4438 and 6070), the phone landing's section spacing was trimmed so its content fits, and the dark landing boards set a dark page background. Canvas version after the last publish of Task 5: `1795085127-2733` (version 412, later 413, see Task 6; round 1 `1795084593-2439`; first draw `1795083951-78a5`, before: `1795083243-cfdb`).

### Task 6: Records and pull request

**Files:** `.design/prototype/INFORMATION_ARCHITECTURE.md` (the page, `/energy-certificate`, entry points, no number in the address), `docs/references/data-sources.md` (EPC register: endpoint, rate limit, schemas), `docs/decisions/README.md` (DA-09 dated note; register lines for the design's agent's calls, open to the founder), `docs/planning/status.md` (item 5b done or in review), About the data scenario for the register (AREA-50 in `14-check-an-area.feature`).

- [x] **Step 1:** Make the record changes; pre-flight grep for "energy certificate", "EPC", "DA-09", "find an energy certificate" and fix anything stale.
- [x] **Step 2:** Map every design requirement and state to its test or scenario in the PR description; `make check`; fresh-context review (Code Review Rules, `code-security-reviewer`, `visual-reviewer`); fix findings.
- [ ] **Step 3:** Push, open the PR with the copy-review list, `@codex review`.

**As done (19 Nov 2026), Task 6:** steps 1 and 2 are done; step 3 (push, open the pull request with the copy-review list, `@codex review`) is next. The whole-branch review and the security review found one P1 on the validity rule: regulation 9(2)(b) ("no other energy performance certificate for the building has since been entered on the register") makes a replaced certificate no longer valid, and the regulation is silent on a cancelled one, so `validUntil` and `moreThanTenYearsOld` are now written only for a current certificate (status `entered`) and `registrationDate` is written for every shown one (test first; ENERGY-10, ENERGY-12, ENERGY-24 to ENERGY-27 updated; DA-33). The security review's two P1s and five P2s are in the specification and records only, as no adapter exists yet: ENERGY-39 to ENERGY-41 reworded (the server's outgoing request to the register carries the number in its query string and is never logged) and ENERGY-53 to ENERGY-60 added for the stage 5b build (real adapter against a fake register server, allow-list of fields, no-store and no Cached label, autofill off, page title without the number, the form without JavaScript, a per-visitor limit DA-35, the privacy notice naming the register), plus the schemas' sample-number pattern tightened. Other fixes: AGENTS.md's `make generate` row, test names and a leap-day test, the README wordings. Canvas fixes (canvas version 413): "valid until" removed from the replaced and cancelled cards (registration date shown), "How we got this" says "valid until" is 10 years from the registration date and that the number goes to the register, the improvements' "Step n" became "Improvement n of 3", the printout says "typical saving", About the data's register entry shows "We look this up when you ask and keep no copy" instead of a date (AREA-50), the Wales card has one action (B22), AreaExport's note counts five route rows; page 16 was checked and fits. The Landing energy link was already 44 px high. All new wording is proposed, for the founder's copy review.
