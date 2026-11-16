# Benchmark Design Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the design gaps the 16 Nov 2026 benchmark found, so that the pilot is "way better" than the competitor before the pilot gate (0052), not only more honest.

**Architecture:** Canvas work only, with no product code. The steps are:
- the quick fixes, done the same day;
- a research note on the data gaps, which decides the topics and map overlays;
- redraws of the three weakest screens (the desktop result, the printout and the map style);
- "check this" rows for the gaps we can't fill yet;
- the founder's review, then dark versions and a PR recording the boards.

Specifications for changed screens follow in the pilot specification files, in the same PR or PR C's.

**Tech Stack:** the design canvas (https://claude.ai/artifact/MpvQNDVYCePp4iWM3j3Jx4), and the generator scripts kept in the session scratchpad.

**Spec:** [`docs/reviews/2026-11-16-design-benchmark.md`](../../reviews/2026-11-16-design-benchmark.md) (the benchmark and the founder's decision). Also the competitor benchmark checklist in [`2026-11-13-competitor-report-comparison.md`](../../reviews/2026-11-13-competitor-report-comparison.md); decisions 0046, 0051, 0052, 0054, 0055 and 0058; and register lines FE-21 (the report), FE-25, FE-27, FE-33, FE-34, FE-46 and AI-12.

## Global Constraints
- **Figures:** rules 1, 2, 4 and 7 apply: no invented facts, no figure typed by hand, no verdicts or scores, and missing data is never zero.
- **Data:** a topic or overlay is drawn with data only after the research note shows its licence allows public, per-postcode use. Otherwise it is a "check this" row that links to the official service.
- **Competitor evidence:** the evidence is used for comparison only. Never copy its layout, wording, colours or images (decision 0045's pattern-only rule, as in doc 05). No competitor name in any tracked file.
- **Boards:** light first, then slate-ink dark (FE-31); 390 and 1440 px; source stamps (FE-33); one "How we got this" per page (FE-34); 44 px targets; the Feedback kit's components; "Sample data: a made-up town" (FE-46).
- **The bar:** each redrawn screen is checked against the benchmark checklist and the 16 Nov benchmark's table, aiming for "better" on every row it touches.
- No agent attribution.

## Review Focus
1. **A striking desktop header** must not reintroduce a score or verdict. Big figures are published facts with their level and source.
2. **The printout lists every topic in `pilot-topics.json` (21 now, 16 counted; was 15, DA-31, 16 Nov 2026),** including missing ones as "Not known" pages, never dropped silently.
3. **The real basemap** keeps a list view as its accessible equivalent, and its attribution text follows the tile licence.
4. **A "check this" row** never implies we checked anything ("we haven't checked this; here is the official service").

---

### Task 1: Quick fixes (done 16 Nov 2026)
- [x] Remove decision and register IDs from user-facing text.
- [x] Reword the landing headline (approved, FE-67). It is proposed wording for the founder to approve.
- [x] Make "(synthetic)" and "(sample)" consistent in user text.
- [x] Hide "Explanation not yet available" until AI-12's texts exist.

### Task 2: Research note on the data gaps
- [x] Commit the research note as `docs/reviews/2026-11-16-data-gaps-research.md`. It covers surface-water and future flood risk with outlines, radon, coal mining, road and rail noise, mobile coverage, postcode rents, planning constraints and a free basemap. For each it gives the licence, resolution, access method and cost, and a recommendation: add, check row, or not now.
- [x] The founder decided each topic in prompt windows (16 Nov 2026): register lines DA-22 to DA-29 and FE-67 (headline). Basemap: OpenStreetMap, self-hosted (DA-25).

### Task 3: Desktop result redraw (AreaResultDesktop)
- [x] Add a place header with the map: the postcode, the area name and its level, and the sample note.
- [x] Show At a glance as a row of big figures with level and source, replacing the 3+1 grid.
- [x] Use the right column under the map (for example questions to ask and check in person, FE-39), and add a jump row to the topics.
- [x] Acceptance: no score or verdict; every big figure is quoted from `area-result.json` with its stamp.

**As drawn (16 Nov 2026), Task 3:** `AreaResultDesktop` now has a place header with the map (postcode, area name and level, the sample note), At a glance as a row of facts each with its level and source (no big figures, no score or verdict) plus a compact line of found, not known and questions counts quoted from `area-result.json`, a jump row to the topics, and the right column under the map for Check in person and Places. On the desktop result an opened topic replaces that right column, which returns when it closes, and the map stays in the header (a note on FE-26). Its map follows FE-42's rings (see Task 5). A dark twin was drawn in Task 7. Specifications for the changed screens follow in their own PR.

### Task 4: Printout redraw (AreaExport, FE-21)
- [x] Add a cover: postcode, date, and the sample or data date.
- [x] Put At a glance on page 1.
- [x] Include every topic in `pilot-topics.json` (21, of which 16 counted; was 15 before DA-31, 16 Nov 2026), with missing ones shown as "Not known".
- [x] Add questions to ask and check in person.
- [x] Add a sources page with each source's date and status (FE-33 printout rule).
- [x] Use greyscale-safe charts and readable type sizes (12 pt or more in print).

**As drawn (16 Nov 2026), Task 4:** `AreaExport` is now 22 pages: a cover with a map, At a glance on page 1, every topic in `pilot-topics.json` (21 now, not the 15 the benchmark counted: ruling that the printout lists every topic, none dropped silently, missing ones as "Not known", with an NB7 1RR specimen), questions to ask, check in person, a sources page with dates only (FE-33, founder 14 Nov: "Dates only, no notes"), no arrows on printed stamps, type of 12 pt or more, and greyscale-safe charts. The Check this rows and the new topics (Task 6b) are on it too. The cover map's numbered badges sit beside the pins after the founder's screenshot feedback. Specifications for the changed screens follow in their own PR.

### Task 5: Basemap style (MapDesktop, MapPhone)
- [x] Following the research note's basemap choice: draw the real map style in light and dark, with its attribution, the list view as the accessible equivalent, and slots for flood and planning overlays where Task 2 allows.

**As drawn (16 Nov 2026), Task 5:** the founder chose to keep FE-42's 3D as the default and add a flat OpenStreetMap-style street map, so this task became FE-68: `MapPhone` and `MapDesktop` keep the 3D style, and new boards `MapPhone2D` and `MapDesktop2D` (plus their dark twins) show the flat map, with "© OpenStreetMap contributors" and the list view as the accessible equivalent. The tiles are drawn as inline SVG, because the canvas cannot load live tiles. All maps, including the desktop result's, now follow FE-42: zoom to fit the places, rings at 500 m and 1 mile, the 3.1 miles search limit in text; the three missing places and AMENITY-10 were added, pins sit at their recorded distances, and numbered badges sit beside the pins. Overlay layers (flood outlines, listed buildings and conservation areas, noise) are switches drawn from `map-layers.json`; the founder had the sample outlines moved clear of the postcode centre (#310), and the boards were redrawn from the moved outlines.

### Task 6a: Sample data for the new topics (before any board shows their figures)
Added after Codex's review of #306 (rule 2: a figure on a board is quoted from the data files, never typed).
- [x] (Built 16 Nov 2026, DA-31, branch feat/design-pass-topic-data) For each topic marked "add" (DA-22 flood outlines, DA-23 radon band, DA-24 listed buildings and conservation areas, DA-27 noise layer, DA-28 broadband by postcode, DA-29 council rent), add synthetic inputs to `packages/fixtures/data/` in the shape of the official source. Each input has its source labelled "Synthetic sample, shaped like <real source>", its level (1 km square, postcode, council), its period and its schema in `packages/fixtures/schemas/`.
- [ ] Where a shown value is calculated, the generator produces it in the generated files, test-first.
- [ ] Run `make check` (`generated-check` and `validate`). This is its own small code PR (Codex review) and comes before Task 6b.

### Task 6b: "Check this" rows and new topics on the boards
- [x] For each topic the founder marked "check row" (DA-26 coal mining, DA-22's checker link, DA-24's Article 4 and tree orders, DA-28's mobile checker), add a row in the area result and the printout: what it is, why it matters, and a ↗ link to the official service, with no data and no implied result.
- [x] For each topic marked "add", draw it in the area result's design quoting only the Task 6a fixtures by ID. Until those fixtures exist, a topic's board shows its missing-data state ("Not known"), never a figure. Specifications follow in their own PR.

**As drawn (16 Nov 2026), Task 6b:** the result boards (`AreaResult`, `AreaResultDesktop`, `DisplaySettings`), the printout, the two 2D map boards and the About the data and states boards now show the new topics from the Task 6a files: Radon as its own topic (the broadband speed priority is replaced), flood outlines and the checker link, listed buildings and conservation areas with the Article 4 and tree orders link, a coal mining Check this row, road noise, broadband coverage, and council-level rent in an affordability context, each row with a link to City Explorer where the council has a page (DA-29). Check this rows say what the thing is, why it matters and link to the official service, and never imply we checked. The founder approved the wording in one prompt window (FE-69); the noise rows' "rail noise isn't in this source" was corrected to the approved "no record" wording under rule 1. Specifications for the changed screens follow in their own PR.

### Task 7: Founder review, dark versions, PR
- [x] The founder reviews in prompt windows (done except the still-proposed list in the note below).
- [x] Draw the dark versions.
- [x] Do a Chrome check at 390 and 1440.
- [x] Re-run the benchmark table for the changed rows (12 better, 6 level, 2 worse; see the benchmark note).
- [ ] Open the PR: the status file, the "As drawn" note and the register lines.

**As drawn (16 Nov 2026), Task 7:** the founder's wording review was one prompt window with four questions, all taken as recommended (FE-69). Every light board got a dark twin in slate ink (FE-31): new twins for the two 2D map boards, all dark boards resized to match their light ones, and 14 boards and 4 notes moved down 1,517 px on the canvas to make room. A whole-pass visual review in Chrome found two critical problems (the dark Priorities boards were rendering light) and several clipping and overlap problems, which were fixed and re-checked; the dark sweep was clean. Canvas version CANVAS_VERSION_TBD. Still proposed for the founder: the added sentences in "How we got this", the "BGS and UKHSA" stamp name, the About the data source label pattern, the printout's Family view, route-only and method lines, and the NB7 gap wording. Specifications for the changed screens follow in their own PR.
