# Stage 5b: the anonymous chat's design step: design

**Date:** 21 Nov 2026  
**Status:** Approved (founder, 21 Nov 2026, prompt window: "Approve (Recommended)")  
**Follows:** [0063](../../decisions/0063-pilot-privacy-and-anonymous-chat-first.md) ("What is left": a design step for the anonymous chat's screens) and [0064](../../decisions/0064-pilot-chat-ai-multi-agent-claude-langsmith.md) (the chat's AI).  
**Next:** the design review for UI work (`design-reviewer`, AGENTS.md step 1b), then the plan (`writing-plans`).

## Intent and why
The pilot's chat opens to everyone without sign-in (0063). The reason is the founder's, from 0058 and kept in 0063: the chat is the part of the pilot that shows AI-engineering and forward-deployed-engineer skills, and an anonymous chat can be tried by anyone at once. The signed-in chat's boards and scenarios passed the pilot gate (0052), but they assume an account: a sidebar of saved areas and past chats, sign-in before the chat, 12-month history, and a count per account. This step redesigns the chat for an anonymous visitor and settles what they see before their first message, while a comparison runs, and when a limit is reached. It also brings the Privacy notice up to date with 0063 and 0064.

## Goals
- A chat page an anonymous visitor reaches from the area pages in one tap, with the area already loaded.
- Explicit consent before the first message, in a button whose own label gives it (0063 point 5), with the bot check running on the same tap.
- Clear, truthful states for the limits: the visitor's own 15 a day, the £2.50 daily cap and the £25 monthly cap (0064), and fail-closed "unavailable".
- Visible progress while a comparison's team of agents works (0064 point 1).
- The Privacy notice names Anthropic and LangChain, the 14-day keeping period and Neon's 7-day history, and the controller's identity.
- One home for every scenario: the signed-in chat's work is kept for when sign-in opens, not copied.

## Non-goals
- Sign-in, accounts, saved areas and chat history (deferred by 0063).
- The chat's AI flow, provider, models and caps: settled in 0064.
- Final wording: every quoted text below is proposed until the founder's copy review, except the fixed texts already approved (FE-55, FE-61, FE-66).
- The build itself (the plan after this).

## Anti-goals (a failure even if it works)
- Consent that a visitor can miss, or that is assumed from typing or reading.
- Any chat state written to the visitor's device (no cookies, no local storage; 0063).
- A pause that reads as the visitor's fault when it is everyone's (the daily or monthly cap).
- A limit or count shown below zero, or a missing count shown as a full one (rule 7).
- The area pages depending on the chat: when the chat is paused or down, search, results and City Explorer work as before.

## Constraints
- AGENTS.md rules 1 to 9, especially rule 4 (never "verified", "safe" or "approved"; AI never calculates numbers), rule 5 (public repository; changed for one item by the new decision below) and rule 7.
- 0063: 15 messages per IP address per day, counted in memory, reset at midnight UK time; ALTCHA self-hosted; fail closed; nothing on the device; explicit consent with a consent receipt per trace.
- 0064: a comparison counts as 3 messages (amended below for a low balance); at most 3 areas; the £2.50 daily and £25 monthly caps with reserve-before-call; words kept 14 days in Neon, words-free traces in LangSmith.
- The pilot's design bar (doc 04, stage 5b) and the competitor benchmark checklist apply to every board.
- Accessibility as the signed-in chat: keyboard alone (WCHAT-61), announcements once per answer (WCHAT-62), actions at least 44 px, no spinners (WCHAT-109).

## Approaches considered

### Where the chat lives (founder's choice)
| | Own chat page (chosen) | Drawer on each page | Drawer that expands |
|---|---|---|---|
| What it is | A `/chat` page: chat in the middle, the full result in a right panel (a sheet on a phone); no sidebar | The chat slides over the area result, City Explorer and the landing, like the withdrawn on-page chat (0056) | A drawer on the result that can open into the full page |
| Reuse | Most of the drawn boards and WCHAT scenarios | Little; a drawer for every page type | Both layouts to design and test |
| The conversation | Lasts while the visitor stays on the page | Ends on moving to another page unless extra code carries it | As the drawer, plus a hand-over between layouts |

Founder, 21 Nov 2026, prompt window: **"Own chat page (Recommended)"**.

### The consent step (founder's choice)
- **Card before the chat (chosen):** a short card opens the chat; the message box and suggested starts work after one tap on the consent button.
- **Consent on first Send:** the visitor types first; the first Send reads "Agree and send". Quicker, but suggested starts and "Ask about this area" each need their own consent wording, and consent is easier to miss.
- **Don't keep the words:** reverse part of 0063 and 0064 so real chats' words are not stored. Loses the ability to read what went wrong in a real chat, and messages still pass through Anthropic, so the consent question does not fully go away (not checked).

The founder first asked (typed): "we are not a health startup, how is it our fault that user is putting sentsitive info even with disclaimer?" [sic]. The agent answered from the ICO's pages, read on 21 Nov 2026: information that "clearly reveals or concerns" one of the special categories is special category data ([what is special category data](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-is-special-category-data/)); the intent test applies to inferences, not to details a person states; and "There are no other exemptions from article 9" beyond the public interest one for journalism, academia, art or literature ([the rules](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-are-the-rules-on-special-category-data/)). The ICO's pages say nothing directly about details a visitor volunteers, or about warnings, so "we still need a condition" is the agent's reading, not an ICO statement about chatbots; a data protection lawyer could confirm it. The warning still helps as data minimisation. Founder, prompt window: **"Card before the chat (Recommended)"**.

### How the existing documents change (founder's choice)
- **Change in place (chosen):** `docs/specs/pilot/workspace-chat.feature` becomes the anonymous chat's file. Scenarios that fit keep their WCHAT numbers, changed ones are rewritten keeping their numbers, and the sign-in-only ones move unchanged to a "later" file. Boards: anonymous chat boards on the pilot page; the signed-in boards move to "Home workspace (later)". Each scenario has one home, as 0058 did for the CHAT scenarios.
- **New file, copy shared:** about 80 scenarios would exist twice and drift apart.
- **New file, differences only:** Gherkin files can't include each other, so the tests would run the signed-in file as the anonymous chat.

Founder, prompt window: **"Change in place (Recommended)"**, after typing "options should be in prompt window with recommendations, you keep forgetting your instructions" when the agent first wrote these options as chat text (logged on agent-workflows#31).

## Decisions

### 1. The chat page
```text
Desktop (1440)                              Phone (390)
┌──────────────────────┬─────────────────┐  ┌──────────────────┐
│ AI badge · header    │ Area result     │  │ AI badge · header│
│ chat (centre)        │ panel (region)  │  │ chat             │
│  … answers, widgets  │                 │  │ [Open full result]│ → modal sheet
│ [ message box ]      │                 │  │ [ message box ]  │
└──────────────────────┴─────────────────┘  └──────────────────┘
```
- **Layout:** as the signed-in chat (WCHAT-01 to WCHAT-05) without the sidebar. The right panel shows the full result the chat is discussing; on a phone "Open full result" opens it as a modal sheet.
- **Header:** the AI badge and FE-13's line, the display control (FE-59), and **"New chat"**, which clears the tab's conversation after a confirmation that nothing is kept (*agent's call*; there is no history to go back to).
- **Entry points:** "Ask about this area" on each area result (Check an area, Nearby, Nearby › Schools); a link beside the postcode box on the landing, which opens the chat empty with suggested starts; and **"Ask about this council"** on each City Explorer council page (*agent's call*: the chat already has the council tools, and 0063 names "each result"). "Ask more about this" under a topic (AI-12, CHAT-52) opens the chat on that topic. No entry carries the postcode or question in the address (WCHAT-66); the area is handed over in the page's memory.
- **When the chat is paused or down, the entry points still show** (*agent's call*, builder check): the area pages never ask the chat for its state, so they cannot fail because of it (anti-goal). The chat page shows the pause on arrival. WCHAT-56 (the pause line in place of "Ask more about this") is rewritten to match.
- **No history:** the conversation lives in the tab's memory; closing the tab ends it (0063). So consent is asked once per tab.

### 2. The consent card (founder: "Card before the chat (Recommended)")
```text
┌───────────────────────────────────────────────┐
│ AI  Ask about NB1 4XY                          │
│ Answers come from official sources, written   │
│ by AI (Anthropic's Claude). Your messages,     │
│ including any health or personal details you   │
│ type, go to Anthropic (processed in the US),   │
│ which deletes them within 30 days (flagged     │
│ content up to 2 years). We keep them 14 days   │
│ to fix problems. Please don't share personal   │
│ or health details. You can withdraw: stop, and │
│ email privacy@ to delete.  Privacy notice ↗    │
│                                                │
│ 15 messages a day. A comparison uses up to 3.  │
│        [ Agree and start chat ]                │
└───────────────────────────────────────────────┘
```
- The card is the chat's first state; the message box and suggested starts are not usable until the tap. The words are proposed for the copy review, which may shorten them but keeps every fact in section 7's first point (design review, P1); the button's own label must carry the agreement (0063).
- **The bot check runs on the same tap:** ALTCHA's widget has an `invisible` display and a `verify()` method ([ALTCHA v3.5.0 README](https://github.com/altcha-org/altcha/blob/v3.5.0/README.md)), so the proof-of-work runs with nothing extra on screen. The button reads "Agree and start chat", then "Checking…", then the chat opens; if the check fails, "Try again" with a plain cause (*agent's call*, WCHAT-109's no-spinner rule).
- **The consent receipt** (0063) records the time and the statement version shown; the version changes whenever the card's words change. Since nothing is kept on the device or in a session, the tab holds the receipt in memory and sends it with each message, and the server writes it with each trace (design review; the plan sets the format).
- ALTCHA runs again, invisibly, after a set number of messages (0063; the number is the plan's).

### 3. Limits and pauses
| State | Text (status) |
|---|---|
| After message 14 | "1 message left today" (FE-55, approved) |
| The visitor's 15 used | "Chat is paused for today, the area check still works" (approved) |
| £2.50 daily cap reached, for everyone | "The chat has reached today's limit for everyone and is paused until midnight. The area check still works" (new; copy review; "busy" dropped as untrue for a spending cap, design review) |
| £25 monthly cap reached | "Chat is paused for this month, the area check still works." (FE-61, approved) |
| Bot check or limiter down | "Chat unavailable right now" (FE-66, fail closed) |

- **Arriving while paused or down** (*agent's call*, builder check): the pause or unavailable line shows in place of the consent card, with the way back to the area result; no consent receipt is made and no bot check runs for a chat that can't run.
- **Which line wins** when several apply (*agent's call*): unavailable, then the monthly cap, then the daily cap, then the visitor's own 15, so a visitor never sees their own-limit line when everyone is paused.
- **The daily cap** pauses when a day's spend reaches £2.50, as 0064 point 5 records (the founder's choice; reserve-before-call means no call can take it over), while the monthly cap pauses at 95% of £25 as 0064 says; the daily cap resets at midnight Europe/London, the same as the 15-a-day count (WCHAT-26, WCHAT-95, WCHAT-111) (*agent's call*).
- **What counts as a comparison:** a comparison from the classifier, from "Compare with…" or "Compare another area" (which call the compare tool directly, 0064), and Regenerate on a comparison each count as up to 3 (*agent's call*).
- The visitor's own pause and everyone's pause use different words, so nobody thinks they did something wrong (*agent's call*).
- **A comparison with 1 or 2 messages left** (founder, prompt window: **"Allow, use what's left"**, over the agent's "Refuse, explain"): the comparison runs and counts only the messages left, so the count reaches 0 and never goes below it. This amends 0064 point 2 for a low balance; the £2.50 daily cap and the reserve-before-call guard still bound the cost. The card says "A comparison uses up to 3" (*agent's call* for the proposal).
- **A warning before a comparison** (founder, 21 Nov 2026, prompt window: **"Show on compare (Recommended)"**, after the design review found a comparison can jump past FE-55's warning): when 3 or fewer messages are left, the compare actions show "Uses up to 3 · N left today" (for example "· 2 left today"), and a line above the message box says "N left today · a comparison uses up to 3", so a visitor who types a comparison is warned too (*agent's call* for the line above the box, pre-push review: 0064 sends a typed comparison straight to the team, with no confirmation step); wording for the copy review.
- **A comparison that doesn't fit the day's remaining budget** while a single question would (design review): that comparison gets the daily-cap line for comparisons only, and single questions keep working; the plan sets the exact text and test.

### 4. Progress while a comparison runs
```text
✓ Looked up NB1 4XY
✓ Looked up NB7 1RR
● Writing the comparison…
○ Checking the figures
```
- The team's steps show as a short list under the question, each step announced once to screen readers, never word by word (WCHAT-62) (*agent's call*). The writer's sentences then stream as any answer; a sentence the checker stops never appears (WCHAT-10).
- Stop works at every step and keeps what is shown; the counting rules for a stopped answer carry over (WCHAT-108).

### 5. The Privacy notice
- **New content** (from 0063 and 0064): the chat section names Anthropic (US or "global" processing, deleted within 30 days, flagged content up to 2 years) and LangChain (Netherlands; words-free trace data only); real chats' words kept 14 days in our own Neon database (Frankfurt), gone from Neon's 7-day history a week later; the IP address used in memory for the day's count and never stored; explicit consent for special category details and how to withdraw it (stop using the chat, and email privacy@ to have the kept words deleted: withdrawing consent removes the Article 9 condition, so a request to delete is acted on whenever the trace can be found, case by case, UK GDPR Article 11(2)); ALTCHA sets no cookies. Plus section 7's Article 13 items. **Launch blocker:** the chat doesn't go public until the notice has all of these (design review, P1).
- **The controller's identity** (founder, prompt window: **"Exception to rule 5"**, over the agent's "Filled in at deploy"): UK GDPR Article 13(1)(a) requires "the identity and the contact details of the controller" ([legislation.gov.uk](https://www.legislation.gov.uk/eur/2016/679/article/13), read 21 Nov 2026), so an email address alone is not enough. The founder's name is written into the notice in the repository. Rule 5 is an integrity rule, so this needs its own decision record (**0065**, below); the founder's name will be in the public history for good. **Form and contact** (founder, 21 Nov 2026, prompt window): the founder's full name as on their commits ("(Recommended)"), and the contact **privacy@vestagraph.co.uk** ("privacy@vestagraph.co.uk (Recommended)"; IN-06 registered both domains). The name itself is written only in 0065's pull request, not in this design.
- **0065 ships in its own pull request** (*agent's call*, builder check): the rule 5 exception and the name in the notice are a founder merge, so the boards and scenarios don't wait on it.
- The PRIV scenarios in `public-pages.feature` and the notice's board are updated to match.

### 6. The documents (founder: "Change in place (Recommended)")
- **`workspace-chat.feature`** becomes the anonymous chat's file, renamed to `chat.feature` with the same WCHAT numbers (*agent's call*: "workspace" names the signed-in page). Its header loses sign-in and gains the consent card, entry points and caps.
- **Kept as they are** (streaming, guards, sources, widgets, injection, logs, accessibility): for example WCHAT-09 to WCHAT-22, WCHAT-30 to WCHAT-39, WCHAT-58, WCHAT-60 to WCHAT-62, WCHAT-67 to WCHAT-92.
- **Rewritten, same numbers:** the count per IP address instead of per account (WCHAT-23 to WCHAT-26, WCHAT-95, WCHAT-111, WCHAT-74, WCHAT-77); traces kept 14 days in Neon and words-free in LangSmith (WCHAT-59, WCHAT-63); WCHAT-06 (first visit shows the consent card); WCHAT-55 and WCHAT-105 ("Ask more about this" opens the chat, no sign-in); WCHAT-75 (nothing on the device).
- **Moved unchanged to `chat-signed-in-later.feature`** (sign-in only, tagged so they don't run): WCHAT-07, WCHAT-40 to WCHAT-53, WCHAT-57, WCHAT-64, WCHAT-93, WCHAT-94, WCHAT-98, WCHAT-100, WCHAT-101, WCHAT-103, WCHAT-104, WCHAT-110. The plan confirms the full list scenario by scenario.
- **New scenarios** (new WCHAT numbers from WCHAT-112): the consent card and its receipt; the warning before a comparison; a comparison that doesn't fit the day's budget; reload and new tab; JavaScript off; the re-check failing; the bot check on the tap and its failure; the low-balance comparison; the progress list; the daily-cap pause; "Ask about this council"; "New chat".
- **Also stale and fixed in the same work:** `sign-in.feature` and `account.feature` (marked for later), the landing's chat entry (`01-landing.feature`), the area result and City Explorer entries, doc 04, `docs/architecture/README.md`, and the information architecture.
- **The canvas:** new "Pilot · Anonymous chat" boards, light and dark, desktop and phone: the consent card, the chat with an area, a comparison in progress, and the pause and unavailable states. The "Pilot · Signed-in chat" boards move to "Home workspace (later)". A visual review in Chrome before the founder sees them.

### 7. Edge cases added (design review, 21 Nov 2026)
None of these changes a founder decision; each follows from a decision or rule already cited.
- **What the consent statement must contain** (0063 point 5 and the 0064 note for what is sent where and kept how long; UK GDPR Article 7(3) "Prior to giving consent, the data subject shall be informed thereof" for withdrawal): that messages, including any health or similar details, go to Anthropic in the US or "global" processing, which deletes them within 30 days (flagged content up to 2 years); that we keep the words 14 days; and that consent can be withdrawn and how. The proposed card wording above leaves out the US, Anthropic's own keeping period and withdrawal; the copy review keeps the wording short but not these facts.
- **The Privacy notice before the chat goes public:** besides section 5, the chat's parts must state the purposes and lawful basis (Article 13(1)(c)), the transfer to the US and its safeguard (13(1)(f); the DPA's UK Addendum, 0064), the keeping periods (13(2)(a)), the right to withdraw consent (13(2)(c)) and the right to complain to the ICO (13(2)(d)) ([Article 13](https://www.legislation.gov.uk/eur/2016/679/article/13), read 21 Nov 2026). PRIV-14's placeholders can't stay for these once the chat is public. PRIV-08 ("an invisible check reads signals from your device", no provider) and PRIV-13 (sign-in, 30 days) become wrong and are rewritten: ALTCHA is a self-hosted proof-of-work check that runs on the consent tap.
- **Nothing in session storage either:** 0063 says nothing on the device, and with no sign-in there is no return target, so WCHAT-75 and WCHAT-66 are rewritten to "nothing in session storage, local storage, IndexedDB or cookies"; the hand-over lives only in the app's memory.
- **Reload, back and new tab:** a reload, or "Ask about this area" opened in a new tab, starts again: the consent card, no area (the empty landing state), no earlier messages. Back from the chat to the area result works through the in-memory hand-over. The plan decides whether a leave-page warning is shown while a conversation exists.
- **No area loaded** (the landing entry, a reload): the card's title names no postcode, and the desktop panel shows an empty state saying what to ask, never a blank region.
- **Entry points only where there is something to ask:** "Ask about this area" is not shown on a "not yet covered" or "not found" result (WCHAT-35, WCHAT-36).
- **The consent tap:** the button is turned off while "Checking…" runs, so a double tap makes one receipt and one check; the label change is announced once as a status, and focus stays on the button. Focus on arrival goes to the card's heading. "Privacy notice" opens in a new tab, says so in its accessible name, and leaves the tab's conversation as it was. If the check takes longer than ALTCHA's timeout, or the browser lacks Web Crypto, the button shows "Try again" with that cause. ALTCHA's image-code fallback is not turned on, so nothing appears on screen. With JavaScript off, the page says the chat needs JavaScript and links back to the area check.
- **The re-check after a set number of messages** fails like the first: the message is not sent, it stays in the box, and "Try again" is offered.
- **More lines and their order:** the rate-limit refusal (WCHAT-29) and the turn limit (WCHAT-72) sit below the visitor's own 15 in the order above. A pause for everyone reached mid-conversation shows on the next Send; the message stays in the box and nothing is counted.
- **"New chat"** keeps the consent and the day's count, resets the turn limit (WCHAT-72 offers it), stops a streaming answer first (which counts, WCHAT-108), keeps the area in the panel, and puts focus in the message box.

## What this changes in the records
- **New decision 0065:** an exception to rule 5 for the controller's name in the Privacy notice (founder, 21 Nov 2026, "Exception to rule 5"); AGENTS.md rule 5 gains a pointer to it. Founder merge (it changes a repository rule).
- **0064:** a dated note for the low-balance comparison.
- **0063:** a dated note: the chat's own page, the consent card before the chat, the entry points.
- **Register:** new FE lines from FE-85 for the chat page and entry points, the consent card, the progress list and the pause wording; SE-10 and AI-16 notes.
- **Status file:** updated in the same pull request.

## Calls the agent made (for the founder to check)
- "Ask about this council" on City Explorer; "New chat" in the header; renaming the file to `chat.feature`.
- The bot check on the consent tap, and the button's "Checking…" and "Try again" states.
- Section 7's edge cases (design review), and the card wording carrying the US, Anthropic's keeping and withdrawal.
- Entry points always shown; the pause shown on the chat page on arrival, in place of the card.
- Which pause line wins; the daily cap at 95% and London midnight; what counts as a comparison.
- The progress list and its announcements.
- 0065 in its own pull request.

## What is left
- **To the founder:** the copy review of the card, the new pause line, the progress steps and the Privacy notice; approval of this design.
- **To the builder (the plan):** the ALTCHA re-check interval; the confirmation text for "New chat"; the full scenario-by-scenario sort of WCHAT; board names on the canvas; the consent statement's version scheme.
