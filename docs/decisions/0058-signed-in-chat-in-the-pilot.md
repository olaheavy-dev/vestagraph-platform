# 0058: Signed-in chat in the pilot

**ID:** PD-20 (also decides SE-01 for the pilot)  
**Status:** Accepted (founder, 16 Nov 2026, prompt window: "Merge and accept 0058 (Recommended)", after Codex found no issues on #296); the founder's choices were made 15 and 16 Nov 2026, typed and in prompt windows  
**Date:** 2026-11-16  
**Stage:** 5b (the pilot)  
**Amends (no older text is rewritten):** [0051](0051-ai-in-the-public-pilot.md) (PD-15): its chat launch blockers come back for the signed-in chat, its bot check on the chat moves to sign-up, and its safeguard that we store nothing of a chat no longer holds for signed-in users; [0004](0004-ai-in-the-product.md) (PD-04): the chat may answer across a user's saved areas and compare two postcodes or councils, not only the current area; [0056](0056-no-on-page-chat-in-the-pilot.md) (PD-18): an AI chat comes back into the pilot, for signed-in users only, and the launch blockers that left with the on-page chat come back for it; [0046](0046-public-area-check-first.md) (PD-12): accounts arrive in the pilot instead of after it, while saved homes still wait; [0014](0014-privacy-and-data-protection.md) (SE-02): signed-in users' chats are kept without a separate Save (below); register lines SE-01, SE-02, AI-01, AI-03, AI-04, AI-09, IN-05, FE-13 and FE-18; the pilot gate ([0052](0052-pilot-only-gate.md)) grows. **Unchanged:** the public pages stay open with no account; anonymous visitors still get no AI calls (0014, 0056); the public MCP server and [0057](0057-chatgpt-call-details.md) are untouched.

## Context
Decision 0056 (15 Nov 2026) took the on-page chat out of the pilot and planned a chat in the signed-in home workspace later. Later the same day the founder typed: "Would be a stretch to say that having a chat will strenghtns me for ai engineering, and fde job should be part of the pilot it would the chat with tabs and reuse every of the ui we have built as widgets and display only the features that are planned for the pilot" [sic]. The agent answered that it is not a stretch. The founder then typed: "I think the chat should be after a user signs up either using Google , Github or any other easy sso sign on" [sic], and chose in a prompt window: "In the pilot, for signed-up users (Recommended)". (SSO, single sign-on: signing in with an account you already have elsewhere, such as Google.)

**Why (the founder's reason):** the chat is the part of the pilot that shows AI-engineering and forward-deployed-engineer skills: an agent with tools, grounding, evaluation, limits and real users.

What it changes:
- **Running cost and abuse come back:** every chat message costs money for the AI model, so a per-account daily cap, output guards, prompt-injection defence (stopping instructions hidden in source text or user text from steering the model) and cost monitoring are launch blockers again, as they were under [0051](0051-ai-in-the-public-pilot.md).
- **Personal data:** an account, saved chats and saved areas are personal data, which 0014 so far allowed only when a user saves a home.
- **Work before the pilot gate:** sign-in, an account page, the chat boards and scenarios, and the chat's evaluation cases.
- **What already exists:** the withdrawn chat scenarios (`docs/specs/pilot/area-chat.feature`, CHAT-01 to CHAT-53, tagged `@withdrawn`) and the chat boards on the canvas page "Home workspace (later)"; the signed-in workspace pattern in `docs/product/05-ideas-and-product-thinking.md` (founder, 14 Nov 2026); both templates' sign-in hooks, which leave the provider open (the FastAPI template's `authenticate` function in `app/auth.py` answers 401 to every protected route until a project fills it in).

## Options and choices
Each choice was made in a prompt window unless marked typed. Where the founder chose differently from the agent's recommendation, both are recorded.

### 1. What signing in keeps
- **Account only (recommended by the agent):** email, name and a usage counter; chats vanish when the tab closes. Least data, fastest.
- **Account + chat history:** past chats can be reopened.
- **Account + history + saved areas:** also pinned postcodes and councils.

**Chosen: "Account + history + saved areas"** (over the agent's recommendation). Saved homes (costs, questions, documents, what changed) still wait for the home workspace (0046).

### 2. The screen's structure
The agent first asked which tabs a signed-in dashboard should have. The founder asked back, typed: "is this question talking about the chat design or the general dashboard, chat design would be like the competitor, then we would even make it much more" [sic], and then: "please present in a prompt window". The agent explained that the chat itself could be the workspace and offered:
- **Chat is the workspace (recommended by the agent):** a sidebar (saved areas, past chats) and the chat with modes.
- **Dashboard with a chat tab.**
- **Both: chat plus a side panel:** the chat in the middle and a panel on the right showing the full area or council result the chat is discussing.

**Chosen: "Both: chat plus a side panel"** (over the agent's recommendation). The layout pattern follows doc 05's signed-in workspace note (pattern only; every surface in Vestagraph's own design system, never the competitor's colours, illustrations, icons, labels or wording).

### 3. "Much more" than the competitor's chat
The founder chose three of four offered (multiple choice):
- **"Sources and 'not known' on every fact":** each fact in an answer carries its source stamp (FE-33) and level (postcode, council), says "Not known" when data is missing (rule 7), and "How we got this" is at hand.
- **"Remembers your saved areas":** "compare my two saved areas" works without retyping.
- **"Live widgets you can act on":** answers show the designed widgets (area card, Nearby list, council figures, compare table), each with Save, Compare with…, Open full result and Print.

Not chosen for the pilot: "Gaps become questions to ask" (a gap the data can't answer saved as a question). It stays an idea; doc 05 already records it under "Chat panel about a home".

### 4. Sign-in service
Prices from each provider's own page, read 16 Nov 2026 (US dollars):

| Service | Free | After that | Notes |
|---|---|---|---|
| Better Auth | Free, MIT licence ([GitHub](https://github.com/better-auth/better-auth)) | Our own database and upkeep | A library in our own app; it now maintains Auth.js and recommends itself for new projects ([announcement, 22 Sep 2025](https://www.better-auth.com/blog/authjs-joins-better-auth)) |
| Clerk | 50,000 retained users a month per app, up to 3 social connections ([pricing](https://clerk.com/pricing)) | Pro $25 a month, then $0.02 a user | The pricing page does not state where user data is stored |
| Supabase Auth | 50,000 monthly active users ([pricing](https://supabase.com/pricing)) | Pro from $25 a month | "Free projects are paused after 1 week of inactivity" |
| Microsoft Entra External ID | First 50,000 monthly active users ([FAQ](https://learn.microsoft.com/entra/external-id/customers/faq-customers#external-id-pricing)) | Charged per monthly active user; add-ons have no free tier | Needs an Azure subscription |

**Chosen: "Better Auth (Recommended)".** Accounts live in our own database beside chats and saved areas: one place holds the personal data, we choose where it is, and deleting an account is one operation. No running fee and no lock-in. The cost is that we own its security updates. **This choice is the founder's approval of the `better-auth` npm package** (MIT), which was not on the pre-approved list (decision 0035 point 9 and its additions).

### 5. Sign-in methods
- **Google + GitHub (recommended by the agent):** no passwords and no email service.
- **Google + GitHub + Microsoft.**
- **Those + email link.**

**Chosen: Google, GitHub and an email link** (the founder's answer, "Google + GitHub + email link", over the agent's recommendation). Better Auth does not send email itself: its magic-link plugin calls a `sendMagicLink` function we write, and a link lasts 5 minutes by default ([magic link docs](https://www.better-auth.com/docs/plugins/magic-link)). So the email link needs an **email-sending service**, chosen by the founder at build time (it holds users' email addresses and has a running cost; see "Still open").

### 6. Keeping and deleting
- **Saved chats:** "12 months after last use (Recommended)": a chat is deleted 12 months after it was last opened or last had a message sent, whichever is later.
- **Unused accounts:** "Delete after 24 months idle (Recommended)": the whole account (email, name, saved areas, chats) is removed 24 months after the last sign-in, without a warning email. *Agent's call:* any request with a valid sign-in counts as use, so a session that stays signed in keeps the account.
- **Always:** a user can delete any chat, or the whole account, themselves, at any time, and the rules above are in the privacy notice and on the account page.

### 7. Daily cap
- **30 messages a day (recommended by the agent).**
- **15 messages a day.**
- **60 messages a day.**

**Chosen: "15 messages a day"** (over the agent's recommendation): 15 chat messages per account per day. When it is reached, the chat says it is paused for today (the wording is a design step) and the rest of the site keeps working. *Agent's call (open to the founder):* only messages the user sends count; the fixed AI-11 reply counts like any message, and a message that fails on our side does not; the count resets at midnight UK time; it is stored in the database with the account. The monthly cap in pounds for the whole pilot stays IN-05's, set by the founder before launch.

### 8. How the chat gets its facts
- **Call the tool functions directly (recommended by the agent):** the chat agent and the public MCP server share one Python package of area and council tools; the chat calls them inside the API.
- **Connect to our own MCP server:** the chat is an MCP client of the public server, like ChatGPT and Claude.

**Chosen: "Call the tool functions directly (Recommended)".** One code path to test, no extra network hop, and the public server's per-host caps don't limit our own signed-in users.

### 9. Chat text in tracing and AI tests
The builder check found that "nothing from a chat in any trace" conflicts with tracing (finding faults and watching cost; AI-09 compares frameworks on it). Offered:
- **Never: metadata only (recommended by the agent):** traces keep tool names, timings, token counts, cost and errors, never the words; AI tests use made-up conversations.
- **Short-lived traces with text:** full traces including the words, kept 30 days, visible only to the founder, then deleted.
- **Users can opt in to share:** metadata only, plus a "report this answer" flag that sends one chat for review.

**Chosen: "Short-lived traces with text"** (over the agent's recommendation): chat traces may include the words of the conversation and the tool calls; they are kept for **30 days**, then deleted; only the founder can see them; the privacy notice says so. Deleting a chat or an account also deletes its traces: a tracing tool is chosen only if it can delete one user's or one chat's traces on request, so the delete promise in choice 6 holds without a 30-day exception. *Agent's call:* the AI tests (AI-03) still use only conversations we write; traces are never copied into the tests without a later decision. Where the traces are stored (our own database or a tracing service, which would hold personal data) is decided with AI-09 and IN-02.

## Decision
The pilot gains a **signed-in chat workspace**:
1. **Who:** anyone who signs in with Google, GitHub or an email link. Every public page (area check, Nearby, City Explorer, the "Use in ChatGPT or Claude" page) stays open with no account; anonymous visitors get no AI calls (0014 and 0056 unchanged for them).
2. **The screen:** a left sidebar (saved areas, past chats), the chat in the middle, and a right side panel showing the full area or council result the chat is discussing; on a phone the side panel becomes a sheet. Only pilot features appear (area check with Nearby, City Explorer, compare two postcodes or councils). Exact modes, tabs and wording are the design step's.
3. **What the chat does:** answers only from Vestagraph's tested area and council tools, the same functions the MCP server uses (choice 8), with every fact's source stamp and level, "Not known" for missing data, "How we got this" at hand, and the designed widgets with Save, Compare with…, Open full result and Print. It never calculates figures and never gives a verdict (rules 2 and 4; [0004](0004-ai-in-the-product.md); AI-11's fixed reply for "is this area safe?").
   **How a widget is chosen (agent's proposal, explained to the founder on 16 Nov 2026 when the founder asked "how will this be implement, would we have certain widgets mapped to some types of question or what is the engineering behind this" [sic]):** widgets follow the **tool result**, not the question. The model picks a tool (tool calling); each tool returns typed data with a `kind` (for example `nearby`, `council`, `compare`) whose figures come from the tested packages; the page maps each `kind` to one widget component and draws it from that data, and "Open full result" hands the same data to the side panel. The model writes only the words around the widget. The stream to the page carries text and tool events (the AG-UI protocol, [docs.ag-ui.com](https://docs.ag-ui.com/introduction), is one way, and AI-09 already compares frameworks on it). The same typed results feed the MCP server's widget in ChatGPT and Claude.
4. **What is kept for a signed-in user:** the account (an opaque user ID, email, name, sign-in method), past chats, and saved areas (a postcode or council name only, not why it was saved), plus a per-day message count for the cap. Nothing from a chat (messages, postcodes, place names) goes into any ordinary log or error report (0014's rule for searches, extended to chats). **Traces are the one exception** (choice 9).
5. **Sign-in:** Better Auth runs in the Next.js app with its tables in our database. The FastAPI API checks each request's short-lived token against Better Auth's public keys: its JWT plugin publishes them at `/api/auth/jwks`, signs with EdDSA (Ed25519) by default and gives tokens a 15-minute life ([JWT plugin docs](https://www.better-auth.com/docs/plugins/jwt)); the API's `authenticate` hook does this check, and `User.id` is Better Auth's user ID, never the email.
6. **Keeping and deleting:** choice 6. **Daily cap:** 15 messages per account (choice 7).
7. **The AI model and framework** are not chosen here: the AI-09 trial at 5b decides AI-04, and AI-01 picks the provider, as 0056 kept them. The provider terms 0051 recorded ("No training, short checks OK") apply: the model provider may not train on chat text.

## Quality requirements (founder, 16 Nov 2026)
The founder typed: "Everything we are building has to be scalable, performant, secure, latency, and also can we use streamwed response with widgets?" [sic]. So the chat must meet these, and the plan turns each into measurable checks:
- **Streamed answers with widgets:** answers stream to the page as events over one connection (Server-Sent Events, [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)): text as it is written, a placeholder when a tool starts, and the widget when the tool's typed result arrives ([AG-UI events](https://docs.ag-ui.com/concepts/events) are one standard for these). Widget figures come only from the tool result, never from the streamed text.
- **Latency:** targets for time to first text or placeholder and time to a complete widget are set by the founder in the plan and measured in tests; none are assumed here.
- **Scalable:** the API holds no per-user state in memory between requests (chats, counts and sessions live in the database), so more copies can run side by side; the cap is enforced in the database so it holds across copies.
- **Performant:** tools read precomputed, tested data (`vestagraph_area`, the council results), not live calculations per message.
- **Secure:** every request's sign-in token is checked; per-account and per-client rate limits; chat text never in ordinary logs (traces as choice 9); prompt-injection defence for user and source text; the OWASP Top 10 for LLM applications ([OWASP GenAI](https://genai.owasp.org/llm-top-10/)) is the checklist for the chat's threat review.

## What this changes in the records
- **0056:** "No on-page AI chat in the pilot" now means no chat for anonymous visitors; the signed-in chat is in the pilot. Its launch blockers that left with the chat come back for the signed-in chat: the daily cap (15 per account) with its "paused for today" state, 0025's output guards, prompt-injection defence for user text as well as source text, cost monitoring, and the chat's AI evaluation cases (AI-03). A bot check moves to sign-up and the email-link request (where abuse would start), to be confirmed in the design step.
- **0046:** accounts (SE-01) move into the pilot for the chat and saved areas only. Saved homes, costs, questions, compare-homes and "what changed" for a home still wait for the home workspace.
- **0014:** its rule "store user data only when a home is saved" gains three exceptions for users who sign in: the account itself; saved areas, stored only when the user saves one; and chats, kept automatically for 12 months after last use, because the user chose to sign in to a chat that keeps history. Each can be deleted by the user at any time. Anonymous visitors are unchanged.
- **SE-01** is decided for the pilot (Better Auth; Google, GitHub, email link) and its stage moves from 6 to 5b. **SE-02** gains account, chat and saved-area data (lawful basis and DPIA below); the parts of its full privacy work that cover these move to 5b, and the rest (saved homes, documents) stays at 6.
- **0051's provider terms** ("No training, short checks OK") were accepted when we stored nothing of a chat; with chats kept, the privacy notice wording they relied on is re-checked in the privacy work.
- **AI-01, AI-04, AI-09:** "for the workspace chat" now means the pilot's signed-in chat; nothing else changes.
- **AI-03:** the chat's evaluation cases return to the pilot.
- **FE-13** (AI badge) and **FE-18** (phone chat preview) apply to the signed-in chat in the pilot.
- **The withdrawn chat scenarios** (CHAT-01 to CHAT-53 and the withdrawn CARD scenarios) are reviewed for the signed-in chat in the specification step: kept and re-tagged where they still fit, rewritten where the side panel or sign-in changes them, keeping their IDs.
- **The canvas:** the chat boards on "Home workspace (later)" are redrawn for the pilot's signed-in chat (side panel, sidebar, sign-in, account page, paused state), light and dark (drawn 16 Nov 2026 on 'Pilot · Signed-in chat', canvas version 355).
- **The pilot gate (0052)** also checks the signed-in chat's boards and specifications.

## Builder notes (agent's calls, open to the founder)
From the builder check on 16 Nov 2026; a builder could settle these without changing what is built, so the agent did:
- **Who stores what:** Better Auth's tables (user, session, account, verification) and our own tables (chats, saved areas, daily counts) live in one database, kept apart from the public-data tables (0014's design rule), in separate schemas. The FastAPI API owns our tables and the deletion jobs and enforces the cap; Next.js only runs sign-in. Which database and where it is hosted stays with DA-03 and IN-02.
- **One account per email:** signing in with Google, GitHub or an email link that carries the same verified email address reaches the same account (Better Auth account linking); unverified emails are never linked.
- **Saved areas reach the model through a tool** (for example `list_saved_areas`), returning typed data like every other tool, never pasted into the prompt as text.
- **Framework:** the chat agent sits behind a framework-neutral interface (AI-04 already requires this), so the boards and specifications don't wait for AI-09; the agent code waits for AI-09.
- **Bot check:** the plan names a candidate; a new package or service needs the founder's approval.
- **Privacy items** (lawful basis, DPIA, export, the email-sending service) are launch blockers, not pilot-gate items: the gate (0052) checks boards and specifications. The account page's boards include deleting chats and the account; an export button is drawn only if the privacy work decides on one.

## Still open (not decided here)
- **The email-sending service** for the email link (founder: cost, licence, where it stores addresses). Until it is chosen, the email link can't ship; Google and GitHub can.
- **Hosting and the database** (IN-02, DA-03): Better Auth needs a database for accounts; it supports PostgreSQL ([installation](https://www.better-auth.com/docs/installation)). Where the data is stored matters for UK GDPR transfers.
- **Lawful basis** for accounts, chats and saved areas, and whether a DPIA (data protection impact assessment) is needed for an AI chat that stores user text: to be worked out from the ICO's guidance in the privacy work before launch (SE-02), not assumed here.
- **What the AI provider keeps** of chat text and for how long: checked against the provider's terms when AI-01 is decided.
- **The Python library** that checks Better Auth's tokens (EdDSA): named in the plan; if it is not pre-approved, the founder approves it.
- **Access requests:** how a user's right of access (UK GDPR) is met, and data portability if the lawful basis is consent or contract; a download button on the account page is optional, settled in the privacy work.
- **Cookies (PECR):** the check of Better Auth's sign-in session cookies against PECR moves from stage 6 (0014) to a 5b launch blocker.
- **"Explain this":** whether its "Ask more about this" link (removed by 0056) comes back for signed-in users; a design-step question. *16 Nov 2026: settled, for everyone ([FE-58](README.md)).*

## Consequences
- More work before the pilot gate: the signed-in chat's boards and specifications, sign-in, the account page and the chat's evaluation set; then, in the build, Better Auth, the token check, the database, the chat agent and its limits.
- New running costs: AI model use (capped at 15 messages per account per day and by IN-05's monthly cap), the database, and the email-sending service.
- **Reversible:** the chat can be switched off without touching the public pages; accounts are harder to take back once users exist, which is why deletion and retention are fixed now.
- **Revisit if** AI costs pass IN-05's cap in the pilot, sign-up abuse appears, or the AI-09 trial changes what the chat can do safely.

**Note, 16 Nov 2026 (design review, before the boards):** the founder's answers to the design review's questions are recorded as register lines AI-13, FE-51 to FE-56 and OP-05 in the [register](README.md), with the [plan](../superpowers/plans/2026-11-16-signed-in-chat.md). These are the agent's calls, open to the founder:
- A returning user opens a new chat, with the last chat first in the sidebar.
- An answer stopped by the guard counts toward the 15 messages a day, and so does a regenerate.
- A dropped connection on our side does not count.
- The monthly IN-05 cap has its own state: "Chat is paused for this month, the area check still works".
- Deleting a saved area leaves past chats readable, with their stored widgets.

Scenario IDs: the plan's rule replaces "keeping their IDs" in "What this changes in the records": a withdrawn scenario whose meaning changes stays `@withdrawn` with "Replaced by <new ID>" and the new meaning gets a new ID, because docs/specs/README.md rule 2 never reuses an ID. This refines choice 7's agent's call: an answer stopped by the output guard is a completed answer, not a failure on our side, so it counts; Regenerate is a message the user sends, so it counts; a dropped connection or server error on our side does not.

**Note, 16 Nov 2026 (board review):** the founder's answers while reviewing the boards are recorded as register lines FE-57 to FE-66 and SE-06 in the [register](README.md), with the [plan](../superpowers/plans/2026-11-16-signed-in-chat.md). These are the agent's calls made while drawing, open to the founder:
- Deleting one chat or one saved area (ruling): the server hides the item at once and commits the delete itself 10 seconds after the request, so it happens even if the browser closes or crashes; Undo is a request to the server before then; the message does not pause on hover or focus. The chat's traces are deleted when it commits.
- "Delete all chats" asks first.
- "Chat unavailable right now" is a warning.
- The email-link method has no Remove: an email link always reaches the account at its verified address.
- A dropped connection on our side does not count, and Retry counts only if the answer completes.
- The 15 messages are counted in one atomic step per account.
