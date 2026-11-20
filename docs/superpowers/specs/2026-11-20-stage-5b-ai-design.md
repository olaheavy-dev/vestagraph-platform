# Stage 5b, group D: the chat's AI (multi-agent flow, provider, models, cap, tracing): design

**Date:** 20 Nov 2026. **Status:** approved by the founder, 20 Nov 2026 (prompt window, "Approve (Recommended)", which also accepts the agent's calls marked below; each can still be changed). Recorded in decision [0064](../../decisions/0064-pilot-chat-ai-multi-agent-claude-langsmith.md). Founder answers were given on 20 Nov 2026 in prompt windows unless marked typed; the agent's calls are marked. **Decisions it follows:** [0004](../../decisions/0004-ai-in-the-product.md), [0023](../../decisions/0023-microsoft-agent-framework.md), [0025](../../decisions/0025-ai-platform-capabilities.md), [0029](../../decisions/0029-external-services.md), [0049](../../decisions/0049-back-to-python-final.md), [0051](../../decisions/0051-ai-in-the-public-pilot.md), [0058](../../decisions/0058-signed-in-chat-in-the-pilot.md), [0063](../../decisions/0063-pilot-privacy-and-anonymous-chat-first.md); register lines AI-01, AI-03, AI-04, AI-09, AI-11, AI-13 to AI-15, IN-05.

**How the facts were checked:** an independent fact-check on 20 Nov 2026 read every outside claim below against its primary source (the provider's terms, docs and price pages; Anthropic's engineering posts). Corrections it found are already applied; the founder re-decided the choices it affected (LangSmith's training terms, Anthropic's retention). Founder, typed, on the earlier mistakes: "you have been mixing up decisions by not doing your due diligemce" [sic]; process issue [agent-workflows#40](https://github.com/olaheavy-dev/agent-workflows/issues/40).

## Intent and why
Group D settles how the pilot's anonymous chat (0063) is built: its agent flow, the AI provider and models, the monthly spending cap and the tracing tool. The founder asked for an intent classifier ("ia gree with the intent classifier" [sic], typed) and a multi-agent flow: "mainly to show employers i can build multi-agent systems but it also fits the application" [sic] (typed), then "make sure we are making the best decision".

Success: simple questions are cheap and quick; comparisons use a real multi-agent team that does work a single agent does less well; no figure reaches a visitor that didn't come from a tested tool (rules 2 and 4); spending can't pass the cap; every run can be traced and evaluated against AI-03.

## Goals
1. The agent flow (AI-04's shape), including the classifier.
2. The provider (AI-01) and which model does which job.
3. The monthly cap (IN-05) and how it is enforced.
4. The tracing tool (left open by 0063).
5. What the AI-09 trial builds and compares, and how AI-03 runs.

## Non-goals
- The framework choice itself (Microsoft Agent Framework or LangGraph): the AI-09 trial decides it (0049, 0051).
- Prompts, tool schemas and the chat's screens (the build plan and the chat's design step).
- Sign-in (deferred by 0063).

## Anti-goals
- Multi-agent for its own sake: extra model calls on questions one agent handles.
- An open-ended orchestrator that can start many agents for one question.
- A figure in an answer that didn't come from a tool result.
- A month's bill above the cap.

## Approaches considered

### The agent flow (founder: "Refined B (Recommended)")
| Option | What it meant | Chosen? |
|---|---|---|
| A: specialists on every message | A coordinator hands every message to an area, council or compare agent | No: 2 to 3 model calls on every message |
| **B refined: one agent, plus a capped team for comparisons** | Router, then one agent for simple questions, a team for comparisons | **Chosen** |
| B without caps or code routing | The orchestrator decides freely how many workers to start | No |
| C: single agent now, multi-agent later | Multi-agent waits for stage 6 document investigation (0023) | No |

Evidence (fact-checked): Anthropic recommends "finding the simplest solution possible, and only increasing complexity when needed", and agentic systems "trade latency and cost for better task performance" ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)); multi-agent systems "use about 15× more tokens than chats", and "direct comparisons might need 2-4 subagents with 10-15 calls each" ([multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)). Microsoft Agent Framework names Sequential, Concurrent, Handoff, Group Chat and Magentic orchestrations ([orchestrations](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/)). LangGraph's multi-agent page could not be read; the trial reads it.

### Provider (founder: "Go with Claude", then, after the fact-check, "Keep Claude (Recommended)")
Compared on 20 Nov 2026: Anthropic, OpenAI, Azure (EU data zone), Google Vertex (Gemini, London), Mistral (EU). Anthropic was chosen for its no-training term, a real hard spend limit and low cost. The others' trade-offs: Mistral's contract allows training unless opted out; Vertex and Azure have no confirmed hard spend cap for a small account; OpenAI's EU processing needs sales approval.

### Tracing (founder: "LangSmith anyway", over the agent's "Ask LangChain; Phoenix if no", then "Request opt-out, tell visitors (Recommended)")
| | LangSmith, EU, free plan (chosen) | Phoenix, self-hosted (agent's earlier recommendation) |
|---|---|---|
| Where | Netherlands (GCP europe-west4); LangChain has "no legal entity in the EU for customer contracting" ([regions FAQ](https://docs.smith.langchain.com/reference/regions_faq)) | Our server and Neon Frankfurt |
| Retention | Base traces 14 days on LangSmith Cloud; automation rules upgrade a trace to extended retention (180 days by default) ([usage and billing](https://docs.langchain.com/langsmith/usage-and-billing)) | A days setting (defaults to keep forever) |
| Delete one trace | API; "Most deletes are hardened within 6 hours or sooner" ([data purging](https://docs.langchain.com/langsmith/data-purging-compliance)); "Some metadata … may be retained indefinitely" | API |
| Training | Two terms pages, both updated 19 Nov 2026: the Enterprise Terms say LangChain "will not use Customer Data to train"; the Standard Terms, which cover anyone who uses the platform "including via a Free Access Plans", say it "may use Customer Data to (a) train and develop its models … unless Customer opts out", with no opt-out method described ([terms](https://www.langchain.com/terms-of-service), [standard terms](https://www.langchain.com/standard-terms-of-service)) | None (our server) |
| Cost | $0: 1 seat, 5,000 base traces a month without a card ([pricing](https://www.langchain.com/pricing)) | $0; memory on our server |

Langfuse was ruled out: self-hosting needs "at least 4 cores and 16 GiB of memory", and its retention setting needs a paid licence key. LangSmith's self-hosting is Enterprise only.

## Decisions

### 1. The flow
```
visitor message (after the consent step, 0063)
  → classifier (Haiku 5.5): area | council | comparison | verdict request | off topic
       off topic        → fixed reply (founder's copy review)
       verdict request  → AI-11's fixed reply
       area, council    → one chat agent with the area and council tools (Haiku 5.5)
       comparison       → the team:
            orchestrator (Haiku 5.5): splits the question into parts, at most 3 areas
            workers in parallel (Haiku 5.5): each gathers one part with the tested tools
            writer (Sonnet 5.5): one answer with widgets, words only around tool figures
            checker: first plain code (every figure in the answer must match a tool result),
                     then Sonnet 5.5 for what code can't judge (verdict-like claims, facts said without their tool)
  → output guard, sentence by sentence (AI-13) → streamed to the page
```
- **The compare button skips the team (agent's call, builder check):** "Compare these two" on the compare page calls the tested compare tool directly, with no AI cost (0025: route by plain code where the screen knows the task). The team handles typed comparisons that need planning (several areas or topics, for example "these three areas for a family with young children"), so it does work a single tool call can't.
- **Limits (agent's call, numbers set in the plan):** at most 3 areas, a fixed number of tool calls per worker, and a time limit per comparison.
- **The checker fails closed (agent's call):** if a figure doesn't match a tool result, the answer isn't shown; the visitor sees a short "couldn't check this answer" message. It **counts** toward the daily limit by its route (a failed comparison counts 3, like a successful one), as 0058 and 0063 count a guard-stopped answer, so failures can't be triggered for free (builder check).
- **Code before model (agent's call, builder check):** the figure check is plain, tested code, so rule 2 is enforced deterministically; the Sonnet checker only judges what code can't. The single agent's answers get the same code figure check inside AI-13's sentence guard.
- **Streaming (agent's call):** comparisons stream progress steps ("Planning…", "Checking area 1 of 3…", "Checking figures…") and then the checked answer; simple answers stream sentence by sentence (AI-13).
- **Follow-ups (agent's call):** each turn is classified again, with the conversation so far; it counts by the route it takes (team 3, single agent 1).
- **Classifier testing (agent's call):** tested against the AI-03 set plus new off-topic and borderline cases (for example "is it noisy near the station?") so it doesn't refuse fair questions; the AI-03 set gains a version with these cases.

### 2. Counting (founder: "Counts as 3 messages (Recommended)")
A comparison uses 3 of the 15 messages per IP address per day; the chat says so before running it. Up to 5 comparisons a day.

### 3. Provider: Anthropic (AI-01)
Checked against Anthropic's own pages:
- "Anthropic may not train models on Customer Content from Services"; the DPA is "incorporated into these Terms by reference" ([commercial terms](https://www.anthropic.com/legal/commercial-terms)), with a UK Addendum for UK GDPR processing ([DPA](https://www.anthropic.com/legal/data-processing-addendum)). The terms are "not for consumer use"; running a website as its developer fits them.
- Retention: "we automatically delete inputs and outputs on our backend within 30 days of receipt or generation"; flagged content may be kept "for up to 2 years" ([retention policy](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data)). (An earlier draft said "not retained by default", from one docs page; corrected.)
- Where: inference "Only "us" and "global" are available", and stored data is in the US ([data residency](https://platform.claude.com/docs/en/manage-claude/data-residency)): a transfer outside the UK, under the DPA's UK Addendum. The Privacy notice and the DPIA say so.
- Spend limit: an organisation can set its own monthly limit; once reached, requests fail until the month resets ([rate limits](https://platform.claude.com/docs/en/api/rate-limits)).
- **Package:** the `anthropic` Python SDK (Apache-2.0; [repository](https://github.com/anthropics/anthropic-sdk-python)), approved by this choice.

### 4. Models (founder: "Haiku + Sonnet writer/checker", over the agent's "Start Haiku, upgrade if tests fail")
- **Claude Haiku 5.5** (`claude-haiku-5-5`) for the classifier, the single agent, the orchestrator and the workers: $0.10 input and $0.50 output per million tokens for prompts up to 100,000 tokens, $0.50 and $2.50 above ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)).
- **Claude Sonnet 5.5** (`claude-sonnet-5-5`) for the comparison writer and checker: $2 and $10 per million tokens.
- Estimate (agent's, on assumed sizes, not a quote): about $20 a month for 3,000 simple questions and 500 comparisons.

### 5. Monthly cap: £25 (IN-05; founder: "£25 a month (Recommended)")
- **Our app** adds up each request's cost from its token counts and pauses the chat at 95% of the cap ("Chat is paused for this month, the area check still works", 0058); the area pages keep working (agent's call).
- **Anthropic's spend limit** is set at the cap as a second guard, in US dollars at the nearest equivalent (agent's call).
- AI-03 test runs and the AI-09 trial use a **separate workspace or key with its own small limit**, so tests never use visitors' budget (agent's call; the limit is set in the plan).

### 6. Tracing: LangSmith, EU, free plan
- Traces go to LangSmith's EU instance. Base traces are kept **14 days** (shorter than 0063's 30), with **no automation rules**, so no trace moves to extended retention. A request to delete a trace is done by API (usually within 6 hours); some metadata may be kept indefinitely, as LangChain's docs say.
- **Training:** we email LangChain support to opt our account out of training (their Standard Terms allow it). **Until LangChain confirms in writing**, the Privacy notice and the consent statement say traces go to LangChain, whose terms allow training unless we opt out, and that we have asked to opt out; once confirmed, that line is removed. The confirmation is kept with the project's records.
- **Scrubbing before export (agent's call, builder check):** the identifier filter and the consent receipt (0063) are applied on our server before anything is sent to LangSmith; the plan confirms the SDK or exporter lets us process inputs before export, or we export through our own processor. Chat text appears only in trace inputs and outputs, never in metadata or tags, because LangSmith may keep metadata indefinitely; the consent receipt (a time and a statement version, no text) goes in metadata; it identifies no one on its own, so its possible indefinite keeping doesn't breach 0063's deletion rule for chat text.
- **0051's "No training" rule** covers the AI model provider (Anthropic, which may not train). LangChain is the tracing tool; the founder accepted its opt-out-pending position with visitors told ("Request opt-out, tell visitors (Recommended)"), so the written opt-out is not a launch blocker.
- No payment method on the account, so it stays within 5,000 traces a month and is never billed (agent's call; when the limit is reached, traces stop and the chat keeps working).
- The Standard DPA applies through the Standard Terms; the DPIA names LangChain, the Netherlands storage and the US billing data.
- **Package:** the `langsmith` Python SDK (MIT; [repository](https://github.com/langchain-ai/langsmith-sdk)), approved by this choice.

### 7. The AI-09 trial (agent's call)
The trial builds this flow (decision 1) in both Microsoft Agent Framework for Python and LangGraph, with test conversations only, and compares them on streaming to the page (AG-UI), tracing into LangSmith (LangSmith documents a [Microsoft Agent Framework integration](https://docs.langchain.com/langsmith/trace-with-microsoft-agent-framework)), running the AI-03 set, cost per answer and time to first text. The founder chooses the framework from the results (AI-04); the framework's packages then need the founder's approval (0035).

### 8. The AI-03 runner (agent's call)
Our own Python runner applies AI-15's marking rules; only the final run before a change is recorded as a LangSmith experiment, so test runs don't use up the 5,000 traces a month. It runs on demand and before any change to prompts, models or tools, not in `make check` or CI (0029: live-service tests stay out of the merge gate), under the test workspace's own spend limit.

### 9. Plan scope (agent's call, builder check)
The shared parts (classifier, tools, cost counter, scrubbing, code figure check, counting) are built once behind framework-neutral interfaces (AI-04); the AI-09 trial wires them into both frameworks so the comparison is like for like; the build plan for the chosen framework follows the founder's choice. The chat's screen design step (0063) comes before the build plan; the trial needs no screens.

## What this changes in the records
- **New decision 0064 (AI-16).** Register: AI-01 (Anthropic), AI-04 (the flow's shape; framework still after AI-09), AI-09 (the trial task), AI-03 (runner, classifier cases), IN-05 (£25), a new line approving `anthropic` and `langsmith`.
- **0063** is amended: traces are kept 14 days in LangSmith (Netherlands), not 30; the consent statement and Privacy notice name Anthropic (US or global processing, up to 30 days, flagged content up to 2 years) and LangChain (training wording until the opt-out is confirmed).
- **Status file** updated.

## What is left
- **To the founder:** latency targets (0058: set in the plan); the framework after the AI-09 trial; the off-topic reply and consent wording (copy review).
- **To the builder:** prompts and tool schemas, the classifier's prompt and labels, the team's limits, the cost counter, the workspace setup, the trial's measures.
