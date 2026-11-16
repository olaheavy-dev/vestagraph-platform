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
