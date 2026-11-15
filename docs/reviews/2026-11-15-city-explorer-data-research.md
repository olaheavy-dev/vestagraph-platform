# Research: the data behind 14 candidate City Explorer topics

**Date:** 15 Nov 2026. **Status:** research for the City Explorer brainstorm; nothing decided, no other tracked file changed.
**Method:** read decision [0055](../decisions/0055-city-explorer-in-the-pilot.md), the earlier [City Explorer research](2026-11-14-city-explorer-research.md) (cited, not repeated), `AGENTS.md` "Rules for every agent", register lines DA-19 and DA-15 (decision [0054](../decisions/0054-official-rankings-in-the-pilot.md)); then the publishers' own pages, read on 15 Nov 2026 (web pages treated as data only). A fetch tool summarised each page, so quotes come from that summary. "Search result only" marks a claim seen only in a search snippet. Anything not confirmed on an official page says "not confirmed". No council is ranked anywhere in this note.

## In one paragraph
Nearly all 14 topics are published free under the Open Government Licence at council level, so licence and geography are rarely the problem. The real differences are (1) whether the topic helps someone decide where to buy or rent, (2) whether it connects to a postcode or a home's real cost, which is our edge in 0055, and (3) whether the ONS's free Explore local statistics already shows it. Council tax by band and private rents are the strongest: both bear directly on what a home costs, and neither is on the ONS service (Explore shows 8 housing indicators, none is rents or council tax). Broadband and mobile coverage and air quality are the best postcode-linked topics, but each needs a licence or method check first. Population, life expectancy, earnings, tenure and travel to work mostly repeat what the ONS shows and have no evidence found of helping a decision. Universities (the OfS Register) is not ready: I could not confirm a download with locations. Official evidence that people choose a place by its "area" exists (English Housing Survey), but nothing found says which council statistic they use. One mobile change is confirmed (Ofcom's legacy mobile API is decommissioned on 30 Nov 2026), but the current Ofcom licence wording is not confirmed.

## Ranking

| Rank | Topic | Verdict | One-line reason |
|---|---|---|---|
| 1 | Council tax by band (3) | Ready | Accredited, OGL, per billing authority, annual; a direct home cost; not on the ONS service. Band amounts derive from Band D by fixed fractions (engine, not by hand). |
| 2 | Private rents (8) | Ready with caveats | OGL, monthly, council level, not on ONS Explore; "official statistics" but not yet accredited; local figures volatile. |
| 3 | Broadband and mobile coverage (10) | Ready with caveats | Postcode-level fixed data exists (our edge); licence wording on the 2026 page not confirmed; predictions, not measurements. |
| 4 | UK House Price Index (4) | Ready | Accredited, OGL, monthly, council level with history; ONS Explore shows only "Average house price", so trend and sales add something. |
| 5 | Housing affordability ratio (2) | Ready with caveats | OGL, annual, already planned (DA-16); also on ONS Explore; workplace-based median ratio, no household income or deposit. |
| 6 | Air quality (13) | Ready with caveats | Modelled 1 km background maps fit a postcode, OGL; modelled not measured, LAQM-only guidance; not on ONS Explore as a pollutant figure. |
| 7 | New homes planned and housing supply (12) | Ready with caveats (supply and delivery); not ready (local plans) | Net additions and Housing Delivery Test are accredited or official, OGL, by council; planning.data.gov.uk local plans are incomplete. |
| 8 | DfT transport connectivity (6) | Ready with caveats | Already in 0054; LSOA and council scores; single provisional first edition. |
| 9 | Tenure, owners and renters (9) | Ready with caveats | Census 2021, OGL, council and small areas; one 2021 point in time; no decision evidence found. |
| 10 | Travel to work (14) | Ready with caveats | Census 2021, OGL; collected during the pandemic and uses the 2001 specification. |
| 11 | Life expectancy (7) | Ready with caveats | Accredited, OGL, council level; already on ONS Explore; no evidence it helps a home choice. |
| 12 | Population estimates (5) | Ready | Accredited, OGL, 318 councils; already on ONS Explore; little decision value alone. |
| 13 | Earnings, ASHE (11) | Ready with caveats | Accredited, OGL; 1% sample and "unreliable" cells suppressed; ONS Explore shows a pay measure already. |
| 14 | Universities, OfS Register (1) | Not ready | OGL confirmed, but no confirmed council or location field; register content and cadence unclear. |

## Topic sections

### 1. Universities and higher education providers (OfS Register)
- **Source:** Office for Students, [The OfS Register](https://www.officeforstudents.org.uk/for-providers/regulatory-resources/the-ofs-register/) and [Guide to the OfS Register](https://www.officeforstudents.org.uk/for-providers/registering-with-the-ofs/guide-to-the-ofs-register/).
- **Licence:** OGL stated on the [copyright page](https://www.officeforstudents.org.uk/copyright/): "All content owned by the OfS is available for re-use under the terms of the OGL". The register page footer says "All rights reserved". Which governs the register is not confirmed.
- **Geography:** Provider records, not places. The guide lists status, trading names, fee limit, TEF rating, degree-awarding powers and conditions; it does not mention address or location (not confirmed whether they exist). Fits neither City Explorer nor the postcode result as published.
- **Freshness:** The guide says 425 registered providers and was published 3 Feb 2022; update frequency not stated; a spreadsheet download was seen only in a search result about the guide; the register page itself offers none (not confirmed). Time series: not stated.
- **Reliability:** Regulatory status, not a measure of quality. Includes deregistered providers.
- **Already free elsewhere:** The OfS publishes it; ONS Explore shows no higher education indicator (closest is Level 3 qualifications), per the [indicator list](https://www.ons.gov.uk/explore-local-statistics/indicators).
- **Evidence it helps a buyer or renter:** None found.
- **Open questions:** Does a current register download include campus addresses? A "university in this council" fact would need a campus location source, which is a different dataset (not assessed).

### 2. Housing affordability ratio (ONS)
- **Source:** ONS, [Housing affordability in England and Wales: 2025](https://www.ons.gov.uk/peoplepopulationandcommunity/housing/bulletins/housingaffordabilityinenglandandwales/2025).
- **Licence:** OGL: "available under the Open Government Licence v3.0".
- **Geography:** 318 local authorities, former authorities and combined authorities, plus constituencies and MSOAs. Council level: fits City Explorer. The postcode area result could use MSOA prices (earlier research, section 3; DA-16 shows council level).
- **Freshness:** Released 26 Mar 2026, next March 2027; a correction on 13 May 2026 changed London from 10.5 to 10.6; annual time series, with caveats below.
- **Reliability:** Median price divided by median workplace-based full-time earnings, from a 1% ASHE sample; prices not mix-adjusted; excludes household income, deposits, equity and upfront costs; comparability over time limited (COVID-19, 2021 coding change, 2023 and 2024 method changes); accreditation status not stated on the page.
- **Already free elsewhere:** Yes: ONS Explore has "Housing affordability ratio (residence-based)" ([indicators](https://www.ons.gov.uk/explore-local-statistics/indicators)). The earlier research confirmed the bulletin and DA-16 plans it.
- **Evidence it helps a decision:** None found for the ratio itself. It is a standard measure, but I found no study of buyers using it.
- **Open questions:** Workplace-based (bulletin) versus residence-based (Explore): which is shown, and labelled how? Accreditation status.

### 3. Council tax by band
- **Source:** MHCLG, [Council Tax levels set by local authorities in England 2026 to 2027](https://www.gov.uk/government/statistics/council-tax-levels-set-by-local-authorities-in-england-2026-to-2027) and its [technical notes](https://www.gov.uk/government/statistics/council-tax-levels-set-by-local-authorities-in-england-2026-to-2027/council-tax-levels-set-by-local-authorities-in-england-2026-to-2027-technical-notes).
- **Licence:** OGL: "available under the Open Government Licence v3.0".
- **Geography:** Billing authority (council) in England; Table 10 is titled "Local Authority Level Data" (contents not confirmed). The technical notes say bands are fixed fractions of Band D (6/9 for A to 18/9 for H), so band amounts can be derived by the cost engine (rule 2). Fits both: the council page and the postcode result, where the home's band gives a real cost.
- **Freshness:** Published 25 Mar 2026 for 2026 to 2027; annual, with earlier years published as time series (earlier years not checked). Parish and town precepts are averaged across the whole billing area, so the figure may differ from a specific parish. Revisions to Medway and North Kesteven mean earlier years are not directly comparable.
- **Reliability:** Labelled "Accredited official statistics". Band D figure is for a two-adult dwelling before discounts, exemptions or benefits.
- **Already free elsewhere:** Not on ONS Explore (checked its health, education, crime and five other topic lists). Councils publish their own bands.
- **Evidence it helps a decision:** None found as a study. It is a cost every buyer or renter-in-charge pays; a regulatory rule, not a survey.
- **Open questions:** Does Table 10 give parish-level amounts? Which council the home's parish falls in (a postcode problem, not a council one).

### 4. UK House Price Index
- **Source:** HM Land Registry with ONS, [UK House Price Index: reports](https://www.gov.uk/government/collections/uk-house-price-index-reports); [downloads](https://www.gov.uk/government/statistical-data-sets/uk-house-price-index-data-downloads-april-2026); [Land Registry tool](https://landregistry.data.gov.uk/app/ukhpi/browse).
- **Licence:** OGL: "All content is available under the Open Government Licence v3.0".
- **Geography:** More than 441 areas in the UK including English councils (search result only for the count); Isles of Scilly excluded. Council level: fits City Explorer.
- **Freshness:** August 2026 data published 21 Oct 2026; September 2026 due 18 Nov 2026. Monthly; the app says back to 1995 (earlier research).
- **Reliability:** Accredited official statistics. Newest 12 months are provisional; new-build estimates uncertain; revisions may be larger than historic.
- **Already free elsewhere:** Partly: ONS Explore shows "Average house price" only, not trend, property type or sales.
- **Evidence it helps a decision:** None found.
- **Open questions:** Sales-volume field and the UK HPI's DA-05 entry in `docs/references/data-sources.md` (earlier research said not yet assessed).

### 5. Population estimates
- **Source:** ONS, [Population estimates for England and Wales: mid-2025](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/populationestimatesforenglandandwales/mid2025).
- **Licence:** OGL: "available under the Open Government Licence v3.0".
- **Geography:** 318 local authorities. City Explorer only.
- **Freshness:** Released 29 Jul 2026; next release not announced; annual series (confirmed in the earlier research).
- **Reliability:** Accredited; uncertainty larger for small areas; Isles of Scilly can be outlying; revised later.
- **Already free elsewhere:** Yes: ONS Explore shows total population, density, five-year change, median age and three age bands.
- **Evidence it helps a decision:** None found.
- **Open questions:** None beyond the earlier research.

### 6. DfT transport connectivity metric
- **Source:** Department for Transport, [Transport connectivity metric](https://www.gov.uk/government/publications/transport-connectivity-metric/transport-connectivity-metric).
- **Licence:** OGL v3.0, Crown copyright 2025.
- **Geography:** Output areas, LSOAs, local authority districts, regions (England and Wales); the 100 m grid is limited to the Connectivity Tool. Fits City Explorer (council) and the postcode result (LSOA).
- **Freshness:** First edition, published 29 Sep 2025, provisional; destination data mostly Q4 2024 or Q1 2025. DfT plans annual updates; no time series yet. A search result says the tool was opened to everyone online in December 2025 (search result only).
- **Reliability:** "First estimates"; assumes no delays or cancellations; no route quality, safety or cost; not adjusted for post-COVID travel; 60-minute limit; the default score excludes driving (search result only).
- **Already free elsewhere:** ONS Explore has travel time to employment centre by car, bicycle and public transport, a different measure.
- **Evidence it helps a decision:** None found.
- **Open questions:** Is a 0 to 100 score a "score" under 0055's "no arbitrary scores"? It is DfT's own, but the brainstorm should decide.

### 7. Life expectancy
- **Source:** ONS, [Life expectancy for local areas of the UK](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/bulletins/lifeexpectancyforlocalareasoftheuk/latest).
- **Licence:** OGL v3.0.
- **Geography:** Lower-tier local authorities in England; City of London and Isles of Scilly excluded. City Explorer only.
- **Freshness:** 2022 to 2024, released 10 Dec 2025; next release "to be announced" (the earlier research recorded Dec 2026 to Jan 2027 as provisional; not confirmed today). Time series from 2001 to 2003.
- **Reliability:** Accredited. Period estimates, not what a baby born there will live; COVID-19 still affects figures; differences not tested for significance.
- **Already free elsewhere:** Yes: ONS Explore shows female and male life expectancy and healthy life expectancy.
- **Evidence it helps a decision:** None found.
- **Open questions:** A figure like this could read as a verdict on an area (rule 4); wording needs care.

### 8. Private rents
- **Source:** ONS, [Private rent and house prices, UK](https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/privaterentandhousepricesuk/latest), which carries the Price Index of Private Rents (PIPR). The older [Private rental market summary statistics](https://www.ons.gov.uk/peoplepopulationandcommunity/housing/bulletins/privaterentalmarketsummarystatisticsinengland/latest) was discontinued, last release 20 Dec 2023, replaced by PIPR.
- **Licence:** OGL v3.0 ("All content is available under the Open Government Licence v3.0").
- **Geography:** Local authorities in England and Wales; City of London and Isles of Scilly not published. City Explorer only.
- **Freshness:** Released 21 Oct 2026, next 18 Nov 2026; monthly. Latest two months provisional.
- **Reliability:** PIPR became official statistics on 20 May 2026 and is "not yet accredited". Local figures can be volatile; ONS recommends longer-term trends. The bulletin (21 Oct 2026) gives average monthly rents in pounds for each local authority in England and Wales, in an interactive chart (Figure 7; checked again by the reviewer and the controller on 15 Nov 2026). Whether the downloadable dataset gives pounds per council is not confirmed (the dataset page mentions "price levels" only).
- **Already free elsewhere:** Not on ONS Explore (no private rent indicator in the housing list).
- **Evidence it helps a decision:** English Housing Survey 2023 to 24: private renters most often moved for a better area (14%), larger home (12%) or work (12%), per a [search result only](https://www.gov.uk/government/statistics/english-housing-survey-2023-to-2024-rented-sectors/english-housing-survey-2023-24-rented-sectors). That is about moving, not about rent levels.
- **Open questions:** Confirm the downloadable dataset carries pounds per council before promising a "typical rent" fact.

### 9. Tenure, who rents and who owns
- **Source:** ONS, [Housing, England and Wales: Census 2021](https://www.ons.gov.uk/peoplepopulationandcommunity/housing/bulletins/housingenglandandwales/census2021).
- **Licence:** OGL v3.0.
- **Geography:** Local authorities and, through Census maps, neighbourhoods. Fits both City Explorer and (with small-area tables, not checked) the postcode area result.
- **Freshness:** Census Day 21 Mar 2021, released 5 Jan 2023; next release not announced; one point in time (decennial). Comparison with 2011 geographies changed (earlier research).
- **Reliability:** 97% person response overall, over 88% in every local authority; no tenure data for household spaces with no usual residents.
- **Already free elsewhere:** ONS publishes it with a tenure-by-council chart (Figure 3). ONS Explore shows no tenure indicator.
- **Evidence it helps a decision:** None found.
- **Open questions:** Five-year-old data on a market that changed (private rented share, Renters' Rights Act); would the page be stale on launch?

### 10. Broadband and mobile coverage
- **Source:** Ofcom, [Connected Nations update: Spring 2026](https://www.ofcom.org.uk/phones-and-broadband/coverage-and-speeds/connected-nations-update-spring-2026); [data downloads](https://www.ofcom.org.uk/phones-and-broadband/coverage-and-speeds/data-downloads3).
- **Licence:** Not confirmed for 2026. The Spring 2026 page says "Please see our terms of use for our licence conditions". Search results say the 2023 and 2024 files are under the OGL (search result only). The brainstorm needs the terms-of-use text before relying on it.
- **Geography:** Fixed broadband: local and unitary authority in the Spring 2026 download. The data-downloads page (Connected Nations 2020 era) also lists postcode unit and output area for fixed coverage; mobile at constituency and council only. Postcode-level availability for 2026 is not confirmed. Fits both.
- **Freshness:** Spring update published 13 May 2026, data to January 2026; main report due late in the year (the 2025 one was 19 Nov 2025; the 2026 one not seen). Twice a year.
- **Reliability:** Operator-predicted coverage, not measured; Vodafone and Three reported separately; "good" 4G coverage is a share of landmass. Ofcom proposed in 2023 to stop its home broadband performance reports (search result only).
- **Mobile change on 30 Nov 2026: confirmed.** Ofcom's developer portal says support for existing subscriptions ends on 30 November 2026, when "the legacy API will be decommissioned" ([api.ofcom.org.uk](https://api.ofcom.org.uk)). That is the legacy mobile API (a developer service), so it affects anyone using it, not coverage figures. Ofcom's switch-off page (updated 4 Nov 2026) says 3G is already off and 2G ends from May 2029 for EE.
- **Already free elsewhere:** Partly: ONS Explore shows 4G, 5G, gigabit, superfast, ultrafast, full fibre and below-30 Mbps premises by council. Ofcom's own checker is by address (not checked).
- **Evidence it helps a decision:** None found for house buyers; Ofcom consumer research ranks speed and reliability high but cost first (search result only, mostly 2016 to 2023).
- **Open questions:** Licence wording; whether 2026 postcode-level files exist; relation to 0029 adapters.

### 11. Earnings (ASHE)
- **Source:** ONS, [Annual Survey of Hours and Earnings](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/latest).
- **Licence:** OGL v3.0.
- **Geography:** Local authority (Great Britain, by place of work in the bulletin; earlier research: Table 8 residence, Table 7 workplace).
- **Freshness:** 2026 provisional released 22 Oct 2026; final Oct 2027; annual.
- **Reliability:** Accredited; a 1% PAYE sample (197,000 in 2026); some cells are "unreliable because of their small sample size" and not given.
- **Already free elsewhere:** Partly: ONS Explore shows "Gross median weekly pay".
- **Evidence it helps a decision:** None found. It already feeds the affordability ratio.
- **Open questions:** Residence or workplace basis; whether to show both.

### 12. New homes planned and housing supply
- **Source:** MHCLG, [Housing supply: net additional dwellings, England 2024 to 2025](https://www.gov.uk/government/statistics/housing-supply-net-additional-dwellings-england-2024-to-2025) and its [collection](https://www.gov.uk/government/collections/net-supply-of-housing); [Housing Delivery Test](https://www.gov.uk/government/collections/housing-delivery-test); [planning.data.gov.uk local plans](https://www.planning.data.gov.uk/dataset/local-plan).
- **Licence:** OGL v3.0 on the net additional dwellings, the Housing Delivery Test and (search result only) the planning data pages.
- **Geography:** Net additions: the page says "Applies to England"; the collection says the live tables give "all of the available detail, geographic disaggregations", but whether a council table exists is not confirmed on the page (ONS Explore has an England net-additions indicator by area). Housing Delivery Test: local planning authority (not confirmed on the page). Local plans: authority, 337 planning authorities listed.
- **Freshness:** Net additions 2024 to 25 published 20 Nov 2025; 2025 to 26 due November 2026 (provisional, date not confirmed). Housing Delivery Test: 2024 and 2025 measurements both published 17 Aug 2026 (the 2023 one on 12 Dec 2024), so publication is late and irregular (search result only for the lateness). Local plans: 990 plans from 84 providers and a warning that it may not cover England (search result only; the page returned a server error when I fetched it).
- **Reliability:** Net additions "Accredited official statistics". A Housing Delivery Test result compares homes delivered with a requirement; it is not a plan of homes to come. Council local plans: incomplete; "homes planned" has no confirmed national field.
- **Already free elsewhere:** Net additions yes (ONS Explore). Housing Delivery Test and local plans: not found.
- **Evidence it helps a decision:** None found.
- **Open questions:** What "new homes planned" would mean without a national dataset; whether Housing Delivery Test results can be shown without reading as a verdict on a council (rule 4, 0054).

### 13. Air quality
- **Source:** Defra, [UK-AIR modelled background maps (PCM)](https://uk-air.defra.gov.uk/data/pcm-data), [LAQM background maps](https://uk-air.defra.gov.uk/data/laqm-background-maps) and [AQMAs](https://uk-air.defra.gov.uk/aqma/).
- **Licence:** OGL v3.0 on all three pages; the PCM page asks users to acknowledge Defra.
- **Geography:** PCM: 1 x 1 km grid cells (fits the postcode result), plus population-weighted PM2.5 by local authority from 2010 (fits City Explorer). AQMAs: a list by local authority and a map; a download is not mentioned.
- **Freshness:** PCM up to 2024 for most pollutants, modelled 2025 data on GOV.UK (not opened); annual time series from 2001 but "the methodology changes most years". LAQM maps carry 2021 base with projections to 2040; release date not stated.
- **Reliability:** Modelled background levels, not what is at a street or a road; "specifically for LAQM purposes only", use alongside the user guide; some files republished to fix errors.
- **Already free elsewhere:** ONS Explore has no pollutant figure (only "Air pollution regulating", an ecosystem measure). Defra's own map and a postcode look-up exist (not checked).
- **Evidence it helps a decision:** None found. Health risk from pollution is not evidence of what buyers use.
- **Open questions:** Whether a 1 km background figure may be quoted for a postcode without implying a street is "clean" (rules 4 and 7).

### 14. Travel to work
- **Source:** ONS, [Travel to work, England and Wales: Census 2021](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/traveltoworkenglandandwales/census2021); datasets TS061, RM077 (search result only).
- **Licence:** OGL v3.0.
- **Geography:** Lower-tier local authorities, regions, country; small areas via Census maps.
- **Freshness:** Census Day 21 Mar 2021, released 8 Dec 2022; one point in time.
- **Reliability:** Pandemic: "Census 2021 took place during the coronavirus (COVID-19) pandemic"; lockdown and furlough likely affected travel; 2001 specification excludes people who work from home but use other transport.
- **Already free elsewhere:** Published by the ONS with local authority data; ONS Explore shows no commute indicator (it has travel time to employment centre).
- **Evidence it helps a decision:** None found.
- **Open questions:** Stale and odd for a commute question in 2026; DfT's connectivity metric (topic 6) is the nearer alternative.

## Already free elsewhere: summary
The ONS Explore local statistics indicator list shows population, average house price, affordability ratio, net additions, life expectancy, gross median weekly pay and the broadband and mobile measures by council ([indicators](https://www.ons.gov.uk/explore-local-statistics/indicators)). It does not show rents, council tax, tenure, higher education, a commute mode or a pollutant figure. This confirms the earlier research's point that comparison by council is already free.

## What this means for the brainstorm
- **Lead with what a home costs.** Council tax by band and private rents are the two topics that change what someone pays, and neither is on ONS Explore. Council tax also meets 0055's postcode edge, because the band belongs to the home.
- **Use the postcode edge for broadband and air quality, after checks.** They are the topics with postcode-scale data, but broadband needs the Ofcom licence wording and air quality needs a rule for wording a modelled background figure.
- **Skip or defer topics ONS already shows.** Population, life expectancy, earnings and the affordability ratio repeat ONS Explore; keep the affordability ratio only because DA-16 plans it for the postcode.
- **Evidence of need is thin.** The only official evidence found is the English Housing Survey on moving "to a better area" (search result only); nothing found says which council statistic a buyer or renter uses. The brainstorm should treat usefulness as a hypothesis to test with the pilot.
- **Mind the rules.** Everything shown must be a published figure or an engine output (rule 2), with no council ranking (0054, DA-15) and no employment rates (DA-19). Housing Delivery Test results and life expectancy are the likeliest to read as a verdict on a council.
- **Not ready:** universities (no confirmed location data) and "homes planned" from local plans (incomplete national data).

## Not confirmed
- The Ofcom 2026 licence wording; postcode-level 2026 Ofcom files.
- Whether the downloadable PIPR dataset gives pounds per council; whether the council tax Table 10 has parish detail; whether a council-level net additions table exists on the page.
- OfS Register current download and location fields; the planning.data.gov.uk local plan counts (page unavailable when fetched).
- Pages that returned errors on fetch: the Housing Delivery Test 2025 measurement page, the ONS Explore visualisation page.

## Checked
Publisher pages read on 15 Nov 2026: officeforstudents.org.uk, ons.gov.uk, gov.uk (MHCLG, Land Registry, DfT, Housing Delivery Test collection), ofcom.org.uk, uk-air.defra.gov.uk, planning.data.gov.uk (search result only). Earlier research: [2026-11-14-city-explorer-research.md](2026-11-14-city-explorer-research.md).
