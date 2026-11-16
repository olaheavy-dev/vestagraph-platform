# Data gaps research: ten topics the competitor shows

Research note, 16 November 2026. The founder chose "Research the data gaps" after the competitor benchmark found ten topics Vestagraph lacks. Every fact below comes from a publisher page read on 16 Nov 2026 unless marked otherwise. "Not confirmed" means the page could not be loaded or did not say; nothing has been guessed. Search-engine summaries are marked "(search result only)" and need a direct read before build.

The recommendation words mean:
- **ADD (with conditions):** ingest the data and show it as a sourced fact, once it passes the licence register (DA-05) and the conditions listed.
- **CHECK ROW:** show a "check this" row that links to the official service, with no data of our own.
- **NOT NOW:** leave it out for the pilot; the reason is given.

## Summary

| # | Topic | Recommendation | Licence | Resolution | Repository today |
|---|---|---|---|---|---|
| 1 | Surface water flood risk | CHECK ROW now (link to "Check your long term flood risk"); the outline joins topic 3's map | OGL (data.gov.uk) | Modelled on 2 m cells, rainfall on a 1 km grid; area only, "not enough information to determine flood risk to individual properties"; no postcode summary file | Only a link-out row ("EA long-term flood risk", data licence unverified) |
| 2 | Future flood risk (climate change) | CHECK ROW (the official checker already shows it); NOT NOW for our own data | OGL (data.gov.uk); one CKAN record says "No Licence Provided" | Same as the present-day layers; one scenario (2050s, Central allowance) | Not planned anywhere |
| 3 | Flood outlines on a map | ADD (with conditions): Flood Zones 2 and 3 through the official OGC API Features or WMS, plus the surface water WMS | OGL (data.gov.uk); CKAN shows "No Licence Provided"; attribution "© Environment Agency copyright and/or database right 2025. All rights reserved." | Area of land; "not suitable for showing whether an individual property is at risk" | FE-25 wants outlines once a dataset passes DA-05 |
| 4 | Radon | ADD (with conditions): BGS/UKHSA Indicative Atlas, 1 km square, plus a link to the £3.90 address report | OGL ("Free for commercial, research and public use") | 1 km grid; each square takes the highest potential in it; "indicative rather than definitive" | Deferred: "terms unverified; address report paid" (the open BGS atlas was not found then) |
| 5 | Coal mining | CHECK ROW (free postcode search); a coalfield map layer later | OGL, with "re-use is not permitted for any activity that is part of the Coal Authority's public task responsibilities" | Area polygons, shown through WMS or WMTS; no vector download confirmed | Route-only link already recorded |
| 6 | Road and rail noise | ADD (with conditions) as a map layer only, no per-home number; else CHECK ROW to the publication | OGL for the octave-band dataset; "No Licence Provided" on the All Metrics CKAN record | 10 m grid, 4 m above ground, modelled for 2021, "no actual noise measurements were taken" | Route-only link already recorded |
| 7 | Broadband and mobile | ADD (with conditions) fixed broadband by postcode from the Connected Nations file; CHECK ROW for mobile until the API terms are read | OGL for Connected Nations files (Ofcom's data note); API terms not confirmed | Postcode (fixed, Jan 2026 snapshot; gigabit-capable but not full fibre at postcode); mobile granularity not confirmed | Ofcom API row, terms unread; mobile v1 API ends 30 Nov 2026 |
| 8 | Rents | ADD (with conditions) at council level only (DA-10); no official postcode or small-area rent exists | OGL v3.0 | Local authority (England and Wales); by bedrooms at local level not confirmed in the file | PIPR researched (City Explorer), status wording now stale |
| 9 | Planning constraints | ADD (with conditions) listed buildings and conservation areas; CHECK ROW for Article 4 and tree preservation | OGL v3.0 on every dataset | Points (listed buildings) and polygons; coverage incomplete ("an absence of results does not mean no constraints exist") | DA-11: add if Planning Data passes DA-05; platform pages were down on 11 Nov |
| 10 | Free basemap | ADD (with conditions): self-hosted OS Open Zoomstack as an option for FE-03, next to self-hosted OpenStreetMap; never OSM public tiles | OS OpenData under OGL; Zoomstack's own pages say "Free to use for everyone" without naming the licence | Great Britain, national to street scale (1:5,000,000 to 1:10,000) | FE-03: own OSM tiles, "price it first"; OSM public tiles marked "not suitable for production" |

## What the repository already plans

Searched `docs/references/data-sources.md`, the DA- lines (and related FE- lines) in `docs/decisions/README.md`, and `docs/reviews/`:

- **Flood:** `data-sources.md` line 16 has "EA long-term flood risk" as link-out only ("data licence unverified"); line 17 and DA-16 add the Environment Agency's "Postcodes in Areas at Risk" file for rivers and the sea. FE-25 asks for the postcode band and "official outlines on the flood topic's own flat map" once a dataset passes DA-05. Nothing mentions surface water data, climate change projections or NaFRA2.
- **Radon:** `data-sources.md` lines 36 and 145 ("Defer"; "link out; do not ingest"; "No API or reuse terms were seen (unverified)"); priority row 20 deferred; the unverified list at line 215.
- **Coal mining and noise:** `data-sources.md` lines 159 to 161, "route-only topics" with link labels.
- **Broadband and mobile:** `data-sources.md` lines 32, 128 to 129 and row 11 (terms unread). `docs/reviews/2026-11-15-city-explorer-data-research.md` lines 122 to 129 and 184 (Ofcom licence wording and postcode files still to check).
- **Rents:** DA-10 (council area and bedrooms, if licensed); `data-sources.md` line 166; `docs/reviews/2026-11-16-city-explorer-sources.md` section 2 (Table 1, 294 English councils for Sept 2026).
- **Planning constraints:** DA-11 (conservation areas, listed buildings, Article 4, Green Belt if they pass DA-05); `data-sources.md` lines 31 and 123 to 124 (pages returned 503 on 11 Nov 2026).
- **Basemap:** FE-03 ("OpenStreetMap tiles we store and serve from our own domain", "price it first"); `data-sources.md` lines 27 and 90 to 97 (OSM public tiles "Not suitable for production"); DA-06 and DA-08 for geocoding and routing.
- **Design review:** `docs/reviews/2026-11-14-pilot-design-review.md` line 70 (B30) already asks that each topic the competitor shows is "either covered or explicitly routed".

Two repository statements are now stale (fixed in the same pull request as this note):
1. `data-sources.md` line 166 calls PIPR "official statistics in development". ONS's bulletin says "On 20 May 2026, PIPR data became "official statistics" and are no longer considered to be "in development"". The 21 Oct 2026 workbook cover, as read in `2026-11-16-city-explorer-sources.md`, still says "in development", so the two ONS sources disagree; quote the bulletin and note the workbook wording.
2. `data-sources.md` line 145 says radon has no reuse terms. BGS publishes the radon Indicative Atlas under OGL (topic 4).

## 1. Surface water flood risk

- **Publisher:** Environment Agency.
- **Dataset:** Risk of Flooding from Surface Water (RoFSW, NaFRA2, published 28 Jan 2025) ([data.gov.uk](https://www.data.gov.uk/dataset/risk-of-flooding-from-surface-water3)); [how to use the map](https://www.gov.uk/government/publications/flood-risk-maps-for-surface-water-how-to-use-the-map/risk-of-flooding-from-surface-water-understanding-and-using-the-map); [update timeline](https://www.gov.uk/guidance/updates-to-national-flood-and-coastal-erosion-risk-information).
- **Licence:** "Open Government Licence" (data.gov.uk). The long-term flood risk service's [risk data page](https://check-long-term-flood-risk.service.gov.uk/risk-data) adds that address and mapping data in the service is under Ordnance Survey terms.
- **Resolution:** "a ground level to every 2m x 2m model cell"; "Rainfall data is then mapped onto a 1km grid". The WMS is "set to 1:50 000". Layers for extent and depths of 0.2, 0.3, 0.6, 0.9 and 1.2 m. It is a probabilistic product showing "overall risk".
- **Property-level warnings:** "The map does not contain enough information to determine flood risk to individual properties"; "cannot specify whether individual buildings are themselves at risk"; "We do not currently provide warnings for flooding from surface water." The risk data page: "The datasets are not suitable for identifying if an individual property will flood."
- **Access:** WMS, download by area of interest, product description PDF, layer file. No WFS or API listed. No surface-water version of the postcode summary exists: the only postcode file covers rivers and the sea ([data.gov.uk](https://www.data.gov.uk/dataset/5a98b0a1-2741-4b2f-a51b-5b42f13219f2/risk-of-flooding-from-rivers-and-sea-postcodes-in-areas-at-risk2), last updated 4 Nov 2026). The [key summary file](https://www.data.gov.uk/dataset/risk-of-flooding-from-surface-water-key-summary-information) gives counts by council, constituency and similar areas, not postcode.
- **Postcode lookup:** The official [Check your long term flood risk](https://www.gov.uk/check-long-term-flood-risk) service takes a postcode and covers rivers and the sea, surface water, reservoirs and groundwater "where data is available"; it tells "the flood risk of an area, not a specific property" ([service](https://check-long-term-flood-risk.service.gov.uk/postcode)). No API for that service was found.
- **Update:** "asNeeded"; last updated 13 Nov 2026. **Cost:** free. **Key or rate limit:** none stated.
- **Recommendation: CHECK ROW.** There is no official postcode figure, and sampling the map at a postcode centre would make our own per-location verdict that the Environment Agency says the map cannot support. Link to "Check your long term flood risk". Draw the extent as an outline on the flood map under topic 3.

## 2. Future flood risk (climate change)

- **Publisher:** Environment Agency (NaFRA2, which "includes the potential impact of climate change on flood risk, based on UK Climate Projections (UKCP18)" ([update timeline](https://www.gov.uk/guidance/updates-to-national-flood-and-coastal-erosion-risk-information))).
- **Datasets:** "Risk of Flooding from Surface Water - Climate Change 1" ([data.gov.uk](https://www.data.gov.uk/dataset/ca2b02ce-3115-4949-94ce-592bdbb9c717/risk-of-flooding-from-surface-water-climate-change-1)): "the 'Central' allowance for the 2050s epoch (2040-2060)", RCP 8.5. "Risk of Flooding from Rivers and Sea - Climate Change 1" ([CKAN](https://ckan.publishing.service.gov.uk/dataset/risk-of-flooding-from-rivers-and-sea-climate-change-1)): Central allowance for the 2050s (the page says 2040 to 2069) for rivers and "Higher Central" for the sea, likelihood bands High (3.3% or more a year), Medium, Low and Very Low.
- **Licence:** "Open Government Licence" on data.gov.uk for surface water; the rivers and sea CKAN record says "No Licence Provided". Confirm in DA-05.
- **Access:** WMS and download by area of interest; no OGC API listed for either.
- **Scope notes:** NaFRA "was not developed or tested for insurance underwriting or setting insurance premiums". Only one scenario per source is published (search results: the Flood Map for Planning uses a different, upper-end 2070s scenario for planning, and 2026 Environment Agency briefings advise planners not to use the checker's surface water layers; this is search-result only, not read on a gov.uk page).
- **Update:** last updated 13 Nov 2026 (surface water) and 4 Nov 2026 (rivers and sea). **Cost:** free.
- **Recommendation: CHECK ROW** ("How climate change may change this", linking to the official checker, which says it shows "how climate change might increase the chance of flooding in an area"); **NOT NOW** for our own data: one modelled scenario, two different time windows, and no postcode summary, so a figure from us would be harder to word honestly than the official page.

## 3. Flood outlines on a map

- **Publisher:** Environment Agency.
- **Dataset:** Flood Map for Planning, Flood Zones 2 and 3 (rivers and sea) ([data.gov.uk](https://www.data.gov.uk/dataset/flood-map-for-planning-flood-zones1), last updated 22 Oct 2026; [CKAN](https://ckan.publishing.service.gov.uk/dataset/flood-map-for-planning-flood-zones1)). Shows "present-day risk of flooding from rivers and the sea, ignoring the benefits of defences"; Flood Zone 1 is not in the data. The older separate Flood Zone 2 and Flood Zone 3 records are retired (search result only).
- **Licence:** data.gov.uk says "Open Government Licence"; the CKAN record says "No Licence Provided". Attribution (CKAN): "© Environment Agency copyright and/or database right 2025. All rights reserved."
- **Use limit:** "The Flood Zones are designed to only give an indication of flood risk to an area of land and are not suitable for showing whether an individual property is at risk of flooding." "Users of these datasets should always check they are suitable for the intended use."
- **Access:** OGC API Features (`https://environment.data.gov.uk/spatialdata/flood-map-for-planning-flood-zones/ogc/features/v1`), WMS and WFS at the same path, full download as GeoJSON, GeoPackage or File Geodatabase. No key or rate limit stated (the Defra Data Services Platform pages load only with JavaScript and could not be read: not confirmed).
- **Other outlines:** Risk of Flooding from Rivers and Sea (with defences) and RoFSW (topic 1) have WMS and download only.
- **Update:** "asNeeded". **Cost:** free.
- **Recommendation: ADD (with conditions).** This meets FE-25's "official outlines". Conditions: settle the OGL versus "No Licence Provided" mismatch in DA-05 (ask the Environment Agency's data team if needed); label each layer with its own words ("land at risk, not this home"; Flood Zones "ignore flood defences"); show the attribution; never show "no outline here" as "no risk" (rule 7); keep the official checker link first.

## 4. Radon

- **Publishers:** UK Health Security Agency (UKHSA) and British Geological Survey (BGS).
- **Open dataset:** BGS/UKHSA Indicative Atlas of Radon ([BGS](https://www.bgs.ac.uk/datasets/radon-data-indicative-atlas-of-radon/)): "Great Britain and Northern Ireland", "1 km grid size (approx. 1:1 000 000)", "Free for commercial, research and public use under the Open Government Licence". Major update with UKHSA on 1 Dec 2022; no later version date shown. Use level: "Local-level to regional-level use"; "indicative rather than definitive"; for definitive Affected Areas it points to the paid Radon Potential dataset ("Premium access is subject to number of users, licence fee and data preparation fee").
- **Attribution:** BGS asks users to "acknowledge the material". The required wording found in the dataset record was "Radon Potential classification © UK Health Security Agency © Crown copyright 2022" and "Contains British Geological Survey materials © UKRI [year]" (search result only; confirm from the download).
- **Access:** Shapefile or GeoPackage download; GeoIndex viewer; OGC WMS. **Cost:** free (open atlas).
- **Per-address check:** [UKradon address search](https://www.ukradon.org/services/address_search): "This service currently costs £3.90 including vat"; it gives "the estimated probability that an address is above the Action Level"; only a measurement gives the actual level. UKradon's [maps page](https://www.ukradon.org/information/ukmaps) shows "© Crown Copyright"; its terms page was not read (not confirmed).
- **Recommendation: ADD (with conditions).** Show the 1 km square's published class, labelled "this 1 km square, the highest level found in it; indicative, not a test of any home", with the UKradon address report and measurement advice linked. Conditions: DA-05 entry; confirm the attribution text from the download; never turn a low class into "no radon risk" (rule 7). This changes `data-sources.md`'s "Defer" line, which did not know of the open atlas.

## 5. Coal mining

- **Publisher:** Mining Remediation Authority (formerly the Coal Authority).
- **Free check:** [Find out if a property is affected by coal mining](https://www.gov.uk/check-if-property-is-affected-by-coal-mining): free search by postcode and boundary; "You can search for free, but you'll have to pay for a report"; reports from "£27 (plus VAT)"; [interactive map](https://datamine-cauk.hub.arcgis.com/).
- **Open datasets:** Coal Development High Risk Area ([data.gov.uk](https://www.data.gov.uk/dataset/b39be416-c1ca-41a0-ba0d-f32e6a1f6c31/coal-development-high-risk-area), last updated 11 Nov 2026): "UK Open Government Licence (OGL)"; WMTS service and map viewer; no download listed. Coal Mining Reporting Areas WMS ([data.gov.uk](https://www.data.gov.uk/dataset/coal-authority-coal-mining-reporting-areas-view-service-wms), last updated 8 Dec 2025): "supplied free of charge under the terms of the Open Government Licence", "subject to the following overriding re-use condition: re-use is not permitted for any activity that is part of the Coal Authority's public task responsibilities". Other data is licensed by application ([guidance](https://www.gov.uk/guidance/using-coal-mining-information)).
- **Resolution:** area polygons served as map images; no vector download or point query confirmed. **Update:** not stated.
- **Recommendation: CHECK ROW** (keep the recorded link "Check if a property is affected by coal mining (gov.uk)", shown in coalfield areas and elsewhere alike). A map layer of the reporting area could follow later, but the re-use condition needs a DA-05 reading first, since saying whether a home needs a mining report is close to the Authority's own service.

## 6. Road and rail noise

- **Publisher:** Department for Environment, Food and Rural Affairs (Defra).
- **Datasets:** Road Noise - All Metrics - England Round 4 ([CKAN](https://ckan.publishing.service.gov.uk/dataset/38b1444f-47a0-42ca-a358-0d145fcf7d5c), last updated 28 July 2025), its rail counterpart, and octave-band datasets ([data.gov.uk](https://www.data.gov.uk/dataset/road-noise-octave-band-data-england-round-4)). Explanation: [Explaining the 2022 noise maps](https://www.gov.uk/government/publications/strategic-noise-mapping-2022/explaining-the-2022-noise-maps).
- **Licence:** "Open Government Licence" (octave-band dataset on data.gov.uk); the All Metrics CKAN record says "No Licence Provided" with "© Department for Environment, Food & Rural Affairs copyright and/or database right 2023. All rights reserved." Confirm in DA-05.
- **Resolution:** "Noise levels are modelled on a 10 metre (m) grid at a receptor height of 4m above ground"; metrics Lden, LAeq,16h, Lday, Leve and Lnight; lower cut-off 35 dB (Lnight) and 40 dB (others).
- **Limits:** "No actual noise measurements were taken in the production of the strategic maps"; the data "does not necessarily represent an exact picture of the current situation on the ground". Mapping is every 5 years; the next round's date is not stated.
- **Access:** WMS, WCS and download by area of interest. No official address or postcode look-up was found (only a third-party one). **Cost:** free.
- **Recommendation: ADD (with conditions)** as a map layer only (Lden bands, "modelled for 2021, not measured"), with no single decibel figure per home or postcode, because a 10 m modelled value read at a postcode centre would look precise and could be wrong for the home. Conditions: DA-05 licence check (the two records disagree); label the year and method. If the map layer is not wanted, **CHECK ROW** to the publication page.

## 7. Broadband and mobile coverage

- **Publisher:** Ofcom.
- **Dataset:** Connected Nations update: Spring 2026 ([page](https://www.ofcom.org.uk/phones-and-broadband/coverage-and-speeds/connected-nations-update-spring-2026), published 13 May 2026, snapshot January 2026). The fixed-coverage data note ([PDF](https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/multi-sector/infrastructure-research/connected-nations-spring-2026/about-this-data-fixed-broadband-coverage-and-full-fibre-take-up-2026.pdf), v2 of 7 July 2026): files for "local and unitary authorities, Westminster parliamentary and devolved constituencies, census output areas and postcodes"; 121 postcode-area CSV files (all premises, 1,741,096 rows) plus residential-only files; "For census output area and postcode, we report on gigabit-capable coverage but not on full-fibre coverage due to commercial confidentiality."
- **Licence:** "We are providing this data on an open basis via the Open Government Licence" (data note). Ofcom's general [terms of use](https://www.ofcom.org.uk/about-ofcom/our-website/terms-of-use) ask that material be "acknowledged as Ofcom copyright and the title of the document/publication specified" and "not used in a misleading context".
- **API:** [api.ofcom.org.uk](https://api.ofcom.org.uk/): sign up for a key; "The broadband API is unaffected"; the legacy mobile API takes no new subscriptions and "Support for existing subscriptions will end on 30 November 2026"; new 2G and 4G/5G APIs are on a separate portal. Rate limits, cost and the API's terms of use: **not confirmed** (no terms page found).
- **Mobile download:** a 254 KB mobile ZIP and summary tables exist; their geography is **not confirmed**.
- **Update:** Connected Nations is published twice a year (spring update and annual report; next date not stated). **Cost:** free.
- **Recommendation: ADD (with conditions)** fixed broadband for the postcode from the bulk file (it fits DA-14's "this postcode"): label "predicted availability from providers, January 2026", gigabit-capable only, and link the Ofcom checker for the address. **CHECK ROW** for mobile (Ofcom's checker) until the new API's terms are read.

## 8. Rents for a small area

- **Publisher:** Office for National Statistics (using Valuation Office Agency rental data for England, per ONS search results).
- **Dataset:** Price Index of Private Rents, UK: monthly price statistics ([dataset](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/priceindexofprivaterentsukmonthlypricestatistics); [bulletin](https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/privaterentandhousepricesuk/latest), released 21 Oct 2026; next 18 Nov 2026).
- **Licence:** "Open Government Licence v3.0, except where otherwise stated."
- **Geography:** lowest is local authorities in England and Wales (Broad Rental Market Areas in Scotland and Northern Ireland). UK averages are given by bedrooms (one to four or more); the bulletin's Figure 8 charts local authority data by property size, but whether the workbook gives council figures by bedroom count is **not confirmed** (the repository's 16 Nov read of Table 1 does not say). No official postcode, LSOA or other small-area rent was found; the older VOA-based "Private rental market summary statistics" bulletin is marked discontinued (search result only).
- **Status:** "On 20 May 2026, PIPR data became "official statistics" and are no longer considered to be "in development""; not accredited yet.
- **Update:** monthly. **Cost:** free.
- **Recommendation: ADD (with conditions)** at council level only (DA-10 and DA-14): the council's name on the figure, the month, no relabelling to the postcode, and "not published" for councils with no figure (rule 7). Fix the stale status wording first.

## 9. Planning constraints

- **Publisher:** Ministry of Housing, Communities and Local Government's Planning Data platform; listed buildings come from Historic England.
- **Platform:** [API docs](https://www.planning.data.gov.uk/docs): beta API, no key mentioned; point search with `latitude` and `longitude` on `/entity.json` or `/entity.geojson`; no batch endpoint and "Apply polite rate-limiting between requests"; bulk downloads as CSV, JSON, GeoJSON and Parquet; from November 2026 searches are capped at 10,000 results. Licence: "Open Government Licence v3.0". Coverage: "an absence of results does not mean no constraints exist"; "data coverage varies by area".
- **Datasets (read 16 Nov 2026, each "Licensed under the Open Government Licence v.3.0" and each warning "The data may be incomplete and not yet cover all of England"):**
  - [Listed buildings](https://www.planning.data.gov.uk/dataset/listed-building): 382,382 records from Historic England; a point inside the building that "does not define the extent of the area affected by the listing"; attribution "© Historic England 2026. Contains Ordnance Survey data © Crown copyright and database right 2026."
  - [Conservation areas](https://www.planning.data.gov.uk/dataset/conservation-area): 10,778 from 159 providers; contains duplicates being reconciled; same attribution as listed buildings.
  - [Article 4 direction areas](https://www.planning.data.gov.uk/dataset/article-4-direction-area): 7,626 from 121 providers; "© Crown copyright and database right 2026".
  - [Tree preservation zones](https://www.planning.data.gov.uk/dataset/tree-preservation-zone): 105,178 from 84 providers ("a small group of local planning authorities").
- **Historic England's own Open Data Hub and its terms page returned 403 (not confirmed).** Search results say its GIS data is under OGL and updated daily, and that its terms ask users to state the date the data was obtained (search result only).
- **Update:** collected daily (last run 16 Nov 2026). **Cost:** free.
- **Recommendation: ADD (with conditions)** listed buildings and conservation areas (the best-covered sets): "In this source" or "Not in this source; check with <council>" (never "none"), the council's planning link, the attribution, and a "listing point, not the protected extent" note. **CHECK ROW** for Article 4 directions and tree preservation orders (121 and 84 providers out of England's planning authorities, so most answers would be "not in this source"); link to the council. Both meet DA-11 once DA-05 records the licence.

## 10. A free basemap

- **OpenStreetMap public tiles** ([tile usage policy](https://operations.osmfoundation.org/policies/tiles/)): commercial use is not banned but "access may be withdrawn at any point"; "there is no SLA or guarantee"; attribution must be visible on the map; a unique User-Agent and valid Referer are required; no bulk or offline downloading. Unsuitable for a public product, as `data-sources.md` already says.
- **OS Open Zoomstack** ([OS product page](https://www.ordnancesurvey.co.uk/products/os-open-zoomstack); [docs](https://docs.os.uk/os-downloads/products/maps-and-imagery-portfolio/os-open-zoomstack)): "Free to use for everyone"; Great Britain; GeoPackage and vector tiles (one MBTiles file "around 3GB", Web Mercator); "updated every six months in June and December"; national to street scale (1:5,000,000 to 1:10,000). Neither page names the licence; OS states OS OpenData is under the OGL with attribution "Contains OS data © Crown copyright [and database right] [year]" ([copyright acknowledgements](https://www.ordnancesurvey.co.uk/customers/public-sector/public-sector-licensing/copyright-acknowledgments), search result only). The [vector tiles guide](https://docs.os.uk/os-downloads/products/maps-and-imagery-portfolio/os-open-zoomstack/os-open-zoomstack-getting-started-guide/zoomstack-vector-tiles) mentions "a Creative Commons Attribution 3.0 US License", most likely for the style material: **not confirmed**.
- **OS Maps API and OS Vector Tile API:** both on the "OS OpenData Plan (FREE)" ([Maps API](https://www.ordnancesurvey.co.uk/products/os-maps-api), [Vector Tile API](https://www.ordnancesurvey.co.uk/products/os-vector-tile-api)); the [Data Hub page](https://www.ordnancesurvey.co.uk/developers/os-data-hub) says OpenData is "no-cost access with unlimited usage, subject to a data limit based on the dataset's detail" and Premium includes "free premium data (API transactions) up to £1,000 per month". Which styles and zoom levels OpenData covers, rate limits, and the API's terms: **not confirmed**. Calling OS from the visitor's browser would also tell OS which places people look at, which FE-03 chose to avoid.
- **Recommendation: ADD (with conditions)** self-hosted OS Open Zoomstack as an option in FE-03's pricing, next to self-hosted OpenStreetMap tiles: it is one free 3 GB file, OGL, needs no share-alike (OSM's ODbL does), and fits "serve from our own domain". Great Britain only, which suits England first. Conditions: confirm the licence on OS's licence page; show the OS attribution; refresh each June and December. This is the founder's call under FE-03, not a change to it.

## Pages that could not be read (not confirmed)

- Defra Data Services Platform dataset pages (environment.data.gov.uk): load only with JavaScript; no key or rate-limit statement read.
- Historic England Open Data Hub and its data download terms: HTTP 403.
- UKradon terms and conditions page: not read; BGS radon attribution wording is from a search result.
- Ofcom API terms of use, rate limits and cost; the geography of the Spring 2026 mobile coverage files.
- Whether the PIPR workbook gives council-level figures by bedroom count.
- OS Open Zoomstack's named licence (OS pages say "free to use" without naming it); OS Maps API OpenData zoom levels and limits.
- Whether the coal reporting area WMS supports a point query, and any coal data update frequency.
- Licence mismatches to settle in DA-05: Flood Zones and the rivers-and-sea climate change layer ("No Licence Provided" on CKAN, OGL on data.gov.uk); Road Noise All Metrics ("No Licence Provided" on CKAN).

All pages were read on 16 November 2026.
