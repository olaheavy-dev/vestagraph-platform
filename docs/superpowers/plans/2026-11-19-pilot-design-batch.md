# Pilot design batch: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the design gaps that failed round 1 of the pilot gate (PD-21, FE-71, FE-72): boards and specifications for Compare two postcodes, Share a link, Recent postcodes, Report a problem, the How it works, Privacy and Accessibility pages, the area card inside the signed-in chat and the phone neighbourhoods map sheet, plus the audit's tidy-ups.

**Architecture:** Four pull requests (founder, 19 Nov 2026: "Three by area (Recommended)", after this one). PR 0 (this plan's own) records the design, the plan and the register lines. PR 1 adds the one new data contract (the Report a problem daily count, a JSON Schema with a sample file the validator checks) and the area result features' specifications and boards. PR 2 adds the public pages. PR 3 adds the in-chat card, the map sheet, canvas tidy-ups, the extras' scenarios and the audit's small items. Each feature pull request carries its specifications and its canvas boards together; boards and scenarios quote existing sample data only.

**Tech Stack:** Gherkin specifications run by pytest-bdd (data scenarios; `@ui` scenarios are deselected until the frontend exists), JSON Schema 2020-12 with the Python fixture validator, the design canvas (https://claude.ai/artifact/MpvQNDVYCePp4iWM3j3Jx4). No new packages.

**Spec:** `docs/superpowers/specs/2026-11-19-pilot-design-batch-design.md` (approved 19 Nov 2026).

## Global Constraints
- No code changes except the PR 1 schema, its sample file and their fixture tests; no generator change (design, "Sample data"). A state with no sample record keeps its scenario with a `# fixture needed: #NNN` note and a `noticed` issue.
- Every figure and line on a board or in a scenario is quoted from the sample data or generated files (`area-result.json`, `council-result.json`), or is wording from the design or an approved specification (rule 2).
- Compare is never sorted, ranked, totalled, coloured better or worse, and never shows a worked-out difference (rule 4).
- Postcodes and priority limits never in a query string, a log, an error report or analytics; a shared link carries postcodes after the `#` only, never limits (0014, 0053, PRIO-16).
- Nothing stored on the device until the visitor turns it on: "Remember postcodes on this device" is its own setting; the "Reported" marker lives in page memory only (PECR, 0014).
- Report a problem: fixed reasons "Wrong", "Out of date", "Missing something"; no free text; daily counts only, three shapes (design §4), kept 90 days, internal only. On the area result, compare, City Explorer's council and neighbourhood pages and council compare; not on the energy page, the chat's area card or compare table, or the ChatGPT and Claude widget; the signed-in chat's side panel shows the full area result, so its topic details get the link (agent's call, pre-push review, open to the founder).
- Privacy and Accessibility pages: legal parts read "To be written before launch (SE-02)"; contact reads "Contact details to be added before launch"; Accessibility says the site has not been tested yet and never claims conformance (rule 1).
- Missing is never zero, blank or clean; one side's gap reads the record's own gap line, "Not known right now" when a source is down, or "Not yet covered" ("Unavailable" is withdrawn; rule 7). England only: "not yet covered" for other nations (rule 6).
- Boards: pilot style (FE-29 to FE-33, FE-42), light first then dark twins (FE-31's slate ink; printouts have no dark twin), phone 390 px and desktop 1440 px, 44 px targets, "Sample data" on each board.
- Scenario wording is proposed until the founder's copy review; specifications cite the canvas version they were checked against.
- Test names `test_<method>_<condition>_<result>` (0039). Commit prefixes `docs:` or `test:`; no agent attribution.
- Canvas publishing: a subagent's publish can be refused ("not the latest version") or blocked; read the whole artifact first, and if blocked, ask the founder before the main session publishes (lesson of 19 Nov 2026).

## Review Focus
1. **A postcode in a shared compare link with spaces, lower case or one invalid side:** opening it runs both searches as typed would, and an invalid side shows the search's own error on that side only; Task 2's COMPARE scenarios pin it.
2. **The same postcode on both sides:** compare works and says nothing odd (no "identical" verdict); Task 2 adds a scenario.
3. **Report a problem on a sold-price or planning fact (any fact whose record points to one address or property):** the count carries no record ID; Task 1's schema rejection test pins it.
4. **Browser storage blocked while turning on Recent postcodes:** the setting says it can't be turned on here and the search still works; Task 2's RECENT scenario pins it.
5. **A privacy or accessibility placeholder drawn so it reads like finished text:** the board shows each placeholder in the placeholder style; Task 6's PUBLIC scenarios assert the exact placeholder lines.

---

## PR 0: design and plan

### Task 0: Records and pull request

**Files:**
- Already written: `docs/superpowers/specs/2026-11-19-pilot-design-batch-design.md`, this plan.
- Modify: `docs/decisions/README.md` (new lines FE-73, FE-74, SE-07; dated notes on FE-05 and PD-21), `docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md` (dated note on goal 7: the reason choices, the in-memory "Reported", City Explorer), `docs/product/05-ideas-and-product-thinking.md` (a compare printout as a later idea), `docs/planning/status.md` (item 6(b): design and plan done, PR 1 next).

- [ ] **Step 1:** Write FE-73 (compare topic by topic, with the agent's calls), FE-74 (Report a problem with a reason, where it appears, the three count shapes, internal only; amends goal 7 and FE-05), SE-07 (Privacy drawn with placeholders until SE-02), each quoting the founder's prompt-window answer.
- [ ] **Step 2:** Pre-flight: grep for "Report a problem", "Share a link", "Recent postcodes", "Compare two postcodes", "how-it-works", "accessibility statement", "PD-21", "FE-05" and fix anything the design makes stale.
- [ ] **Step 3:** `make check`. Expected: all steps pass.
- [ ] **Step 4:** Commit `docs: pilot design batch design, plan and register lines`; documentation only, so a fresh-context Opus review (Code Review Rules); push; open the PR (`pr` skill); `@codex review`.

## PR 1: area result features (Compare, Share, Recent postcodes, Report a problem)

### Task 1: Report a problem count contract

**Files:**
- Create: `packages/fixtures/schema/problem-report-counts.schema.json`, `packages/fixtures/data/problem-report-counts.json`
- Test: `packages/vestagraph-fixture-validator/tests/test_fixtures_problem_report_counts_schema_rejection.py`

**Interfaces:**
- Produces: a document `{ "retentionDays": 90, "counts": [ ... ] }`; each count is one of three shapes, all with `date` (`YYYY-MM-DD`), `source`, `reason` (`"wrong" | "out-of-date" | "missing-something"`), `count` (integer ≥ 1), `additionalProperties: false`:
  - `fact`: `topic`, `factRecordId`, `localAuthority` (a council code);
  - `area`: `topic`, `localAuthority`, no `factRecordId` (required for any fact whose record points to one address or property, today topics `sold-nearby` and `planning-nearby`, and for gaps);
  - `councilFigure`: `figure`, `areaCode`, `areaLevel` (`"council" | "neighbourhood"`).
  Topic keys and council codes come from `pilot-topics.json` and `council-area.json`. The sample has at least one record of each shape for the NB1 4XY area and council E06999001.

- [ ] **Step 1: Write the failing tests**, each starting from the real sample and breaking one thing:
  `test_validate_instance_problem_report_counts_real_file_is_accepted` (no problems);
  `..._postcode_field_is_rejected` (add `"postcode": "NB1 4XY"`, mentions `postcode`);
  `..._time_field_is_rejected` (add `"time": "09:40"`);
  `..._unknown_reason_is_rejected` (`"reason": "offensive"`);
  `..._free_text_is_rejected` (add `"comment": "x"`);
  `..._sold_prices_with_record_id_is_rejected` (topic `sold-nearby` with `factRecordId`, mentions `factRecordId`);
  `..._planning_with_record_id_is_rejected` (topic `planning-nearby`);
  `test_validate_instance_problem_report_counts_banned_topics_exist_in_registry` (each topic in the schema's no-record-ID list is a key in `pilot-topics.json`, so a renamed topic cannot silently reopen the ban);
  `..._zero_count_is_rejected` (`"count": 0`);
  `..._date_with_time_is_rejected` (`"date": "2026-11-19T09:40"`);
  `..._retention_not_90_is_rejected` (`"retentionDays": 365`).
- [ ] **Step 2:** `uv run pytest packages/vestagraph-fixture-validator/tests/test_fixtures_problem_report_counts_schema_rejection.py -v`. Expected: FAIL (schema not found).
- [ ] **Step 3:** Write the schema (`retentionDays` `const: 90`; the record-ID ban as `if topic in [sold-nearby, planning-nearby] then not required factRecordId`, with the `area` shape) and the sample file.
- [ ] **Step 4:** Run the tests, then `make validate`. Expected: PASS.
- [ ] **Step 5:** Commit `test: Report a problem daily count contract (FE-74)`.

### Task 2: Specifications

**Files:**
- Create: `docs/specs/pilot/area-compare.feature` (COMPARE-01 onwards), `docs/specs/pilot/area-share.feature` (SHARE-01 onwards, RECENT-01 onwards), `docs/specs/pilot/report-a-problem.feature` (REPORT-01 onwards)
- Modify: `docs/specs/screens/01-landing.feature` (Recent postcodes under the search box, LAND-22 onwards), `docs/specs/pilot/area-topics.feature` (a pointer from the topic detail to REPORT), `docs/specs/pilot/city-explorer.feature` and `city-explorer-neighbourhood.feature` (pointers to REPORT for council and neighbourhood facts), `packages/specs/tests/specs_steps.py` (data steps for the REPORT shape scenarios, reading the Task 1 sample)
- Test: the feature files themselves through `make test`

**Interfaces:**
- Consumes: Task 1's sample file; `area-result.json` (NB1 4XY, NB7 1RR); `council-result.json`.
- Produces: scenario IDs the boards in Task 3 map to (each feature's "Required states" header lists state → scenario).

- [ ] **Step 1:** `area-compare.feature`: a "Required states" header for every compare state in the design (empty second postcode, invalid, not England, unknown, source down on one side, topic missing on one side, offline, swapped, same postcode twice, priorities set and not set, shared link) and scenarios for: the way in from the result with this postcode first; At a glance quoted for each; every topic in the result's order with both summary lines quoted from `area-result.json` for NB1 4XY and NB7 1RR; tap opens both details with their own stamps; never sorted, ranked, totalled or a difference (one scenario checks no "more", "fewer", "better", "worse" or number difference appears); Swap; "Share this comparison" carries both postcodes after the `#` and never limits; postcodes never in a query string or log; keyboard, 44 px, no sideways scroll, dark twin. UI scenarios `@ui`.
- [ ] **Step 2:** `area-share.feature`: SHARE (share sheet on phone, "Link copied" on desktop, copy failed with the link shown and selected, only the postcode after the `#`, opening a shared link searches as typed); RECENT (off by default with "Remember postcodes on this device" and "Turn on"; on with up to 5 newest first; checked, compared and shared-link postcodes added; Clear; Turn off deletes list and setting; storage unavailable; never sent to the server; separate from "Remember councils on this device").
- [ ] **Step 3:** `report-a-problem.feature`: where it appears (topic detail, compare detail, council facts, neighbourhood facts, council compare) and where it does not (summary lines, energy page, chat card and compare table, widget; the chat's side panel does get it); the three reasons and Cancel; sent ("Reported" until the page closes, nothing stored on the device); failed, offline, rate-limited (same wording as failed); gaps reportable; data scenarios quoting the Task 1 sample for each count shape, the sold-price and planning rule, no postcode, no time, 90 days.
- [ ] **Step 4:** Landing and pointer edits; data steps; open a `noticed` issue for each state with no sample record (for example a source identifier for a fact count, #349) and cite it in the header.
- [ ] **Step 5:** `make test`. Expected: PASS (`@ui` deselected; data scenarios pass).
- [ ] **Step 6:** Commit `docs: compare, share, recent postcodes and report a problem specifications`.

### Task 3: Canvas boards for PR 1

**Files:** the design canvas, page "Pilot · public area check", a new section "Pilot 8 · Compare, share, report" below the energy section; "Pilot · City Explorer" for the council Report a problem state; generator scripts in the session scratchpad.

- [x] **Step 1:** Read the canvas's current version and the Brand and style boards; keep FE-29 to FE-33 and FE-31's dark.
- [x] **Step 2:** Draw, light first: `ComparePhone`, `CompareDesktop` (NB1 4XY with NB7 1RR; At a glance, priorities, jump list, rows, an open row's two details); `CompareStates` (each state in Task 2's header); `ShareStates` (share sheet, copied, copy failed); `RecentPostcodes` (off, on with entries, empty, storage unavailable, on landing and result); `ReportProblem` (link on a fact, the three reasons, sent, failed, offline) on an area topic detail and on a council fact. Every line quoted from the sample data or Task 2's scenarios.
- [x] **Step 3:** Dark twins of every board.
- [x] **Step 4:** Visual review in Chrome at 390 and 1440 px (`visual-reviewer`) and the competitor benchmark checklist; fix; re-check; record the canvas version.
- [x] **Step 5:** Update Task 2's headers with the board names and canvas version; write "As drawn" under this task.

**As drawn (19 Nov 2026), Task 3 (first draw; the review fixes are in the note after it):** on the page "Pilot · public area check" a new section "Pilot 8 · Compare, share, report" sits below the energy section (title note at y 39600, light boards from y 39900, dark twins in a row from y 44881). Boards: `ComparePhone` (900 wide: the 390 px page with no priorities set and the jump list closed, and the open Schools sheet with both details), `CompareDesktop` (1440, priorities set, jump chips, rows table and the Schools panel), `CompareStates` (fifteen phone-width cards covering every state in the specification header), `ShareStates` (six cards: header with Share and Compare, share sheet, copied, copy failed, shared links), `RecentPostcodes` (eight cards: landing off, consent text, on empty, on with postcodes, cleared, storage unavailable, result off and on), `ReportProblem` (eight phone cards and three desktop panels) and the dark twin of each; on "Pilot · City Explorer" a new section "City Explorer 4" holds `CouncilReportProblem` and its dark twin (five cards, including council compare). Every line is quoted from `area-result.json`, `postcode-area.json`, `council-result.json` or the specifications; counts, outcomes and priorities come from `area-result.json`. Canvas version after the publish: `1795107206-3e0d` (before: `1795105581-020c`). Visual check: frames were measured in headless Chrome at their widths (content height + 32 px) and the published canvas was viewed in Chrome with no overlap or clipping; fixes made before publishing: the reasons group heading no longer wraps over its border, the phone share sheet no longer overlaps its note, the flood row no longer nests a link inside a link, and the scrim label was removed. Agent's calls (open to the founder): no "Questions to ask" tile on compare's At a glance (the specification lists found, not known and coverage only); the Everyday places and Planning lines for NB7 1RR are built from its records (the planning description is test text and is not shown on the row); "ZZ1 0AA" is the Wales stand-in of the area states board; the Share and Compare controls are drawn in `ShareStates` but not yet added to the `AreaResult` boards. Recent postcodes shows two entries because only two sample postcodes exist.

**Task 3 review fixes (19 Nov 2026, canvas `1795107206-3e0d`):** every compare At a glance has the "Questions to ask" tile (counts from `area-result.json`; COMPARE-09 amended); rows carry the result's gap lines, "Not known right now" sentences and area lines (COMPARE-13 amended); Recent postcodes on the result lists the checked postcode first; the source-down card keeps registry order; Swap, offline colour, reasons heading, one Schools anatomy (every fact its own link and stamp, admissions its own fact), council failed and offline (split), the loading line and card 15's height are fixed; a rate-limit card and COMPARE-39 were added; desktop cards were added for Share, Recent postcodes and the failed and offline report panels (the `AreaResult` boards are still unchanged); dark info notices use the canvas's existing pair. The dark row moved down to y 45609 because `ComparePhone` grew. NB7 1RR's Planning line is marked as the agent's call and fixture issue #348 is open.

### Task 4: Records and pull request 1

**Files:** `.design/prototype/INFORMATION_ARCHITECTURE.md` (compare route, Share and Recent postcodes on the result and landing, Report a problem on details), `docs/planning/status.md`.

- [ ] **Step 1:** Record changes; pre-flight grep for the terms in Task 0 step 2 plus "COMPARE-", "REPORT-", "Remember postcodes".
- [ ] **Step 2:** Map each design requirement and state to its scenario or test in the PR description; `make check`; fresh-context review (Code Review Rules, `code-security-reviewer`, `visual-reviewer`); fix findings.
- [ ] **Step 3:** Push, open the PR with the copy-review list (every proposed line), `@codex review`.

## PR 2: public pages

### Task 5: Public pages specification

**Files:**
- Create: `docs/specs/pilot/public-pages.feature` (HOW-01, PRIV-01, A11Y-01 onwards)
- Modify: `docs/specs/screens/01-landing.feature` (footer and "How it works" line point to the pages; check LAND-20)

- [ ] **Step 1:** HOW: the seven sections in the design's order; links to About the data, Use in ChatGPT or Claude, Report a problem; no verdict words. PRIV: each section named in the design, with the decided facts quoted from their records (0014, 0053, 0056, 0057, 0058, DA-09, FE-11) and each legal part reading exactly "To be written before launch (SE-02)"; contact reads "Contact details to be added before launch". A11Y: target WCAG 2.2 level AA; "not been tested yet"; results placeholder "To be completed after testing, before launch"; never claims conformance. All three: footer links, keyboard, 44 px, dark twin. `@ui`.
- [ ] **Step 2:** `make test`. Expected: PASS.
- [ ] **Step 3:** Commit `docs: how it works, privacy and accessibility page specifications`.

### Task 6: Public pages boards and pull request 2

**Files:** the canvas, page "Pilot · public area check", section "Pilot 9 · Public pages"; `.design/prototype/INFORMATION_ARCHITECTURE.md`; `docs/planning/status.md`.

- [x] **Step 1:** Draw `HowItWorks`, `Privacy`, `Accessibility`, phone and desktop, light then dark; placeholders in one visible placeholder style (never body text style); any illustration recorded in `docs/assets/README.md`.
- [x] **Step 2:** Visual review and benchmark checklist; record the canvas version; update the feature header and "As drawn".
- [ ] **Step 3:** Records, pre-flight, `make check`, fresh-context review, push, PR with copy-review list, `@codex review`. (Records and `make check` done in Task 6; the controller runs the review and the push.)

**As drawn (19 Nov 2026), Task 6:** on "Pilot · public area check" a new section "Pilot 9 · Public pages" sits below Pilot 8 (title note at y 51500, light boards from y 51800, dark twins from y 57776). Boards, left to right: `HowItWorksPhone` (390), `HowItWorks` (1440), `PrivacyPhone`, `Privacy`, `AccessibilityPhone`, `Accessibility`, and a Dark twin of each (12 boards; desktop boards are fluid pages). Each page has the site header, "← Back to Vestagraph", one level-1 heading, the section headings as level-2 headings, and the footer with the five links of HOWTO-31. Wording is quoted from `public-pages.feature`; the words around the facts are proposed. Placeholders use one style (a dashed, hatched slate box with a "Placeholder" label in small monospace, its exact text in monospace; dark: #1A2329 with #93B8CE), never body text; the PRIV-11 draft line uses the same box with a "Draft" label. No illustration is drawn, so `docs/assets/README.md` is unchanged. Canvas version after the publish: 421, version id `1795110030-aefc` (before: `1795109806-b696`); after the pre-push review fixes: 422, `1795110762-a77a` (see the note below). The Privacy boards include the "Maps" section (PRIV-18). Visual check: all twelve boards were rendered in headless Chrome at 390 and 1440 and measured by script: no horizontal scroll, no element past the page edge, every link and button at least 44 px tall, every text pair at WCAG AA contrast (4.5:1, or 3:1 for large text); screenshots of the Privacy phone and desktop boards were read for overlap and clipping. The published canvas itself was not opened in a browser. Agent's calls (open to the founder): one placeholder box covers each group the specification lists in one sentence (for example the bot check's lawful basis, retention and PECR position); "Links to other sites" names only Google Maps because no record names other recipients; the Accessibility headings ("Our aim", "Where we are", "Test results and known issues", "Report an accessibility problem") are proposed, the specification fixes none; the link rows are standalone lines so each reaches 44 px; the landing boards' footer still reads "Privacy" where HOWTO-31 and LAND-25 say "Privacy notice", and those boards are not changed here (changed after review, see the next note).

**Review fixes (19 Nov 2026), canvas version 422 (`1795110762-a77a`):** the four Landing boards now read "Privacy notice" in the footer, add "Use in ChatGPT or Claude" to it (HOWTO-31) and end the How it works section with "More on how it works" (LAND-25, LAND-26); their frames grew by 76 px (desktop) and 60 px (phone) so nothing is clipped. The Privacy boards gain a "Hosting and security" placeholder section (PRIV-19), the full-list placeholder under "Links to other sites", per-section lawful-basis and retention placeholders, Cloudflare and OpenFreeMap's stated log practice under "Maps", per-client rate-limit wording and "never stored or logged" for remembered limits; the dark twins' body text is #E6E8EA; the Accessibility lead line and the w3.org link are reworded. Re-rendered in headless Chrome at 390 and 1440: no overflow, targets at least 44 px on the new pages, AA contrast. `area-priorities.feature` PRIO-15's consent text is not yet on the priorities boards (they wait for the founder's copy review).

## PR 3: in-chat card, map sheet, tidy-ups

### Task 7: In-chat area card and phone map sheet boards

**Files:** the canvas, "Pilot · Signed-in chat" (FE-71) and "Pilot · City Explorer" (FE-72); `docs/specs/pilot/area-card.feature` and `docs/specs/pilot/city-explorer-neighbourhood.feature` headers (board names, canvas version).

- [x] **Step 1:** Draw the in-chat card: compact card with Expand, the expanded dialog, the phone preview with "Open map"; phone and desktop, light and dark; matching CARD-02, 23, 27, 28, 31, 36 to 42. Update canvas note `s12`.
- [x] **Step 2:** Draw the phone neighbourhoods map sheet (map, list and panel in a sheet at 390 px, FE-43), light and dark.
- [x] **Step 3:** Draw Share and Compare in the AreaResult boards' header (light and dark, phone and desktop), as ShareStates draws them (Task 3 review). Canvas tidy-ups: remove the "AI error (CHAT-19 to CHAT-24, CHAT-53)" frame on AreaStatesPilot and its Dark twin; delete the pass B Nearby, NearbySchools and their Dark twins; redraw "Check" as "Search" on the desktop council boards and remove the old placeholder (#317).
- [x] **Step 3b:** Draw the "Show map" state (FE-75, MAP-28 to MAP-30) on the area result's map areas and on the City Explorer council and neighbourhood boards (CITY-113, HOOD-43), light and dark, phone and desktop. Redraw HOOD-27's board line as "Map drawing is a placeholder for the street map (OpenFreeMap tiles). It is not coloured by any figure." and update the quoted line in HOOD-27 then.
- [x] **Step 4 (records; the separate visual review follows):** Visual review; record the canvas version; update the headers; edit #303 (item 1 done), #318 (the other items as build-ticket criteria, including the desktop "Check"), #317.

**As drawn (19 Nov 2026), Task 7:** canvas version 424, version id `1795111932-7bf7` (before: 423, `1795110991-c508`). On "Pilot · Signed-in chat" a new section "Signed-in chat 9 · The area card in the chat" (title note at y 24800, boards from y 25100, dark twins 8000 px to the right): `SignedInChatAreaCard` (desktop 1440: the compact card with Expand inside an answer, and the expanded dialog over the chat dimmed behind a scrim; CARD-02, 23, 27, 28) and `SignedInChatAreaCardPhone` (four phone cards: the preview with the strip, "Nearest 10 places · up to 900 m", "Closest: Mill Court bus stop, 120 m" and "Open map" with every place listed below; the full-screen view; Close with focus back on "Open map"; what a screen reader reads; CARD-31, 36 to 42). The card, dialog and full-screen view are the widget boards' own drawings lifted in, so the two versions draw the same places (CARD-02). On "Pilot · City Explorer" a new section "City Explorer 5" (y 22300): `NeighbourhoodsMapSheet` (phone sheet at 390: Show map, the map with the list, a neighbourhood chosen with its panel; FE-43, FE-72; CITY-25, 87 to 90) and `CityShowMap` (council page, neighbourhood page desktop and phone in the Show map state; CITY-113, HOOD-43), each with a Dark twin. On "Pilot · public area check" a new section "Pilot 10 · Show map on the area result" (y 66000): `AreaShowMap` (desktop and phone; MAP-28 to MAP-30), with a Dark twin below. Share and Compare with another postcode are now in the header of AreaResult, AreaResultDesktop and their Dark twins, as ShareStates draws them (the phone frame grew 60 px). Tidy-ups: the "AI error (CHAT-19 to CHAT-24, CHAT-53)" frame is removed from AreaStatesPilot and its Dark twin (frame 544 px shorter); Nearby, NearbySchools and their Dark twins are deleted (and the title note "Pilot 3 · Nearby topics"); on CouncilPage and CouncilPageDesktop (and Dark twins) the button reads "Search" and the placeholder "Enter a postcode" (FE-70, FE-37; #317); the map lines on NeighbourhoodPage, NeighbourhoodPageDesktop and CouncilPageDesktop (and Dark twins) read "Map drawing is a placeholder for the street map (OpenFreeMap tiles)." (HOOD-27 quote updated). The neighbourhood boards keep "Check" because HOOD-05 quotes it. Note s12 and s3 updated. Visual check: each new board was rendered in headless Chrome at its width (1520, 1760, 1330, 2470, 1510): no text past the page edge, no low-contrast text pairs by script, every control I drew at least 44 px tall (the only shorter targets are the existing source stamps and the inline "Privacy notice" link inside the lifted chat chrome); screenshots of the desktop and phone chat boards (light and dark), the map sheet, Show map and the AreaResult headers were read for overlap and clipping. The published canvas itself was not opened in a browser. Agent's calls (open to the founder): the Show map line "Loading the map asks OpenFreeMap for map tiles. Nothing is requested until you choose." is proposed; "Show map" is drawn in new states boards, not on the existing loaded-map boards; the phone result page has no map area, so the phone Show map card is the result with the map first and the places below; the "Closest: ..." sentence is proposed; the one-place preview is described, not drawn, because no sample result has one place; "Enter a postcode" follows FE-37's postcode placeholder for the council page's postcode-only box; the Compare button is full width on the phone and beside Share on desktop.

**Review fixes (19 Nov 2026), canvas version 426 (`1795112769-63d0`; the canvas was at `1795112207-256e` when I started, from a later publish of the public pages, and I built on it):** `AreaShowMap` (+Dark) is redrawn on the real layouts: the area result's desktop map column with its filter chips and legend (the chips stay usable while the map is hidden and apply when it loads: agent's call), the phone Map screen (`MapPhone`) and a topic panel's Map section; the result page on a phone has no map, so no map area is added there; the list keeps its quoted heading "Places on the map, nearest first". The phone card in the chat now offers "Open map" and "Open full result" (founder, "Both buttons", FE-78, CARD-48). The preview strip scales to its box so "Postcode centre" is whole, and the full-screen zoom buttons moved to the bottom right so the callout no longer meets "+". The NeighbourhoodPage boards (+Dark) read "Search" (founder, "'Search' everywhere", FE-70 amended, HOOD-05). CouncilStates' last note now says the neighbourhood fact wording is still to be drawn (HOOD-14, HOOD-38). Notes pguide, s12, pilot10 and chat_guide4 corrected. FE-50 is founder-confirmed (light only); the radon label is approved (DA-31, area-topics.feature); FE-70 and CITY-05's comment no longer say the board draws "Check"; CITY-25's title says Neighbourhoods is drawn. #303 comment corrected (item 3 desktop and item 2 remain); #318 commented; `noticed` issue #352 lists the About the data and Display settings desktop boards. Re-rendered in headless Chrome: no overflow, no low-contrast pairs by script, my controls at least 44 px. Not opened in a browser.

### Task 8: Extras' scenarios and the audit's small items

**Files:** `docs/specs/pilot/area-topics.feature`, `docs/specs/pilot/area-tools.feature`, `docs/specs/pilot/city-explorer.feature`, `docs/specs/pilot/city-explorer-neighbourhood.feature`, `docs/specs/pilot/city-explorer-part-2.feature`, `docs/specs/screens/14-check-an-area.feature`, `docs/specs/pilot/workspace-chat.feature`, `.design/prototype/INFORMATION_ARCHITECTURE.md`, `docs/decisions/README.md`, `packages/specs/tests/specs_steps.py`

- [x] **Step 1:** Audit P2-1: one data and one `@ui` scenario per extra in `area-topics.feature`, quoting `area-result.json`: buses as routes per stop at 8am and midday, never a stop total (DA-18); school demand as past-year facts, never a chance of a place; green space as the voluntary standard for the neighbourhood around the postcode (changed 19 Nov 2026 after the PR 3 review, DA-16); flood by postcode as published, no single verdict (DA-16); council tax by band "may include parish charges"; air quality and connectivity never combined (0054). A missing sample value gets a `noticed` issue.
- [x] **Step 2:** Audit P2-10, P2-12, P2-13 and the P3 list as the design names them; P2-11 (shared council comparison's address) and P2-14 (compare list for a council with nothing recorded) are asked in one prompt window with the audit's suggested defaults first, then recorded as register lines with the founder's words. Edit #302's body (P2-15); comment on #99 and #102.
- [x] **Step 3:** `make test`. Expected: PASS.
- [x] **Step 4:** Commit `docs: extras scenarios and pilot gate audit small items`.

**As built (19 Nov 2026), Task 8:** TOPIC-43 to TOPIC-54 (the six extras), TOOLS-67 to TOOLS-72, WCHAT-111, FE-76 and FE-77; the pre-push review's fixes followed (green space for the neighbourhood, DA-16).

### Task 9: Records and pull request 3

- [x] **Step 1:** `docs/planning/status.md`: the design batch done, next the AI-03 brainstorm, then gate round 2; pre-flight grep for FE-71, FE-72, #303, #317, #318, "AI error", "NearbySchools".
- [ ] **Step 2:** Map criteria to scenarios; `make check`; fresh-context review with `visual-reviewer`; fix findings.
- [ ] **Step 3:** Push, PR with copy-review list, `@codex review`.
