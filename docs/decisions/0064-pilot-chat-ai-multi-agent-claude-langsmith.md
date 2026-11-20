# 0064: The pilot chat's AI: a router, one agent and a capped multi-agent team, on Claude, traced in LangSmith

**ID:** AI-16 (with register lines AI-01, AI-03, AI-04, AI-09, IN-05 and BE-43)  
**Status:** Accepted (founder, 20 Nov 2026, prompt windows; the design approved with "Approve (Recommended)", including the agent's calls: a code-first checker, and the compare button calling the compare tool directly)  
**Date:** 2026-11-20  
**Stage:** 5b (group D of the stage 5b decisions)  
**Amends (no older text is rewritten):** [0063](0063-pilot-privacy-and-anonymous-chat-first.md) (traces are kept 14 days in LangSmith, not 30; the notice and consent statement name Anthropic and LangChain); [0023](0023-microsoft-agent-framework.md) ("the chat panel: a single agent with a session" becomes a router, one agent and a capped team for comparisons).  
**Design:** [`2026-11-20-stage-5b-ai-design.md`](../superpowers/specs/2026-11-20-stage-5b-ai-design.md), which holds the options, the fact-checked sources, every founder answer and every agent's call.

## Context
0063 opened the pilot's chat to anonymous visitors. Group D settles how it is built. The founder agreed to an intent classifier and asked for a multi-agent flow: "mainly to show employers i can build multi-agent systems but it also fits the application" [sic] (typed), then "make sure we are making the best decision". After the founder said the agent had been "mixing up decisions by not doing your due diligemce" [sic], an independent fact-check read every outside claim against its primary source, and the founder re-decided the choices it affected.

## Decision
The founder's choices, 20 Nov 2026, in prompt windows unless marked typed:
1. **Flow: "Refined B (Recommended)".** A classifier routes off-topic and verdict questions to fixed replies, simple area and council questions to one agent, and comparisons to a team: an orchestrator, parallel workers, a writer and a checker that confirms every figure came from a tool. At most 3 areas; plain code routes straight to the team where the page already knows it is a comparison. Supported by Anthropic's guidance (simplest first; multi-agent for breadth, about 15× the tokens).
2. **A comparison counts as 3 of the 15 daily messages** ("Counts as 3 messages (Recommended)").
3. **Provider: Anthropic** ("Go with Claude"; after the fact-check corrected retention to "within 30 days", flagged up to 2 years: "Keep Claude (Recommended)"). No training on our content; a hard spend limit; processing in the US or "global" under the DPA's UK Addendum. Approves the `anthropic` package (Apache-2.0).
4. **Models: "Haiku + Sonnet writer/checker"** (over the agent's "Start Haiku, upgrade if tests fail"): Haiku 5.5 for the classifier, the single agent, the orchestrator and the workers; Sonnet 5.5 for the writer and checker. About $20 a month at the assumed use (an estimate).
5. **Monthly cap: £25** ("£25 a month (Recommended)"): our app pauses the chat at 95%; Anthropic's spend limit is the second guard; tests use a separate workspace with its own limit.
6. **Tracing: LangSmith, EU, free plan** ("LangSmith anyway", over the agent's "Ask LangChain; Phoenix if no", which the agent recommended because LangChain's Standard Terms allow training "unless Customer opts out"); then "Request opt-out, tell visitors (Recommended)": we ask LangChain to opt us out, and until it confirms in writing, the notice and the consent statement say so. Base traces kept 14 days, no automation rules, no payment method. Approves the `langsmith` package (MIT).
7. **The AI-09 trial** builds this flow in both Microsoft Agent Framework and LangGraph with test conversations, and the founder chooses the framework from the results (AI-04).

## Consequences
- **0051's provider safeguard** ("No training, short checks OK": inputs "kept only briefly for abuse checks") is met by Anthropic's no-training term and deletion within 30 days; flagged content kept up to 2 years is the one longer case, which the founder accepted with "Keep Claude (Recommended)" and the notice states.
- Simple questions stay cheap; comparisons carry the multi-agent showcase and its cost, limited by the 3-message count, the 3-area limit and the £25 cap.
- Chat text leaves the UK twice: to Anthropic (US or global) and to LangChain (Netherlands, with US billing data); both are named in the Privacy notice, the DPIA and the consent statement.
- LangSmith's training position rests on an opt-out request until LangChain confirms; the founder accepted that over the agent's recommendation.
- **Revisit if** the AI-03 results show Haiku isn't good enough for a role, the cap is reached often, LangChain refuses the opt-out, or the trial shows the team adds no value over one agent.
