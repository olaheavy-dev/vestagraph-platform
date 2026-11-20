# First design batch: the area result (design brief)

Status: **approved by the founder** (14 Nov 2026, prompt window: "Approve (Recommended)"). Status file item 1 (c); order from the [pilot design review](../../reviews/2026-11-14-pilot-design-review.md) ("Missing, in the design batches that follow").


> **Note, 15 Nov 2026 ([0056](../../decisions/0056-no-on-page-chat-in-the-pilot.md)) and 16 Nov 2026 ([0058](../../decisions/0058-signed-in-chat-in-the-pilot.md)):** the on-page chat left the pilot, and its error and "Ask more about this" passages below (the "AI error" state, CHAT-19 to CHAT-24, CHAT-53, and "Explain this ... ending in 'Ask more about this'", CHAT-52) are kept as approved on 14 Nov 2026. Read them as follows: the public result has no chat error; a topic's missing explanation reads "Explanation not yet available" (TOPIC-24); "Ask more about this" lives in the signed-in chat (WCHAT-55); the CHAT IDs are withdrawn (`area-chat.feature`). The "AI error" frame on AreaStatesPilot is canvas work to remove (the pilot gate audit, [round 1](../../reviews/2026-11-19-pilot-gate-audit.md)).

## Intent
The area result is the screen every pilot visitor sees after typing a postcode, and the [pilot design review](../../reviews/2026-11-14-pilot-design-review.md) found it the weakest: no At a glance, no topic detail, no desktop result. This batch draws it on the design canvas so it can pass the competitor benchmark checklist (founder, 13 Nov 2026: "our minimum now is to be way better than [the competitor]") and then be specified. Canvas first, then the specifications (#68 style feature files), then the build.

## Goals
1. **At a glance** at the top of the result (FE-22, B20): rule-built counts (found, unknown or unavailable, questions to ask), each count linking to its items, and "Things to check in person" without a count (FE-41), and a coverage line ("<n> of <m> topics returned facts", worked out by a tested module, rule 2).
2. **One topic anatomy** (B29), shown as a bottom sheet on a phone and a side panel on desktop (FE-20, FE-26), drawn once for each **kind** of topic (founder, 14 Nov 2026, prompt window: "One per kind (Recommended)").
3. **Priorities** set from At a glance (founder, 14 Nov 2026, prompt window: "In At a glance (Recommended)"; FE-22, decision 0053).
4. **The result's short "How we got this"** note (a paragraph, one line per topic with its icon, name and source links, and a link to About the data; FE-24 amended 14 Nov 2026).
5. **The desktop result** for Check an area (FE-26 layering).
6. **The missing states** (B22, B32): loading, postcode not found, postcode service down, sparse area, stale source, all sources down, offline, AI error.
7. **Theme and text size** (FE-23, B16).

## Non-goals
- The designed report and Share a link (next batch, FE-21).
- The energy certificate, the street map, the public pages (later batches).
- Every one of the ~15 topics drawn in full: the other topics are listed in the table below with their kind and content, not drawn.
- The home workspace (signed-in) result.

## Anti-goals (a failure even if it looks good)
- Any verdict, score, band or "better area" word (rule 4, B1). **At a glance never tallies priorities** ("3 of 4 met" reads as a score); it lists each priority with its own result.
- A missing fact shown as a miss, zero, a dash or a clean result (rule 7, B2). An unknown priority result says "Not known", never "Misses".
- A figure typed onto a board instead of read from the sample data (rule 2).
- A limit line back on rows or sheet tops (FE-34), or a status word or date on a fact (FE-33; the flood check time is the one exception, DA-12). *Dated note, 20 Nov 2026: the flood check time is gone too, because no flood warnings copy is kept ([0061](../../decisions/0061-pilot-data-pipeline-postcodes-and-walking-times.md)).*

## Constraints
- Canvas version 138 style: soft gloss (FE-29), ledger rows (FE-30), source stamps (FE-33), one marker language, seven type sizes, three weights, England distances in metres under 1 mile and miles from 1 mile (FE-27). Values in `.design/prototype/tokens.css` (synced in #254).
- **Sample data:** NB1 4XY (full), NB7 1RR (sparse), NB9 9ZZ (an unknown postcode: "We couldn't find that postcode", AREA-05) from `packages/fixtures/data/postcode-area.json` (#250). It has transport, amenities, schools and inspections, flood (with the 09:40 check time), crime, sold prices, planning and broadband, with straight-line distances only. **One sample-data pull request comes first** (agent's call: drawing these as gaps would defeat the per-kind examples): synthetic records, each with its level and source (DA-14), for a deprivation decile (0054), school demand, walking times, buses per hour, flood risk by postcode (DA-16); no flood warning count is stored, because a count would be a calculated figure, with any schema change they need. *Dated note, 20 Nov 2026: the flood sample no longer has a 09:40 check time or a warning record; the flood row links to GOV.UK ([0061](../../decisions/0061-pilot-data-pipeline-postcodes-and-walking-times.md)).*
- Checklist items B2, B4 and B10 are read as amended by the founder's later decisions: a fact's date sits on About the data with no status word (FE-33 amended 14 Nov 2026, "Dates only, no notes"), so B2's "Old" gap state is not shown at all, and limits sit on the general About the data page (FE-34 amended 14 Nov 2026).
- WCAG 2.2 AA in both themes; no sideways scrolling at 320 to 390 px (B15); touch targets at least 44 px (the enhanced level, WCAG 2.5.5; stricter than AA's 24 px in 2.5.8); every map has a list.

## Founder answers to the builder check (14 Nov 2026, prompt windows)
- **Counts:** "Small tested module (Recommended)": At a glance's counts and coverage line come from a small tested module in the generator, writing a generated file as `costs.json` does, before the boards are drawn (FE-38).
- **What counts as found:** "Source answered = found (Recommended)": found when the source answered, including "no record in this source" and "none found within the radius"; not known when our stored copy failed or is unavailable; "not yet covered" topics are left out of the total (FE-38).
- **Next steps:** "Gaps + fixed list (Recommended)": questions to ask come from gaps, one per gap from a reviewed template (TOOLS-15); check in person comes from a fixed, reviewed list per topic of things data can't show, written in advance like Explain this (FE-39).
- **Rank notes:** "In the fact's own words (Recommended)": decision 0054's two notes are written into the rank fact, as the flood wording is (DA-17).

- **After the design review (14 Nov 2026):** priorities stay in the pilot without sign-in, and the result works fully without them ("Keep in pilot (Recommended)"); a priority on "no record in this source" reads Not known (after asking "do we have data source for childcare?": "Not known (Recommended)"); "within" includes the limit and the unit is chosen from the rounded value ("Round first; limit counts (Recommended)", FE-27 amended, FE-40); "Check in person" shows no count ("No number (Recommended)", FE-41); walking times are a sourced input with their method ("Sourced input (Recommended)", DA-18). While planning: each bus stop lists its routes with how often each runs at 8am and midday on weekdays, never a stop total (after asking "will this be useful people take different bus number or routes": "Routes with how often (Recommended)", DA-18 amended); a place recorded beyond the limit reads "Misses your limit · nearest recorded <distance>" ("Misses, show nearest (Recommended)", FE-40).

Agent's calls from the design review: buses per hour counted by a tested module from synthetic departures (rule 2, DA-18); every pilot topic gets an explicit sample record, a value or a stated gap, and generation fails for a topic with none (so `make check` fails); the priority states (checking, couldn't check, all three results on the board, limits beyond the 5 km search "Not known beyond 3.1 miles" (founder, 14 Nov 2026: "Use miles (Recommended)"), validation of the limit box); the priorities panel follows FE-26; "postcode service down" means we can't look up postcodes ("Try again", never "not found"); when all sources are down the rows stay and one page line points to About the data; the flood example has no map until outlines exist (FE-25); topics we only link to (council tax band, noise, ground and mining, mobile by network until the new Ofcom service is recorded) are "Not yet covered" rows with the official route, left out of the total; Escape closes a sheet, the phone sheet holds focus, the desktop panel moves focus to its heading, a shared link never carries priorities; noted for the plan: the Ofcom mobile service change on 30 Nov 2026, quoted source text checked as quoted, sold prices by street and type only (DA-13), a legend and place list beside the desktop map, display settings not remembered until the PECR check.

Agent's calls from the builder check: the extra sample data above; an **About the data** board, because a stale source looks normal on the result (FE-33) and shows only there; the **AI error** state is the chat drawer's error (CHAT-19 to CHAT-24), plus a topic's "Explanation not yet available" text (CHAT-53). The pilot's topic list (B13: "not written down") is fixed in the plan from the table below and the coverage registry design.

## Approaches
Considered for the topic sheets (founder chose the first):
- **One per kind (chosen):** one anatomy, drawn with one example of each kind of topic; the rest in a table. About 8 topic boards; topics whose licence checks are open (DA-05, DA-09 to DA-11, DA-13) aren't drawn twice.
- **Every topic:** about 60 boards with dark versions; several sessions, likely redrawing.
- **Template only:** quickest, but number-only, ranking and warning topics unseen.

Considered for priorities (founder chose the first):
- **In At a glance (chosen):** one "What matters to you" sheet; At a glance lists each priority's result.
- **Inside each topic:** closer to the fact but scattered; At a glance would have to gather them.
- **Before the result:** rejected, it breaks "one step to a result" (B19).

## The design

### At a glance (top of the result)
```
NB1 4XY · Northbridge (sample)
At a glance
  Found: <n> topics       Not known: <n> →
  Questions to ask: <n> → Things to check in person →
  <n> of <m> topics returned facts
  What matters to you  [Set priorities]
    GP surgery within 15 min walk ....... Meets your limit
    Railway station within 0.5 miles .... Misses your limit
    Childcare within 1 mile ............. Not known
```
Sketch only: `<n>` marks a count the boards take from the sample data, and the two priorities are examples. Counts come from rules over the facts (as CHAT-10 and TOOLS-15 make questions from gaps), never typed. Each count opens a list of its items, each item opening its topic. How the counts and the coverage line are worked out (what counts as found, not known and left out) is listed on the general About the data page, as the "How At a glance is counted" row (FE-24 and FE-34 amended 14 Nov 2026; B6).

### Priorities sheet
"What matters to you": a short list of ready-made limits, each with an editable number and unit: GP surgery, pharmacy, primary school, secondary school, railway station, bus stop, supermarket, park or green space, childcare provider, hospital, broadband speed (broadband speed removed 16 Nov 2026, DA-31; founder: "Replace it now") (the agent's starting list read "station or stop" and had no childcare or hospital; the agent added childcare provider and hospital, which the sample priorities use, and named the item "railway station" while drawing the boards (canvas review, 14 Nov 2026); the founder added bus stop, 14 Nov 2026, prompt window: "Add bus stop"; a worship limit follows PD-13, and whether it is sent like the others or checked only in the browser is decided in the privacy review, SE-02 part 2, before launch, 0053). How meets or misses is worked out is listed in the "How priorities are checked" row on About the data (FE-24 and FE-34 amended 14 Nov 2026). Limits use walking time where the pilot has it (DA-08) and straight-line distance otherwise, labelled with which. Limits are sent to the server to work out meets or misses (0053), never stored or logged; remembering them between visits is opt-in and stays in the browser (FE-22).

### Topic anatomy (one order for every topic, B29)
1. Title, icon and headline fact (the same line as the summary row).
2. Your priority result for this topic, if one is set.
3. The facts as ledger rows, each with the area or radius it covers beside it (B3).
4. Map view, only for topics with places (crime never on a map, B5; flood keeps its own flat map, FE-25).
5. Gaps in their own wording (B2): no record in this source; none found within the stated radius; Not known right now; not yet covered.
6. What to do next (B21): a question to ask, a thing to check in person, the official link.
7. "Explain this" (pre-written, AI-12) ending in "Ask more about this" (CHAT-52).
8. Source stamps (FE-33). Close button; the phone's Back closes it; focus returns to the row; the open topic is linkable (B14). No "How we got this" inside the sheet (FE-34).

### The four kinds, and which topic each board uses
| Kind | Drawn with | Other topics of this kind |
|---|---|---|
| A list of places | Schools (with inspection dates and school demand) | Getting around (with buses per hour), everyday places (with walking times), places of worship, family view, planning nearby |
| Figures for an area | Recorded crime (counts by month and category for a stated radius) | Sold nearby, broadband and mobile, air quality, council tax by band, housing affordability |
| An official ranking or standard | Deprivation decile (needs the fixture record first) | Transport connectivity, green space standard |
| A warning | Flood (a link to GOV.UK flood warnings, since 20 Nov 2026, 0061; long-term risk link; risk by postcode) | none yet |

### Boards (light first; dark versions after the founder approves the light ones)
1. Check an area result, phone: header, At a glance, topic rows, the "Ask about this area" entry with its AI badge (FE-13; the pilot design review's first batch lists an entry to the chat from the phone result), the short "How we got this" note with its link to About the data.
2. Check an area result, desktop: At a glance and topic list on the left, map on the right (FE-26).
3. Priorities sheet (phone) and panel (desktop), with the result showing meets, misses and not known, the checking state and the couldn't-check state. Board 1 is the result with no priorities set.
4. Topic sheet (phone) and panel (desktop) for each of the four kinds: 8 boards.
5. About the data as topic rows, one opened to its method, limits and coverage, phone.
6. About the data: each source with its link and date, no status word, "We hold no current copy" in place of a date where there is none (FE-33 amended 14 Nov 2026).
7. States, every one in the information architecture's list, so nothing is lost when the old boards go: loading (skeletons with a status), invalid format (AREA-04), postcode not found (NB9 9ZZ, AREA-05), couldn't load (AREA-19), outside England (AREA-08), a search crossing the border (B9), the area rate limit, postcode service down, sparse area (NB7 1RR), stale source (shown as FE-33 decides: the fact unchanged, its date on About the data), all sources down, offline, AI error (the chat drawer's error, and "Explanation not yet available" in a topic); each with cause, reassurance and one action (B22).
8. Display settings: the theme switch (device, light, dark) and the text-size control, with the phone result at the largest size and no sideways scroll.

About 16 light boards. The existing Check an area and area-states boards that these replace are removed in the same canvas change (and said which).

## Left to the builder (agent's calls, open to the founder)
- Where the display settings live (agent's default: a "Display" button in the header) and the text-size steps (default: three steps, standard, large, larger).
- Exact wording of counts, gaps and next steps, checked against the specifications' existing wording.
- Board sizes and canvas placement on the "Pilot · public area check" page.

## After approval
A design review of this brief (house-reviewers `design-reviewer`, AGENTS step 1b), then the plan (writing-plans): the sample-data pull request and the tested At a glance module first (backend), then the canvas boards (frontend), the founder's review, the dark versions, and the specifications.
