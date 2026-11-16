# Signed-in Chat (boards and specifications) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draw the pilot's signed-in chat on the design canvas and write its executable specifications, ready for the pilot gate (0052).

**Architecture:** This is stage 3 work, the same shape as City Explorer PRs B and C (#295, PR C):
- Record the founder's answers from the design review as register lines.
- Draw light boards at 390 and 1440 px on a new canvas page, the founder reviews them, then draw dark versions.
- Write the specifications: three new feature files, plus a keep, replace or retire review of every withdrawn chat and card scenario.
- No product code. Sign-in, the API, the agent and the database are built at 5b after AI-09, IN-02 and DA-03.
- The bot check provider and the Python library that checks Better Auth's tokens (0058 builder notes) are named in the 5b build plan, not here; the founder approves any package that is not pre-approved.

**Tech Stack:** The design canvas artifact (https://claude.ai/artifact/MpvQNDVYCePp4iWM3j3Jx4, version 332 onwards). Gherkin run by pytest-bdd (`packages/specs/tests`). No new packages.

**Spec:** [`docs/decisions/0058-signed-in-chat-in-the-pilot.md`](../../decisions/0058-signed-in-chat-in-the-pilot.md) (accepted 16 Nov 2026), plus:
- the design review of 16 Nov 2026 (its findings are listed under "Review Focus" and in the states lists below);
- the founder's answers to it (Task 1).

Also decisions 0004, 0014, 0046, 0051, 0056 and register lines AI-11, FE-13, FE-18, FE-26, FE-33 and FE-34.

## Global Constraints
- **Rules 1, 4 and 7:**
  - no invented facts;
  - never "verified", "safe" or "approved";
  - no score or verdict of our own;
  - missing data is never zero or a clean result.
- **No figure typed by hand (rule 2).**
  - Area figures are quoted from `packages/fixtures/generated/area-result.json` and council figures from `council-result.json`.
  - Specifications cite them by postcode and topic or by figure ID (`docs/specs/README.md` rule 3).
  - The chat never calculates (0004).
- **Postcodes never in a URL query string, a sign-in request or a log** (0014, 0046).
  - A postcode travels after `#` or in a request body.
  - The sign-in `callbackURL` is a path only.
  - The return target (page, postcode, pending action) is kept in `sessionStorage`.
  - The magic-link `token=` is dropped from every log.
- **Founder's answers** (16 Nov 2026, prompt windows; Task 1 records them):
  - sentence-by-sentence streaming;
  - past chats show the stored widget, dated, with an Update button;
  - one chat, with "Compare with…" on widgets (no modes or tabs);
  - speed: first text or placeholder within **2 s** and a complete widget within **6 s**, at the 95th percentile;
  - at most **20** saved areas;
  - chat titles are the first words of the first message, editable;
  - a warning at message **14** ("1 message left today");
  - after sign-in, the user returns to the page they came from.
- **From 0058:**
  - Google, GitHub and an email link;
  - 15 messages per account per day, reset at midnight Europe/London;
  - chats kept 12 months after last use;
  - traces kept 30 days, founder-only;
  - idle accounts deleted after 24 months;
  - the side panel on desktop, a sheet on a phone;
  - the widget is chosen by the tool result's `kind`.
- **Boards:**
  - 390 and 1440 px, light first, then slate-ink dark (FE-31);
  - source stamps (FE-33);
  - one "How we got this" per page (FE-34);
  - the AI badge (FE-13);
  - touch targets at least 44 px;
  - every board passes the competitor benchmark checklist;
  - the competitor is a layout pattern only, never their colours, icons, labels or wording;
  - "Sample data: a made-up town" on every widget.
- **Scenario IDs:** new prefixes are `AUTH-` (sign-in), `WCHAT-` (the workspace chat) and `ACCT-` (the account page).
  - An ID is never reused or renumbered.
  - A withdrawn scenario whose meaning changes is not edited. It stays `@withdrawn` with "Replaced by <new ID>", and the new scenario carries the new meaning.
  - Only a scenario whose text still holds word for word loses its `@withdrawn` tag.
- **Tags:** browser and server checks are `@ui`, as in `area-chat.feature` ("The ui tag also covers server checks"). Add no new tags; `pyproject.toml` markers are strict.
- **Copy:** quoted messages are proposed wording that the founder approves at board review. The exceptions are the fixed texts the specs carry: FE-13's AI label, "1 message left today", and the existing "Chat is paused for today, the area check still works" and "Chat unavailable right now".
- No agent attribution in commits or pull requests.

## Review Focus
1. **Two tabs send message 15 at the same moment.**
   - Only one is accepted.
   - The other gets "paused for today" with no model call. The count is one atomic database step.
   - Test: WCHAT scenario in Task 6.
2. **A user signs out or deletes their account, then a request arrives with a token that has not expired yet** (15-minute JWT).
   - Writes (send a message, save an area) are refused because the session no longer exists.
   - Nothing is stored after the delete.
   - Test: AUTH and ACCT scenarios in Tasks 6 and 7.
3. **The email link is opened on another device, or opened twice, or after 5 minutes.**
   - Another device: the user is signed in to a new chat with a short note. The postcode is never in the link.
   - Opened twice or too late: an "expired or used" page with one action, "Send a new link".
   - Asking for a link gives the same message whether or not an account exists.
   - Test: AUTH scenarios in Task 6.
4. **A past chat is reopened after its source has a newer edition.**
   - The widget shows its stored figures with their original source date and an Update button. It never looks current.
   - After Update, the old words stay and are marked as written about the earlier data.
   - Test: WCHAT scenario in Task 6.
5. **A sentence fails the output guard partway through an answer.**
   - The sentences already shown stay.
   - The failing sentence never appears, and the answer ends with a notice.
   - The stored chat matches what was shown, and the message counts toward the 15 (agent's call, Task 1).
   - Test: WCHAT scenario in Task 6.

## Pull requests
- **PR 1 (documentation):** Task 1 and this plan. Branch `docs/signed-in-chat-plan`.
- **PR 2 (canvas record):** Tasks 2 to 5. Branch `docs/signed-in-chat-boards`.
- **PR 3 (specifications):** Tasks 6 to 8, after the founder approves the boards. Branch `docs/signed-in-chat-specs`.

All three are documentation and specifications. Each one runs `make check`, then the pre-push review, then Codex, and merges when the merge rules hold.

---

### Task 1: Record the founder's answers (PR 1)

**Files:**
- Modify: `docs/decisions/README.md` (new register lines after FE-50, AI-12 and OP-04)
- Modify: `docs/decisions/0058-signed-in-chat-in-the-pilot.md` (one dated note pointing to the lines)
- Modify: `docs/planning/status.md`
- Create: this plan

- [ ] **Step 1:** Add the register lines. Status is `Default`, and each line quotes the founder's choice:
  - AI-13: sentence-by-sentence streaming, each sentence checked before it shows ("Sentence by sentence (Recommended)").
  - FE-51: past chats show the stored widget with its source date and Update ("Stored result, dated, Update button (Recommended)").
  - FE-52: one chat, with "Compare with…" on widgets ("One chat, Compare on widgets (Recommended)").
  - OP-05: speed targets of 2 s to first text or placeholder and 6 s to a complete widget, at the 95th percentile, reviewed after AI-09 ("2 s first sign, 6 s widget (Recommended)").
  - FE-53: at most 20 saved areas ("20 (Recommended)").
  - FE-54: chat titles are the first words, editable ("First words, editable (Recommended)").
  - FE-55: "1 message left today" after message 14 ("Warn at 14 (Recommended)").
  - FE-56: after sign-in, return to the page and finish the action, with the postcode held only in the tab ("Back where they were (Recommended)").
- [ ] **Step 2:** Add the agent's calls, open to the founder, as a "Builder notes" addition in the 0058 note:
  - a returning user opens a new chat, with the last chat first in the sidebar;
  - an answer stopped by the guard counts toward the 15, and so does a regenerate;
  - a dropped connection on our side does not count;
  - the monthly IN-05 cap has its own state, "Chat is paused for this month, the area check still works";
  - deleting a saved area leaves past chats readable, with their stored widgets.
- [ ] **Step 3:** Update the status file: the next steps follow this plan's PRs.
- [ ] **Step 4:** Run `make check`. Expected: pass.
- [ ] **Step 5:** Commit `docs: signed-in chat plan and the founder's answers (0058)`. Then the pre-push review, push, the pull request, Codex, and merge.

### Task 2: Canvas, workspace boards (light)

The canvas page is new: **"Pilot · Signed-in chat"**. The chat boards on "Home workspace (later)" that these replace are removed in the same change (house rule: clean up what you replace), and the PR lists them. Figures are quoted, never worked out: NB1 4XY from `area-result.json`, Northbridge and Southvale from `council-result.json`.

- [x] **Workspace, desktop (1440)** for NB1 4XY:
  - **Sidebar:** saved areas (3 of 20), past chats titled by their first words, "New chat", the account link.
  - **Chat:** the user's question; an answer mid-stream with two sentences shown; a Nearby widget placeholder, then the Nearby widget with source stamps; a "Writing…" status; Stop.
  - **Side panel:** a labelled region showing the full area result's topic.
  - **Widget actions:** Save, Compare with…, Open full result, Print.
  - **Header:** the AI badge and disclaimer (FE-13). The disclaimer now says chats are saved for 12 months and can be deleted, and links the privacy notice.
- [x] **Workspace, phone (390):**
  - the sidebar as a drawer;
  - the chat;
  - "Open full result" opening the side panel as a modal sheet;
  - the composer above the keyboard.
- [x] **Compare in the chat,** desktop and phone: two postcodes (NB1 4XY and NB7 1RR), and two councils (Northbridge and Southvale), as compare tables in rows. Each side keeps its own levels and stamps, and there are no verdict words.
- [x] **First visit (empty)** and **returning user** (new chat, last chat first in the sidebar), desktop and phone:
  - suggested starts that name things the tools can answer;
  - no saved areas yet, with how to save one.
- [x] **"Ask more about this" (proposal for the founder):** on the area result's "Explain this" for a signed-in user, a link that opens the workspace chat on that topic; drawn as a proposal and asked at Task 5.
- [x] **Acceptance:**
  - every figure has a source stamp and level;
  - "Not known" appears where the sample data has a gap (NB7 1RR);
  - no verdict words;
  - 44 px targets;
  - the competitor checklist passes.

### Task 3: Canvas, sign-in and account boards (light)
- [x] **Sign-in page,** phone and desktop:
  - Google, GitHub, "Email me a link";
  - one line on what signing in keeps, linking the privacy notice;
  - shown before the first message.
- [x] **Email link states:**
  - "Check your email" (the same wording whether or not an account exists);
  - link expired or already used, with one action, "Send a new link";
  - opened on another device, landing in a new chat with a note;
  - email service unavailable.
- [x] **GitHub with no verified or public email:** the cause, reassurance and one action (use Google or an email link), register line B22.
- [x] **Signed out on a public page:** "Ask about this area" and Save on the area result and the council page lead to sign-in. Show the return: the page, then the area saved.
- [x] **Account page,** phone and desktop:
  - **Saved areas:** remove, and the 20 limit.
  - **Chats:** rename, delete one, delete all.
  - **Sign-in methods:** the linked methods, with the last one unremovable.
  - **Sign out, Sign out everywhere.**
  - **Delete account:** confirm by signing in again, then a list of what is deleted.
  - **Retention lines:** chats 12 months after last use, traces 30 days, idle accounts 24 months.
- [x] **Acceptance:** no postcode is shown in any sign-in URL drawn on a board; the delete flow names everything 0058 says is removed.

### Task 4: Canvas, states board (light)
One board, phone frames, each state with its cause, reassurance and one action:
- [x] **Limits:**
  - "1 message left today" after message 14;
  - "Chat is paused for today, the area check still works" (message 15 sent);
  - the monthly cap state;
  - "Chat unavailable right now" (switched off or provider down).
- [x] **Answers:**
  - a sentence stopped by the guard (earlier sentences stay, and a notice ends the answer);
  - a tool failed (the other parts shown, and that part marked Unavailable);
  - a source unavailable;
  - a fact published only for the council or county, shown with its level.
- [x] **Places:**
  - a postcode outside England, "not yet covered" (WALES-1);
  - Isle of Man and Channel Islands;
  - an invalid or ended postcode (NB9 9ZZ);
  - a council name that matches two councils (both listed, never auto-picked).
- [x] **Saved areas:**
  - saving a 21st (remove one first);
  - already saved;
  - a past chat that uses a deleted saved area (still readable).
- [x] **Connection and session:**
  - a dropped connection (the partial answer stays, with Retry);
  - the session expired while typing (the draft kept in the tab, then sign in);
  - the same chat open in two tabs (the second shows "This chat is open in another tab", with Reload).
- [x] **Past chat:** a stored widget with its original source date and Update; after Update, the earlier words are marked "Written about the data from <date>".
- [x] **Accessibility notes on the board:**
  - "Writing…" is announced once, and the full answer once when done, never word by word;
  - Stop is reachable by keyboard;
  - the side panel is a region on desktop and a modal sheet on a phone, with focus returned when it closes;
  - reduced motion for placeholders.

### Task 4b: Feedback kit (added 16 Nov 2026)
The founder asked: "do we have beautiful error states, alerts, spinner, that are customised for our brand" [sic], then chose "Yes, add it now (Recommended)". One "Feedback kit" board on the "Brand and style" page, light (dark in Task 5). It follows the Craft sheet's "Every state, designed" and "Motion with one physics" rules:
- [x] **Notices:** information, warning (amber only) and error, as inline and page-top variants. Each has the cause, a reassurance and one action (B22), `role="status"` or `role="alert"`, and a 44 px action.
- [x] **Confirmations ("toasts"):** short messages such as "Saved", "Link sent" and "Already saved". They are polite live-region announcements, stay long enough to read, and can be dismissed. Under reduced motion they don't move.
- [x] **Loading:**
  - skeletons shaped like each widget (area card, Nearby list, council figures, compare table);
  - the button label change;
  - the chat's "Writing…" indicator in the brand: the clay hearth dot on its own beside the word (not the logo mark), pulsing gently; under reduced motion it stops and stays still at full strength; announced once.
  - No generic spinners.
- [x] **Full-page states:** page not found, something went wrong, offline, and signed out. Each has a small isometric illustration in the Imagery style, plain words and one action.
- [x] **Empty states:** no saved areas, no chats, and nothing found, each with a small isometric illustration.
- [x] **Acceptance:**
  - it uses the Craft tokens (type, space, colour, motion);
  - no new colours;
  - every figure in an example is quoted from the fixtures;
  - the boards in Tasks 2 to 4 are then updated to use the kit (Task 5).

### Task 5: Founder review, dark versions, PR 2
- [x] The founder reviews the light boards in a prompt window, one area at a time. Fix what comes back, and record any changed answer as a register line.
- [x] Ask the founder, in a prompt window, whether "Ask more about this" comes back for signed-in users (0058 open item), with the Task 2 proposal board as the example.
- [x] Draw the dark versions (slate ink) of every board, at the light board's x plus 8000, same y.
- [x] Check every board in Chrome at 390 and 1440.
- [x] **PR 2:**
  - the status file (canvas version, boards added, boards removed from "Home workspace (later)");
  - an "As drawn" note in this plan;
  - any register lines from the review.

**As drawn (16 Nov 2026, canvas version 356).** The page "Pilot · Signed-in chat" holds the light boards SignedInChatDesktop, SignedInChatPhone, SignedInChatCompare, SignedInChatComparePhone, SignedInChatFirstVisit, SignedInChatReturning, SignedInChatFirstVisitPhone, SignedInChatAskMore, SignedInSignIn, SignedInSignInPhone, SignedInEmailStates, SignedInEmailStatesDesktop, SignedInGitHubNoEmail, SignedInPublicEntry, SignedInPublicEntryDesktop, SignedInAccount, SignedInAccountPhone, SignedInAccountAreas, SignedInAccountAreasPhone, SignedInAccountChats, SignedInAccountChatsPhone, SignedInChatStates and SignedInChatStates2, and their Dark twins at x + 8000. FeedbackKit and FeedbackKitDark are on "Brand and style". Craft (loading button label change, the loop rule, the error icon proposed) and Imagery (the 404 points to the kit) are updated. Removed from "Home workspace (later)": AreaChat, AreaChatDark, AreaChatPhone, AreaChatPhoneDark, AreaCardChat, AreaCardChatDark, AreaCardChatPhone and AreaCardChatPhoneDark; four notes there were reworded. A Chrome visual check found no overflow; small text, animation and focus rings are to be checked in the build's visual review. The founder's review answers are register lines FE-57 to FE-66 and SE-06.

### Task 6: Specifications, sign-in and the workspace chat (PR 3)

**Files:**
- Create: `docs/specs/pilot/sign-in.feature` (`AUTH-` scenarios, `@ui`)
- Create: `docs/specs/pilot/workspace-chat.feature` (`WCHAT-` scenarios, mostly `@ui`)

Each feature's description follows `area-chat.feature`'s header shape:
- the question it answers;
- modes;
- fixtures;
- where;
- copy;
- the fake AI provider for `@ui` replies;
- which scenarios are also AI-03 evaluation cases;
- a "Required states" map from every state in Tasks 2 to 4 to at least one scenario ID.

- [ ] **Step 1: `sign-in.feature`:** one scenario per item, each with one observable outcome:
  - the three sign-in methods;
  - the privacy line shown before the first message;
  - the bot check runs on sign-up and on each email-link request, not on chat messages (0058);
  - "Check your email" is identical for a known and an unknown address;
  - expired link, used link, other device;
  - GitHub without a verified email;
  - linking by a verified email only, and never through a trusted provider;
  - returning to the page and finishing Save;
  - no sign-in request (URL, body or `callbackURL`) contains a postcode;
  - `token=` is never in a log;
  - signing out sends `Cache-Control: no-store` and clears the sidebar from the page;
  - Sign out everywhere;
  - a revoked session's unexpired token is refused on a write.
- [ ] **Step 2: `workspace-chat.feature`:**
  - **Layout:** desktop, phone, the drawer, the panel as a region, the sheet as a modal.
  - **Visits:** first visit, returning user.
  - **Streaming:**
    - sentence by sentence;
    - the guard-stopped sentence (Review Focus 5);
    - the widget drawn from the tool result's `kind`;
    - the widget's figures equal the tool result's, not the text's.
  - **Speed:** the speed targets, named with OP-05's values.
  - **Stop and errors:** Stop; a dropped connection; Retry and Regenerate counting.
  - **The cap:**
    - message 14's warning;
    - message 15;
    - two tabs at once (Review Focus 1);
    - the reset at midnight Europe/London, including a clock-change day;
    - the monthly state;
    - "Chat unavailable right now".
  - **Facts:** every claim's source stamp; "Not known"; a source unavailable; a tool failed; a council-level fact; outside England; Isle of Man; an ended postcode.
  - **Fixed replies:** "is this area safe?" gets AI-11's fixed reply with no model call.
  - **Data handling:** user and source text treated as data (prompt injection).
  - **Rate limits:** per account and per client, on top of the daily cap; a refusal makes no model call.
  - **Saved areas:**
    - save, up to 20;
    - the 21st;
    - a duplicate after postcode formatting;
    - the `list_saved_areas` tool returns typed data, never prompt text;
    - "compare my two saved areas".
  - **Past chats:** stored widget with its date and Update (Review Focus 4); titles; rename. Update makes no model call and doesn't count toward the 15 (FE-62).
  - **Countries:** Isle of Man and Channel Islands show "Not covered" (FE-60).
  - **Compare:** "Compare another area" asks which side to replace (FE-57).
  - **"Ask more about this":** for everyone, and replaced by the pause line when the chat is paused for everyone (FE-58).
  - **Deleting while streaming:** delete a chat while it streams.
  - **Logs and traces:** no message text, postcode or tool argument in any ordinary log; a trace holds them for at most 30 days.
- [ ] **Step 3:** Cite figures by ID only: area facts by postcode and topic from `area-result.json`, council figures by figure ID from `council-result.json`.
- [ ] **Step 4:** Run `make check`. Expected: pass, with the new `@ui` scenarios collected and deselected and no duplicate ID error from `name_scenarios_by_id`.

### Task 7: Specifications, the account page, and the withdrawn scenarios (PR 3)

**Files:**
- Create: `docs/specs/pilot/account.feature` (`ACCT-` scenarios, `@ui`)
- Modify: `docs/specs/pilot/area-chat.feature` (header and tags)
- Modify: `docs/specs/pilot/area-card.feature` (withdrawn CARD scenarios)

- [ ] **Step 1: `account.feature`:**
  - saved areas, list and remove;
  - rename and delete one chat;
  - delete all chats;
  - the last sign-in method can't be removed;
  - deleting the account needs a fresh sign-in;
  - deleting removes chats, saved areas, the daily count, traces, the sign-in tables and the email service's copy, with nothing written afterwards (Review Focus 2);
  - the `/account` overview with its own pages `/account/areas` and `/account/chats` (FE-66);
  - chats: newest 20 then "Show more", grouped Today, This week, This month and Older, with title search (FE-65);
  - deleting one chat or one saved area hides it at once with Undo, as 0058's board-review ruling says (the server commits after 10 seconds); "Delete all chats" confirms first;
  - the email-link method has no Remove;
  - retention: chats deleted 12 months after last use, traces after 30 days, idle accounts after 24 months, with "use" as defined in 0058 choice 6.
- [ ] **Step 2: Review CHAT-01 to CHAT-53 and the withdrawn CARD scenarios** (CARD-02, 22, 23, 27, 28, 31, 36 to 42). Put the review table in the feature's description: ID, then keep, replace or retire, then the reason, then the new ID. Known outcomes from the design review:
  - **Replaced:** CHAT-04 ("Chats aren't saved"), CHAT-06 and CHAT-38 (drawer and dialog), CHAT-17 (current area only), CHAT-23 and CHAT-45 (bot check on each chat request), CHAT-25 and CHAT-26 (cleared on a new postcode or reload), CHAT-34 (no trace), CHAT-35 (no copy kept), CARD-22.
  - **Kept:** only scenarios whose text still holds word for word. A kept scenario loses `@withdrawn` and keeps its other tags.
  - **Retired:** anything only about the anonymous on-page chat; it stays `@withdrawn`.
  - **The header:** "Modes: anyone, with no account" becomes signed-in users only, pointing to 0058 and the new files.
- [ ] **Step 3: "Ask more about this" (CHAT-52, CHAT-53, 0058's open item):** follow the founder's answer from Task 5. Keep or replace by the same rule as Step 2.
- [ ] **Step 4:** Run `make check`. Expected: pass. Then `grep -cE '^\s+@.*\bwithdrawn\b' docs/specs/pilot/area-chat.feature` (tag lines only; the header also contains the word) equals the number of retired plus replaced rows in the table.

### Task 8: Knock-on documents, review and merge (PR 3)
- [ ] **`.design/prototype/INFORMATION_ARCHITECTURE.md`:**
  - routes `/sign-in`, `/chat`, `/account`, `/account/areas` and `/account/chats` (a postcode only after `#`);
  - the sidebar and side panel in "Layering";
  - the sign-in entry on the area result and the council page.
- [ ] **`docs/specs/README.md`:** layout rows for the three new files and the `area-chat.feature` row.
- [ ] **AI-03:** list the WCHAT scenarios that are evaluation cases in `workspace-chat.feature`'s description, and add a line to backlog row 38f.
- [ ] **Pre-flight:** search for CHAT IDs, "Chats aren't saved", "anyone, with no account" and "drawer" in live documents, and fix anything stale.
- [ ] **Map criteria to scenarios:** every state in Tasks 2 to 5 (including 4b), register lines FE-57 to FE-66 and SE-06, and every Review Focus line names its scenario ID. A state with no scenario is a gap; fix it before the review.
- [ ] Run `make check`, the pre-push review (Code Review Rules), the status file update, the PR, Codex, then merge.
