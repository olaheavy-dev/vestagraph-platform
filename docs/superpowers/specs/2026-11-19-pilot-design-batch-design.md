# Pilot design batch (before the pilot gate): design

**Date:** 19 Nov 2026. **Status:** approved by the founder, 19 Nov 2026 (prompt window, "Approve (Recommended)", which also accepts the agent's calls marked below; each can still be changed). **Decisions it follows:** PD-21, FE-71, FE-72 (founder, 19 Nov 2026, prompt windows; recorded as a dated note on [0052](../../decisions/0052-pilot-only-gate.md)); the pilot design ([2026-11-13](2026-11-13-pilot-area-ai-design.md), goal 7 and builder answer 7); [the pilot gate audit, round 1](../../reviews/2026-11-19-pilot-gate-audit.md). **Stage:** boards and specifications before the pilot gate (0052); the build is stage 5b.

## Intent and why
Round 1 of the pilot gate audit did not pass, mainly on **scope**: pilot features that the pilot design promised but that have no specification or board. The founder chose to design all of them before the gate, keeping one pilot phase (PD-21), to draw the area card inside the signed-in chat (FE-71) and to draw the phone neighbourhoods map sheet now (FE-72). This batch closes those gaps so round 2 of the gate can pass. Success: every P1 and P2 design item in the audit's section 4, point 2, has a board (where it is a screen) and scenarios, and passes the competitor benchmark checklist ([pilot design review](../../reviews/2026-11-14-pilot-design-review.md)) before the founder sees it.

Most rules are already decided (pilot design goal 7, decisions 0014, 0053, 0056, 0058). This batch is mostly drawing and specifying, not new rules; where a rule is new, it is listed under "What the founder decided".

## Goals
1. **Compare two postcodes** (a page feature): boards and scenarios.
2. **Share a link** and **Recent postcodes** on the area result and landing: boards and scenarios.
3. **Report a problem with this fact**: boards, scenarios and the shape of the daily count.
4. **How it works, Privacy and Accessibility** pages: boards and scenarios.
5. **The area card inside the signed-in chat** (FE-71) and **the phone neighbourhoods map sheet** (FE-72): boards, mapped to the scenarios that already exist.
6. **Tidy-ups from the audit**: canvas fixes, the extras' missing scenarios, and the small open items listed below.

## Non-goals
- Building anything (stage 5b). No code changes in this batch except fixture data that scenarios need.
- The final privacy notice text (SE-02; founder chose placeholders, below) and the accessibility test results (no test has run).
- The AI-03 evaluation set (its own brainstorm next, AI-14) and the council tools' `tenureShares` (a separate code task, audit P2-9).
- The other #318 items (they become City Explorer build-ticket criteria, FE-72).
- Comparing more than two postcodes, comparing a postcode with a council, or compare in the MCP tools or the chat (pilot design builder answer 7: the tools stay one postcode at a time).

## Anti-goals (a failure even if it works)
- Compare works out a difference, ranks, sorts, totals or names a "better" area (rule 4, pilot design builder answer 7).
- A postcode, a priority limit or a report in a query string, a log, an error report or analytics (0014, 0053).
- Something stored on the visitor's device before they turn it on (PECR, 0014): Recent postcodes and the "Reported" marker included.
- A Report a problem record that could point to a person or an address: free text, a postcode, a per-report row, a time finer than the day, a client key or IP address, or a sold-price record ID.
- A public page that states a legal position or an accessibility result nobody has decided or tested (rule 1).
- A gap shown as blank, zero or a clean result on either side of compare (rule 7).

## Constraints
- AGENTS rules 1 to 9; decisions 0004, 0014, 0028, 0029, 0052, 0053, 0054, 0056, 0058; register lines FE-20, FE-22, FE-27, FE-33, FE-34, FE-39 to FE-41, AI-12, DA-12 to DA-14.
- The design's look: the canvas pilot style (pass A, FE-29 to FE-33, FE-42), light and dark, phone 390 px and desktop; 44 px targets, keyboard access, no sideways scrolling.
- Same patterns as City Explorer where one exists, so the two halves of the pilot behave alike and the approved wording is reused: council compare (CITY2-01 to CITY2-29), Share (CITY2-30 to CITY2-32), "Remember councils on this device" (CITY2-46 onward).
- Specifications in Gherkin under `docs/specs/` (0043), with the state maps and fixture notes the gate checks (0052 condition 2); any scenario that waits for sample data gets a `noticed` issue.

## Approaches
How the work is split (the design is the same in each):
- **Chosen: three pull requests by area of the site** (founder, 19 Nov 2026: "Three by area (Recommended)"), after a first pull request with this design and its plan: (1) Compare, Share, Recent postcodes, Report a problem; (2) How it works, Privacy, Accessibility; (3) the in-chat card, the map sheet, canvas tidy-ups, the extras' scenarios and the audit's small items. Each carries its boards and specifications, so each is reviewable in one sitting and a problem in one doesn't hold up the others.
- **Not chosen: boards first, then specifications** (the City Explorer pattern): two very large reviews, and a board change holds up every specification.
- **Not chosen: one pull request**: one very large review that reviewers handle less reliably; one finding blocks everything.

## What the founder decided (19 Nov 2026, prompt windows)
1. **Compare two postcodes: "Topic by topic (Recommended)".** Every topic in the usual order; each topic is one row with both postcodes' summary lines (stacked on phone, two columns on desktop); tapping a row opens both details; priorities, if set, show meets, misses or not known for each. Over "Visitor picks topics", "Glance + priorities only" and "Two results, swipe".
2. **Privacy page: "Sections + placeholders (Recommended)".** Draw the page with every section the notice needs, using facts already decided, and mark the legal parts "To be written before launch (SE-02)". Over "Draft the full notice now" and "Specify only, no board".
3. **Report a problem: "Pick a reason (Recommended)".** After the tap, three fixed choices, "Wrong", "Out of date", "Missing something"; counted per fact, per reason, per day; still no free text. Over "One tap only" (the 13 Nov design).
4. **The pull request split:** "Three by area (Recommended)" (above).
5. **Where Report a problem appears: "Also City Explorer"** (over the agent's "Area facts + compare (Recommended)" and "Everywhere facts appear"): on each fact in a topic's detail on the area result and compare, and on City Explorer's council and neighbourhood facts (and in council compare's detail). Not on the energy certificate page, the area card inside the chat or the ChatGPT and Claude widget.

The builder check (a fresh reviewer reading this as its builder, 19 Nov 2026) asked seven questions; the founder answered question 5 above, and the agent settled the rest as marked "agent's call (builder check)" below.

The founder confirmed the agent's playback of every part below ("looks right", 19 Nov 2026); the details marked "agent's call" are open to the founder.

## The features

### 1. Compare two postcodes
- **Way in** (agent's call): "Compare with another postcode" on the area result opens compare with this postcode first and an empty postcode box for the second, as council compare does (CITY2-02). Compare also has its own route (proposed `/compare#NB1 4XY,NB7 1RR`, postcodes after the `#`; exact form left to the builder, never a query string).
- **Before the second postcode:** no rows and no figures, only the box (as CITY2-05). An invalid, non-English or unknown second postcode shows the same states as the area result's search (England first, rule 6: "not yet covered").
- **Top of the page:** both postcodes with a Swap control (swaps the columns and changes nothing else, as CITY2-04); At a glance for each (the FE-22 and FE-41 counts, quoted for each postcode, never a difference); priority results for each if the visitor has set any (limits sent in the request body only, 0053); a topic jump list.
- **Priorities on compare** (agent's call, builder check): the limits set on the area result carry over in the page's memory and can be changed on compare with the same controls; with none set, compare shows the "set what matters to you" entry and works fully without it (FE-40). A shared compare link opens with no limits (PRIO-16).
- **Rows:** every pilot topic in the area result's order; each row has the topic name and each postcode's summary line (the same text as the area result, FE-20), labelled with its postcode. Tap opens a sheet (phone) or panel (desktop) with both postcodes' details one after the other, each with its own source stamp (FE-33).
- **Gaps:** a topic one side lacks reads "Not known" on that side, with that topic's usual reason (rule 7); a source that is down reads "Unavailable" on that side.
- **Never:** sorted, ranked, totalled, coloured as better or worse, or a difference worked out ("2 more schools").
- **How we got this:** one per page (FE-34), saying both columns come from the same sources and editions, and that nothing is ranked.
- **Share this comparison:** both postcodes after the `#`, never the limits (PRIO-16's rule extended).
- **Offline:** results already shown stay; a new postcode waits (as CITY2-27).
- **Printout:** not in this batch (agent's call: the area printout covers one postcode; a compare printout can be a later idea in doc 05). Print on compare is not offered.

```
Phone, 390 px
┌──────────────────────────────┐
│ Compare two areas            │
│ NB1 4XY  ⇄  NB7 1RR          │
│ At a glance  12 found · 3 ?  │
│              8 found · 7 ?   │
│ Jump to: Schools ▾           │
├──────────────────────────────┤
│ Schools                    › │
│ A  3 primary within 1 mile   │
│ B  1 primary within 1 mile   │
├──────────────────────────────┤
│ Flood                      › │
│ A  No warning at 09:40       │
│ B  Not known                 │
└──────────────────────────────┘
```
(Sketch only; the counts and lines on the boards are quoted from the sample data.)

### 2. Share a link
- "Share" in the area result's header (agent's call). On phone it opens the device's share sheet; on desktop it copies the link and says "Link copied". If copying fails: "Couldn't copy. Here's the link to copy yourself", with the link shown and selected.
- The link carries the postcode after the `#` only (pilot design goal 7), never limits (PRIO-16), display settings or the open topic.
- Opening a shared link runs the search as if typed; nothing is stored or logged.

### 3. Recent postcodes
- Under the search box on the landing and on the area result (agent's call).
- Off by default: "Remember postcodes on this device" with "Turn on" (PECR consent, 0014 "Recently viewed"); wording mirrors City Explorer's "Remember councils on this device".
- On: up to 5 postcodes, newest first (agent's call on the number), each a link; "Clear" empties the list; "Turn off" deletes the list and the setting. Kept only in the browser, never sent to us.
- Its own setting, separate from "Remember councils on this device", because each purpose is its own PECR consent; City Explorer's scenarios are unchanged (agent's call, builder check). While on, postcodes checked on the area result, entered on compare or opened from a shared link are all added.
- If browser storage is unavailable (private window, blocked), the setting says it can't be turned on here; the search still works.
- Named in the privacy notice (section list below).

### 4. Report a problem with this fact
- A small "Report a problem" link on each fact in a topic's detail (sheet or panel), not on the summary line (agent's call), on the area result, compare, and City Explorer's council and neighbourhood pages and council compare (founder's choice 5). Not on the energy certificate page, the chat's area card or the ChatGPT and Claude widget.
- It can also be used on a gap ("Not known", "Unavailable", "Not yet covered"), where "Missing something" is the natural reason (agent's call, builder check).
- Tap opens three fixed choices: "Wrong", "Out of date", "Missing something" (founder's choice), plus Cancel. Choosing one sends it, behind the invisible bot check, and says: "Thanks. We count reports for each fact to see what needs checking. We can't reply." (agent's wording, for the founder's copy review).
- **States:** sent ("Reported" on that fact until the page is closed; kept in the page's memory only, nothing stored on the device: agent's call, correcting the agent's earlier "already reported today on this device", which would need PECR consent); bot check failed or server error ("Couldn't send. Try again."); offline ("You're offline. Try again when you're back online."); rate limit reached (same wording as a failure, so it reveals nothing).
- **What is stored** (pilot design goal 7, plus the reason): one daily count per date, source, topic, fact record ID, local authority and reason. Never the postcode, a per-report row, a time finer than the day, a client key or IP address. Kept 90 days. Part of FE-05. Three shapes (agent's call, builder check):
  - **A fact with a record ID that names no address** (a school, a GP, a bus stop, a flood warning area): as above.
  - **A fact that points to one address** (sold prices, as goal 7 set, and planning applications, which also name one site) **or a gap with no record** ("Not known", "Unavailable", "Not yet covered"): per date, source, topic, local authority and reason, with no record ID.
  - **A City Explorer figure** (council or neighbourhood level): per date, source, the figure's name (for example council tax Band D, private rent, average price for flats), the council or neighbourhood code and reason. These codes are public area codes, never an address.
- **The counts stay internal** (agent's call, builder check): never shown on the site or published, so no small-number suppression is needed; read only by the founder to decide what to check. If they are ever published, that needs its own decision (SE-05's small-number rules would apply).
- The data contract (a JSON Schema for the count record, with a sample file) is written in pull request 1, so the build has one shape to follow.

### 5. How it works page (`/how-it-works`)
Sections (agent's call, open to the founder's copy review): what Vestagraph is (facts about an area in England, each with its source and date); where the facts come from (link to About the data); what it never does (no verdicts, scores or "safe"; missing data never shown as zero); what "Not known" and the source stamp mean; Explain this is pre-written, reviewed text, not AI; Use in ChatGPT or Claude (link); Report a problem. Linked from the footer and the landing's "How it works" line. Plain, short, one illustration at most in the isometric style (FE-10), recorded in `docs/assets/README.md` if added.

### 6. Privacy page (`/privacy`)
Every section the notice needs, filled with facts already decided and marked placeholders for the rest (founder's choice). Sections: who we are; what we collect and what we never collect (postcodes in the `#` or request body only, never logged, 0014, 0053); Recent postcodes and "Remember councils on this device" (only in your browser); Report a problem counts; the bot check (device signals, 0014 part 1); outbound links that may carry the postcode on a click (FE-11); using Vestagraph in ChatGPT or Claude (the host's terms, 0056, 0057); the energy certificate number (never stored, DA-09); signed-in accounts and chat (0058); your rights; contact ("Contact details to be added before launch": no contact route is decided, so none is invented; agent's call, builder check). Each legal part (lawful basis, retention wording, controller details, rights wording) reads "To be written before launch (SE-02)". The board shows the placeholders plainly, never as finished text.

### 7. Accessibility page (`/accessibility`)
States the target, WCAG 2.2 level AA ([W3C](https://www.w3.org/TR/WCAG22/)); says the site has not been tested yet, with a placeholder for the test results and known issues ("To be completed after testing, before launch"); its contact route is the same placeholder as the privacy page's ("Contact details to be added before launch"). Never claims conformance before a test (rule 1).

### 8. Area card inside the signed-in chat (FE-71)
As FE-71 sets it: the compact card with Expand, the expanded dialog, and the phone preview with "Open map", phone and desktop, light and dark, on "Pilot · Signed-in chat", matching CARD-02, 23, 27, 28, 31 and 36 to 42. Update the canvas note `s12`. Closes #303 item 1.

### 9. Phone neighbourhoods map sheet (FE-72)
Map, list and panel in a sheet at 390 px (FE-43), light and dark, on "Pilot · City Explorer". The other #318 items are written onto #318 as City Explorer build-ticket criteria.

### 10. Tidy-ups (pull request 3)
- Canvas: remove the "AI error (CHAT-19 to CHAT-24, CHAT-53)" frame from AreaStatesPilot and its Dark twin; delete the stale pass B Nearby, NearbySchools and their Dark twins (newer versions already sit on "Home workspace (later)"; agent's call, delete rather than move); redraw "Check" as "Search" on the desktop council boards and remove the old placeholder (#317).
- Specifications (audit P2-1): one data and one `@ui` scenario per extra in `area-topics.feature`: buses as routes per stop at 8am and midday, never a stop total (DA-18); school demand as past-year facts, never a chance of a place; green space as the voluntary standard, measured from the postcode; flood by postcode as published, never one verdict (DA-16); council tax by band "may include parish charges"; air quality and connectivity never combined (0054).
- The audit's small open items: the find-council tool's four search scenarios (P2-10); register lines with defaults for the shared comparison's address (P2-11, suggested `/council/compare/<first>/<second>`) and the compare list for a council with nothing recorded (P2-14, suggested every council in England, gaps as on the council page); HOOD-14 and HOOD-38 quote the board's wording (P2-12); CITY-78's header (P2-13); edit #302's body (P2-15); the P3 list (radon label, no certificate tool on the MCP server, FE-11 links in AREA-18's examples, FE-50 status, #318's desktop "Check", canvas version citations, WCHAT notes, IA `/sign-in`, #99, #102, #303 item 2). Any of these that turns out to need a founder decision is asked in a prompt window, not guessed.

## States to cover (each mapped to a scenario, 0052 condition 2)
Compare: empty second postcode, invalid, not England, unknown, a source down on one side, a topic missing on one side, offline, swapped. Share: copied, share sheet, copy failed. Recent postcodes: off, on and empty, on with entries, cleared, storage unavailable. Report a problem: choices open, sent, failed, offline, rate-limited. Public pages: placeholder sections (Privacy), untested (Accessibility).

## Sample data (agent's call, builder check)
No code changes in this batch, the generator included. Boards and scenarios quote the sample data that exists (`area-result.json` has NB1 4XY and the sparse NB7 1RR; the council sample files for City Explorer). A state with no sample record, such as a source down on one side of compare, keeps its scenario with a "fixture needed" note and a `noticed` issue, as 0052 condition 2 allows; the issues are listed in the pull request that adds the scenarios.

## Records this changes
- Register (`docs/decisions/README.md`): **FE-73** compare topic by topic (with the agent's calls above); **FE-74** Report a problem with a reason, on the area result, compare and City Explorer, with the three count shapes, internal only (amends goal 7 of the pilot design and FE-05's scope); **SE-07** the privacy page drawn with placeholders until SE-02. FE-05 note: the count's shape and its schema.
- Pilot design (2026-11-13): a dated note on goal 7 for the reason and the in-memory "Reported" marker.
- `.design/prototype/INFORMATION_ARCHITECTURE.md`: compare route; Share and Recent postcodes on the result and landing; Report a problem on topic details.
- `docs/planning/status.md`: the batch's progress in each pull request.
- `docs/product/05-ideas-and-product-thinking.md`: a compare printout as a later idea.

## Left to the builder
Board layouts within the pilot style; exact compare route form (postcodes after the `#`); scenario IDs and file placement (new `area-compare.feature`, `area-share.feature` or sections in existing files); the count schema's field names; which sample postcodes the compare boards use (NB1 4XY with NB7 1RR shows gaps well).
