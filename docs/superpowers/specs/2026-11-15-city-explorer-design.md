# City Explorer: one page per council (design)

**Date:** 15 Nov 2026 · **Stage:** 3 (for the pilot, stage 5b) · **Decision:** [0055](../../decisions/0055-city-explorer-in-the-pilot.md) (PD-17) · **Research:** [City Explorer research](../../reviews/2026-11-14-city-explorer-research.md), [City Explorer data research](../../reviews/2026-11-15-city-explorer-data-research.md) · **Status:** approved by the founder (15 Nov 2026, prompt window: "Approve (Recommended)"), with the agent's calls marked in the text

## Intent
City Explorer gives people who are researching a move **before they have a postcode** a page for each council area in England. The founder chose it for the pilot to "Reach people earlier" (0055). In this brainstorm the founder set the bar: it must set Vestagraph apart from the ONS's free [Explore local statistics](https://www.ons.gov.uk/explore-local-statistics/) service and give people a reason to come back (founder, 15 Nov 2026, typed: "what would set us apart and keep customer hooked and also set us apart from ONS?").

The ONS service already shows 116 council indicators, compares councils ([City Explorer research](../../reviews/2026-11-14-city-explorer-research.md), 0055) and charts house prices by council ([data research](../../reviews/2026-11-15-city-explorer-data-research.md), topic 4). What it never does is turn a figure into **what a home would cost you each month**, or take you from a council **down to a postcode**. City Explorer is built around those two things.

## Founder answers (15 Nov 2026)
Prompt windows unless marked typed; the founder's own words in quotes.
- **What a visitor leaves with:** "What it costs (Recommended)": the page leads with what living in the council area costs.
- **Who it serves:** "Both equally (Recommended)": buyers and renters side by side.
- **Link into the postcode check:** "Search box and map" (over the agent's "Search box (Recommended)").
- **First-version topics:** council tax by band, private rents, the affordability ratio, the UK House Price Index, DfT transport connectivity, who rents and who owns (Census 2021), and population as one line under the council's name.
- **Order:** the founder typed "keep cost first in the summary, and make the order match what you think"; the agent's order is in "The page" below.
- **Later:** air quality, new homes and housing supply, travel to work, universities. **Dropped:** broadband and mobile ("we already have broadband in the postcode check and more useful there"), life expectancy, earnings.
- **Approach:** "Chart-led profile page", over the agent's "Same layout (Recommended)". Reason, typed: "this should be part of the brainstorm and deep thinking, what would set us apart and keep customer hooked and also set us apart from ONS?"
- **Charts that set it apart, first version:** all four offered: "Rent vs buy monthly (Recommended)", "Plain-words captions (Recommended)", "Neighbourhood map", "Your budget".
- **Reasons to come back, first version:** all four offered: "What changed (Recommended)", "Compare two councils", "Ask the area chat", "Share or print summary" (the area chat later left the pilot, below).
- **Delivery:** "Two parts, both pre-gate (Recommended)": part 1 is the council page; part 2 adds compare, the area chat and tools (the chat later left the pilot, below), share or print, and what changed. Both are in the pilot; the pilot gate (0052) waits for both.
- **Interest rate for rent vs buy:** "Official average (Recommended)": the Bank of England's published average rate on new mortgages, labelled with its month, editable.
- **AI tools:** "Chat and tools, part 2 (Recommended)": the area chat and the public area tools (MCP, 0051) both cover council pages (the chat part superseded by the next answer).
- **On-page AI chat leaves the pilot** (same session, after the answer above): the founder typed "I am thinking we should move anything AI chat to when after the pilot, this is just a discussion, the AI chat when a user logs in will have different tabs like comparison, property search, like the competitor, and just do claude and chatgpt mcp connection", then chose "Move chat after pilot (Recommended)". So City Explorer has **no on-page chat**; council tools in ChatGPT and Claude (MCP) stay in part 2. Recorded for the whole pilot in decision [0056](../../decisions/0056-no-on-page-chat-in-the-pilot.md), which amends 0051.

## Goals
1. **Cost first.** The page opens with what living there costs: council tax for one band, the average monthly rent and the average house price, side by side.
2. **Rent or buy, per month.** The average rent beside the monthly cost of buying the average-priced home (repayment plus council tax), from the cost engine, with every assumption shown and the deposit, rate and term editable. These are council-level figures for anyone, not a saved home's costs: 0046 put a home's costs, compare and what changed behind sign-in, and the founder's choices here put their council-level forms on a public page; decision [0056](../../decisions/0056-no-on-page-chat-in-the-pilot.md) records that clarification of 0046 (its point 6) with the chat change.
3. **A chart for every topic**, each with a one-sentence plain-words caption built by rule from tested figures, never by AI.
4. **Your budget.** A monthly budget the visitor types; each cost line says whether it is within or above it.
5. **From council to postcode.** A "check a postcode in this council" box and a neighbourhood map whose areas open the postcode check.
6. **Reasons to return (part 2):** what changed since the last visit, compare two councils, council facts in the visitor's own ChatGPT or Claude (the area tools, MCP), share or print a summary.

## Non-goals
- Later topics (air quality, new homes, travel to work, universities) and dropped ones (broadband and mobile, life expectancy, earnings).
- Accounts, saved councils on a server, email alerts (0046: no accounts in the pilot).
- Wales, Scotland and Northern Ireland: "not yet covered" (rule 6), though the data contract keeps a nation field.
- Price or rent forecasts of any kind.
- An on-page AI chat (moved to the signed-in workspace after the pilot, founder 15 Nov 2026).
- Searching by street or house: that is the postcode check's job.

## Anti-goals (a failure even if it looks good)
- **A ranking of councils**, a "1st of N", a table sorted by a figure, or a "best" or "better area" word (0054, FE-22, rule 4). Compare shows two councils side by side in the order the visitor picked them.
- **A score or rank drawn on a map** (0054: ranks are "never drawn on maps").
- **Advice.** Rent vs buy is arithmetic with its inputs on show, never "you should buy".
- **A figure typed by hand** (rule 2), a caption written by AI, or AI working out a number (rule 4, 0004).
- **Missing data shown as zero**, a flat line or a gap-free chart (rule 7): a missing month is a visible gap; a council a source doesn't publish (for example City of London for rents) says so.
- **A copy of the ONS service.** The page as a whole must add the cost and postcode links the ONS service lacks; if the design shows it only repeats that service, 0055's last consequence (narrow to its option A) applies. Single sections the founder chose (the affordability ratio, which the ONS also shows) stay; the average house price also feeds rent or buy and the budget check.

## Constraints
- **Unit:** one page per council, titled with its name (for example "Northbridge Council area"), searchable by city or town name (0055 point 3). Every figure is at its official level, with its source, edition and period (DA-14). Two-tier areas: county-level figures say so.
- **Look:** the pilot's brand system (soft gloss FE-29, ledger rows FE-30, source stamps FE-33, slate-ink dark mode FE-31, seven type sizes, three weights, `.design/prototype/tokens.css`). Charts are a new component and get their own style rules on the canvas's Brand and style page before the boards.
- **Accessibility:** WCAG 2.2 AA in both themes; every chart has a table view and a text alternative (its caption plus the values); colour is never the only way a series is told apart; touch targets at least 44 px; no sideways scrolling at 320 to 390 px.
- **Figures:** inputs live once in sample data with their source; every calculated figure (band amounts, monthly amounts, the rent-vs-buy figures, caption changes, within or above budget, what changed) comes from tested code (rule 2), with test expectations worked out independently.
- **Privacy:** typed place names, postcodes, budgets, the rent-vs-buy inputs and the compare choice are never stored or logged (0046, 0014, 0053). They travel in the request body or the URL fragment, never the query string; the privacy notice names them; the gate's log checks cover them (0053). A council page's own address (for example `/council/northbridge`) is an ordinary page view, logged like any page, with IP addresses dropped or anonymised before logs are written (0046). The new endpoints (budget, rent or buy, compare, place-name search) carry the same rate limits as the pilot's other public endpoints. "What changed" remembers only in the visitor's browser and only after the PECR check (part 2).
- **Licences:** every new source gets its DA-05 check and a `docs/references/data-sources.md` entry before build. "Bank of England" is a trade mark ([legal page](https://www.bankofengland.co.uk/legal), as recorded in `data-sources.md`): the page names it as a source only.

## Approaches
Considered for the page (the founder chose B):
- **A. Same layout at council level** (the agent's recommendation): reuse the postcode result's rows, sheets and states, with trends only inside topic sheets. Fewest boards, smallest delay to the gate.
- **B. Chart-led profile page (chosen):** its own page, a chart for every topic, plus the features that set it apart. Distinctive; more boards, specs and sources; the gate moves later. The founder's reason is above. This replaces 0055 point 4's "reusing that layout" for the page; the brand system, source stamps, states, "How we got this" and About the data are still reused (noted on PD-17).
- **Dropped:** a council section inside the postcode result only (0055's option A, declined for "Reach people earlier").

Delivery (the founder chose the first): **two parts, both before the gate**; part 2 after launch; all at once.

## The page (part 1)
Sketch only. `<…>` marks a value the boards take from sample data or a generated file; the council is synthetic.
```
Northbridge Council area (sample)                [Compare] [Share]
Population <n> (mid-<year>)          Check a postcode here [________]

What it costs here
  Council tax, Band D  £<n> a year (£<n> a month)
  Average rent         £<n> a month
  Average price        £<n>
  Your monthly budget  [£____]   → each line: "within your budget" / "above it"

Rent or buy, per month                 Deposit [10%]  Rate [<r>%]  Term [25 yrs]
  Rent  ▇▇▇▇▇▇ £<n>    (rent £<n> + council tax £<n>)
  Buy   ▇▇▇▇▇▇▇▇ £<n>  (repayment £<n> + council tax £<n>)
  "On these inputs, buying the average-priced home costs £<n> more a month than the average rent."
  (or "… £<n> less …" / "… about the same as …"; averages of different homes)

Council tax by band      bars A–H                       + caption
Private rents            line, monthly                  + caption
House prices             line, monthly                  + caption
Affordability ratio      line, yearly                   + caption
Who rents, who owns      one stacked bar, 2021          + caption
Neighbourhoods           map; tap one → its facts and "Check a postcode here"
How we got this
```

### Sections in order (agent's order at the founder's request)
1. **Header:** the council's name, population as one line ("Population <n> (mid-<year> estimate)", ONS), the postcode box, and part 2's Compare and Share.
2. **What it costs here:** three figures side by side: council tax for **Band D**, the average monthly rent and the average house price. *Agent's call:* Band D because it is the official reference band every council publishes; "the most common band here" would need another dataset (VOA stock by band). Monthly council tax is the yearly amount divided by 12 (the rule #197 asks to record; this design relies on it).
3. **Your budget:** one optional box, "Your monthly budget". Rent plus council tax and the buying cost plus council tax each say "within your budget" or "above it". Empty box: no labels, no nagging. *Agent's call:* handled like priority limits (0053): the amount goes to a tested module on the server, which answers within or above; never stored or logged; never in a share link or printout.
4. **Rent or buy, per month:** renting = the average monthly rent plus council tax for Band D monthly; buying = the monthly repayment on the average price (cost engine, `vestagraph_engine`) plus the same council tax. Council tax is on both sides because the person living in a home, owner or tenant, normally pays it (*agent's call*, fixing a builder-check P1: leaving it off the rent side would overstate the gap by the whole monthly council tax). With the example inputs the figures are in the generated file; when the visitor changes an input, the inputs go to the same tested module on the server (0053's pattern), never stored or logged. Example inputs, labelled "example" and editable: deposit 10%, term 25 years (*agent's calls*), and the Bank of England's published average rate on new mortgages for the latest month (founder). Labelled "repayment and council tax only; not the full cost of owning or renting", and "the average rent and the average price describe different homes" (the rent covers every size of rented home and the price every type sold), also in "How we got this". The difference sentence follows the caption rules, with three patterns: "more", "less" and "about the same" (within the same stated threshold as "unchanged"). Inputs are checked first: deposit from 0% to below 100% of the price, a term of 1 to 40 years, a rate from 0% (repayment is then the loan divided by the months, no interest; worked test case needed) to a stated upper bound; negative, empty or non-numeric values say what is wrong and show no figure.
5. **Council tax by band:** bars for A to H. Band amounts quoted from MHCLG if its table publishes them per band; otherwise derived from Band D by the fixed proportions in a tested module: A 6/9, B 7/9, C 8/9, D 9/9, E 11/9, F 13/9, G 15/9, H 18/9 (as MHCLG's [technical notes](https://www.gov.uk/government/statistics/council-tax-levels-set-by-local-authorities-in-england-2026-to-2027/council-tax-levels-set-by-local-authorities-in-england-2026-to-2027-technical-notes) state, per the data research; the statutory source, section 5 of the Local Government Finance Act 1992, to confirm). These go in a versioned rule table with source and effective date (rule 3), which the founder merges (AGENTS.md: tax rule tables). Labelled "average for the council area, two adults, before discounts; parish charges vary".
6. **Private rents:** a monthly line from the ONS Price Index of Private Rents, with the latest provisional months marked "provisional" and the series' status quoted from the ONS at build. *Two ONS texts differ:* the bulletin says it became official statistics on 20 May 2026, "not yet accredited" (data research, topic 8), while the spreadsheet's cover sheet says "official statistics in development"; the licence check settles which to quote. Checked 15 Nov 2026 (recorded in the data research, topic 8): the [dataset](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/priceindexofprivaterentsukmonthlypricestatistics) spreadsheet (21 Oct 2026 edition, OGL v3.0) has a "Rental price" column in pounds per area, councils included, "rounded to the nearest £1" (its note 6), with index columns by bedroom count, from January 2015.
7. **House prices:** a monthly line from the UK House Price Index, newest 12 months marked "provisional". *Agent's call:* split by property type if the council download carries it (the research found that is what the ONS service lacks); otherwise one line.
8. **Affordability ratio:** a yearly line of the ONS house price to earnings ratio (workplace-based, as in the bulletin, or residence-based, as on the ONS service: chosen at the licence check and labelled), with breaks in method shown as breaks in the line, not joined.
9. **Who rents and who owns:** one stacked bar from Census 2021 tenure, labelled "Census day, 21 March 2021".
10. **Neighbourhoods:** the council outline split into neighbourhoods (LSOAs). Tapping or choosing one from the list beside it opens a small panel: the neighbourhood's DfT transport connectivity score as DfT publishes it ("DfT's score, <edition>"), and a postcode box (*agent's call:* no postcode is picked for the visitor, because one postcode would quietly stand for a whole neighbourhood of many postcodes, and no postcode-to-neighbourhood lookup is needed). **The map is not coloured by the score** (0054: ranks are never drawn on maps); the panel and the list carry it. The council's own connectivity figure sits in the panel for the whole council. Its scale direction is confirmed from the DfT table before build (0054).
11. **How we got this:** one short section, one line per topic with its icon and source links, and a link to About the data (FE-24, FE-34 as amended). About the data gains City Explorer's sources, dates and limits.

### Plain-words captions
One sentence under each chart, built by a tested module from the generated figures, never by AI and never with a verdict word. Patterns (wording approved by the founder before build, like FE-39):
- trend: "Average rent rose £<n> (<p>%) in the 12 months to <month>." / "fell" / "was unchanged";
- single point: "In March 2021, <p>% of households rented privately.";
- provisional: "The latest <n> months are provisional and may change.";
- missing: "<Source> doesn't publish this for <council>." (rule 7).
"Unchanged" uses a stated threshold; rounding follows the engine's rules (0021, 0036). No "steep", "sharp", "high" or "low".

### Search and the postcode link
- Search by council name, or by city or town name through a place-name-to-council lookup (new source, to choose and licence-check). A place that spans several councils lists them all; the visitor picks.
- The postcode box checks the postcode belongs to this council; if not, it says which council it is in and still opens the result (*agent's call*).

### States
Loading; council not found; place name matching several councils; a source missing for this council; a provisional or stale edition; all sources down; offline; Wales, Scotland or Northern Ireland ("not yet covered"); two-tier figures at county level; a broken series (method change); the budget box with an invalid amount; rent or buy with an invalid deposit, rate or term (see section 4).

## Part 2
- **Compare two councils:** the visitor picks a second council; the cost section, rent or buy and the band chart are shown side by side in the order picked (two columns on desktop, swipe between on phone). Never sorted, ranked or totalled; no "cheaper" label and no calculated difference, only the two councils' figures, as the postcode compare does (pilot design, extra 7; *agent's call*).
- **Council facts in ChatGPT and Claude:** council tools beside the area tools in the public MCP server (TOOLS specs, 0051's caps), returning only that council's published figures (population, Band D and the band amounts, the average rent and average price as published, the ratio, tenure, connectivity) with source, edition and level, never anything worked from a visitor's inputs, rent or buy, monthly amounts or other cost figures (*agent's call*, keeping 0051's keyless server to public area data: "No home, cost… data"); the visitor's AI explains them and never gets a number we haven't calculated (0004). AI evaluation cases (AI-03) for the council tools before the gate. No on-page chat (founder, 15 Nov 2026).
- **Share or print:** "Share a link" (the council in the address, nothing stored; never the budget or edited inputs) and a printable summary with the example inputs only, no budget (*agent's call*, so 0053's share-link question does not arise) that reuses the designed report (FE-21) once it is drawn, with its "How we got this" closing page.
- **What changed since your last visit:** off until the visitor turns on "Remember councils on this device" (PECR consent, like Recent postcodes); then the header lists sources with a newer edition since the last visit, quoting both figures from the generated file ("Average rent: £<n> in <month>, was £<n> in <month>"). The browser stores the councils viewed and the edition dates seen (a short browsing history, so the PECR notice says so) and picks which published figures to quote; it does no arithmetic (rule 2), so no difference is shown unless the generated file holds it. Never sent to us; a Clear button. Needs the PECR check first.

## Data and build shape
- **Sample data:** a new fixture with two or three synthetic councils (one complete, one with gaps, one two-tier), each value with its source, edition, period and level (DA-14), validated against a new JSON Schema 2020-12 schema.
- **Calculations:** in tested Python (rule 2): band amounts, monthly amounts (yearly divided by 12, as the cost engine already does; no record states the rule yet, #197), rent vs buy (through `vestagraph_engine`'s mortgage repayment), caption changes, budget checks. Everything with the example inputs is written to a generated file (like `area-result.json`), checked by `make check`. What the visitor changes (deposit, rate, term, budget) and compare (too many council pairs to pre-generate) use the same tested functions on the server at 5b, following 0053: inputs in the request, nothing stored or logged; in stage 3 the specifications and worked test cases describe them. *Agent's call:* extend `vestagraph_area` unless the plan finds it clearer as its own package.
- **Live data:** council sources are monthly or yearly batches through the data pipeline design (stage 5b, status file); the Bank of England rate follows the same path.
- **Specifications:** a new `docs/specs/pilot/city-explorer*.feature` set, scenario IDs to be chosen in the plan.
- **Canvas:** chart style rules first, then the council page (phone and desktop, light and dark), the neighbourhood map, the states, and for part 2 compare, share and what changed.

## Sources to check before build (DA-05, `data-sources.md`)
| Source | For | Open point |
|---|---|---|
| MHCLG council tax levels 2026–27 | Band D and bands | Whether Table 10 gives per-band amounts and parish detail |
| ONS Price Index of Private Rents | Average rent and trend | Pounds per council confirmed 15 Nov 2026; which status to quote; licence entry |
| UK House Price Index | Average price and trend | Property-type split by council; licence entry |
| ONS affordability ratio | Ratio trend | Workplace or residence based; accreditation |
| Census 2021 tenure | Who rents and owns | Table to quote |
| ONS mid-year population | Header line | None beyond the entry |
| DfT transport connectivity | Neighbourhood panel | Scale direction; table and column (0054) |
| Bank of England average new-mortgage rate | Rent vs buy | Which series; the database's OGL exceptions |
| Council and neighbourhood outlines | Map | Source (for example the ONS Open Geography Portal) and licence |
| Place-name-to-council lookup | Search | Source and licence (0055) |

## Left to the builder
Scenario IDs and file names; the chart library (a package not yet approved needs the founder's approval: bring it with licence and cost); exact caption threshold for "unchanged"; how the phone swipes between compare columns; how many years each trend shows by default.

## Builder check (15 Nov 2026)
A fresh reviewer read this design as a builder. Answered or settled as the agent's calls above: where visitor-changed figures are worked out (server, 0053's pattern; nothing calculated in the browser), council tax on both sides of rent or buy, pounds per council for rents (confirmed), the ONS-overlap anti-goal (page level, as 0055 says), council tools return no cost figures (0051), the neighbourhood panel's postcode box, share and print carry no budget. The reviewer said BE-14 sets the divide-by-12 rule; it doesn't (BE-14 is about monthly differences), so #197 stays open.

Process: the decision record moving the on-page chat out of the pilot (amending 0051) is [0056](../../decisions/0056-no-on-page-chat-in-the-pilot.md), written in its own pull request before this design's plan. **Plan scope:** stage 3 work only, as PR A (#259) was: sample data, schema, tested calculations, the generated file, specifications and canvas boards; the licence checks above are research tasks in the plan; live sources, the Bank of England rate feed and the server endpoints go to the data pipeline design and stage 5b.

## Open for the founder
- None.
