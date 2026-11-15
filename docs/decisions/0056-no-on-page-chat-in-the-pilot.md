# 0056: No on-page AI chat in the pilot; AI through ChatGPT and Claude only

**ID:** PD-18  
**Status:** Accepted (founder, 15 Nov 2026, typed and in prompt windows)  
**Date:** 2026-11-15  
**Stage:** 3 (for the pilot, stage 5b)  
**Amends (no older text is rewritten):** [0051](0051-ai-in-the-public-pilot.md) (PD-15): its point 2, the on-page area chat, leaves the pilot, and the launch blockers that existed only for the chat go with it; [0014](0014-privacy-and-data-protection.md): the pilot's exception to "no AI calls per anonymous visitor" is no longer needed, so the rule applies to the whole pilot again; register lines AI-12 (the "Ask more about this" link goes), FE-13 and FE-18 (they now apply to the signed-in workspace chat); [0004](0004-ai-in-the-product.md) and [0025](0025-ai-platform-capabilities.md): their pilot chat parts (via 0051) apply to the workspace chat; [0046](0046-public-area-check-first.md): clarified for City Explorer (below); [0055](0055-city-explorer-in-the-pilot.md): its open question on the area chat and tools for council pages is answered (tools yes, chat no)

## Context
Decision 0051 (13 Nov 2026) put AI in the public pilot in two places from day one: an on-page area chat, and Vestagraph's area tools in the visitor's own ChatGPT or Claude through a public, read-only MCP server (MCP, the Model Context Protocol, is the standard way an AI app connects to an outside service: [modelcontextprotocol.io](https://modelcontextprotocol.io)). The founder chose "Both on day one" over the agent's staged recommendation, and the chat was specified in full (`docs/specs/pilot/area-chat.feature`, CHAT-01 to CHAT-53).

On 15 Nov 2026, during the City Explorer brainstorm, the founder typed: "I am thinking we should move anything AI chat to when after the pilot, this is just a discussion, the AI chat when a user logs in will have different tabs like comparison, property search, like the competitor, and just do claude and chatgpt mcp connection".

What the on-page chat costs the pilot, and what removing it changes:
- **Running cost and abuse:** the on-page chat is the only part of the pilot where Vestagraph pays for AI answers; it needs a daily AI cap, a bot check, output guards and prompt-injection defence. Through MCP, the visitor's own ChatGPT or Claude does the AI work and pays for it; our server only returns sourced facts.
- **Work before the pilot gate (0052):** the chat panel's boards, scenarios and most of the AI evaluation cases.
- **Reach:** visitors without ChatGPT or Claude get no AI in the pilot. Connecting takes a few steps, and ChatGPT allowed a connection with no sign-in only in developer mode (Settings, Connectors, Advanced), as recorded on 13 Nov 2026 in `docs/specs/pilot/area-tools.feature`; to re-check before build, because hosts change these rules.
- **Where the chat goes:** the signed-in workspace pattern in `docs/product/05-ideas-and-product-thinking.md` already plans a chat with tabs (comparison, property search) and modes, tied to the user's saved homes.

## Options
### Option A: Move the on-page chat after the pilot (recommended by the agent)
The pilot keeps the MCP server and the pre-written "Explain this"; the chat is built in the signed-in workspace. Lower running cost and risk, less work before the gate; less AI reach in the pilot.

### Option B: Keep 0051 as it is
The on-page chat and the MCP server both on day one.

## Decision
**Option A**, the founder's choice (15 Nov 2026, prompt window: "Move chat after pilot (Recommended)"), for the reason in the founder's words above. In the same session, in prompt windows:
1. **AI provider and framework timing:** "Keep at stage 5b", over the agent's recommendation of moving AI-01, AI-04 and the AI-09 trial back to stage 6 with the workspace chat. Reason (founder, typed): "decide AI as early as possible". They stay at 5b, ready for the workspace chat; the pilot itself makes no model calls.
2. **How visitors find the MCP connection:** "How-to page, linked (Recommended)": a "Use in ChatGPT or Claude" page with steps for each app (it must say plainly what any risky setting such as ChatGPT's developer mode means and what it trades off, that the host app sees what it sends to us and what we return under its own terms, and link the privacy notice; its steps are re-checked against each host's current documentation before launch), linked from each area result, each City Explorer page and the footer. The founder then asked "should this be on the home page too" and chose "Short section on landing (Recommended)": one line, a small illustration and a "How to connect" link, below the landing's explanation sections (the agent first said "above \"Data from\"", but that section comes earlier on the landing; placed after "How to read a result", before "Coming next"); the postcode box stays first (0046).
3. **The canvas's chat boards:** "Move to workspace page (Recommended)": the chat drawer, the phone chat and the area card inside our chat move to the canvas page "Home workspace (later)", light and dark; the pilot page keeps the card widget used in ChatGPT and Claude.

What this means:
1. **No on-page AI chat in the pilot**, on the area result or City Explorer. The chat specifications (CHAT-01 to CHAT-53) and the area card scenarios that apply only inside our chat or compare it with the widget (CARD-02, CARD-22, CARD-23, CARD-27, CARD-28, CARD-31 and the phone chat preview CARD-36 to CARD-42) are tagged `@withdrawn`; the widget gains its own keyboard and naming scenarios (CARD-45, CARD-46), and CARD-32 to CARD-35 start from its full-screen view and kept, with their IDs, for the signed-in workspace chat. FE-13 (the AI badge) and FE-18 (the phone chat preview) apply to that chat.
2. **The MCP server stays** exactly as 0051 point 1 and point 4 set it: public area data only, read only, no keys, rate-limited, with its tool descriptions and documentation. City Explorer's council tools join it (City Explorer design, part 2).
3. **"Explain this" stays** (AI-12): pre-written, reviewed text, no model call. Its "Ask more about this" link (CHAT-52, CHAT-53) goes, since there is no chat to open.
4. **Launch blockers that go with the chat:** the daily AI cap and its "paused for today" state, the bot check on the chat, 0025's output guards, prompt-injection defence and cost monitoring for the chat. **Launch blockers that stay:** the IN-05 monthly cap; rate limits per anonymised client for the API (including City Explorer's calculations) and a global and a per-host cap for the MCP server; the bot check on Report a problem; no visitor input (postcode, place name, budget, calculator input, tool argument) in any log (0014, 0053); source text returned as data, never instructions, because hosts' models read it (TOOLS-21), with attack cases in the evaluation set; the privacy notice (SE-02 parts 1 and 2), which names the MCP server and how hosts send us tool calls; the AI evaluation set (AI-03) for the tool outputs and descriptions, which hosts' models read.
5. **Privacy (0014):** the pilot makes no AI calls per anonymous visitor, so 0051's exception is not used and 0014's rule applies again in full. The AI provider terms 0051 recorded ("No training, short checks OK") apply when the workspace chat is built.
6. **0046 clarified for City Explorer:** 0046 put "costs, questions, compare and what changed" behind sign-in; that is about a user's own saved homes. City Explorer's council-level figures (rent or buy per month with example or typed inputs, compare two councils, "what changed since your last visit", off until the visitor turns on "Remember councils on this device" (PECR consent) and kept only in the browser, as in the City Explorer design) are public facts and arithmetic for anyone, so they need no account. Nothing about a person or their home is stored.

## Consequences
- The pilot gate (0052) no longer waits for the chat's boards, scenarios or most AI evaluation cases; it gains the "Use in ChatGPT or Claude" page and its scenarios.
- **AI-01, AI-04 and the AI-09 trial stay at 5b** (founder's choice above): they are chosen for the workspace chat during the pilot stage, with nothing in the pilot calling a model.
- The pilot design (`docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md`), doc 04 §9, the site plan and the status file carry a note pointing here; dated plans and reviews stay as written.
- The canvas's chat boards move to "Home workspace (later)" after this record merges.
- **Reversible:** a later decision can bring an on-page chat back into the pilot; the withdrawn scenarios keep their IDs for that.
- **Revisit if** the host apps stop allowing a keyless server, or the pilot shows visitors want AI on the page.
