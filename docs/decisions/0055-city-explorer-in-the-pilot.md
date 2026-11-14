# 0055: City Explorer in the pilot

**ID:** PD-17  
**Status:** Accepted (founder, 14 Nov 2026, in prompt windows)  
**Date:** 2026-11-14  
**Stage:** 3 (for the pilot, stage 5b)  
**Research:** [City Explorer research](../reviews/2026-11-14-city-explorer-research.md)  
**Applies (no older text is rewritten):** decision [0052](0052-pilot-only-gate.md) (the pilot-only gate now also covers City Explorer's specifications), register line PD-16 (one pilot phase); [0054](0054-official-rankings-in-the-pilot.md) and DA-14 are unchanged

## Context
On 14 Nov 2026 the founder shared a written proposal for a "City Explorer": pages about a place, built from official statistics and linked to the postcode area check, for people who don't yet have a postcode ("help users move from understanding a city to understanding the specific areas where they might live"). It proposed population and demographics, house prices and affordability, employment and earnings, transport connectivity, historical trends and city comparison in the pilot, with education, deprivation and health later; "derived statistical rankings" of comparable local authorities; free during the pilot; and no arbitrary scores, subjective recommendations or unnecessary AI.

The founder asked for research before deciding ("can you spin up a reasearch on the side on this, we can discuss this first" [sic]). The agent's research (14 Nov 2026; official pages checked that day) found:
- **"City" is not one official unit in England.** Nearly every dataset publishes by council (local authority district or unitary authority). A city can span several councils, a council can include countryside, two-tier areas publish some figures only at county level, London has 33 authorities, and council mergers between 2019 and 2023 break some trends. Calling council figures "city" figures would break DA-14.
- **Derived rankings conflict with recorded decisions.** Ranking councils ourselves by a published figure is a ranking we make; 0054 allows only government-published ranks, and FE-22, AI-10 ("listed, never ranked") and doc 05 point 5 rule out our own rankings.
- **Council employment rates are unreliable.** The ONS has withdrawn accredited status for the Annual Population Survey's local outputs and warns against reading small differences between places.
- **The comparison itself already exists, free.** The ONS's Explore local statistics service searches by postcode or council, shows 116 indicators and compares councils, including with statistically similar ones. Vestagraph's gap is linking council facts to the postcode being checked, and later to the home and its real cost.
- **Data:** the population estimates, UK House Price Index, affordability ratio, DfT transport connectivity metric and life expectancy figures checked are free under the Open Government Licence where confirmed. Some have no time series: the connectivity metric is a single 2025 edition and the Indices of Deprivation are not a time series. Each new source still needs its licence check (DA-05) and a `docs/references/data-sources.md` entry.
- **Cost:** new screens add specifications, canvas boards, scenarios and AI evaluation cases before the pilot gate (0052), so the gate comes later.

## Options
### Option A: "About this council area" on the postcode result
A section on the postcode result using council-level facts already planned (council tax by band, the affordability ratio, the DfT metric), labelled with the council's name, with a link to the ONS for comparisons. Small, fits every decision, no gate delay. The agent's recommendation.

### Option B: Full City Explorer in the pilot
Its own pages with trends and comparisons. Large: new screens, specifications, boards and AI tests before the gate; the "city" unit and ranking questions need deciding.

### Option C: After the pilot
Nothing now; an ideas entry in doc 05.

### Option D: Not at all
A link to the ONS service only.

## Recommendation
Option A, with the idea logged in doc 05 for after the pilot: it fills the real gap (council facts beside the postcode being checked) without copying the ONS or delaying the gate.

## Decision
The founder chose **Option B, the full City Explorer in the pilot**, over the agent's recommendation, for this reason (prompt window, the founder's chosen answer): **"Reach people earlier"**: people researching a move before they have a postcode should find Vestagraph; the postcode check alone misses them.

In the same prompt windows the founder decided:
1. **Rankings:** "No, official only (Recommended)": 0054 stands. City Explorer quotes only government-published ranks, never our own ranking or a sortable "1st of N".
2. **Employment and unemployment rates:** "Not in the pilot (Recommended)", because of the ONS's warning on local figures (register DA-19).
3. **Page unit:** "The council (Recommended)": one page per council, titled with the council's name (for example "Leeds City Council area") and searchable by a city or town name, so every figure is true for the area shown (DA-14).
4. **Order:** "After area boards (Recommended)": the postcode area result's PR A and canvas boards come first; City Explorer is then brainstormed, designed and planned, reusing that layout and the data pipeline. The pilot gate (0052) waits for both.
5. **Ideas list:** "Yes, log it (Recommended)": doc 05 records "Choosing where to look" with this record, so it is not researched twice.

## Consequences
- City Explorer gets its own brainstorm, design brief, design review, plan and canvas boards after the area-result boards. The topic list, the comparison view, which trends to show and how a council page links to the postcode check are decided there, each fact at its official level (DA-14), with source, edition and period.
- No ranking of our own anywhere on City Explorer (0054, FE-22, rule 4); no council employment or unemployment rates in the pilot (DA-19); no verdict words ("best", "better area").
- Each new source (for example population estimates, the UK House Price Index, life expectancy) needs its licence check (DA-05) and a `data-sources.md` entry before build. The data pipeline design (status file, stage 5b) covers council-level batch sources.
- Free during the pilot, like the postcode check (no account, decision 0051's caps apply to any AI on it).
- The pilot gate (0052) now also checks City Explorer's specifications, so it passes later than planned.
- Reversible: a later decision can narrow City Explorer to Option A if the design shows the pages repeat the ONS service without the postcode link.
