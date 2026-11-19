# 0052: A pilot-only gate, so the pilot is built before the home workspace

**ID:** WW-18  
**Status:** Accepted (founder, 13 Nov 2026, in a prompt window)  
**Date:** 2026-11-13  
**Stage:** 3  
**Supersedes in part (no older text is rewritten):** doc 04 §9's order "stage 3 gate, then stage 5, then stage 5b" for the pilot's screens; the stage 3 gate (#71) as one gate over every screen; [0046](0046-public-area-check-first.md) Option B point 1 ("stage 5, area first": the area screens built on fixtures in the private prototype before 5b) for the pilot's screens; the backlog's start condition for #86 (after the full stage 3 gate), which becomes the pilot gate

## Context
The founder chose, on 13 Nov 2026, to write the pilot's specifications first ("Pilot specs first (Recommended)") and then typed: "Let us document just what we need for Pilot specs document where we stpped on the home specs and start the devlopment tickets as as we are done with pilot specs" [sic]. The stage 3 gate (#71) expects every screen's specification, including the home workspace screens (#68 parts 2 and 3) and the story scripts (#69, #70), before anything is built. The pilot (stage 5b, decisions 0046 and 0051) needs none of the home screens.

## Options
### Option A: Pilot-only gate (recommended)
Split the gate. A short gate checks that the pilot's specifications alone are complete and buildable; then the pilot's development tickets start. The home specifications, story scripts and the full stage 3 gate resume before the home workspace is built.

### Option B: No gate
Write the pilot's tickets as soon as its specifications merge. Fastest, but nothing checks the specifications are complete before building.

### Option C: Keep the full gate
Finish every specification and pass the whole stage 3 gate first. Slowest; today's plan.

## Decision
**Option A** (founder, 13 Nov 2026: "Pilot-only gate (Recommended)").

**The pilot gate passes when:**
- every pilot screen and feature in the design (`docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md`) has a specification in `docs/specs/` and, where it is a screen, a board on the design canvas's "Pilot · public area check" page;
- every required state in those specifications maps to a scenario, and every missing fixture has a `noticed` issue;
- the AI evaluation set (AI-03) is written;
- no `review-followup` issue is open anywhere in the repository (the `AGENTS.md` rule for every stage gate applies to the pilot gate unchanged).

**Then:** one development ticket per buildable slice, each with acceptance criteria and its tests, starting with the stage 5b decisions (0046) and the app shell (#86).

## Consequences
- **#68 pauses** after part 1 (#217), with the resume point recorded on the issue (13 Nov 2026). #69, #70 and the full gate (#71) follow later, before the home workspace is built.
- **The private prototype (stage 5) for the home workspace** comes after the pilot. The pilot's own screens are built on real data in stage 5b, not first as a fixture-only prototype; the area fixtures still serve the tests.
- **Doc 04 §9 and the status file** show the pilot track first.
- **Revisit if** the pilot's build shows that the home screens' design changes the shared components (the app shell, the topic summary or the map) enough to rework the pilot.

**Note, 16 Nov 2026 ([0058](0058-signed-in-chat-in-the-pilot.md), accepted by the founder 16 Nov 2026):** the pilot gate also checks the signed-in chat's boards and specifications.

**Note, 14 Nov 2026 ([0055](0055-city-explorer-in-the-pilot.md); recorded 19 Nov 2026):** City Explorer is part of the pilot, so the gate also checks its boards and specifications (and its AI evaluation cases, 0055 Consequences).

**Note, 19 Nov 2026 (round 1 of the gate: [the pilot gate audit](../reviews/2026-11-19-pilot-gate-audit.md)):** the gate did **not** pass. The founder's answers in prompt windows that day:
- **Missing pilot features** (Report a problem; Share a link with Recent postcodes; Compare two postcodes; the How it works, Privacy and Accessibility pages): "Design all, before the gate (Recommended)": one design batch (brainstorm, boards, specifications) before the gate; PD-16's single pilot phase stays (register line PD-21).
- **The area card inside the signed-in chat:** "Draw the card (Recommended)" (FE-71).
- **#318:** "Map sheet now, rest in tickets (Recommended)": draw the phone neighbourhoods map sheet in the design batch; the other items become acceptance criteria on City Explorer's build tickets (FE-72).
- **AI-03:** "One set, brainstorm first (Recommended)": one versioned evaluation set for the area tools, the council tools and the signed-in chat (AI-14).
- **#286** (earlier that day): "Fix now-items, move 5b items (Recommended)" (WW-21), with the caption "less than 0.1%" (DA-36; #338 closed #286).

*Note, 19 Nov 2026: condition 3 is met: the AI-03 set is written (`packages/fixtures/evaluation/ai-03-set.json`, 152 cases, AI-14 and AI-15), with the founder's spot-check of 10 cases approved; only the runner waits for stage 5b.*

The gate is re-checked after the design batch, the AI-03 set, and the council tools returning tenure shares.
