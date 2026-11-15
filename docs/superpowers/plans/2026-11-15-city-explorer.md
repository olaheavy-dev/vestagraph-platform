# City Explorer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Anything numeric also follows `.claude/skills/test-first/` (decision 0031).

**Goal:** Give City Explorer's council and neighbourhood pages real, tested figures from synthetic sample data. Then draw them on the design canvas, then write their specifications, ready for the pilot gate (0052).

**Architecture:** This is stage 3 work only, the same shape as the first design batch (#259):
- Research the sources first, so the sample data takes the real sources' shapes.
- The data contract comes next: a council sample file and its schema. The eight council tax bands are published inputs (MHCLG Table 9), so there is no band table.
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
- **Rule 3:** there is **no band rule table**. The eight council tax band amounts are published inputs from MHCLG's [council tax levels 2026-27](https://www.gov.uk/government/statistics/council-tax-levels-set-by-local-authorities-in-england-2026-to-2027) Table 9, each recorded with its source (founder, 15 Nov 2026: "Record all eight bands", reason "Match the publication"). Nothing is derived from Band D by proportions, and there are no ratio tests. The mortgage rates are inputs from the Bank of England series (sources in Task 1's note).
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
- **Money:** in `Pence`, rounding halves away from zero, once per published figure (0021). A band's yearly amount is the published amount, recorded in pence as given; its monthly amount is that yearly amount ÷ 12 via `Pence.annual_to_monthly`, rounded once, because the monthly figure comes from the published yearly figure (#197 notes that no record states the ÷ 12 rule yet). Captions show money in whole pounds (rounded from pence, halves away from zero); the generated file keeps pence.
- **Exact numbers in generated files:** a whole `Fraction` is written as an integer, any other as an exact decimal string (`"34.5"`), as `area-result.json` does; never a float.
- **Rankings note:** the official deprivation rank and decile are allowed, quoted as published with 0054's notes ("relative, not absolute"; "describes the neighbourhood, not a street"); what is banned is a ranking we make.
- **Percentages:** one decimal place, halves away from zero, from an exact `Fraction`.
- **Sample data stays synthetic.**
  - Councils are named "Northbridge", "Eastmere" and "Southvale", each with "(synthetic)".
  - Neighbourhood names are made up.
  - `source.label` reads "Synthetic sample, shaped like <real source>".
- **Test names:** `test_<method>_<condition>_<result>` (0039). Test files are `test_council_*.py`.
- No agent attribution in commits or pull requests.

## Review Focus
1. **A deposit of 100% or more, or a loan of zero,** gives "deposit too large: no mortgage needed" on the buy side, never a crash or £0; the rent side stays. The test is in Task 4.
2. **A loan above the highest published band** (for example a 3% deposit when the bands stop at 95%) gives `rate-band-unavailable` on every buy side; the rent side stays. **A product with no rate at the deposit's band** (the 5-year fixed is published only at 75% and 95%) gives `rate-band-unavailable` on that product's buy side only; the 2-year side stays. A band is never borrowed from another band or product. A small loan takes the lowest band that covers it (bands mean "up to X% loan"; a 50% loan takes the 60% band). The tests are in Task 4.
6. **Missing council tax** (the band's published amount is a gap) gives `council-tax-missing`, with no side, comparison or budget label, never £0. The test is in Task 4.
7. **A very large typed rate** gives `rate-too-high`, never a crash. The test is in Task 4.
3. **A council with no published rent** gets the buy side only: no difference sentence and no budget label for rent. The test is in Tasks 4 and 6.
4. **A trend whose month 12 months earlier is missing or across a method break** gets no change caption. It shows only "not published" or "not comparable". The test is in Task 5.
5. **Two places with the same name in different counties** are both returned, labelled with their county, and never auto-picked. The test is in Task 7.

## Pull requests
- **PR R (research, documentation):** Task 1. Branch `docs/city-explorer-sources`.
- **PR A (code, Codex review):** Tasks 2 to 9. Branch `feat/council-result-data`.
  - It is no longer a founder merge for the tax rule-table reason, because there is no band rule table (founder: "Record all eight bands"). Task 9 checks that nothing else on the founder-only list is in it.
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

  - list which products (for example 2-year and 5-year fixed) the Bank quotes for each band.

  This fixes the sample data's band list. **Founder question** (prompt window, with a recommendation): which product the example uses.
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
- Modify: `packages/fixtures/README.md`
- Test: `make validate`

**Interfaces:**
- **Produces `council-area.json`:**
  `{ "$schema", "councils": [Council], "places": [PlaceName], "rateBands": [RateBand] }`
  - **Council:**
    `{ "code", "name", "nation", "tier": "unitary"|"district", "county"?, "formedOn"?, "formerNames"?: [..], "population": Fact, "bands": Fact, "rentSeries": Series, "priceSeries": Series (also `byType`: `{detached, semiDetached, terraced, flat}`, each a Series; added by the pounds-and-types change), "affordabilitySeries": Series, "tenure": Fact, "connectivity": Fact, "neighbourhoods": [Neighbourhood] }`
  - **Fact:**
    `{ "status": "recorded"|"no-record-in-source"|"source-failed"|"not-covered", "value"?, "level": {kind, name}, "source": {label, url, edition, period} }`
  - **Series:**
    `{ "status", "unit": "pence-per-month"|"pence"|"ratio", "points": [ {"period": "YYYY-MM"|"YYYY", "value"?: int|decimal-string, "status": "recorded"|"provisional"|"not-published", "methodBreakBefore"?: true} ], "level", "source" }`
  - **Bands value (the `bands` Fact):** `{ "A": int, "B": int, …, "H": int }`: the eight published yearly band amounts in pence, from MHCLG Table 9 ("Area council tax for a dwelling occupied by two adults by band"). A recorded `bands` Fact has all eight keys; a gap status carries no value. The Fact's `source` names Table 9 and its edition.
  - **Tenure value:** `{ "ownedOutright", "ownedWithMortgage", "socialRented", "privateRented", "other" }`. These are whole household counts; shares are worked out.
  - **Neighbourhood:**
    `{ "code" (the full LSOA code, for example a synthetic "E01999012"), "shortCode" (the suffix shown and used after the `#`, for example "012C"), "largerAreaName", "facts": { "connectivity": Fact, "deprivation": Fact (value {decile, rank, ofAreas, edition}), "tenure": Fact } }`
  - **PlaceName:** `{ "name", "county", "region", "councilCodes": [..] }`
  - **RateBand:** `{ "product": "2-year-fixed"|"5-year-fixed", "maxLoanToValuePercent": int, "rateBasisPoints": int, "month": "YYYY-MM", "source" }`. The bands are shaped like the Bank's published ones (Task 1): the 2-year fixed at 60, 75, 85, 90 and 95%; the 5-year fixed at 75 and 95% only.
  - Every rate stays an input, never a calculated figure.

- [ ] **Step 1:** Write the schemas (`additionalProperties: false`; a gap status carries no `value`).
- [ ] **Step 2:** Write the sample data:
  - **Northbridge (synthetic), unitary:** complete, with 24 monthly rent and price points, the last 2 rent and the last 12 price points provisional, and 3 neighbourhoods.
  - **Eastmere (synthetic), district in "Westshire (synthetic)":** `formedOn` 2023-04-01 with a former name, rents `no-record-in-source`, and an affordability series with a `methodBreakBefore`.
  - **Southvale (synthetic):** a council whose price point 12 months back is `not-published`.
  - **Westshire (synthetic)** has two districts: Eastmere and "Westmere (synthetic)" (a small district record, other facts as gaps).
  - **Places:** "Northbridge" (one council), "Newbury (synthetic)" twice in two counties, "Westshire" (the county, listing both districts), a place spanning Eastmere and Westmere, a "London"-style region name listing several councils (synthetic "Capital (synthetic)" with two council codes), and a Welsh-style place with `nation: "wales"`.
  - **Postcodes:** a short list mapping sample postcodes to councils (`"postcodes": [{postcode, councilCode}]`, NB1 4XY to Northbridge, one to Southvale), for the "postcode in another council" check.
  - **Rate bands:** 2-year fixed at 60, 75, 85, 90 and 95; 5-year fixed at 75 and 95 (as the Bank quotes them, Task 1). The rate values are synthetic and carry their source label.
  - **Council tax bands:** each complete council records all eight band amounts as a `bands` Fact; Westmere's `bands` is a gap (`no-record-in-source`), to test the missing-council-tax case.
- [ ] **Step 3:** Run `make validate`. Expected: PASS.
- [ ] **Step 4:** Commit: `feat: council sample data and schema`.

### Task 3: Council records reader and council tax band amounts

**Files:**
- Create:
  - `packages/vestagraph-area/src/vestagraph_area/council_records.py`
  - `packages/vestagraph-area/src/vestagraph_area/council_tax.py`
  - `packages/fixtures/test-cases/council-tax.json`
  - `packages/vestagraph-area/tests/test_council_tax.py`
  - `packages/vestagraph-area/tests/test_council_records.py`
- Modify:
  - `packages/vestagraph-area/pyproject.toml` (`dependencies = ["vestagraph-engine"]` plus the workspace source)
  - the root `pyproject.toml` (paths)
  - `uv.lock`

**Interfaces:**
- **Produces in `council_records.py`:**
  - `read_council_area(path) -> CouncilArea`
  - frozen dataclasses mirroring Task 2 (`Council`, `Fact`, `Series`, `SeriesPoint`, `Neighbourhood`, `PlaceName`, `RateBand`)
  - it raises `InvalidAreaDataError` (from `records.py`) for anything not understood, with the same refusals as `read_postcode_area`.
- **Produces in `council_tax.py`:**
  - `band_yearly(bands: Fact, band: str) -> Pence | None`, which reads the published yearly amount for that band from the council's `bands` Fact, and returns `None` when the Fact is a gap (never £0, rule 7);
  - `band_monthly(yearly: Pence) -> Pence`, which is `yearly.annual_to_monthly()`.
  - An unknown band raises `InvalidAreaDataError`.

- [ ] **Step 1:** Work the cases by hand, with the working shown:
  - each of the eight sample band amounts and its monthly amount (yearly ÷ 12, rounded once, halves away from zero);
  - a yearly amount leaving exactly half a penny when ÷ 12 (for example 6 pence a year: 6 ÷ 12 = 0.5, which rounds to 1 penny), to show halves away from zero;
  - a yearly amount that divides exactly;
  - a `bands` gap (no amount, no monthly figure).
  - There are no ratio cases: the amounts are published, not derived.
- [ ] **Step 2:** Write the tests:
  - `test_band_yearly_returns_the_published_amount_for_each_band`
  - `test_band_yearly_unknown_band_raises`
  - `test_band_yearly_gap_returns_none_not_zero`
  - `test_band_monthly_worked_cases_match_expected`
  - `test_band_monthly_exact_half_penny_rounds_away_from_zero`
  - `test_read_council_area_gap_with_value_raises`
  - `test_read_council_area_recorded_bands_missing_a_band_raises`
- [ ] **Step 3:** Run `uv run pytest packages/vestagraph-area -q -k council`. Expected: FAIL (the module is missing).
- [ ] **Step 4:** Implement it. Run again. Expected: PASS.
- [ ] **Step 5:** Commit: `feat: council records reader and council tax band amounts`.

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
  - `rate_band_for(deposit_percent: Fraction, bands: Sequence[RateBand], product: "2-year-fixed"|"5-year-fixed") -> RateBand | None`.
    - The loan-to-value is `100 − deposit_percent`.
    - The band is chosen on the **whole band grid** (the loan-to-value values of every product's bands together: 60, 75, 85, 90, 95): the smallest grid band whose `maxLoanToValuePercent` is at least the loan-to-value (bands mean "up to X% loan").
    - The function then returns that product's rate **at that same grid band**, or `None` when the product publishes none there. A band is never borrowed from another band or product, so the 5-year fixed has a rate only for loans taking the 75% or 95% grid band.
    - It returns `None` for every product when the loan-to-value is above the highest grid band or at or below 0.
    - This reading of "a 5-year line where the Bank quotes one, and no published rate elsewhere" is the agent's call, for the founder to review in PR A: a 5-year rate from the 95% band is not used for an 80% loan.
  - `rent_or_buy(rent_monthly: Pence | None, price: Pence | None, council_tax_monthly: Pence | None, deposit_percent: Fraction, term_years: int, rate_basis_points: int | None, bands: Sequence[RateBand]) -> RentOrBuy`
  - `RentOrBuy(rent_side: Pence | None, buy_sides: tuple[BuySide, ...], problem: str | None)`
  - `BuySide(product: "2-year-fixed"|"5-year-fixed"|"typed-rate", buy_side: Pence | None, repayment: Pence | None, rate_used: RateBand | None, comparison: "more"|"less"|"about-the-same"|None, difference: Pence | None, problem: str | None)`
  - `ABOUT_THE_SAME_PENCE = 1000` (£10 a month, the agent's call, for the founder to review in PR A).
- **Rules:**
  - `rent_side` = rent + council tax.
  - Each `buy_side` = repayment + council tax.
  - **One buy side per product** (founder, 15 Nov 2026: "Both where each exists"). Without a typed rate, `buy_sides` holds a 2-year-fixed side and a 5-year-fixed side. A product with no rate at the deposit's band gives a side with `buy_side None` and `problem "rate-band-unavailable"`; the other product's side and the rent side stay.
  - The repayment is on `price × (100 − deposit_percent) / 100`, rounded once, from the engine.
  - A typed `rate_basis_points` overrides the bands: `buy_sides` then holds one side with `product "typed-rate"` and no `rate_used`.
  - A 0% typed rate gives a repayment of loan ÷ payments, rounded once (the engine refuses 0).
  - **Problems.** A problem with the buying inputs hides every buy side and their comparisons: the rent side and its budget check stay, as the design's missing-input rule says. `RentOrBuy.problem` carries it: `deposit-too-large`, `deposit-negative`, `term-out-of-range`, `rate-negative`, `rate-too-high`. `rate-band-unavailable` sits on each `BuySide` (every side when the loan is above the highest band; one side when only that product lacks the band). Only `council-tax-missing` hides both rent and buy sides:
    - `deposit-too-large`: a deposit of 100% or more;
    - `deposit-negative`;
    - `term-out-of-range`: a term outside 1 to 40;
    - `rate-band-unavailable`: no rate at the band for that product, and no typed rate;
    - `rate-negative`;
    - `rate-too-high`: a typed rate above `MAX_TYPED_RATE_BASIS_POINTS = 2000` (20%, the agent's call, for the founder to review in PR A);
    - `council-tax-missing`: no council tax for the band (its published amount is a gap); never treated as £0.
  - A missing rent or price gives that side `None`, `comparison None` and `difference None`.
  - Each side's `comparison` is "about-the-same" when |buy − rent| < 1000 pence. Otherwise it is "more" or "less" (buy compared with rent).

- [ ] **Step 1:** Work the cases by hand from the Northbridge sample:
  - deposits of 10% (a 90% loan: the 2-year fixed has a 90% band, the 5-year has none), 20% (an 80% loan, which takes the 85% band: no 5-year rate), 25% (75%: both products), 5% (95%: both products), 40% (60%: 2-year only) and 3% (no band for either);
  - 0%, 100% and −5% deposits;
  - a 0% typed rate;
  - Eastmere with no rent;
  - a pair within £10;
  - a 50% deposit (takes the 60% band);
  - a typed rate (one "typed-rate" side);
  - missing council tax; a typed rate of 2,001 basis points.

  Show the engine's formula working for one case.
- [ ] **Step 2:** Write the tests:
  - `test_rent_or_buy_worked_cases_match_expected`
  - `test_rate_band_for_two_year_eighty_percent_loan_takes_eighty_five_band`
  - `test_rate_band_for_five_year_without_a_band_at_the_grid_band_is_none`
  - `test_rent_or_buy_returns_one_buy_side_per_product`
  - `test_rent_or_buy_five_year_unavailable_keeps_two_year_side_and_rent_side`
  - `test_rent_or_buy_typed_rate_gives_one_typed_rate_side`
  - `test_rate_band_for_loan_above_highest_band_is_none`
  - `test_rent_or_buy_deposit_one_hundred_percent_is_deposit_too_large`
  - `test_rent_or_buy_missing_rent_has_buy_side_only_and_no_comparison`
  - `test_rent_or_buy_zero_typed_rate_divides_loan_by_payments`
  - `test_rent_or_buy_within_ten_pounds_is_about_the_same`
  - `test_rate_band_for_fifty_percent_loan_takes_lowest_band`
  - `test_rent_or_buy_missing_council_tax_is_problem_not_zero`
  - `test_rent_or_buy_rate_above_limit_is_rate_too_high`
  - `test_rent_or_buy_no_rate_band_keeps_rent_side_and_hides_buy_side`
- [ ] **Step 3:** Run them (FAIL), implement, run them again (PASS).
- [ ] **Step 4:** Commit: `feat: rent or buy per month with the rate for the deposit band and product`.

### Task 5: Plain-words captions

**Files:**
- Create:
  - `packages/vestagraph-area/src/vestagraph_area/captions.py`
  - `packages/fixtures/test-cases/council-captions.json`
  - `packages/vestagraph-area/tests/test_council_captions.py`

**Interfaces:**
- **Produces:**
  - `twelve_month_change(series: Series, latest_period: str) -> Change | None`
  - `Change(from_period, to_period, from_value, to_value, amount: Pence | Fraction, percent: Fraction | None, direction: "rose"|"fell"|"unchanged", provisional_points: int)`
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
  - `provisional_points` counts provisional points in the latest 12 months.
  - For a yearly series (periods `YYYY`), the change is from the previous year; the caption names the two years.
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
  - Real data (stage 5b) comes from OS Open Names settlements joined to councils through a tested name-mapping table (founder: "Use it, match by name (Recommended)"; three attribution lines; quarterly refresh). The sample places in this plan stay synthetic.
  - The search looks at council names, `formerNames` (giving note `former-name`) and places.
  - Several councils, or several same-name places, give `choose`, each labelled "<place>, <county>".
  - A non-England place gives `not-covered`.
  - The search never picks one for the visitor.
- **Produces in `place_search.py`:** `council_for_postcode(postcode: str, area: CouncilArea) -> str | None` (from the sample `postcodes` list; at 5b the postcode lookup, DA-06), so the page can say "This postcode is in <council>" and still open its result.

- [ ] **Step 1:** Work the tenure cases by hand: Northbridge, plus a case where the rounded shares total 99.9.
- [ ] **Step 2:** Write the tests:
  - `test_tenure_shares_worked_cases_match_expected`
  - `test_find_councils_same_name_in_two_counties_is_choose_with_counties`
  - `test_find_councils_county_lists_its_districts`
  - `test_find_councils_former_name_leads_to_current_with_note`
  - `test_find_councils_welsh_place_is_not_covered`
  - `test_find_councils_unknown_is_not_found`
  - `test_find_councils_region_lists_several_councils`
  - `test_find_councils_place_spanning_two_councils_is_choose`
  - `test_council_for_postcode_in_another_council_returns_that_council`
- [ ] **Step 3:** Run them (FAIL), implement, run them again (PASS).
- [ ] **Step 4:** Commit: `feat: tenure shares and council search by place name`.

### Task 8: Generator writes `council-result.json`

**Files:**
- Create:
  - `packages/fixtures/schema/generated-council-result.schema.json`
  - `packages/vestagraph-generator/src/vestagraph_generator/council_generator.py`
  - `packages/vestagraph-generator/tests/test_generator_council.py`
- Modify:
  - `costs_generator.py`: `run()` builds all three documents in memory, then writes them, and keeps `council-result.json` when cleaning `generated/`
  - `__main__.py`: docstring and output lines only
  - the AGENTS.md Commands table
  - `packages/fixtures/README.md`
- Generated: `packages/fixtures/generated/council-result.json`

**Interfaces:**
- **Produces `council-result.json`:**
  `{ "$schema", "formatVersion": 1, "exampleInputs": {depositPercent: "10", termYears: 25}, "councils": [ { "code", "bands": [{band, yearly, monthly}] (yearly is the published amount, monthly is worked out), "rentOrBuy": {byBand: [{band, rentSide?, buySides: [{product, buySide?, repayment?, rateBand?, comparison?, difference?, problem?}], problem?}]}, "captions": [{topic, kind, values}], "tenureShares": {...}?, "neighbourhoods": [{code, label: "<largerAreaName> (<code>)", tenureShares?}] } ], "search": [{query, kind, matches}] }`
  - Everything is sorted, so a rerun is byte-identical.
  - The `search` cases are taken from the sample places.
  - **As built (PR A, after the final review):** the file is the contract; this list is the differences from the line above. `rentOrBuy` also holds `rentPeriod`, `rentPointStatus`, `pricePeriod`, `pricePointStatus` (the month and status of the figure used, never an older month), `rentMissingReason` and `priceMissingReason` (a gap status, or `latest-not-published`) and `councilTaxMissingReason` (the council tax gap status). Each band has `shownRentSide` and each buy side `shownBuySide` and `shownDifference`: whole pounds, each side rounded once, shown difference = shown buy minus shown rent, and the comparison is made on those (`about-the-same` when under £10). `exampleInputs.depositPercent` is a JSON number (10). A tenure share is text with one decimal ("35.0"), the same text the caption quotes; a tenure gap is a `missing` caption (council) or `tenureMissingReason` (neighbourhood). Tenure captions have kind `single-point`; caption values say `provisionalPoints`, not `provisionalMonths`. The postcode search kind is `council-for-postcode`. **Added after PR A (pounds-and-types change, 15 Nov 2026, founder: "Whole pounds via generator" and "Split now"; `docs/superpowers/plans/2026-11-15-city-explorer-pounds-and-types.md`):** every money part a board shows has a whole-pound sibling from the generator, never rounded on a board: `bands[].shownYearly` and `bands[].shownCouncilTax` (beside `yearly`, `monthly`), `rentOrBuy.byBand[].councilTax` with `shownCouncilTax` (only when the council tax is known), and `buySides[].shownRepayment` (only when `repayment` exists); the schema pairs each shown field with its pence field. `priceByType` is a new array of four `{propertyType, kind, values}` captions in the order detached, semiDetached, terraced, flat (`values` is the price caption plus `propertyType`; a gap type is a `missing` caption, never zero). Rent or buy still uses the all-types average price.

- Every new `council-*.json` and `rent-or-buy.json` test-case file names `../schema/area-test-case.schema.json` (the area worked-case format); `packages/fixtures/test-cases/README.md` lists them.

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
  - the caption wording file;
  - the 20% typed-rate limit;
  - how the 5-year line is chosen (a rate only where the Bank publishes one at the deposit's own band).
- [ ] Run the pre-push Opus review with `code-security-reviewer` **before** pushing, and fix its findings.
- [ ] Push, then comment `@codex review`.
- [ ] Merge: not a founder merge for the tax rule-table reason (there is no band rule table). Before merging, check that nothing else on the founder-only list is in the PR (a new package, `LICENSE`, `.claude/settings.json`, CI permissions, infrastructure).
- [ ] Update `docs/planning/status.md` in the PR.

### Task 10: Canvas, chart style and the council page (light)
Board values come only from `council-result.json` and `council-area.json`: quote, never work out.
- [x] **Brand and style:** chart rules:
  - line, bar and stacked bar;
  - the provisional pattern;
  - the "not published" gap;
  - the method-break gap;
  - focus and tap values;
  - the table view;
  - greyscale print.
- [x] **Council page, phone (390) and desktop (1440), Northbridge:**
  - header and population line;
  - the band picker on D;
  - "What it costs here";
  - the budget box (empty, then with a value);
  - rent or buy at the example inputs;
  - the band bars;
  - the rent, price and affordability lines (the price board draws four lines, one per property type, from `priceByType` and the type series, and quotes the `shown*` fields rather than rounding);
  - the tenure bar;
  - the neighbourhood map with its list;
  - "How we got this".
- [x] **Acceptance:**
  - no verdict words;
  - every figure shows its level and period;
  - "repayment and council tax only" and "the averages describe different homes" are on the board;
  - touch targets are at least 44 px.

### Task 11: Canvas, neighbourhood page and states (light)
- [x] **Neighbourhood result page,** phone and desktop. It reuses the area result's layout and shows only published neighbourhood facts. For a topic that needs a postcode, it shows "Check a postcode in this neighbourhood to see this". It includes the postcode box and the way back. The official deprivation rank and decile appear as published, with 0054's notes ("relative, not absolute"; "describes the neighbourhood, not a street").
- [x] **States board.** Every state in the design's States list:
  - working out / couldn't work this out;
  - one side missing (Eastmere);
  - no rate band;
  - choose a council (Newbury);
  - former name;
  - merger series;
  - not covered (Wales);
  - postcode in another council;
  - offline; all sources down; a stale edition;
  - a figure published only for the county;
  - a council replaced during the pilot.

### Task 12: Canvas, part 2 boards and the how-to page (light)
- [x] **Compare** in rows (Northbridge and Southvale), phone and desktop.
- [x] **Share and print:** the printout states the example inputs.
- [x] **"What changed since your last visit":** the consent off and on, a revised month, the Clear button.
- [x] **The "Use in ChatGPT or Claude" page and the landing section (0056):**
  - developer mode explained, with its trade-off;
  - what the host app sees;
  - what your app sends us, and that we keep only anonymous totals (0057);
  - a link to the privacy notice.
- [x] **The widget's full screen on a phone** (CARD-32 to CARD-35).

### Task 13: Founder review, dark versions, PR B
- [x] The founder reviews the light boards; fix what comes back.
- [x] Draw the dark versions (slate ink).
- [ ] **PR B:** the status file (canvas version, boards added), plus any register notes from the review.


**Founder, 15 Nov 2026 (prompt window, "Copy layout, new boards (Recommended)"):** the City Explorer boards are new boards that copy the layout and parts of existing boards; the originals are untouched.

**As drawn (15 Nov 2026, canvas version 332).** Light boards first, then dark versions after the founder accepted the light ones. The "Use in ChatGPT or Claude" steps follow the corrected research (`docs/reviews/2026-11-15-use-in-assistant-research.md`), so "developer mode explained" in Task 12 became "adding a custom MCP server as a plugin, with its trade-off".
- **Dark versions** (the founder, 15 Nov 2026, typed: "go ahead with the dark versions"): 17 boards in all: ChartRulesDark and CouncilPage, CouncilPageDesktop, CouncilBudgetValue, NeighbourhoodPage, NeighbourhoodPageDesktop, CouncilStates, CouncilCompare, CouncilCompareDesktop, CouncilWhatChanged, CouncilWhatChangedDesktop, CouncilAboutData, UseInAssistant, UseInAssistantPhone, LandingAssistantSection, LandingAssistantSectionPhone, AreaCardWidgetFullPhone (the widget on a phone); no dark printout (FE-50).
- **Brand and style:** ChartRules (chart rules, with dash patterns on the four price lines: solid, long dash, short dash, dotted, plus direct labels), ChartRulesDark.
- **Pilot · City Explorer:** row 1 CouncilPage (phone, topic rows that open sheets) and CouncilPageDesktop; CouncilBudgetValue; CouncilPrint (light only, paper); row 2 NeighbourhoodPage and NeighbourhoodPageDesktop, CouncilStates (24 frames); row 3 CouncilCompare and CouncilCompareDesktop, CouncilWhatChanged and CouncilWhatChangedDesktop, CouncilAboutData (the DfT status). Dark versions of every one of these except the printout sit at the light board's x plus 8000, same y.
- **Pilot · public area check:** UseInAssistant (desktop) and UseInAssistantPhone, LandingAssistantSection and LandingAssistantSectionPhone, AreaCardWidgetFullPhone (the widget on a phone), each with a dark version in a "Pilot 6 · dark" row; "Sample data: a made-up town" added to every widget board (new and existing); the four landing boards' hero changed to one box (FE-37) with the four approved rewordings and the FAQ answer "Do you keep my search?".
- **Founder's review changes (15 Nov 2026):** whole pounds for the council parts (generator, #290); house prices split by property type (#290); the phone council page as topic rows that open sheets; one coverage line only; DfT status only on About the data; the four captions approved; typed rate limit 20%; tenure rounding line; dash patterns; one search box for postcode or town; research before approving placeholders. Register lines are in `docs/decisions/README.md` (FE-37 amended, FE-43 to FE-50, DA-21, BE-38, PD-19).
- **Placeholders left on boards** (waiting on testing, the build or the privacy notice; the list is from the R2 redraw report and was not re-checked against every live board): ChatGPT widget support, the Claude card for a URL-added connector, developer mode per account, ChatGPT Free, Plus and Pro availability and "No authentication" per plan, the server address, the example questions, the privacy notice link.

### Task 14: PR C, specifications
- [ ] Write the specification files:
  - `docs/specs/pilot/city-explorer.feature` (council page, search, rent or buy, budget, captions, states, privacy);
  - `docs/specs/pilot/city-explorer-neighbourhood.feature`;
  - `docs/specs/pilot/city-explorer-part-2.feature` (compare, share and print, what changed, council tools);
  - `docs/specs/pilot/use-in-chatgpt-or-claude.feature`.

  Use scenario ID prefixes `CITY-`, `HOOD-`, `CITY2-` and `HOWTO-`. Map every board to its scenarios, and every figure to a `council-result.json` ID.
- [ ] Update the section list in `docs/specs/screens/01-landing.feature` (the council link and the how-to section) and the specs README.
- [ ] Add council tools to `docs/specs/pilot/area-tools.feature`: published figures only (0051, 0056), with their AI evaluation cases (AI-03) listed.
- [ ] Add the area result's "About <council>" link to `docs/specs/pilot/area-display.feature` (or the area result spec that owns its header), and City Explorer's sources to About the data's scenarios.
- [ ] Check `.design/prototype/INFORMATION_ARCHITECTURE.md` still matches the boards (the routes were added in #282).
- [ ] Run `make check`, the pre-push review, Codex, then merge.
