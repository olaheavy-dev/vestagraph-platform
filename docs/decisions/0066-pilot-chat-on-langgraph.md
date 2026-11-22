# 0066: The pilot chat is built on LangGraph

**ID:** AI-04 (with register line BE-44)  
**Status:** Accepted (founder, 22 Nov 2026, prompt window: "LangGraph (Recommended)")  
**Date:** 2026-11-22  
**Stage:** 5b  
**Amends (no older text is rewritten):** [0023](0023-microsoft-agent-framework.md) (Microsoft Agent Framework is no longer the chat's framework; 0049 had already reopened the choice); [0049](0049-back-to-python-final.md) item 9 (the trial ran, and decided).  
**Evidence:** [AI-09 trial results](../reviews/2026-11-22-ai-09-trial.md), from the trial's [design](../superpowers/specs/2026-11-21-ai-09-trial-design.md) and [plan](../superpowers/plans/2026-11-21-ai-09-trial.md).

## Context
0064 fixed the chat's flow (a classifier, one agent for simple questions, a capped team for comparisons) and left the framework to the AI-09 trial. The trial built the same flow in LangGraph and in Microsoft Agent Framework for Python (MAF), on the same shared prompts, tools, models and caps, and ran 87 AI-03 cases through both. The founder chose a balanced scorecard (answer quality, cost and speed, showcase clarity, maintenance; equal weights).

## Options
- **LangGraph** (13 on the scorecard): one nested trace per answer in LangSmith, explicit parallel fan-out, `langgraph` 1.x stable; its AG-UI adapter is pre-1.0.
- **Microsoft Agent Framework** (12): typed hand-offs, strong documentation; a beta Anthropic connector, traces fragmented in LangSmith (possibly the template's set-up, olaheavy-dev/house-template-fastapi#142), a fragile counting workaround.
- **Fix MAF's tracing, then decide:** fairer to MAF on its weakest point, at the cost of a template change and another short run.

The trial found the two equal on answers (79 of 84 scored cases the same; none of the 5 differences was a framework difference), cost ($1.54 for LangGraph and $1.55 for MAF over the full run) and speed (full answer about 4.5 to 4.6 s median; first text about 3.7 to 3.8 s median; about 26 s at the slowest 5%, which are comparisons).

## Decision
**LangGraph** (founder, 22 Nov 2026, prompt window: "LangGraph (Recommended)"). Before choosing, the founder asked (typed): "Sould we use langraph for maf for layover, another project?" [sic]. The agent answered that using LangGraph here and MAF in another project is a reasonable way to show both to employers, as long as each project keeps to one framework, and that the other project's choice is made there (MAF's OpenAI and Azure OpenAI connectors are more mature than its Anthropic one, which is a beta).

**Packages approved by this choice (BE-44, all MIT, versions from the trial):** `langgraph` (1.2.20), `langchain-core` (1.8.0), `langchain` (1.5.0), `langchain-anthropic` (1.7.10), `ag-ui-langgraph` (0.0.47; pre-1.0, so a minor bump counts as major for merging, 0049; the rule for 0.0.x packages is #381) and its `ag-ui-protocol` (1.0.0). `langsmith` and `anthropic` were approved in 0064 (BE-43). The exact pins are set when the chat's code is added, and `docs/references/third-party.md` is updated then.

## Consequences
- This decides the pilot chat only; later chats (stage 6 home workspace, the document investigation) revisit the choice.
- The chat's build plan uses LangGraph: the router and the team as a graph, workers fanned out in parallel, streaming to the page over AG-UI through `ag-ui-langgraph`.
- The trial's lessons carry into that plan: ask for structured output wherever code parses a reply; tools return the data files' display text; prompts say to quote labels, figures and dates as given; record empty or cut-off answers as errors; tag internal model calls so their words never reach the stream; the output guard also on the single-agent route (WCHAT-10).
- Answer quality was limited by the shared prompts and tools in both frameworks (about a third of cases passed); improving it against the AI-03 set is part of the build plan, not a framework question.
- The template's MAF tracing set-up is reported upstream (house-template-fastapi#142). MAF stays available in the template for other projects.
- **Revisit if** `ag-ui-langgraph` stalls before 1.0 or breaks often, or LangSmith tracing stops being the tracing tool (0064).
