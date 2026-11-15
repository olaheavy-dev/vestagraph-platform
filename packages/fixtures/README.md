# Vestagraph fixtures

Synthetic sample data for the prototype (decision 0018, stage 2 plan section 1). Everything here is invented; nothing is a real person, address, postcode or document.

| Folder | What it holds |
|---|---|
| `schema/` | JSON Schema 2020-12 files. `common.schema.json` holds shared pieces (money, sources, dates, nations); the others describe one data file each. |
| `data/` | Hand-maintained **inputs**: household, homes, evidence, documents, questions, replies, snapshot, area, postcode-area, council-area, pilot-topics, sample-priorities. No totals or other calculated figures (AGENTS.md rule 2). |
| `test-cases/` | Independently worked examples (task 3), checked against one of two schemas: `schema/test-case.schema.json` for the cost cases and `schema/area-test-case.schema.json` for the area cases (`area-*.json`, `buses-per-hour.json`, `distance-display.json`, `priority-results.json`). |
| `generated/` | Generator output (task 4b): two files, `costs.json` (the cost engine's output, checked against `schema/generated-costs.schema.json`) and `area-result.json` (the `vestagraph_area` package's output, not the cost engine's: the figures the area design boards quote: At a glance counts, display distances, buses per hour and priority results, checked against `schema/generated-area-result.schema.json`). Written only by the generator (`make generate`) and committed; never edited by hand. `make check` regenerates it and fails if anything under `generated/` differs from what is committed. |

## Which schema checks which file

- `data/NAME.json` is checked against `schema/NAME.schema.json` (by file name). Each data file also carries a `"$schema": "../schema/NAME.schema.json"` line for editors; the validator fails if it names a different schema.
- Every file in `test-cases/` and `generated/` must name its schema in a top-level `"$schema"` field (a relative path into `schema/`); the cost test-case files name `../schema/test-case.schema.json` and the area ones `../schema/area-test-case.schema.json`, `costs.json` names `../schema/generated-costs.schema.json`, and `area-result.json` names `../schema/generated-area-result.schema.json`.

## How values are modelled

- **Money is whole pence** (`"pence": 160000` is £1,600). The schema accepts only integers of at least 1, so decimals and zero are rejected. A `period` (`once`, `month` or `year`) says how often it is charged, as the source states it; the cost engine does conversions.
- **Rates are basis points** (`"basisPoints": 550` is 5.5%), also an integer.
- **Missing data is never zero** (AGENTS.md rule 7). An evidence item's `status` is one of `available`, `missing`, `conflicting`, `stale`, `not-applicable`, `not-calculated` or `included`. Only `available`, `conflicting` and `stale` items may carry a `value`; the other four must not. A bill covered by the rent is `included`; stamp duty, legal fees and internal maintenance are `not-calculated`.
- **Every value has a source:** `origin` (`listing-claim`, `document`, `official-dataset`, `user-entered`, `synthetic`, or `plan` for a value the stage 2 plan itself sets, such as "outside this version's scope"; an origin of `synthetic` forces `synthetic: true`, and all stage 2 data is synthetic), the plain-language `label`, a `date` (year, year-month or full date, so a year-only source is not given an invented day), a `synthetic` flag, and an optional `citationUrl` with `citedText`.
- **Context-only costs:** `contextOnly: true` means the value is shown but never enters a total. Energy-certificate costs must be context-only.
- **Statuses are as at the snapshot** (23 October 2026), after each story has finished. `storyStep` and `usedFromStep` put events in order (1 to 4); they are not calendar time. An item with `supersedes` keeps the earlier value it replaces.
- **Nations:** every address has a `nation`. Outside England, `coverage` must be `not-yet-covered`.
- **Question statuses** are the eight in doc 02 section 6, written as `to-ask`, `waiting-for-reply`, `reply-needs-checking`, `answer-recorded`, `partially-answered`, `needs-professional-review`, `closed-by-user-without-answer` and `reopened`. Each question lists its transitions with a reason.

Run `make validate` after editing any file here.

## Rules for the cost engine (task 4b)

- **Which item applies.** An evidence item applies from its `usedFromStep` (step 1 if absent) until another item names it in `supersedes`. B1's 2026 budget (`B1-SC-BUDGET`, from step 4) supersedes the listing claim (`B1-SC-LISTING`); the listing item is kept, not deleted.
- **`conflicting` is a label, not an instruction.** It says sources disagree; it does not by itself decide whether an item enters a total. The engine decides from the case being calculated: before R1's water is settled it leaves water out and flags the total partial, and from step 4 it uses `R1-WATER-ESTIMATE`.
- **R1 water.** `R1-WATER-LISTING` ("Water included", `conflicting`) and `R1-WATER-WSOT` ("Tenant pays water") are evidence about who pays, category `water-responsibility`. They never carry an amount. `R1-WATER-ESTIMATE` (category `water`, from step 4) is the amount. In `test-cases/story-calculations.json` the R1 `water` line is `conflicting` before the user confirms and carries 4,500p a month after.
- **Included and not-calculated items** carry no value and add nothing to a total; they are never treated as zero.

### Test-case line categories and data categories

| Test-case `category` | Data `category` (evidence item) |
|---|---|
| `mortgage-deposit` (buyer upfront deposit) | `mortgage-deposit` (`HH-MORTGAGE-DEPOSIT`) |
| `deposit` (renter upfront deposit) | `deposit` (`R1-DEPOSIT`, `R2-DEPOSIT`) |
| `moving-costs`, `first-month-rent`, `rent`, `service-charge`, `ground-rent`, `council-tax`, `energy`, `water`, `broadband`, `buildings-insurance`, `maintenance`, `stamp-duty`, `legal-fees` | the same name |
| `mortgage-repayment` | none: a calculated output from `mortgage-deposit`, `mortgage-rate`, `mortgage-term` and `asking-price` |

Items that only describe a home (`council-tax-band`, `energy-certificate`, `energy-certificate-cost`, `lease-term`, `tenancy-type`, `water-responsibility`) have no test-case line.

## Area data (stage 3, #120)

`data/area.json` holds synthetic area context for the Nearby screen, checked by `schema/area.schema.json`. Founder decision, 11 Nov 2026: area information comes first, "alongside costs": "these ones should come first as they are everyday needs for renting and mortgage". Nothing in it is calculated, and nothing enters a cost total; council tax stays a user-entered cost input.

- **Topics** (the schema's `topic` enum, in priority order): `transport-stop`, `school`, `crime`, `flood`, `sold-price`, `amenity` (subtypes: supermarket, shop, park, pharmacy, police-station, hospital, gp-surgery, clinic, dentist, childcare, place-of-worship), `energy-certificate`, `school-inspection`, `broadband`, `bank-rate`, `commute`, `planning`, `leasehold-company`. Shapes, limits and "does not establish" wording mirror the sources assessed in `docs/references/data-sources.md`.
- **IDs:** `HOME-AREA-TOPIC-N`, for example `B1-AREA-SCHOOL-1`. The one shared Bank Rate item is `UK-AREA-BANK-RATE-1` and has no `homeId`.
- **Statuses:** `recorded`, `no-record-in-source` (never "none": it does not mean none exists), `stale`, `not-covered`, `source-failed`. Only `recorded` and `stale` carry a `value`; a gap is never zero or clean (rule 7). WALES-1 has `not-covered` items only (rule 6).
- **Every item** has a `source` (the same shape as evidence sources, all synthetic), a `coverage` text and a `doesNotEstablish` text, plus an optional `link` (for example the long-term flood risk checker) and `note`.
- **Distances and journey times** are synthetic inputs and each names its method (`distanceMethod`, for example "straight-line distance, synthetic"); the code calculates nothing, and a distance is never a walking time.
- **Flood** subtypes are `rivers-and-sea` and `groundwater` (the Environment Agency issues no surface-water warnings; long-term surface-water risk is a link to the checker). **Amenities:** every England home has each category (supermarket or shop, park, healthcare, police station, childcare, place of worship) as an item or an explicit `no-record-in-source` item. **Commute** times are the household's own estimates (origin `user-entered`), not routed journeys; routing stays deferred (DA-06). Item origins use the real kind (`official-dataset`, `user-entered`, `plan`) with `synthetic: true`.
- **Places of worship** carry `value.religion` (christian, muslim, jewish, sikh, hindu, buddhist, jain, multifaith, other, not-recorded), mapped from the source's tag. They are shown only as the nearest places by distance, every faith alike: never counts, densities or an area's religious makeup, and a user's own faith is never stored (register PD-13, decision 0014).
- **Crime** is recorded counts by category and month (at least 1; a category with none recorded is absent, never 0). The crime value allows no rating, score or level field, and no wording in this file calls a home safe, unsafe, verified or approved (rule 4).
- **Energy** items only point at the home's certificate and cost items in `evidence.json` (`evidenceItemIds`); the rating, year and cost are recorded once there (rule 2), are never actual bills, and never enter a total. **School inspections** carry a framework, a date and outcomes per area; there is no single overall grade field.
- Tests: `AreaSchemaRejectionTests` (the schema refuses bad records) and `AreaDataTests` (every England home has each topic or an explicit gap, WALES-1 is not covered, links resolve, wording rules hold).

## Postcode area data (#216)

`data/postcode-area.json` is checked by `schema/postcode-area.schema.json`. It holds synthetic area facts measured from a **postcode centre**, for the pilot's public area check, beside the home-keyed `area.json` (which it does not replace). The schema reuses the value shapes of `area.schema.json` by `$ref` and adds a `postcode` key (never a `homeId`), a `level` (register DA-14: each fact at its official level) and, for flood items, a `checkedAt` time with an explicit offset (register DA-12).

- **Postcodes** (England only, all synthetic): `NB1 4XY` (role `sample`, the normal result, mirroring the B1 records so the canvas figures stay), `NB7 1RR` (role `test`, sparse: three places between 1 and 5 km, no supermarket in the source, a failed flood lookup with no time, and a planning record with instruction-like text for the tools' "text is data" scenarios) and `NB9 9ZZ` (well-formed, listed under `unknownPostcodes`, no records).
- **Levels by topic:** transport stops, schools and amenities `from-postcode-centre`; school inspections `named-place`; crime `radius` of exactly 1609.344 m (police.uk's 1 mile); sold prices and planning `radius` 500 m; flood and broadband `postcode`.
- **Distances are inputs** with the method "straight-line from the postcode centre, synthetic". Live distances will come from the pilot's tested geometry module, not from this file.
- **Worked miles figures for later UI tests** (metres divided by 1609.344, one decimal): 2400 m is 1.49, shown "1.5 miles"; 3100 m is 1.93, "1.9 miles"; 4600 m is 2.86, "2.9 miles".
- Tests: `test_fixtures_postcode_area_schema_rejection.py` (the schema refuses bad records) and `test_fixtures_postcode_area_data.py` (levels, the exact mile, the flood time, unique IDs across both area files, listed postcodes, the sparse rules).

## Council area data (City Explorer)

`data/council-area.json` is checked by `schema/council-area.schema.json`. It holds synthetic council-level inputs for City Explorer, each with a `source` shaped like the real publisher (council tax Table 9, ONS rents, UK HPI, ONS affordability, population, Census tenure, DfT connectivity, Bank of England quoted rates); every value is invented and labelled "Synthetic sample, shaped like ...". Council codes are invented (999 in the middle, for example `E06999001`), never real ONS codes. Nothing in it is calculated (rule 2).

- **Councils:** Northbridge (unitary, complete, 24 monthly rent and price points, three neighbourhoods), Southvale (unitary, one price point `not-published`), Eastmere (district in Westshire, formed 2023-04-01 with a former name, rents `no-record-in-source`, an affordability series with `methodBreakBefore`) and Westmere (district, every fact a gap, council tax `bands` a gap).
- **Gaps:** a status other than `recorded` carries no `value` (rule 7); a series with a gap status has no points; a point with status `not-published` has no value.
- **Also in the file:** `places` (place names with nation and council codes), `postcodes` (postcode to council) and `rateBands` (2-year fixed at 60, 75, 85, 90 and 95%, 5-year fixed at 75 and 95%, as basis points).

## Pilot topics and sample priorities (first design batch)

- `data/pilot-topics.json` (`schema/pilot-topics.schema.json`) is the registry of the pilot's area topics in display order: the postcode-area record topics (and subtypes) each one reads, a `gapQuestionTemplate` with at most one `{subject}` slot (for a record that is a gap; the subject is a plain name from the registry's `subtypeNames`, else the topic's name, never a record label), a check-in-person list and, for route-only topics, an `officialRoute`. Each record belongs to exactly one counted topic; the family view has `counted: false` and is never in the counts. Every template and list is `reviewed` (the founder approved the wording on 14 Nov 2026, FE-39); every route-only topic's route has a label and a URL.
- `data/sample-priorities.json` (`schema/sample-priorities.schema.json`) holds synthetic example limits, kept as typed (a decimal string with a unit), used only to draw the boards. Tested code converts them exactly to metres.
- `postcode-area.schema.json` gains the topics `deprivation-rank`, `transport-connectivity`, `green-space`, `air-quality`, `council-tax`, `affordability`, `flood-risk-postcode`, `school-demand` and `bus-departures` with their value shapes; place values in `area.schema.json` gain optional `walkingMinutes` with a required `walkingMethod` (register DA-18).

## Known limits

- `partialDate` checks the shape (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`) but not that the date exists (2026-02-31 passes). Harmless for now.
- JSON Schema cannot say that `selectedUnitId` is one of `candidateUnits`, or that a question's `status` equals its last transition, or that references point at real records. Python tests in `packages/vestagraph-fixture-validator/tests/` check these.

## Fictional placeholders

WALES-1 ("7 Harbour Mews, Afonbryn", postcode `ZZ1 0AA`) is invented. A web search found no place called Afonbryn, and `ZZ` is not a geographic postcode area. Northbridge and the `NB` postcodes are also fictional (`NB` is not a UK postcode area).
