# City Explorer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Anything numeric also follows `.claude/skills/test-first/` (decision 0031).

**Goal:** Give City Explorer's council and neighbourhood pages real, tested figures from synthetic sample data. Then draw them on the design canvas, then write their specifications, ready for the pilot gate (0052).

**Architecture:** This is stage 3 work only, the same shape as the first design batch (#259):
- Research the sources first, so the sample data takes the real sources' shapes.
- The data contract comes next: a council sample file and its schema, plus a versioned council tax band table.
- New pure modules in `vestagraph_area` work out every figure. They call `vestagraph_engine` for the mortgage repayment.
- The generator writes a third generated file, `council-result.json`, with every figure for the example inputs and all eight bands.
- The canvas boards quote that file.
- The specifications follow the founder's approval of the boards.
- Live sources, the server endpoints and the Bank of England feed belong to stage 5b and the data pipeline design.

**Tech Stack:** Python 3.14, uv workspace, pytest, mypy strict, ruff, JSON Schema 2020-12. No new third-party packages: `vestagraph-area` gains a dependency on the workspace package `vestagraph-engine`. Design canvas: version 180 onwards.

**Spec:** `docs/superpowers/specs/2026-11-15-city-explorer-design.md` (approved 15 Nov 2026, design review fixes in #282). Also decisions 0046, 0053, 0054, 0055 and 0056, and DA-14.

## Global Constraints
- **Rule 2:** no calculated figure is typed by hand.
  - Inputs carry a source.
  - Outputs come from `vestagraph_area` through `council-result.json`.
  - Test expectations are worked out independently, with their working (the test-first skill).
- **Rule 3:** the band proportions live in a versioned rule table. Its source is the [Local Government Finance Act 1992, s.5(1)](https://www.legislation.gov.uk/ukpga/1992/14/section/5), England, 6:7:8:9:11:13:15:18 over 9, with an effective date. Adding that table makes PR A a founder merge (AGENTS.md: tax rule tables).
- **Rule 7:** missing is never zero, a flat line or a clean result.
  - A gap status never becomes a value.
  - A trend caption needs both end points.
  - A difference needs both sides.
- **No calculation in the browser.** The generator works out the example inputs and all eight bands. Visitor-changed inputs go to the same functions on the server at 5b (0053).
- **Rankings (0054):**
  - no ranking of councils or neighbourhoods;
  - no "1st of N";
  - no score drawn on a map;
  - no combined score;
  - no verdict words ("best", "better", "cheaper", "high", "low", "steep", "sharp").
- **Money:** in `Pence`, rounding halves away from zero, once (0021). Monthly = yearly ÷ 12 via `Pence.annual_to_monthly` (#197 notes that no record states this rule yet).
- **Percentages:** one decimal place, halves away from zero, from an exact `Fraction`.
- **Sample data stays synthetic.**
  - Councils are named "Northbridge", "Eastmere" and "Southvale", each with "(synthetic)".
  - Neighbourhood names are made up.
  - `source.label` reads "Synthetic sample, shaped like <real source>".
- **Test names:** `test_<method>_<condition>_<result>` (0039). Test files are `test_council_*.py`.
- No agent attribution in commits or pull requests.

## Review Focus
1. **A deposit of 100% or more, or a loan of zero,** gives "deposit too large: no mortgage needed", never a crash or £0. The test is in Task 4.
2. **A loan above the highest published band** (for example a 3% deposit when the bands stop at 95%), or below the lowest, gives `rate-band-unavailable`. It never falls back to the nearest band. The test is in Task 4.
3. **A council with no published rent** gets the buy side only: no difference sentence and no budget label for rent. The test is in Tasks 4 and 6.
4. **A trend whose month 12 months earlier is missing or across a method break** gets no change caption. It shows only "not published" or "not comparable". The test is in Task 5.
5. **Two places with the same name in different counties** are both returned, labelled with their county, and never auto-picked. The test is in Task 7.

## Pull requests
- **PR R (research, documentation):** Task 1. Branch `docs/city-explorer-sources`.
- **PR A (code, Codex review):** Tasks 2 to 9. Branch `feat/council-result-data`.
  - The founder merges it, because it adds the band rule table.
  - The pre-push review runs **before** the push (agent-workflows#23). The builder's brief ends at a local commit and `make check`.
- **PR B (canvas record):** Tasks 10 to 13.
- **PR C (specifications):** Task 14, after the founder approves the boards.

---

### Task 1: Research the sources (DA-05 shapes and licences)

**Files:**
- Create: `docs/reviews/2026-11-16-city-explorer-sources.md`
- Modify: `docs/references/data-sources.md` (one entry per source, marked "research, not yet used")
- Modify: the design's sources table (each open point answered, or still open with a reason)

- [ ] **Step 1:** For each row of the design's "Sources to check before build", read the publisher's own page and record:
  - the licence, quoted;
  - the geography and level;
  - the edition and cadence;
  - the fields to quote (table and column);
  - what is not confirmed.

  The rows are: MHCLG council tax levels (Table 10; per-band amounts; parish precepts in or out), ONS private rents, UK House Price Index (property type by council), the affordability ratio (workplace or residence), Census 2021 tenure (council and LSOA tables), mid-year population, DfT connectivity (scale direction, LSOA and council columns), Bank of England quoted rates by deposit band, council and LSOA boundaries, House of Commons Library MSOA names, LSOA-level facts, and a place-name-to-council lookup.
- [ ] **Step 2:** For the Bank of England:
  - list the published loan-to-value bands and their series codes;
  - give the latest month;
  - confirm the data is the Bank's own, not LSEG data.

  This fixes the sample data's band list.
- [ ] **Step 3:** For the place-name lookup, pick a recommended source, or "none suitable", giving the licence conflict the design review found. Give the founder a question with options if a choice is needed.
- [ ] **Step 4:**
  - Run the pre-push review.
  - Open PR R with `@codex review`.
  - Update `docs/planning/status.md`.
  - Merge under AGENTS "When merging" (documentation fallback allowed).

### Task 2: Council sample data and schema (data contract)

**Files:**
- Create:
  - `packages/fixtures/schema/council-area.schema.json`
  - `packages/fixtures/data/council-area.json`
  - `packages/fixtures/schema/council-tax-bands.schema.json`
  - `packages/fixtures/data/council-tax-bands.json`
- Modify: `packages/fixtures/README.md`
- Test: `make validate`

**Interfaces:**
- **Produces `council-tax-bands.json`:**
  `{ "$schema", "nation": "england", "effectiveFrom": "1993-04-01", "source": {label, url: "https://www.legislation.gov.uk/ukpga/1992/14/section/5"}, "bands": [ {"band": "A", "numerator": 6}, …, {"band": "H", "numerator": 18} ], "denominator": 9 }`
  - The numerators are 6, 7, 8, 9, 11, 13, 15, 18.
  - Set `effectiveFrom` to the date the Act's s.5 took effect for council tax. Confirm it in Task 1, and leave a `TODO-confirm` field if it is not found.
- **Produces `council-area.json`:**
  `{ "$schema", "councils": [Council], "places": [PlaceName], "rateBands": [RateBand] }`
  - **Council:**
    `{ "code", "name", "nation", "tier": "unitary"|"district", "county"?, "formedOn"?, "formerNames"?: [..], "population": Fact, "bandD": Fact, "rentSeries": Series, "priceSeries": Series, "affordabilitySeries": Series, "tenure": Fact, "connectivity": Fact, "neighbourhoods": [Neighbourhood] }`
  - **Fact:**
    `{ "status": "recorded"|"no-record-in-source"|"source-failed"|"not-covered", "value"?, "level": {kind, name}, "source": {label, url, edition, period} }`
  - **Series:**
    `{ "status", "unit": "pence-per-month"|"pence"|"ratio", "points": [ {"period": "YYYY-MM"|"YYYY", "value"?: int|decimal-string, "status": "recorded"|"provisional"|"not-published", "methodBreakBefore"?: true} ], "level", "source" }`
  - **Tenure value:** `{ "ownedOutright", "ownedWithMortgage", "socialRented", "privateRented", "other" }`. These are whole household counts; shares are worked out.
  - **Neighbourhood:**
    `{ "code", "largerAreaName", "facts": { "connectivity": Fact, "deprivation": Fact (value {decile, rank, ofAreas, edition}), "tenure": Fact } }`
  - **PlaceName:** `{ "name", "county", "region", "councilCodes": [..] }`
  - **RateBand:** `{ "maxLoanToValuePercent": int, "rateBasisPoints": int, "month": "YYYY-MM", "source" }`. The bands are shaped like the Bank's published ones (Task 1).
  - Every rate stays an input, never a calculated figure.

- [ ] **Step 1:** Write the schemas (`additionalProperties: false`; a gap status carries no `value`).
- [ ] **Step 2:** Write the sample data:
  - **Northbridge (synthetic), unitary:** complete, with 24 monthly rent and price points, the last 2 rent and the last 12 price points provisional, and 3 neighbourhoods.
  - **Eastmere (synthetic), district in "Westshire (synthetic)":** `formedOn` 2023-04-01 with a former name, rents `no-record-in-source`, and an affordability series with a `methodBreakBefore`.
  - **Southvale (synthetic):** a council whose price point 12 months back is `not-published`.
  - **Places:** "Northbridge" (one council), "Newbury (synthetic)" twice in two counties, a county name listing its districts, and a Welsh-style place with `nation: "wales"`.
  - **Rate bands:** 60, 75, 85, 90 and 95.
- [ ] **Step 3:** Run `make validate`. Expected: PASS.
- [ ] **Step 4:** Commit: `feat: council sample data, schema and the band rule table`.

### Task 3: Council records reader and council tax bands

**Files:**
- Create:
  - `packages/vestagraph-area/src/vestagraph_area/council_records.py`
  - `packages/vestagraph-area/src/vestagraph_area/council_tax.py`
  - `packages/fixtures/test-cases/council-tax-bands.json`
  - `packages/vestagraph-area/tests/test_council_tax.py`
  - `packages/vestagraph-area/tests/test_council_records.py`
- Modify:
  - `packages/vestagraph-area/pyproject.toml` (`dependencies = ["vestagraph-engine"]` plus the workspace source)
  - the root `pyproject.toml` (paths)
  - `uv.lock`

**Interfaces:**
- **Produces in `council_records.py`:**
  - `read_council_area(path) -> CouncilArea`
  - `read_band_table(path) -> BandTable`
  - frozen dataclasses mirroring Task 2 (`Council`, `Fact`, `Series`, `SeriesPoint`, `Neighbourhood`, `PlaceName`, `RateBand`, `BandTable`)
  - it raises `InvalidAreaDataError` (from `records.py`) for anything not understood, with the same refusals as `read_postcode_area`.
- **Produces in `council_tax.py`:**
  - `band_yearly(band_d_yearly: Pence, band: str, table: BandTable) -> Pence`, which is `round_ratio(band_d × numerator, denominator)`;
  - `band_monthly(yearly: Pence) -> Pence`, which is `yearly.annual_to_monthly()`.
  - An unknown band raises `InvalidAreaDataError`.

- [ ] **Step 1:** Work the cases by hand, with the working shown:
  - the Band D example for all 8 bands;
  - a Band D giving an exact half penny on band A (×6/9), to show the rounding;
  - each band's monthly amount.
- [ ] **Step 2:** Write the tests:
  - `test_band_yearly_worked_cases_match_expected`
  - `test_band_yearly_band_d_is_unchanged`
  - `test_band_yearly_unknown_band_raises`
  - `test_read_council_area_gap_with_value_raises`
  - `test_read_band_table_wrong_numerators_count_raises`
- [ ] **Step 3:** Run `uv run pytest packages/vestagraph-area -q -k council`. Expected: FAIL (the module is missing).
- [ ] **Step 4:** Implement it. Run again. Expected: PASS.
- [ ] **Step 5:** Commit: `feat: council records reader and council tax bands (LGFA 1992 s.5)`.

### Task 4: Rent or buy, per month

**Files:**
- Create:
  - `packages/vestagraph-area/src/vestagraph_area/rent_or_buy.py`
  - `packages/fixtures/test-cases/rent-or-buy.json`
  - `packages/vestagraph-area/tests/test_council_rent_or_buy.py`

**Interfaces:**
- **Consumes:**
  - `vestagraph_engine.mortgage.monthly_repayment(loan: Pence, rate_basis_points: int, term_years: int) -> Result[MortgageRepayment]`
  - `band_monthly` (Task 3)
- **Produces:**
  - `rate_band_for(deposit_percent: Fraction, bands: Sequence[RateBand]) -> RateBand | None`. The loan-to-value is `100 − deposit_percent`. The function returns the smallest band whose `maxLoanToValuePercent` is at least that (bands mean "up to X% loan"), and `None` when the loan-to-value is above the highest band or at or below 0.
  - `rent_or_buy(rent_monthly: Pence | None, price: Pence | None, council_tax_monthly: Pence, deposit_percent: Fraction, term_years: int, rate_basis_points: int | None, bands: Sequence[RateBand]) -> RentOrBuy`
  - `RentOrBuy(rent_side: Pence | None, buy_side: Pence | None, repayment: Pence | None, rate_used: RateBand | None, comparison: "more"|"less"|"about-the-same"|None, difference: Pence | None, problem: str | None)`
  - `ABOUT_THE_SAME_PENCE = 1000` (£10 a month, the agent's call, for the founder to review in PR A).
- **Rules:**
  - `rent_side` = rent + council tax.
  - `buy_side` = repayment + council tax.
  - The repayment is on `price × (100 − deposit_percent) / 100`, rounded once, from the engine.
  - A typed `rate_basis_points` overrides the band.
  - A 0% typed rate gives a repayment of loan ÷ payments, rounded once (the engine refuses 0).
  - **Problems** (`problem`), each with no side shown and no comparison:
    - `deposit-too-large`: a deposit of 100% or more;
    - `deposit-negative`;
    - `term-out-of-range`: a term outside 1 to 40;
    - `rate-band-unavailable`: no band and no typed rate;
    - `rate-negative`.
  - A missing rent or price gives that side `None`, `comparison None` and `difference None`.
  - `comparison` is "about-the-same" when |buy − rent| < 1000 pence. Otherwise it is "more" or "less" (buy compared with rent).

- [ ] **Step 1:** Work the cases by hand from the Northbridge sample:
  - deposits of 10%, 20% (an 80% loan, which takes the 85% band), 25% (75%), 40% (60%) and 3% (no band);
  - 0%, 100% and −5% deposits;
  - a 0% typed rate;
  - Eastmere with no rent;
  - a pair within £10.

  Show the engine's formula working for one case.
- [ ] **Step 2:** Write the tests:
  - `test_rent_or_buy_worked_cases_match_expected`
  - `test_rate_band_for_eighty_percent_loan_takes_eighty_five_band`
  - `test_rate_band_for_loan_above_highest_band_is_none`
  - `test_rent_or_buy_deposit_one_hundred_percent_is_deposit_too_large`
  - `test_rent_or_buy_missing_rent_has_buy_side_only_and_no_comparison`
  - `test_rent_or_buy_zero_typed_rate_divides_loan_by_payments`
  - `test_rent_or_buy_within_ten_pounds_is_about_the_same`
- [ ] **Step 3:** Run them (FAIL), implement, run them again (PASS).
- [ ] **Step 4:** Commit: `feat: rent or buy per month with the rate for the deposit band`.

### Task 5: Plain-words captions

**Files:**
- Create:
  - `packages/vestagraph-area/src/vestagraph_area/captions.py`
  - `packages/fixtures/test-cases/council-captions.json`
  - `packages/vestagraph-area/tests/test_council_captions.py`

**Interfaces:**
- **Produces:**
  - `twelve_month_change(series: Series, latest_period: str) -> Change | None`
  - `Change(from_period, to_period, from_value, to_value, amount: Pence | Fraction, percent: Fraction | None, direction: "rose"|"fell"|"unchanged", provisional_months: int)`
  - `caption_for(topic: str, series: Series, latest_period: str) -> Caption` (the tenure single-point caption is built in the generator from `tenure_shares`)
  - `Caption(kind: "trend"|"single-point"|"missing"|"not-comparable", values: dict[str, str])`
  - Captions carry **values and a pattern key**, not finished sentences. The wording is approved by the founder (like FE-39) and lives in a wording file the boards and specs quote.
- **Rules:**
  - Returns `None` (and caption `missing` or `not-comparable`) when:
    - either end point is `not-published`;
    - a `methodBreakBefore` lies between the two end points;
    - the series status is a gap.
  - "unchanged" means the amount rounds to £0 (money) or to 0.0 (ratio). That threshold is separate from `ABOUT_THE_SAME_PENCE`.
  - The percent is `amount / from_value × 100` to one decimal place.
  - `provisional_months` counts provisional points in the latest 12.
  - Tenure single point: the shares come from `tenure_shares` (Task 7).

- [ ] **Step 1:** Work the cases by hand:
  - Northbridge rent (rose, with 2 provisional months);
  - a flat month;
  - Southvale price (the end point 12 months back is not published);
  - the Eastmere affordability ratio across its break;
  - a fall.
- [ ] **Step 2:** Write the tests:
  - `test_twelve_month_change_worked_cases_match_expected`
  - `test_twelve_month_change_missing_start_point_is_none`
  - `test_twelve_month_change_across_method_break_is_not_comparable`
  - `test_twelve_month_change_rounding_to_zero_is_unchanged`
- [ ] **Step 3:** Run them (FAIL), implement, run them again (PASS).
- [ ] **Step 4:** Commit: `feat: plain-words caption values for council trends`.

### Task 6: Budget check

**Files:**
- Create:
  - `packages/vestagraph-area/src/vestagraph_area/budget.py`
  - cases in `packages/fixtures/test-cases/council-budget.json`
  - `packages/vestagraph-area/tests/test_council_budget.py`

**Interfaces:**
- **Produces:**
  - `budget_check(budget_monthly: Pence, rent_or_buy: RentOrBuy) -> BudgetCheck`
  - `BudgetCheck(rent: "within"|"above"|None, buy: "within"|"above"|None, problem: "budget-not-positive"|None)`
  - "within" includes equal to the budget.
  - A missing side gives `None`, never "within".
  - A budget of zero or below is a `problem`.

- [ ] **Step 1:** Work the cases by hand:
  - each side below, equal to and above the budget;
  - Eastmere (rent `None`);
  - a zero budget.
- [ ] **Step 2:** Write the tests:
  - `test_budget_check_worked_cases_match_expected`
  - `test_budget_check_equal_to_budget_is_within`
  - `test_budget_check_missing_side_is_none_not_within`
- [ ] **Step 3:** Run them (FAIL), implement, run them again (PASS).
- [ ] **Step 4:** Commit: `feat: budget check against rent and buy (within includes the budget)`.

### Task 7: Tenure shares and place search

**Files:**
- Create:
  - `packages/vestagraph-area/src/vestagraph_area/tenure.py`
  - `packages/vestagraph-area/src/vestagraph_area/place_search.py`
  - cases in `packages/fixtures/test-cases/council-tenure.json`
  - `packages/vestagraph-area/tests/test_council_tenure.py`
  - `packages/vestagraph-area/tests/test_council_place_search.py`

**Interfaces:**
- **Produces in `tenure.py`:** `tenure_shares(counts: TenureCounts) -> dict[str, Fraction]`. Each share is a percent to one decimal place. The shares are not forced to total 100, and the board says "shares may not add to 100% because of rounding".
- **Produces in `place_search.py`:**
  - `find_councils(query: str, area: CouncilArea) -> SearchResult`
  - `SearchResult(kind: "council"|"choose"|"not-found"|"not-covered", matches: tuple[Match, ...])`
  - `Match(council_code, label, note: "former-name"|None)`
- **Search rules:**
  - Matching is case and space insensitive, on exact names, never fuzzy.
  - The search looks at council names, `formerNames` (giving note `former-name`) and places.
  - Several councils, or several same-name places, give `choose`, each labelled "<place>, <county>".
  - A non-England place gives `not-covered`.
  - The search never picks one for the visitor.

- [ ] **Step 1:** Work the tenure cases by hand: Northbridge, plus a case where the rounded shares total 99.9.
- [ ] **Step 2:** Write the tests:
  - `test_tenure_shares_worked_cases_match_expected`
  - `test_find_councils_same_name_in_two_counties_is_choose_with_counties`
  - `test_find_councils_county_lists_its_districts`
  - `test_find_councils_former_name_leads_to_current_with_note`
  - `test_find_councils_welsh_place_is_not_covered`
  - `test_find_councils_unknown_is_not_found`
- [ ] **Step 3:** Run them (FAIL), implement, run them again (PASS).
- [ ] **Step 4:** Commit: `feat: tenure shares and council search by place name`.

### Task 8: Generator writes `council-result.json`

**Files:**
- Create:
  - `packages/fixtures/schema/generated-council-result.schema.json`
  - `packages/vestagraph-generator/src/vestagraph_generator/council_generator.py`
  - `packages/vestagraph-generator/tests/test_generator_council.py`
- Modify:
  - `packages/vestagraph-generator/src/vestagraph_generator/__main__.py` (build all three documents in memory, then write)
  - `costs_generator.py` (keep `council-result.json` when cleaning `generated/`)
  - the AGENTS.md Commands table
  - `packages/fixtures/README.md`
- Generated: `packages/fixtures/generated/council-result.json`

**Interfaces:**
- **Produces `council-result.json`:**
  `{ "$schema", "formatVersion": 1, "exampleInputs": {depositPercent: "10", termYears: 25}, "councils": [ { "code", "bands": [{band, yearly, monthly}], "rentOrBuy": {byBand: [{band, rentSide?, buySide?, repayment?, rateBand?, comparison?, difference?, problem?}]}, "captions": [{topic, kind, values}], "tenureShares": {...}?, "neighbourhoods": [{code, label: "<largerAreaName> (<code>)", tenureShares?}] } ], "search": [{query, kind, matches}] }`
  - Everything is sorted, so a rerun is byte-identical.
  - The `search` cases are taken from the sample places.

- [ ] **Step 1:** Write the tests:
  - `test_run_writes_all_three_generated_files_and_keeps_them`
  - `test_run_council_result_twice_is_byte_identical`
  - `test_run_council_data_invalid_exits_two_and_writes_nothing`
- [ ] **Step 2:** Run them (FAIL), implement, then run `make generate` and commit the generated file.
- [ ] **Step 3:** Run `make check`. Expected: PASS.
- [ ] **Step 4:** Commit: `feat: generator writes council-result.json`.

### Task 9: PR A, review and merge
- [ ] Map each rule and each Review Focus item to its test name in the PR description, with the test-first table.
- [ ] Ask the founder in a prompt window to review:
  - the £10 "about the same" threshold;
  - the "unchanged" rule;
  - the caption wording file.
- [ ] Run the pre-push Opus review with `code-security-reviewer` **before** pushing, and fix its findings.
- [ ] Push, then comment `@codex review`.
- [ ] The founder merges: it adds a tax rule table.
- [ ] Update `docs/planning/status.md` in the PR.

### Task 10: Canvas, chart style and the council page (light)
Board values come only from `council-result.json` and `council-area.json`: quote, never work out.
- [ ] **Brand and style:** chart rules:
  - line, bar and stacked bar;
  - the provisional pattern;
  - the "not published" gap;
  - the method-break gap;
  - focus and tap values;
  - the table view;
  - greyscale print.
- [ ] **Council page, phone (390) and desktop (1440), Northbridge:**
  - header and population line;
  - the band picker on D;
  - "What it costs here";
  - the budget box (empty, then with a value);
  - rent or buy at the example inputs;
  - the band bars;
  - the rent, price and affordability lines;
  - the tenure bar;
  - the neighbourhood map with its list;
  - "How we got this".
- [ ] **Acceptance:**
  - no verdict words;
  - every figure shows its level and period;
  - "repayment and council tax only" and "the averages describe different homes" are on the board;
  - touch targets are at least 44 px.

### Task 11: Canvas, neighbourhood page and states (light)
- [ ] **Neighbourhood result page,** phone and desktop. It reuses the area result's layout and shows only published neighbourhood facts. For a topic that needs a postcode, it shows "Check a postcode in this neighbourhood to see this". It includes the postcode box and the way back.
- [ ] **States board.** Every state in the design's States list:
  - working out / couldn't work this out;
  - one side missing (Eastmere);
  - no rate band;
  - choose a council (Newbury);
  - former name;
  - merger series;
  - not covered (Wales).

### Task 12: Canvas, part 2 boards and the how-to page (light)
- [ ] **Compare** in rows (Northbridge and Southvale), phone and desktop.
- [ ] **Share and print:** the printout states the example inputs.
- [ ] **"What changed since your last visit":** the consent off and on, a revised month, the Clear button.
- [ ] **The "Use in ChatGPT or Claude" page and the landing section (0056):**
  - developer mode explained, with its trade-off;
  - what the host app sees;
  - a link to the privacy notice.
- [ ] **The widget's full screen on a phone** (CARD-32 to CARD-35).

### Task 13: Founder review, dark versions, PR B
- [ ] The founder reviews the light boards; fix what comes back.
- [ ] Draw the dark versions (slate ink).
- [ ] **PR B:** the status file (canvas version, boards added), plus any register notes from the review.

### Task 14: PR C, specifications
- [ ] Write the specification files:
  - `docs/specs/pilot/city-explorer.feature` (council page, search, rent or buy, budget, captions, states, privacy);
  - `docs/specs/pilot/city-explorer-neighbourhood.feature`;
  - `docs/specs/pilot/city-explorer-part-2.feature` (compare, share and print, what changed, council tools);
  - `docs/specs/pilot/use-in-chatgpt-or-claude.feature`.

  Use scenario ID prefixes `CITY-`, `HOOD-`, `CITY2-` and `HOWTO-`. Map every board to its scenarios, and every figure to a `council-result.json` ID.
- [ ] Update the section list in `docs/specs/screens/01-landing.feature` (the council link and the how-to section) and the specs README.
- [ ] Add council tools to `docs/specs/pilot/area-tools.feature`: published figures only (0051, 0056).
- [ ] Run `make check`, the pre-push review, Codex, then merge.
