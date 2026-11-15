# City Explorer: whole-pound parts and house prices by property type (plan)

> For agentic workers: test-first (`.claude/skills/test-first/`, decision 0031) for every figure. Builds on PR A (#285).

**Why:** the founder's review of the light City Explorer boards, 15 Nov 2026 (prompt window):
- money parts: "Whole pounds via generator (Recommended)": the boards showed the repayment and monthly council tax to the penny (£1,582.47, £128.33) beside whole-pound totals, because `council-result.json` has whole-pound fields only for the totals, and rounding on a board would break rule 2;
- house prices: "Split now": the spec (item 7, "split by property type if the council download carries it") and the sources research (`docs/reviews/2026-11-16-city-explorer-sources.md`: `Average-prices-Property-Type-2026-08.csv` carries detached, semi-detached, terraced and flat for every English council) both point to four lines.

**Branch:** `feat/council-shown-pounds-and-types`. One pull request (code, Codex review).

## Data contract first
1. `packages/fixtures/data/council-area.json` and its schema: each council's `priceSeries` gains `byType`, an object with exactly the keys `detached`, `semiDetached`, `terraced`, `flat`, each a series of the same shape as `priceSeries` (status, unit `pence`, points with period, value, status). Synthetic values (inputs), each council's `source.label` "Synthetic sample, shaped like the UK House Price Index average prices by property type", with the source URL from the research note. Keep the same periods and gaps as the council's all-types series: Southvale (synthetic) keeps its unpublished month in every type; Eastmere (synthetic) keeps its series start. A type may be missing for a council (status, never zero; rule 7) — include one such case in the sample (for example `flat` not published for one council) so the gap state is tested.
2. `packages/fixtures/generated/council-result.json` and its schema:
   - a 12-month trend caption per property type, using the existing trend caption rules (`captions.py`): both end points needed, no change across a method break, no caption when an end is missing. A caption carries its property type. No caption ever compares two types or two councils.
   - whole-pound siblings for every money part the boards show, rounded once from pence, halves away from zero, with the same helper that produces `shownBuySide` and `shownRentSide`: `shownRepayment` beside `repayment`, `shownCouncilTax` beside the band's monthly council tax wherever it appears (rent-or-buy sides and the band list), and any other pence amount the council boards show (list each in the PR). A missing amount gets no shown field (never 0).
   - Rent or buy keeps using the all-types average price ("average-priced home", spec item 2); the types are shown, not used in the rent-or-buy figure.

## Tasks (backend only; boards are redrawn afterwards on the canvas)
1. Work the expected values by hand first (test-first skill): rounding cases including an exact half (for example 12850 pence → £129, 12849 → £128, 158247 → £1,582, 12833 → £128); a type trend with both ends; a type with a missing end month (no caption); a type not published for a council (gap, no caption, no zero). Record the working beside the cases in `packages/fixtures/test-cases/`.
2. Tests (names `test_<method>_<condition>_<result>`, files `test_council_*.py`), RED, then implement in `vestagraph_area` (pure functions) and `vestagraph_generator` (`council_generator.py`), GREEN.
3. Schemas, sample data, `make generate`, commit the regenerated files.
4. `make check` green. Commit locally. Stop before pushing: the pre-push review runs first (agent-workflows#23).

## Acceptance criteria → tests
- Every pence amount shown on a council board has a whole-pound sibling, rounded once, halves away from zero.
- A missing amount has no whole-pound sibling.
- Each council has four property-type series (or a recorded gap per type).
- Each type gets a trend caption only when both ends are published and no method break lies between them.
- No caption or field compares types or councils.
- Rent or buy figures are unchanged by this change (`costs.json` and existing `council-result.json` values byte-identical apart from the added fields).

## Out of scope
Rent by bedrooms or property type; redrawing boards (canvas work after merge); live sources (stage 5b).
