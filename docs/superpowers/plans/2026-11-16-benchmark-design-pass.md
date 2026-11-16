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
2. **The printout lists all 15 topics,** including missing ones as "Not known" pages, never dropped silently.
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
- [ ] Add a place header with the map: the postcode, the area name and its level, and the sample note.
- [ ] Show At a glance as a row of big figures with level and source, replacing the 3+1 grid.
- [ ] Use the right column under the map (for example questions to ask and check in person, FE-39), and add a jump row to the topics.
- [ ] Acceptance: no score or verdict; every big figure is quoted from `area-result.json` with its stamp.

### Task 4: Printout redraw (AreaExport, FE-21)
- [ ] Add a cover: postcode, date, and the sample or data date.
- [ ] Put At a glance on page 1.
- [ ] Include all 15 topics, with missing ones shown as "Not known".
- [ ] Add questions to ask and check in person.
- [ ] Add a sources page with each source's date and status (FE-33 printout rule).
- [ ] Use greyscale-safe charts and readable type sizes (12 pt or more in print).

### Task 5: Basemap style (MapDesktop, MapPhone)
- [ ] Following the research note's basemap choice: draw the real map style in light and dark, with its attribution, the list view as the accessible equivalent, and slots for flood and planning overlays where Task 2 allows.

### Task 6: "Check this" rows and new topics
- [ ] For each topic the founder marks "check row", add a row in the area result and the printout: what it is, why it matters, and a ↗ link to the official service, with no data and no implied result.
- [ ] For each topic marked "add", add the topic in the area result's design with sample data shaped like the source. The fixtures and specifications follow in their own PR.

### Task 7: Founder review, dark versions, PR
- [ ] The founder reviews in prompt windows.
- [ ] Draw the dark versions.
- [ ] Do a Chrome check at 390 and 1440.
- [ ] Re-run the benchmark table for the changed rows.
- [ ] Open the PR: the status file, the "As drawn" note and the register lines.
