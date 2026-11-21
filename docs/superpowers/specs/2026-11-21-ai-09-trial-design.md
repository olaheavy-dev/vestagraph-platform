# Stage 5b: the AI-09 framework trial: design

**Date:** 21 Nov 2026  
**Status:** Draft for the founder's approval  
**Follows:** [0064](../../decisions/0064-pilot-chat-ai-multi-agent-claude-langsmith.md) (the flow; design section 7, the trial), [0049](../../decisions/0049-back-to-python-final.md) item 9 (the trial runs in the founder's template), register lines AI-09 and AI-04.  
**Next:** the plan (`writing-plans`), then the trial, then the founder's choice of framework (AI-04) and the framework packages' approval (0035).

## Intent and why
0064 fixed the chat's flow: a classifier routes off-topic and verdict questions to fixed replies, simple area and council questions to one agent, and typed comparisons to a capped team (orchestrator, parallel workers, a writer and a code-first checker). It left one choice open: build it in **Microsoft Agent Framework for Python (MAF)** or in **LangGraph**. The founder chooses from evidence, and the founder's reason for the multi-agent flow is to show employers they can build multi-agent systems, while keeping the product sound ("make sure we are making the best decision", 20 Nov 2026). The trial builds the same flow in both and scores them.

## Goals
- The 0064 flow running end to end in both frameworks, on the same shared parts, with test conversations only.
- A scorecard with four equal parts (founder, 21 Nov 2026, prompt window: **"Balanced scorecard (Recommended)"**): answer quality, cost and speed, how clearly the multi-agent part reads in code and traces (the showcase), and how hard it is to maintain.
- A results review in Vestagraph with a recommendation, then the founder's choice in a prompt window.

## Non-goals
- Screens, the consent card, ALTCHA, the IP limiter, the Neon words table: the chat's build plan, after the choice.
- Production quality code: the trial code is discarded after the choice.
- Changing the flow's shape, models or caps (0064).

## Anti-goals (a failure even if it works)
- A comparison that favours one framework through different prompts, tools, models or settings.
- Any real visitor data, or a real key or trace in a committed file.
- Spending past the trial's limit.
- Framework packages entering Vestagraph before the founder chooses.

## Constraints
- Models and settings from 0064: Claude Haiku 5.5 for the classifier, single agent, orchestrator and workers; Claude Sonnet 5.5 for the writer and checker; at most 3 areas per comparison.
- The trial runs in the **test Anthropic workspace** with its own spend limit (0064 point 5), never the visitors' workspace.
- Tracing to LangSmith EU, a separate trial project, test conversations only (0064 point 6). Test words may go to LangSmith in full (0064: "test conversations and evaluations go to LangSmith in full").
- AGENTS.md rules 1, 2 and 4: tools return figures from the tested packages; the AI never calculates; no verdicts.
- Package versions and APIs are checked against each framework's official documentation at build time (AGENTS.md, `docs/references/third-party.md`), not memory.

## Approaches considered

### Where the trial lives (founder's choice)
- **A separate trial project (chosen):** a private, throwaway project made from the founder's FastAPI template (`house-template-fastapi` v0.11.1, which already has both the LangChain/LangGraph gateway and `llm: maf` with LangSmith tracing, the budget and redaction), outside Vestagraph. It reads Vestagraph's area packages and sample data read-only. Only the results come into Vestagraph.
- **Inside Vestagraph, unmerged:** a spike on a never-merged branch; both frameworks' packages enter Vestagraph's lock file there, and the branch could be merged by mistake.
- **First real API slice:** import the template into Vestagraph's API now (#93) and build both behind one interface; the most work, and it brings the API import forward before its plan.

Founder, 21 Nov 2026, prompt window: **"Separate trial project (Recommended)"**.

### How the choice is weighed (founder's choice)
Balanced scorecard (chosen), over "Showcase first" and "Quality and cost first".

## The design

### 1. The trial project (agent's calls)
- A local folder `~/source/code/portfolio/vestagraph-ai09-trial`, not pushed to any remote (discarded after the choice; the results review keeps what matters). Inside it, **two projects generated with Copier from `house-template-fastapi` v0.11.1**, one answering `llm: langchain` and one `llm: maf` (the template installs one framework per project, never both: builder check), plus a small shared package both depend on, so neither framework needs a hand-added workaround (*agent's call*).
- The template's gateway needs PostgreSQL, so the trial runs a local database in Docker; that is a setup cost, left out of the maintenance score (*agent's call*).
- It reads Vestagraph's `vestagraph_area` package and the files in `packages/fixtures/data/` and `packages/fixtures/generated/` by path, read-only, from a clean checkout of Vestagraph's `main` at a recorded commit.
- The template's existing gateway pieces are used as they are: the budget, redaction, LangSmith tracing and both `llm` paths.

### 2. Shared parts, built once (0064 design section 9)
Written once, framework-neutral, and called by both flows, so the comparison is like for like:
- **Tools** (founder, 21 Nov 2026, prompt window: **"Thin readers in the trial (Recommended)"**, over "Real tools first"): small read-only tools in the shared package (find an area, a topic, council facts, nearby, compare, and the others the AI-03 cases call) that read Vestagraph's tested generated files (`area-result.json`, `council-result.json`) and return typed results with a `kind`. They calculate nothing, so rule 2 holds. The real tools are built in the chat's build plan, after the choice.
- **The classifier:** one prompt and labels (off-topic, verdict, simple, comparison), on Haiku.
- **Fixed replies:** the reviewed texts for off-topic and verdict questions (AI-11).
- **The checker, as 0064 sets it:** code first (every figure in the written answer must appear in a tool result; a sentence that fails is stopped), then Sonnet for verdict-like claims code can't judge. Both steps run, so the cost and speed figures include the Sonnet call production will make (builder check).
- **The cost counter:** each call's tokens, from Anthropic's own reported usage, priced from Anthropic's price page read at build time; reserve before the call, settle after (0064). **It is authoritative** for stopping a run and for the reported spend; the template's budget stays on as a second guard (*agent's call*, builder check).
- **The prompts** for the single agent, orchestrator, workers and writer.

### 3. The two flows
- **LangGraph:** a graph with the classifier as the entry, a branch to the single agent, and the team as an orchestrator that fans out workers in parallel, then the writer, then the checker.
- **MAF:** the same steps as a MAF workflow (fan-out and fan-in), using the template's `llm: maf` client.
- Both stream to a test client over **AG-UI** (each framework's AG-UI adapter); the test client records events and times. No screens.

### 4. What is measured
| Part of the scorecard | Measures |
|---|---|
| Answer quality | The AI-03 cases that apply to the chat (`packages/fixtures/evaluation/ai-03-set.json`, marked by AI-15's rules), pass rate per framework, with the single agent's and the team's results shown apart; cases that cite scenarios moved out of the pilot (#373) are left out. AI-15's judge is Claude Sonnet 5.5, and its calls count towards the trial's limit (*agent's call*) |
| Cost and speed | Cost per simple answer and per comparison (from the cost counter, in US dollars); time to first text and to a complete answer (median and 95th percentile) |
| Showcase clarity | How clearly the team's work reads: the LangSmith trace of one comparison in each framework (screenshots for the founder), and the size and shape of the team's code; judged by a fresh reviewer and shown to the founder |
| Maintenance | Lines of code for the flow, number of extra packages, release maturity (stable or pre-1.0), documentation quality, and how many workarounds were needed |

Each part is scored 1 to 5 with its evidence; the total is the plain sum (equal weights). Ties go to the founder with both sets of evidence.

### 4b. New comparison cases first (founder, 21 Nov 2026, prompt window: **"Add to AI-03 set (Recommended)"**, over "Trial-only cases")
Only 2 of the 152 AI-03 cases send a comparison to the team (CHAT-COMPARE-POSTCODES-01, CHAT-COMPARE-COUNCILS-01); the rest were about saved areas, now out of the pilot (#373). So before the trial, a reviewed Vestagraph pull request adds about 10 comparison cases to the AI-03 set (a new set version): two and three areas, a council pair, a topic missing on one side, a source down on one side, a figure the checker must stop, a verdict-like sentence the checker must stop, a low balance (WCHAT-144), and a comparison that doesn't fit the day's budget (WCHAT-147), each with AI-15's examples and the scenario it covers. They serve the real chat afterwards too.

### 5. Spend and safety
- **Trial limit: $10 in total, $1 per run** (the founder's earlier MAF trial cap, 12 Nov 2026), set as the test workspace's spend limit by the founder and checked again by the cost counter, which stops a run at its limit.
- Test conversations use the synthetic postcodes (NB1 4XY, NB7 1RR, NB9 9ZZ, ZZ4 4ZZ, ZZ5 5ZZ). No real data.
- The API key lives in the founder's providers file, is loaded only in a subshell and never printed or committed.

### 6. What comes back into Vestagraph
- A results review `docs/reviews/2026-11-NN-ai-09-trial.md`: the scorecard, the evidence, the trial project's template version and Vestagraph commit, total spend, and a recommendation.
- After the founder's choice: decision 0066 (AI-04), the framework's packages approved and added to the pre-approved list, `docs/references/third-party.md`, and the register. The chat's build plan follows.

## What the founder needs to do first
1. Create a **test workspace** in the Anthropic Console with a **$10 spend limit** and an API key for it, and put the key in the providers file the agents already use (a step only the founder can do: agents never create accounts or keys).
2. Confirm LangSmith's trial project can use the existing EU account.

## What is left to the builder (the plan)
The prompts' text, the classifier's labels' wording, the case subset that fits in $10 (AI-15 runs each rule case 3 times, in both frameworks, judge included), the exact AG-UI test client, the workflow shapes in each framework's current API, and the code-size measure.

## Calls the agent made (for the founder to check)
- Two generated projects and a shared package; a local Postgres in Docker, kept out of the scoring.
- The cost counter is authoritative for stopping and reporting spend; the template's budget is a second guard.
- Sonnet 5.5 as AI-15's judge, counted in the $10.
- The trial folder is local only and discarded after the choice.
