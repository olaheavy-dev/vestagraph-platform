# The anonymous chat's design step: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the signed-in chat's specification and boards into the pilot's anonymous chat (its own page, the consent card with the invisible bot check, the limits and pauses, comparison progress), bring the Privacy notice up to 0063 and 0064, and record the rule 5 exception for the controller's name.

**Architecture:** Three pull requests. **PR A** (branch `docs/anonymous-chat-design`): the design, this plan and the records. **PR B** (`docs/0065-controller-name`): decision 0065, AGENTS.md rule 5's pointer, and the Privacy notice scenarios and board; a founder merge, kept separate so nothing else waits on it. **PR C** (`docs/anonymous-chat-specs`): the chat's specification changed in place, the sign-in-only scenarios moved to a "later" file, the entry points on other pages, the canvas boards and their visual review. The founder's copy review covers PR B and PR C's proposed wording.

**Tech Stack:** Gherkin specifications run by pytest-bdd (every chat scenario is `@ui`, so `make test` deselects them; the runner still parses every file), the design canvas (https://claude.ai/artifact/MpvQNDVYCePp4iWM3j3Jx4). No new packages and no code changes.

**Spec:** `docs/superpowers/specs/2026-11-21-anonymous-chat-design.md` (approved by the founder, 21 Nov 2026).

## Global Constraints
- Documentation only: Markdown, `.feature` files and the canvas. No change to `pyproject.toml`, schemas, fixtures' data or code. A scenario that needs a sample record keeps a `# fixture needed: #NNN` note and a `noticed` issue.
- Every scenario keeps its WCHAT number when kept, rewritten or moved; new scenarios start at **WCHAT-112**. No number is reused.
- Sign-in-only scenarios move **unchanged** to `docs/specs/pilot/chat-signed-in-later.feature`; its header says they wait for sign-in (0063 point 2). They are already `@ui`, so no new tag is needed.
- Fixed texts already approved, quoted exactly: "1 message left today" (FE-55); "Chat is paused for today, the area check still works"; "Chat is paused for this month, the area check still works." (FE-61); "Chat unavailable right now" (FE-66). Every other quoted text is proposed and listed for the copy review.
- The consent statement keeps every fact in the design's section 7, first point: Anthropic, US or "global" processing, deleted within 30 days, flagged content up to 2 years, our 14 days, withdrawal and how. The button's own label carries the agreement.
- Nothing about the chat on the device: no cookies, local storage, session storage or IndexedDB; no postcode or question in any address (0063, WCHAT-66, WCHAT-75).
- The founder's name appears **only** in PR B's files (0065, the PRIV scenario naming the controller, the Privacy board), never in PR A or PR C.
- Pause precedence: unavailable, monthly cap, daily cap, the visitor's own 15, rate limit, turn limit. Daily cap pauses when a day's spend reaches £2.50 (0064 point 5); monthly at 95% of £25; the daily cap resets at midnight Europe/London.
- Settled here (agent's calls, left to the plan by the design): ALTCHA re-checks every **5** messages; the consent statement's version is a whole number starting at **1**, raised whenever the card's words change; "New chat" asks "Start a new chat? This one isn't kept." with "Start new chat" and "Cancel" (copy review); the browser's own leave-page warning shows while a conversation has at least one answer.
- Boards: pilot style (FE-29 to FE-33, FE-42), light first then dark twins (FE-31's slate ink), phone 390 px and desktop 1440 px, 44 px targets, "Sample data" on each board, postcodes from `packages/fixtures/data/postcode-area.json` (NB1 4XY, NB7 1RR).
- Dated records (reviews, earlier plans and designs) are not edited; live documents are.
- Commit prefix `docs:`; no agent attribution. `make check` before every push; a fresh-context Opus review (Code Review Rules) before every push, plus `code-security-reviewer` on PR B and `visual-reviewer` on PR C.
- Canvas publishing: read the whole artifact first; if a publish is refused or blocked, ask the founder before the main session publishes (lesson of 19 Nov 2026).

## Review Focus
1. **A scenario number lost or duplicated in the move:** the WCHAT numbers in `chat.feature` plus `chat-signed-in-later.feature` equal WCHAT-01 to WCHAT-111 plus the new ones, each once; Task 4 step 5 checks it with a grep count.
2. **AI-03 cases pointing at moved scenarios** (the set cites WCHAT-42, WCHAT-51, WCHAT-52, WCHAT-93 and WCHAT-110): a case must not test a feature the pilot no longer has; Task 4 step 6 handles them.
3. **A visitor on a shared connection arriving to "paused for today"** having sent nothing: the line must not blame them; Task 4's pause scenarios include it.
4. **The consent tap pressed twice, or on a slow phone past ALTCHA's 90-second timeout:** one receipt, one check, then "Try again" with the cause; Task 4's consent scenarios pin both.
5. **Reload or a new tab mid-conversation:** the consent card again, no area, no earlier messages, nothing read from storage; Task 4 pins it.

---

## PR A: design, plan and records

### Task 1: Records and pull request A

**Files:**
- Already written: the design and this plan.
- Modify: `docs/decisions/README.md` (new lines **FE-85** the chat's own page and entry points, **FE-86** the consent card with the bot check on the tap, **FE-87** comparison progress and the warning before a comparison, **FE-88** the pause lines and their order; dated notes on SE-10, AI-16 and IN-05), `docs/decisions/0063-pilot-privacy-and-anonymous-chat-first.md` (dated note: own page, card before the chat, entry points), `docs/decisions/0064-pilot-chat-ai-multi-agent-claude-langsmith.md` (dated note: a comparison with 1 or 2 left uses what's left; the warning on compare), `docs/planning/status.md`.

- [ ] **Step 1:** Write FE-85 to FE-88, each quoting the founder's prompt-window answer from the design ("Own chat page (Recommended)", "Card before the chat (Recommended)", "Allow, use what's left", "Show on compare (Recommended)") and marking the agent's calls.
- [ ] **Step 2:** Pre-flight: grep for "signed-in chat", "workspace chat", "Ask about this area", "15 messages per account", "30 days", "sign in", "Better Auth" across live docs; list what PR C fixes and fix only records here.
- [ ] **Step 3:** Status file: item 0 says the design and plan are done and PR B and PR C are next.
- [ ] **Step 4:** `make check`. Expected: every step passes.
- [ ] **Step 5:** Fresh-context Opus review (Code Review Rules); fix; commit `docs: anonymous chat design, plan and register lines`; push; open the PR (`pr` skill); `@codex review`.

## PR B: decision 0065 and the Privacy notice (founder merge)

### Task 2: Decision 0065 and rule 5

**Files:**
- Create: `docs/decisions/0065-controller-name-in-the-privacy-notice.md`
- Modify: `AGENTS.md` rule 5 (one clause: "except the controller's name in the Privacy notice, decision 0065"), `docs/decisions/README.md` (0065 in the index; a register line SE-11).

- [ ] **Step 1:** 0065: context (Article 13(1)(a) "the identity and the contact details of the controller", legislation.gov.uk, read 21 Nov 2026; rule 5; the public repository), options (filled in at deploy, the agent's recommendation; exception to rule 5; ask later), decision (founder, 21 Nov 2026, prompt windows: "Exception to rule 5", the full name as on the founder's commits, contact privacy@vestagraph.co.uk), consequences (the name is in the public history for good; only these files may carry it; revisit if the controller changes, for example a company).
- [ ] **Step 2:** AGENTS.md rule 5 clause; register line SE-11.
- [ ] **Step 3:** Commit `docs: 0065, the controller's name in the Privacy notice`.

### Task 3: Privacy notice scenarios and board

**Files:**
- Modify: `docs/specs/pilot/public-pages.feature` (PRIV scenarios), the canvas section "Pilot 9 · Public pages" (the Privacy board, light and dark).

- [ ] **Step 1:** Rewrite PRIV-08 (ALTCHA: a self-hosted proof-of-work check on the consent tap, no cookies, no outside company) and PRIV-13 (no sign-in in the pilot; real chats' words 14 days in our Neon database, gone from its 7-day history a week later; words-free traces in LangSmith EU), keeping their numbers.
- [ ] **Step 2:** New PRIV scenarios (numbers after the file's last): the controller's name and privacy@vestagraph.co.uk (Article 13(1)(a)); purposes and lawful basis per processing (legitimate interests; explicit consent for special category details) (13(1)(c)); Anthropic, US or "global" processing, the DPA's UK Addendum (13(1)(f)); keeping periods (Anthropic within 30 days, flagged up to 2 years; ours 14 days; Neon's history 7 days) (13(2)(a)); withdrawing consent: stop, and email to have kept words deleted, found case by case (13(2)(c), Article 11(2)); the right to complain to the ICO with its link (13(2)(d)); the IP address used in memory for the day's count and never stored. Each scenario's Then-lines name the fact, not final wording.
- [ ] **Step 3:** Mark these scenarios as a launch blocker for the public chat in the file's header (design section 5).
- [ ] **Step 4:** Redraw the Privacy board's chat section and controller block, light then dark; visual check in Chrome at 390 and 1440 px; record the canvas version in the header.
- [ ] **Step 5:** `make check`; fresh-context Opus review plus `code-security-reviewer`; fix; commit `docs: Privacy notice for the anonymous chat`; push; open the PR with the copy-review list and "Founder merge (rule 5, 0065)"; `@codex review`.

## PR C: the chat's specification and boards

### Task 4: The chat's specification, changed in place

**Files:**
- Rename: `docs/specs/pilot/workspace-chat.feature` → `docs/specs/pilot/chat.feature` (`git mv`, so history follows).
- Create: `docs/specs/pilot/chat-signed-in-later.feature`.
- Modify: references to the old file name in live docs (`docs/specs/README.md`, `area-chat.feature`, `area-card.feature`, `account.feature`, `sign-in.feature`, `.design/prototype/INFORMATION_ARCHITECTURE.md`, `docs/decisions/README.md`).

**Interfaces:**
- Produces: the "Required states" header in `chat.feature`, mapping every state below to its scenario, which Task 6's boards cite.

- [ ] **Step 1:** Sort every WCHAT scenario into kept, rewritten or moved, starting from the design's section 6 lists, and write the sort as a table in this task's "As done" note. A scenario is moved only if it needs an account, saved areas, past chats or history.
- [ ] **Step 2:** Move the sign-in-only scenarios unchanged; the later file's header: "Kept for when sign-in opens (0063 point 2); not part of the pilot."
- [ ] **Step 3:** Rewrite `chat.feature`'s header (where: the chat page without a sidebar; entry points; no history; the consent card; the caps and their order; the fixed texts) and the rewritten scenarios: the count per IP address (WCHAT-23 to WCHAT-26, WCHAT-95, WCHAT-111, WCHAT-74, WCHAT-77), traces (WCHAT-59, WCHAT-63), first visit (WCHAT-06), "Ask more about this" with no sign-in (WCHAT-55, WCHAT-105), the pause on arrival in place of the entry-point pause line (WCHAT-56), nothing in any browser storage (WCHAT-66, WCHAT-75).
- [ ] **Step 4:** New scenarios from WCHAT-112, one per state: the consent card blocks the box and starts; one tap, "Checking…", the chat opens, one receipt with time and statement version; a double tap makes one receipt; check failed and timed out show "Try again" with the cause; Web Crypto missing; JavaScript off; the re-check failing keeps the message in the box; the receipt is sent with each message and written with each trace; arriving while paused shows the pause line and makes no receipt and no check; pause precedence (one scenario per pair that can meet); the daily cap at £2.50 and its own line; a shared connection already at 15; a comparison with 2 left runs and the count reaches 0, never below; "Uses up to 3 · 2 left today" on compare actions when 3 or fewer are left; a comparison that doesn't fit the day's budget while a single question does; the progress list, each step announced once; Stop during a step; "Ask about this council"; no "Ask about this area" on not-covered or not-found results; "New chat" keeps consent and count, resets the turn limit, stops a streaming answer, focus in the box; reload or new tab starts again; the leave-page warning while a conversation has an answer; the re-check after every 5 messages; the "New chat" confirmation; the empty panel with no area; Back returns to the area result through the in-memory hand-over; focus goes to the card heading on arrival, the button's label change is announced once and focus stays on it; "Privacy notice" opens in a new tab, says so in its name and leaves the conversation as it was; ALTCHA's image-code fallback stays off; a pause for everyone reached mid-conversation keeps the message in the box and counts nothing; "New chat" keeps the area in the panel; the line above the message box with 3 or fewer left.
- [ ] **Step 5:** Check numbering: `grep -ohE "WCHAT-[0-9]+" docs/specs/pilot/chat.feature docs/specs/pilot/chat-signed-in-later.feature | grep -v "Replaces" | sort | uniq -d` prints nothing from the Scenario lines, and every number from WCHAT-01 to the last appears once as a Scenario.
- [ ] **Step 6:** AI-03 set: for each case citing WCHAT-42, WCHAT-51, WCHAT-52, WCHAT-93 or WCHAT-110, read `packages/fixtures/evaluation/ai-03-set.json`'s schema; if it has a status or scope field, mark the case for later in a set version 3; if it has none, leave the file and open a `noticed` issue (no schema change in this plan).
- [ ] **Step 7:** `make test`. Expected: PASS (the runner parses both files; `@ui` deselected).
- [ ] **Step 8:** Commit `docs: the chat specification for the anonymous chat`.

**As done (21 Nov 2026).**

*Step 1, the sort.* 111 scenarios: **54 kept**, **32 rewritten** (same numbers), **25 moved** unchanged to `chat-signed-in-later.feature`; **53 new** (WCHAT-112 to WCHAT-164). Check (step 5): no number appears twice as a `Scenario:` across the two files, and WCHAT-01 to WCHAT-164 each appear once.

| Sort | Scenarios | Why |
|---|---|---|
| Kept (only "a signed-in user" became "a visitor", and "workspace page" became "chat page") | WCHAT-02, WCHAT-04 to WCHAT-05, WCHAT-09 to WCHAT-10, WCHAT-12 to WCHAT-22, WCHAT-30 to WCHAT-39, WCHAT-54, WCHAT-58, WCHAT-60 to WCHAT-62, WCHAT-65, WCHAT-67 to WCHAT-73, WCHAT-76, WCHAT-78 to WCHAT-82, WCHAT-84, WCHAT-86 to WCHAT-88, WCHAT-90 to WCHAT-91, WCHAT-99, WCHAT-102, WCHAT-108 | Streaming, guards, sources, widgets, injection, logs, limits at the server, accessibility, the fixed reply and its count. WCHAT-02, 04, 05 (side panel, modal sheet) and WCHAT-54, 86 to 88, 99 (widget actions) also need no account. |
| Rewritten, same number | WCHAT-01, WCHAT-03, WCHAT-06, WCHAT-08, WCHAT-11, WCHAT-23 to WCHAT-29, WCHAT-55 to WCHAT-56, WCHAT-59, WCHAT-63, WCHAT-66, WCHAT-74 to WCHAT-75, WCHAT-77, WCHAT-83, WCHAT-85, WCHAT-89, WCHAT-92, WCHAT-95 to WCHAT-97, WCHAT-105 to WCHAT-107, WCHAT-109, WCHAT-111 | WCHAT-01, 03: no sidebar. WCHAT-06: the consent card first. WCHAT-08: the disclaimer says 14 days and no personal details, adds "New chat". WCHAT-11: a reload no longer reopens a chat. WCHAT-23 to 26, 95, 111, 74, 77, 29, 85: the count is per IP address, in memory. WCHAT-27, 28, 56: the pause on arrival, the fail-closed cases. WCHAT-55, 105, 106, 66: no sign-in. WCHAT-59, 63: kept 14 days in Neon, words-free in LangSmith. WCHAT-75: nothing in any browser storage. WCHAT-83, 89, 92, 96, 97, 107, 109: Save, Update, sidebar, signed-out state or account wording removed (WCHAT-109's example is now "Comparing…", the label wording approved on 18 Nov 2026 stands). |
| Moved unchanged (text identical, same `@ui` tags, no new tag) | WCHAT-07, WCHAT-40 to WCHAT-53, WCHAT-57, WCHAT-64, WCHAT-93 to WCHAT-94, WCHAT-98, WCHAT-100 to WCHAT-101, WCHAT-103 to WCHAT-104, WCHAT-110 | Need an account (WCHAT-07, 93, 94), saved areas (WCHAT-47 to 53), past chats and history (WCHAT-40 to 46, 57, 64, 98, 100, 101, 103, 104, 110). The same set as the design's list; the sort adds none. |

Calls made in the sort (not in the design's lists): WCHAT-01, 03, 08, 11, 28, 83, 85, 89, 92, 96, 97, 107 and 109 were rewritten because they still said sidebar, sign-in, saved areas, a stored chat or a signed-out state; the design's list did not name them. WCHAT-27 was rewritten to show the pause in place of the consent card, as design section 3 says.

*Steps 3 and 4, the new scenarios* are WCHAT-112 to WCHAT-164: the consent card and the tap (WCHAT-112 to WCHAT-113, WCHAT-114, WCHAT-115 to WCHAT-119), the re-check (WCHAT-120, WCHAT-121), the receipt (WCHAT-122), the pauses (WCHAT-123 to WCHAT-127), the 15 pairs of the pause order (WCHAT-128 to WCHAT-142), comparisons (WCHAT-143 to WCHAT-147), progress (WCHAT-148, WCHAT-149), entry points (WCHAT-150 to WCHAT-153), the empty panel (WCHAT-154), "New chat" (WCHAT-155 to WCHAT-158), reload and leave-page (WCHAT-159, WCHAT-160), Back (WCHAT-161), focus and announcements (WCHAT-162, WCHAT-163) and the Privacy notice link (WCHAT-164).

*Proposed wording for the copy review* (every other quoted text is approved or already in a record):
- The consent card's words (WCHAT-112): the facts of design section 7, first point; the button "Agree and start chat", then "Checking…", then "Try again" with a cause ("took too long"; "this browser can't run the check").
- Daily cap line, for everyone (WCHAT-124): "The chat has reached today's limit for everyone and is paused until midnight. The area check still works" (design section 3).
- A comparison that doesn't fit the day's budget (WCHAT-147): "A comparison needs more of today's budget than is left. Single questions still work."
- Compare actions with 3 or fewer left (WCHAT-145): "Uses up to 3 · N left today"; the line above the message box (WCHAT-146): "N left today · a comparison uses up to 3" (design section 3).
- Progress steps (WCHAT-148): "Looked up NB1 4XY", "Looked up NB7 1RR", "Writing the comparison…", "Checking the figures" (design section 4).
- "New chat" confirmation (WCHAT-158): "Start a new chat? This one isn't kept.", "Start new chat", "Cancel" (plan Global Constraints).
- "Privacy notice, opens in a new tab" (WCHAT-164), the header disclaimer (WCHAT-08: messages kept 14 days, no personal or health details) and "Comparing…" (WCHAT-109's example).

*Step 6, AI-03.* `packages/fixtures/evaluation/ai-03-set.json` (schema `packages/fixtures/schema/ai-03-set.schema.json`, `version` const 2, `additionalProperties: false`) has no status or scope field, so the file is unchanged. Nine cases cite moved scenarios: CHAT-STALE-01 (WCHAT-42), CHAT-STALE-02 (WCHAT-110), CHAT-SAVED-OWN-01 and CHAT-SAVED-OWN-02 (WCHAT-51, 93), CHAT-TOOLS-SAVED-COMPARE-01 (WCHAT-51, 52), CHAT-COMPARE-POSTCODES-01 (WCHAT-52, with WCHAT-86), CHAT-INJECT-SAVEDAREA-01 (WCHAT-51, with WCHAT-20), CHAT-SAVED-OTHERUSER-01 and CHAT-INJECT-SAVED-OTHERUSER-01 (WCHAT-51, 93). A `noticed` issue is for the main session to open.

### Task 5: Entry points and stale documents

**Files:**
- Modify: `docs/specs/screens/01-landing.feature` (the chat link beside the postcode box), `docs/specs/screens/14-check-an-area.feature` and `docs/specs/screens/04-nearby.feature` ("Ask about this area"), `docs/specs/pilot/city-explorer.feature` ("Ask about this council"), `docs/specs/pilot/area-topics.feature` ("Ask more about this", CHAT-52's successor), `docs/specs/pilot/sign-in.feature` and `account.feature` (header: kept for later, 0063), `docs/product/04-project-goals-and-delivery.md`, `docs/architecture/README.md`, `.design/prototype/INFORMATION_ARCHITECTURE.md` (the `/chat` route; `/sign-in` and `/account` later).

- [ ] **Step 1:** One scenario per entry point: shown on a covered result, opens the chat with that area in the panel, carries no postcode in the address; not shown on not-covered or not-found results; still shown when the chat is paused.
- [ ] **Step 2:** Headers and live docs that still describe the signed-in chat in the pilot.
- [ ] **Step 3:** `make test`. Expected: PASS. Commit `docs: chat entry points and stale sign-in references`.

**As done (21 Nov 2026).** New entry-point scenarios: LAND-27 and LAND-28 (landing link, shown when paused), AREA-51 to AREA-53 (Check an area), NEAR-17 (Nearby and Nearby > Schools), CITY-114 (council page); the chat's own are WCHAT-150 to WCHAT-153. Pointers and stale statements fixed in: `sign-in.feature` and `account.feature` (headers: kept for later, 0063), `area-topics.feature` (TOPIC-24 comment), `area-tools.feature`, `report-a-problem.feature` (REPORT-05, REPORT-08, header), `area-card.feature` and `area-chat.feature` (pointers only; withdrawn scenarios untouched), doc 04, `docs/architecture/README.md`, `docs/planning/backlog.md`, `docs/references/third-party.md` (Better Auth was already marked deferred), doc 05 and `.design/prototype/INFORMATION_ARCHITECTURE.md`. Not edited, left for the founder or another task: the landing FAQ answer LAND-19 (approved wording, "unless you sign in and save an area"), the landing's "Coming next, with a free account" section (LAND-05), and the Privacy notice scenarios in `public-pages.feature` (PR B). The status file is not edited here (Task 7).

### Task 6: Canvas boards

**Files:** the design canvas: a new page "Pilot · Anonymous chat"; "Pilot · Signed-in chat" boards moved to "Home workspace (later)"; entry-point changes on the existing area result, Nearby, City Explorer and landing boards.

- [ ] **Step 1:** Read the whole canvas and the Brand and style boards.
- [ ] **Step 2:** Draw, light first: `AnonChatDesktop` and `AnonChatPhone` (NB1 4XY loaded, an answer with its widget and stamps); `AnonChatConsent` (the card on phone and desktop, its three button states, "Try again" with a cause, no area loaded); `AnonChatCompare` (NB1 4XY with NB7 1RR: the progress list mid-way, then the answer; the "Uses up to 3 · 2 left today" warning); `AnonChatStates` (each pause line in its place, arriving while paused, unavailable, JavaScript off, the empty panel). Every line quoted from Task 4's scenarios or the sample data.
- [ ] **Step 3:** Dark twins; move the signed-in boards; add the entry points to the existing boards.
- [ ] **Step 4:** Visual review in Chrome at 390 and 1440 px (`visual-reviewer`) and the competitor benchmark checklist; fix; re-check; record the canvas version in `chat.feature`'s header and write "As drawn" under this task.

**As drawn (21 Nov 2026, canvas version 438; steps 1 to 3 done, step 4 (the visual review) is open).**

*New page "Pilot · Anonymous chat"*, light boards with a Dark twin each (the dark ones 8000 px to the right, as on the other pages). Every board carries the "Sample data: a made-up town" badge, uses 44 px targets, and quotes its lines from `chat.feature` or the sample data (NB1 4XY and NB7 1RR in `postcode-area.json`; the "1.5 miles" and "2.9 miles" in the compare table are the earlier signed-in board's display of 2,400 m and 4,600 m). The "Required states" header of `chat.feature` now maps each state to its board and frame.
- `AnonChatDesktop` (1504 wide): NB1 4XY loaded, an answer with its Nearby card and source stamps, header with the AI badge, display control and "New chat", the side panel as a region, no sidebar.
- `AnonChatPhone` (924 wide, two 390 px frames, like the earlier compare boards): the chat, and "Open full result" as a modal sheet.
- `AnonChatConsent` (1504 wide): the card on desktop (frame 1) and phone; the button ready, "Checking…" (a pulsing waiting dot, no spinner), "Try again" with "Took too long" and with "This browser can't run the check"; the no-area card with the empty panel (desktop and phone).
- `AnonChatCompare` (1504 wide): NB1 4XY with NB7 1RR, the progress list mid-way (desktop and phone), the answer with the table, "Uses up to 3 · 2 left today" on "Compare another area" and "Compare with…", and "2 left today · a comparison uses up to 3" above the box.
- `AnonChatStates` (1864 wide, 13 frames): "1 message left today"; the own-15 pause; the daily cap for everyone (the message stays in the box); the monthly cap and a shared connection at 15, both on arrival in place of the card with "Back to the area result"; unavailable; a comparison that doesn't fit the budget; JavaScript off; the turn limit; the rate limit; the failed re-check; the "New chat" confirmation; the empty panel on desktop with the suggested starts.

*Moved:* every "Pilot · Signed-in chat" board and note is now on "Home workspace (later)", below the existing boards (y from 20000), unchanged (the page of that name is gone, since it is empty). The teal note there says why.

*Entry points added* (light and dark): "Ask about this area" with its AI badge on `MapDesktop` (the Nearby list), `MapPhone` (a 44 px icon button in the header, named "Ask about this area, AI"), `TopicPanelSchools` and `TopicSheets` (Schools); "Ask about this council" beside Share on `CouncilPage` and `CouncilPageDesktop`; the chat link "Ask about an area in the chat" beside the postcode box on `Landing` and `LandingPhone`. `AreaResult` and `AreaResultDesktop` already carried "Ask about this area" (no sign-in wording), so they are unchanged.

*Not drawn, and why:* "Ask more about this" (WCHAT-55, 105, 106, 56, 76, 77) on a topic panel: no pilot board has it, so it stays for a later pass; the source-failed and tool-failed states (WCHAT-31, 32) are unchanged on the earlier signed-in board; the guard-stopped sentence is never shown, by design; the consent receipt, the re-check that passes and "New chat" keeping the count are behaviour, not screens. Frame 11's cause line and several state titles ("This chat has reached its limit", "The chat needs JavaScript", "Back to the area result") are proposed wording for the copy review.

*Proposed wording for the copy review* (not approved): the card's words, "Took too long", "This browser can't run the check", the header disclaimer, the daily-cap line, the step names, the 2-left lines, "Ask about an area in the chat" and the lines named above.

### Task 7: Records and pull request C

**Files:** `docs/decisions/README.md` (notes on FE-85 to FE-88 with the board names), `docs/planning/status.md`.

- [ ] **Step 1:** Pre-flight grep for "workspace-chat", "Signed-in chat", "Ask about this area", "WCHAT-", "per account"; fix anything stale in live docs.
- [ ] **Step 2:** Map each design requirement and section 7 edge case to its scenario in the PR description; `make check`; fresh-context Opus review (Code Review Rules) plus `visual-reviewer`; fix findings.
- [ ] **Step 3:** Push; open the PR with the copy-review list (every proposed line); `@codex review`. After the founder's copy review, apply the approved wording in one commit and ask for one re-review.
