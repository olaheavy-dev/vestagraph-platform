# Pilot gate audit, round 2 (19 Nov 2026)

**Verdict: the pilot gate has passed.** Three fresh read-only audits of `main` at b32d379, one per track, checked the gate in decision [0052](../decisions/0052-pilot-only-gate.md), as extended by [0055](../decisions/0055-city-explorer-in-the-pilot.md) (City Explorer) and [0058](../decisions/0058-signed-in-chat-in-the-pilot.md) (signed-in chat). All four conditions are met on every track. There is no P1. There was one P2 and a set of small P3 tidy-ups, and this pull request fixes them all. The founder decided in a prompt window on 19 Nov 2026: "Pass the gate (Recommended)". For the tidy-ups the founder chose "Fix in this audit PR (Recommended)".

Round 1 is in [the round 1 audit](2026-11-19-pilot-gate-audit.md). Tracks: the area check and the energy certificate, with the design batch's new features (A); City Explorer (C); the signed-in chat (S).

**Canvas.** The audits read the design canvas at its live version, id 1795125106-7988. The documents cite version 427 (id 1795115138-a6be). The founder made no edits after 427. The canvas's Design editor has a newer release (1795124224-db4f), so the new version id most likely comes from that editor update. No audit found a board that contradicts the specifications. This pull request's canvas text fixes (below) are canvas version 430, id 1795126820-8fea.

**Tests.** `make validate` passes. `make test` passes with 2772 tests, including the Gherkin specifications and the 557 AI-03 set checks.

## 1. The four gate conditions, per track

| Gate condition (0052) | A: area check, energy certificate, design batch | C: City Explorer | S: signed-in chat |
|---|---|---|---|
| 1. Every pilot screen and feature has a specification and, for a screen, a board | **Passes.** Every feature has a specification and light and dark boards. The two printouts have no dark twin, as FE-31 allows. The "AI error" frame and the old Nearby boards are gone. | **Passes.** All 29 boards exist. Each Dark twin has the same text as its light board. CouncilPrint is light only (FE-50). The phone map sheet (FE-72) and Show map (FE-75) are drawn. | **Passes.** The area card inside the chat is drawn on phone and desktop, light and dark, with the widget's actions (FE-71, FE-78, FE-81). |
| 2. Every required state maps to a scenario; every missing fixture has a `noticed` issue | **Passes.** No IDs are missing or duplicated. Fixture waits cite #342, #349 and #348. | **Passes.** No IDs are missing or duplicated, and there are no gaps in numbering. Fixture waits cite #288, #292, #294 and #339 to #341, all open. | **Passes.** Every header list resolves. #302's body is one complete list. |
| 3. AI-03 evaluation set written | **Passes.** It has 152 cases, unique IDs, and it validates. Round 1's section 5 items 1 to 12 are covered. | **Passes.** It has 20 council-tool cases and 26 council cases in the chat. Items 13 to 19 are covered, including TOOLS-64 to TOOLS-72. | **Passes.** It has 86 chat cases. Items 20 to 25 and every prompt-injection channel are covered. All 78 `@ai03` scenarios have a case. |
| 4. No open `review-followup` issue | **Passes** (none open; #286 is closed) | **Passes** | **Passes** |

## 2. Coverage

| Track | Screens and features checked | Result |
|---|---|---|
| A | Landing (LAND-01 to 26); area result and states (AREA-01 to 50); At a glance, Priorities, Display settings (GLANCE, PRIO, DISP); topics and the extras (TOPIC-01 to 54); maps and Show map (MAP-01 to 30); printout (PRINT-01 to 21); energy certificate (ENERGY-01 to 60); Compare two postcodes (COMPARE-01 to 39); Share a link and Recent postcodes (SHARE-01 to 07, RECENT-01 to 14); Report a problem (REPORT-01 to 31); How it works, Privacy, Accessibility (HOW, PRIV, A11Y); the area card widget, Use in ChatGPT or Claude, the public tools (CARD, HOWTO, TOOLS-01 to 72) | All OK |
| C | Council page, phone and desktop (CITY-01 to 113); neighbourhoods map sheet; Show map; budget with a value; council states (26); neighbourhood page (HOOD-01 to 43); compare two councils, share and print, what changed, About the data (CITY2-01 to 72); Report a problem on a council fact (CITY-112, HOOD-42); council tools (TOOLS-44 to 72); landing and result links | All OK |
| S | Workspace, desktop and phone (WCHAT-01 to 111); compare in the chat; first visit and returning; Ask more about this; states 1 and 2; sign-in (AUTH-01 to 28); account (ACCT-01 to 42); feedback kit; the area card in the chat (CARD-02, 23, 27, 28, 31, 36 to 42, 47 to 49); the withdrawn chat (51 `@withdrawn` tags) | All OK |

## 3. Findings and what was done

### P1
None.

### P2
1. **`status.md` still called finished design batch features "gate blockers"**, in items 1(d) and 1(g). Item 6 already said they were cleared. This is the same kind of contradiction as round 1's P2-5. *Fixed: the status file is rewritten for the gate pass.*

### P3 (all fixed in this pull request unless marked)
1. **Required-state headers left out states.** Fixed:
   - `area-map.feature`: MAP-28 to MAP-30 (Show map, FE-75).
   - `area-card.feature`: CARD-49 (the desktop actions, FE-81).
   - `area-share.feature`: RECENT-03.
2. **`area-card.feature`'s review table said "Kept 11", but it lists 12.** Fixed. The round 1 audit keeps its wording, because it is a dated record.
3. **`workspace-chat.feature`'s Boards line left out SignedInChatAreaCard and SignedInChatAreaCardPhone.** Fixed.
4. **AUTH-03, AUTH-04 and AUTH-05 had no "Replaces" comment** for CHAT-23 and CHAT-45. Fixed in `sign-in.feature`.
5. **City Explorer headers cited canvas version 426.** Fixed to 427, which is where FE-80 redrew CouncilStates.
6. **The pilot's `/compare` and the prototype's `/compare?homes=…` shared a route.** Fixed: the prototype moves to `/prototype/compare` (register line FE-83, an agent's call like FE-79). The IA is updated.
7. **Where City Explorer's search box sits was implicit.** Fixed: council and neighbourhood pages carry no place or council search of their own; their postcode box (CITY-03, CITY-05, FE-70) is separate and unchanged. The box drawn on CouncilStates is the landing's one search (register line FE-84, an agent's call, open to the founder; `city-explorer.feature` line 9).
8. **CITY2-72 expects a desktop City Explorer About the data page that no board or issue tracked.** Fixed: added to #352 as a draw-first build criterion.
9. **#302 did not name the codes the AI-03 cases use** (ZZ4 4ZZ for the Isle of Man, ZZ5 5ZZ for the Channel Islands), nor ACCT-02 by ID. Fixed in #302's body. `status.md`'s short summary of #302 now points to #302 as the complete list.
10. **#318's body still said the compare lists and the compare address were undecided.** Fixed: a comment on #318 records FE-76 and FE-77.
11. **`status.md` said "the desktop placeholder in #317"**, but #317 is closed. Fixed.
12. **Stale canvas text.** Fixed in one canvas publish:
    - note `s12` (the card's places up to 900 m; the sparse area is NB7 1RR, #216 done);
    - note `pguide` (its "still to design" list);
    - the SignedInChatAreaCard board titles (CARD-48, CARD-49, FE-78, FE-81);
    - the CouncilStates note "Eastmere Green (sample, 031A)".
13. **Still open, not gate items:**
    - #314 (the Flood panel's "No map yet", which waits for flood's own topic depth);
    - #352 (desktop About the data and Display settings boards);
    - #318 (undrawn council states, now build criteria);
    - #333 and #334 (energy minors);
    - an unknown or Welsh council code has no TOOLS case yet (round 1's P3-7, for when the tools are built).

## 4. Round 1 items

All round 1 P1 items are confirmed closed on `main`:
- P1-1 to P1-3: the specifications and boards for Report a problem, Share a link and Recent postcodes, and Compare two postcodes.
- P1-4: #342.
- P1-5: the in-chat card.
- P1-6: AI-03.
- P1-7: #286 closed.
- P1-8: #339 to #341.

The P2 items are closed too. Three of them are noted here:
- P2-5 had come back (round 2's P2-1) and is fixed again.
- For P2-9, the code that returns tenure shares is a stage 5b ticket.
- P2-8 to P2-14 were checked against FE-72 and FE-76 to FE-80.

Round 1's P3 items are closed except #352 and P3-7, which are listed above.

## 5. What comes next

Stage 5b's development tickets (0052, "Then"):
- the stage 5b decisions (0046): the AI-09 framework trial and the AI-01 provider, hosting (IN-02), the database (DA-03), the email-sending service, the IN-05 budget caps, the privacy work and the launch guard (OP-06);
- the data pipeline design;
- the app shell (#86).

Build tickets carry #318's and #352's draw-first criteria, the council tools' `tenureShares` code (TOOLS-64 to 66), the typed-price checks and the place search from #286 (WW-21), and the AI-03 runner (AI-15).
