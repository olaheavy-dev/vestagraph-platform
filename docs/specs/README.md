# Specifications

The prototype specification lives here (decision [0043](../decisions/0043-specification-format.md), SP-01). It describes what each screen, story step and MCP tool must do, precisely enough to build and test it from this folder and the fixtures alone (doc 04 §9 stage 3). The specifications are **executable**: a Python project (`packages/specs/tests`) runs these Gherkin files with pytest-bdd (decision 0049; the Reqnroll runner was removed in port step P8).

## Layout
| Path | Holds | Issue |
|---|---|---|
| `screens/NN-<screen>.feature` | One feature per screen in doc 03 §5, numbered in that order (for example `05-real-costs.feature`); 14 screens, with Check an area (decision 0046) appended as `14-check-an-area.feature` so earlier numbers and IDs never move | #68 |
| `pilot/<feature>.feature` | The pilot's specifications (stage 5b, decisions 0051 and 0052), for example `area-tools.feature`; checked by the pilot gate | #223 and later pilot specifications |
| `pilot/area-glance.feature`, `area-priorities.feature`, `area-topics.feature`, `area-display.feature`, `area-map.feature` | The first design batch of the area result: At a glance (GLANCE), priorities (PRIO), the topic sheet and panel (TOPIC) and display settings, theme and text size (DISP) and the maps' behaviour (MAP); its error and edge states are AREA-28 to AREA-36 in `screens/14-check-an-area.feature`. The benchmark design pass (16 Nov 2026) added the desktop result (AREA-37 to AREA-43), About the data and the sparse area's gaps (AREA-44 to AREA-47), the new topics and Check this rows (TOPIC-26 to TOPIC-40) and the map modes and layers (MAP-14 to MAP-26) | — |
| `pilot/area-printout.feature` | The designed area summary printout, "Print or save as PDF" (PRINT, FE-21), redrawn in the benchmark design pass: cover, At a glance with its map, every topic, Check this rows, How we got this, Sources and credits | — |
| `pilot/area-chat.feature` (withdrawn; 2 scenarios kept, which run again) | The on-page area chat (CHAT-01 to CHAT-53) left the pilot on 15 Nov 2026 ([0056](../decisions/0056-no-on-page-chat-in-the-pilot.md)). *16 Nov 2026, 0058: that chat returns to the pilot for signed-in users as the workspace chat. The review is done: 2 scenarios kept (they run again), 50 replaced by new IDs in `sign-in.feature`, `workspace-chat.feature` and `account.feature` (each stays `@withdrawn`, unedited), 1 retired; the table is in the file's description.* The pilot page "Use in ChatGPT or Claude" (0056, decision 2) is specified in `pilot/use-in-chatgpt-or-claude.feature` (HOWTO) | — |
| `pilot/sign-in.feature` | Signing in to chat and save areas: the three methods, the email link's states, account linking, the return to the page, sign out (AUTH-01 to AUTH-28; decision [0058](../decisions/0058-signed-in-chat-in-the-pilot.md), register lines SE-06, FE-56) | — |
| `pilot/workspace-chat.feature` | The signed-in workspace chat: sidebar, chat and side panel, streamed answers and widgets, the 15 messages a day, limits and errors, saved areas, past chats, the output guards, logs and traces, the feedback kit's states (WCHAT-01 to WCHAT-110; 0058, FE-51 to FE-65) | #302 |
| `pilot/account.feature` | The account pages: overview, saved areas, chats, sign-in methods, retention, delete with Undo and deleting the account (ACCT-01 to ACCT-42; 0058, FE-53, FE-65, FE-66) | #302 |
| `pilot/city-explorer.feature` | City Explorer's council page: search, the cost summary, rent or buy, your budget, topic rows and sheets, captions, states, privacy (CITY-01 to CITY-112; decisions 0053, 0054, 0055; register lines FE-37, FE-43 to FE-50, DA-21, BE-38, PD-19) | — |
| `pilot/city-explorer-neighbourhood.feature` | City Explorer's neighbourhood result page: only facts published at that level, the postcode panel, links back (HOOD-01 to HOOD-42) | — |
| `pilot/city-explorer-part-2.feature` | City Explorer part 2: compare two councils, share and print, what changed since your last visit, and City Explorer's About the data (CITY2-01 to CITY2-72) | — |
| `pilot/area-compare.feature` | Compare two postcodes, topic by topic, never ranked (COMPARE-01 onwards; design `docs/superpowers/specs/2026-11-19-pilot-design-batch-design.md`, FE-73) | — |
| `pilot/area-share.feature` | Share a link and Recent postcodes on the area result, compare and landing (SHARE-01 onwards, RECENT-01 onwards; FE-73) | — |
| `pilot/report-a-problem.feature` | Report a problem with this fact: where it appears, the three reasons, the states and the daily count's shape (REPORT-01 onwards; FE-74; count contract `packages/fixtures/schema/problem-report-counts.schema.json`) | — |
| `pilot/energy-certificate.feature` | The page "Check an energy certificate": look up one home certificate by its number, its states, the printout (ENERGY-01 onwards; design `docs/superpowers/specs/2026-11-18-energy-certificate-design.md`) | — |
| `pilot/use-in-chatgpt-or-claude.feature` | The pilot's how-to page "Use in ChatGPT or Claude" (steps for ChatGPT and Claude, what an app sends and what is kept, 0056, 0057) and the landing's short section that links to it (HOWTO-01 to HOWTO-40); the council tools it describes are TOOLS-44 to TOOLS-63 in `pilot/area-tools.feature` | — |
| `stories/buyer.feature`, `stories/renter.feature` | The step-by-step story scripts | #69, #70 |
| `mcp-tools.feature` | The MCP tool surface for AI assistants | #117 |

The design skills' working notes in `.design/<feature>/` (decision 0031) feed these files. If they disagree, this folder wins.

## Rules
1. **Every acceptance criterion is a Gherkin `Scenario:`** whose name starts with a permanent ID, for example `Scenario: COSTS-02 missing insurance is not zero`. Keep each scenario to one observable outcome. For an error state, the cause, the reassurance and the one action (register line B22) count as one outcome.
2. **IDs:** a code for the screen or area plus a number, for example `COSTS-02`, `BUY-3.2` (buyer story, step 3, scenario 2) or `MCP-01`.
   - An ID is never reused or renumbered.
   - A scenario that is no longer needed stays in the file, tagged `@withdrawn`.
3. **Figures are cited by ID, in quotes, never typed** (AGENTS.md rule 2):
   - inputs by evidence ID from `packages/fixtures/data/`;
   - calculated values by figure ID from `packages/fixtures/generated/costs.json`;
   - area results by postcode and topic, priority or record ID from `packages/fixtures/generated/area-result.json`; the search distance from `SEARCH_LIMIT_METRES` (`packages/vestagraph-area/src/vestagraph_area/priorities.py`) shown by `vestagraph_area.distance.display_distance`.

   A value the engine does not produce is written "not calculated". Missing and partial states are named explicitly, and missing is never shown as £0 (rule 7).
4. **Required states:** each feature's description maps every required state from doc 03 §5 that applies to it to at least one scenario, for example ambiguous match, not covered, stale, partial answer or source failed.
5. **No forbidden words:** a scenario never expects the product to call a home or an area "verified", "safe" or "approved" (rule 4), and never expects a score, rating, band or verdict of our own about a place (for example "good", "best", "low risk", "clear", "n/100", "leads"). A classification published by an official source and shown with that source's name and date, such as the Environment Agency's flood risk band (FE-25), is a sourced fact and is allowed. The full word list will live in one shared file, used by the chat's output guard and by the page, report and tool-result scenarios (the pilot design review, A3, still to be written); until it exists, use this rule's examples. The output guard blocks claims, not the bare word (WCHAT-69). An AI step never calculates a figure (decision 0004).
6. **Tags decide when a scenario runs:**
   - `@ui`: browser steps, run with playwright-bdd from stage 5 (decision 0049).
   - `@mcp`: MCP server steps, run from #97.
   - No tag: data steps (fixtures and `costs.json`), run by `make check` from stage 3.

   Tags are lower case; the filter is case-sensitive. Data scenarios (no tag) need no `When`: they check data, not an action, and may have only `Then` steps when no story position applies. `@ui` and `@mcp` scenarios always have a `When`.

   Until their stage, `@ui` and `@mcp` scenarios are excluded by tag, never deleted.

   A scenario tagged both `@ui` and `@mcp` describes a behaviour with two versions (for example the area card, register line FE-15) and runs once in each suite, against that suite's version.

## Running the specifications
- `make test` (and so `make check` and CI) runs every scenario that is **not** tagged `@ui`, `@mcp` or `@withdrawn`. A scenario that cites an ID missing from `packages/fixtures/generated/costs.json` or `packages/fixtures/data/` fails with a message naming the ID.
- To run only the specifications (pytest-bdd, decision 0049 step P6; it replaced the Reqnroll runner in P8): `uv run --locked pytest packages/specs/tests -m "not ui and not mcp and not withdrawn"`. Each tag is a registered pytest marker (`pyproject.toml`; an unregistered tag fails), so `-m screen` runs one tag, and the test name starts with the scenario ID. `-k` matches substrings, case-insensitively: `-k COSTS-0` picks all three COSTS scenarios, so for exactly one use `-k "COSTS-02_"` (trailing underscore) or the full node ID, `packages/specs/tests/test_specs_scenarios.py::test_COSTS-02_missing_buildings_insurance_is_not_shown_as_zero`. The steps are in `packages/specs/tests/specs_steps.py` and `specs_support.py`. The `.feature` files are loaded from this folder in place; nothing is copied. A new tag must be added to `markers` in `pyproject.toml`.
- **Data steps** (`packages/specs/tests/specs_steps.py`):
  - `Given home "B1" is at story step 1`
  - `Then figure "<figure ID>" exists`
  - `Then figure "<figure ID>" has status "<calculated | missing | not-calculated | ...>"`
  - `Then figure "<figure ID>" shows no amount`
  - `Then the total "<figure ID>" is partial with reason "<category>"`
  - `Then figure "<figure ID>" cites evidence "<evidence ID>"` (the figure's evidence list contains it and the evidence exists)
  - `Then evidence "<evidence ID>" exists`
  - `Then area record "<record ID>" has status "<recorded | no-record-in-source | stale | source-failed | not-covered>"` (a record in `packages/fixtures/data/area.json`)
  - `Then area record "<record ID>" shows no value` (the record carries no `value`, so the screen has nothing to show as a result; rule 7)
  - `Then area result "<postcode>" has topic "<topic key>" with outcome "<found | not-known | not-covered>"` (`packages/fixtures/generated/area-result.json`; the postcode is written as in that file, e.g. `NB1 4XY`)
  - `Then area result "<postcode>" leaves topic "<topic key>" out of the coverage total` (the topic is absent from the postcode's `topics` list, because the registry marks it `counted: false`, or its outcome is `not-covered`)
  - `Then area result "<postcode>" asks the gap question for record "<record ID>"` (the glance questions include that record)
  - `Then area result "<postcode>" has priority "<priority ID>" with outcome "<meets | misses | not-known | not-known-beyond-search>"`
  - `Then area result "<postcode>" has priority "<priority ID>" with nearest record "<record ID>"`
  - `Then area result "<postcode>" has a display distance for record "<record ID>"` (the record has a distance with display text; never a typed number)
  - `Then area result "<postcode>" counts buses for stop "<record ID>" on route "<route>" at hour <8 | 12>` (an entry exists; the count is never typed)
  - `Then postcode record "<record ID>" has status "<recorded | no-record-in-source | stale | source-failed | not-covered>"` (a record in `packages/fixtures/data/postcode-area.json`; the `area record` step reads `area.json`)
  - `Then map layer "<layer ID>" has status "<recorded | no-record-in-source | stale | source-failed | not-covered>"` (a layer in `packages/fixtures/data/map-layers.json`)
  - `Then topic "<topic key>" draws map layer "<flood-zones | surface-water | listed-buildings | conservation-areas | road-noise | rail-noise>"` (the topic lists that layer kind under `mapLayers` in `packages/fixtures/data/pilot-topics.json`)
  - `Then home "<home ID>" has coverage "<covered | not-yet-covered>"`
  - `Then council "<code>" has field "<population | bands | rentSeries | priceSeries | affordabilitySeries | tenure | connectivity>" with status "<recorded | no-record-in-source | ...>"` (a council in `packages/fixtures/data/council-area.json`, cited by code)
  - `Then council "<code>" series "<rentSeries | priceSeries | affordabilitySeries>" marks a method break` (a point carries `methodBreakBefore`)
  - `Then council "<code>" at band "<A to H>" has problem "<problem>"` and `... has no rent side` (`packages/fixtures/generated/council-result.json`, `rentOrBuy.byBand`; for example `council-tax-missing`)
  - `Then council "<code>" at band "<A to H>" for product "<2-year-fixed | 5-year-fixed>" has problem "<problem>"` or `has comparison "<more | less | about-the-same>"` or `has no comparison` (the figure is never typed)
  - `Then council "<code>" caption "<rent | price | affordability | tenure | price:<detached | semiDetached | terraced | flat>>" has pattern "<pattern>"` or `has reason "<reason>"` (the generated captions' values)
  - `Then council search "<query>" has kind "<council | choose | council-for-postcode | not-covered | ...>"`, `lists council "<code>"` and `lists council "<code>" with note "<note>"` (`search` in `council-result.json`, the query as written there)
  - `Then council "<code>" neighbourhood "<LSOA code>" has fact "<connectivity | deprivation | tenure>" with status "<recorded | no-record-in-source | ...>"` or `... at level "<neighbourhood | local-authority>"` (`neighbourhoods[].facts` in `council-area.json`; neighbourhoods are cited by their LSOA code)
  - `Then council "<code>" lists neighbourhood "<LSOA code>" with label "<label>"`, `council "<code>" neighbourhood "<LSOA code>" has tenure shares` and `council "<code>" lists no neighbourhoods` (`neighbourhoods` in `council-result.json`; the shares are never typed)

  - `Then the problem report counts are kept for 90 days`, `... hold a fact count for topic "<topic key>" with record "<record ID>" and reason "<wrong | out-of-date | missing-something>"`, `... hold an area count for topic "<topic key>" with reason "<reason>" and no record ID`, `... hold a figure count for "<figure>" at level "<council | neighbourhood>" for area "<area code>"`, `no problem report count has a "<field>" field`, `every problem report count date is a day with no time` `every problem report count has one of the three fixed reasons` and `no two problem report counts share the same key` (`packages/fixtures/data/problem-report-counts.json`, FE-74; the counts are never typed)
  - `Then topic "<topic key>" is route-only and not counted` and `topic "<topic key>" opens the Vestagraph page "<route>"` (`vestagraphRoute` in `pilot-topics.json`)
  - `Then energy certificate "<sample number>" has outcome "<shown | not-domestic | not-yet-covered>"`, `... is more than 10 years old`, `... is not more than 10 years old`, `... has an inspection date`, `... has a registration date`, `... has a valid until date`, `... has no valid until date` (a replaced or cancelled certificate carries neither `validUntil` nor `moreThanTenYearsOld`, regulation 9(2)(b)), `... has status line "<superseded | cancelled | none>"`, `... shows "<propertyType | builtForm | parts | improvements>" as missing` ("Not on this certificate"), `... shows no ratings, costs, parts or improvements` and `... lists improvements in its own order with no total` (`packages/fixtures/generated/energy-certificate-result.json`; the sample number as written there; no date or amount is typed)

  `Given home ... is at story step N` accepts any step from a scenario's `fromStep` to its `toStep` (for B1, step 2 is `from-step-1`) and then requires every figure ID cited in that scenario to start with `<home>.<scenario>.`. `has status` and `shows no amount` apply to cost lines only, not totals. The wording in decision 0043's example is illustrative; this list is the contract.
  A step with no matching wording makes the scenario fail as undefined: add the step to `packages/specs/tests/specs_steps.py` (with tests), rather than rewording the scenario around it.

## Screen template
```gherkin
@screen @buying
Feature: <Screen name>
  Question it answers: "<from doc 03 §5>"
  Modes: buying | renting | both
  Fixtures: <home IDs>; inputs: <evidence IDs>; figures: <figure IDs>
  Required states (doc 03 §5):
    <state> -> <CODE>-NN

  Scenario: <CODE>-01 <short title>
    Given <starting state: story, step, home>
    When <action or screen opening>
    Then <one observable outcome, citing IDs in quotes>

  # Simulated or paid boundaries (labelled) and anything "not calculated" go in scenarios too.
```

## Story template
```gherkin
@story @buying
Feature: Buyer story

  Rule: Step 1 — <title> (snapshot step 1)

    Scenario: BUY-1.1 <short title>
      Given …
      When …
      Then …
```

## Work breakdown
Specifications become build tickets **one story step at a time**: each ticket makes one story step work end to end across the screens it touches (register line SP-02). The stage 5 story items #87 and #88 are epics, split into these step tickets at #71.
