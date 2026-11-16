# Design benchmark against the competitor (16 Nov 2026, anonymised)

**Verdict.** On truthfulness, missing-data handling, phone reading, states, chat and accessibility, our designs are clearly better, and the council cost page has no equivalent. We are not yet "way better" overall: the competitor's area report is more striking, broader (about 35 sections against our 15 topics) and deeper on flood, maps, the home itself and the printout.

**Tally (20 areas): 11 better, 4 level, 5 worse.**

- **Better:** landing (search first), phone result, recorded crime, missing data and "not covered", states, compare, monthly cost (council page), chat, sign-in, accessibility, trust signals.
- **Level:** desktop result (more honest, less impact), topic detail, account pages, overall visual craft.
- **Worse:** flood depth, maps, area printout, facts about the home itself, breadth of topics.

**Top gaps, ranked**
1. P1 Flood: add surface water and the future scenario with official outlines once licensed (FE-25); remove the decision ID shown in user copy.
2. P1 Desktop result: a place header with the map, At a glance as big figures, no empty right column, a jump row.
3. P1 Area printout: cover, At a glance, all 15 topics (six are missing), questions to ask and check in person, sources page; remove the register ID in the attribution line.
4. P2 Replace the "Explanation not yet available" placeholder shown in every topic.
5. P2 Breadth: planning constraints, radon, coal mining, noise, mobile coverage and postcode rents where licensed; otherwise visible "check" rows.
6. P2 Real basemap design; account data download and a reminder before idle deletion.
7. P3 Our landing headline ends with the same words as the competitor's; reword it.

**Not verifiable from designs:** real data and map tiles, licences for flood/rents/planning, phone compare at full size, contrast and screen-reader behaviour, and whether users prefer a score to facts with limits.

## How it was done
A fresh-context design reviewer compared the pilot's canvas boards (version 356) with the competitor evidence captured on 13 Nov 2026 (kept privately on the founder's machine, never committed; see the [13 Nov comparison](2026-11-13-competitor-report-comparison.md)). Five boards were viewed rendered in Chrome; the rest were read as board files. The founder asked: "one question are our designs better than the competitor?" [sic], then "do the review now".

## The agent's weighing (16 Nov 2026)
- **Agreed, quick:** decision and register IDs shown in user text (gap 1 and 3); the landing headline (gap 7); "(synthetic)" against "(sample)"; hiding "Explanation not yet available" until AI-12's reviewed texts exist (gap 4); a designer's note left in the council budget box's UI.
- **Agreed, design work:** the desktop result (gap 2), the printout (gap 3), the real basemap (gap 6).
- **Agreed, research first:** surface-water and future flood risk with outlines, radon, coal mining, noise, mobile coverage, postcode rents, planning constraints (gaps 1 and 5): each needs its licence and resolution checked before it is promised (rules 1 and 3).
- **Not agreed:** the reviewer suggested "Gurdwara 1,300 m" should read in miles; FE-27 (as amended) shows metres under 1 mile, and 1,300 m is under a mile, so it stands.
- **Later decisions:** an account data download (part of the privacy work's access requests, 0058) and a reminder before idle deletion (needs the email-sending service).

## Founder's decision
Prompt window, 16 Nov 2026, choosing three of four: "Quick fixes now (Recommended)", "Design pass before the gate (Recommended)" and "Research the data gaps" (not "Record only, decide later"). The design pass is planned in [`2026-11-16-benchmark-design-pass.md`](../superpowers/plans/2026-11-16-benchmark-design-pass.md).

## Re-run after the design pass (16 Nov 2026)
A fresh-context design reviewer repeated the 20-area comparison against the redrawn boards (canvas version 402; the pass is recorded in [`2026-11-16-benchmark-design-pass.md`](../superpowers/plans/2026-11-16-benchmark-design-pass.md)).

**New tally (20 areas): 12 better, 6 level, 2 worse (was 11 better, 4 level, 5 worse).**

| Area | Before | After | What changed |
|---|---|---|---|
| Desktop result | Level | **Better** | Place header with the map, At a glance as a row of facts with level and source, a jump row, the right column used. |
| Flood depth | Worse | Level (partly) | Flood outlines and the official checker link are drawn, with the warning check kept apart from flood risk. Still not in its own topic or on the printout. |
| Maps | Worse | Level | 3D by default plus a flat OpenStreetMap-style map (FE-68), overlay switches, list view, rings per FE-42. No real basemap yet. |
| Area printout | Worse | Level | Cover, At a glance, every topic (missing ones as "Not known"), questions, check in person and a sources page. Maps on the printout are still small. |
| Breadth of topics | Worse | Worse (narrowed) | Radon, listed buildings and conservation areas, noise, broadband coverage and council rent are added, and coal mining, mobile coverage and planning rules are "Check this" rows. The competitor still has more sections. |
| Facts about the home itself | Worse | Worse | Unchanged: the pilot is about the area, not the home (see the ranked gaps). |
| Landing, phone result, recorded crime, missing data and "not covered", states, compare, monthly cost, chat, sign-in, accessibility, trust signals | Better | Better | Unchanged. |
| Topic detail, account pages, overall visual craft | Level | Level | Unchanged. |

**Caveats, said plainly.** The boards use synthetic sample data for a made-up town ("Sample data: a made-up town"), so nothing here shows real figures. Nothing is built: this compares designs on a canvas, not a running product. The new layers and topics are sample outlines and records shaped like the official sources; their real licences, coverage and quality are still to be checked. Contrast, screen-reader behaviour and whether people prefer facts to a score are still not verifiable from designs.

**Remaining gaps, ranked**
1. Real data and licences for the new topics and layers (research note DA-22 to DA-29), then the data pipeline.
2. Flood in its own topic and on the printout, at the same depth as the map outlines.
3. Facts about the home itself: the pilot shows the area only. Whether to add the energy certificate by certificate number (DA-09) and an index-adjusted past sale (BE-34) is a founder decision.
4. The real basemap: price self-hosted OpenStreetMap tiles first (DA-25, IN-02).
5. Maps on the printout.
6. Account items: a data download and a reminder before idle deletion (0058).
