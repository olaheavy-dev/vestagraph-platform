# Stage 5b, group B: data (the pipeline, licences, postcodes, walking times): design

**Date:** 20 Nov 2026. **Status:** approved by the founder, 20 Nov 2026 (prompt window, "Approve (Recommended)", which also accepts the agent's calls marked below; each can still be changed). Recorded in decision [0061](../../decisions/0061-pilot-data-pipeline-postcodes-and-walking-times.md). **Decisions it follows:** [0028](../../decisions/0028-no-scraping.md) (no scraping), [0029](../../decisions/0029-external-services.md) (adapters label Live, Cached, Fallback or Unavailable; live-service tests stay out of the merge gate), [0046](../../decisions/0046-public-area-check-first.md) (searched postcodes never reach logs; postcode only), [0054](../../decisions/0054-official-rankings-in-the-pilot.md) (official rankings quoted, never our own score), [0059](../../decisions/0059-pilot-basemap-from-openfreemap.md) (basemap), [0060](../../decisions/0060-pilot-foundation-hosting-and-database.md) (group A: the server, Neon, releases, secrets). **Settles:** DA-04, DA-05, DA-06, DA-08. **Stage:** 5b, the decisions before the build.

## Intent and why
The pilot shows about 40 official and open datasets (flood, crime, schools, transport, prices, council figures and more). The founder asked, on 14 Nov 2026: "we would need proper and robust system design for data ingestion from the sources, process them into structure format, saving them, monitoring and viewing their versions" [sic]. Every figure a visitor sees comes from these copies (0046: the area tools read only our cached copies), so a bad download that goes live shows wrong facts on a public site. The pipeline must therefore check each new copy before it goes live, keep the previous one to roll back to, and tell the founder when a source stops updating.

Success: each source arrives on its own schedule as a numbered edition, goes live only after its checks pass, can be rolled back in one step, is visible to the founder with its history, and raises an alert when it is late; licences, credits and freshness live in one register that also feeds About the data.

## Goals
1. One pattern for every source: fetch, keep the raw file, check, save an edition, switch live, roll back (DA-04).
2. One licence register that the pipeline, the alerts and About the data all read (DA-05).
3. Postcode lookup with no outside service (DA-06).
4. Walking times from each postcode to nearby places (DA-08).
5. The founder sees every source's editions, checks and runs, and can roll back.

## Non-goals
- The privacy notice, lawful basis and DPIA (group C), the AI work (group D).
- Address-level lookup (0046: postcode only); the energy certificate lookup stays live per request, storing nothing (DA-09).
- Building anything: the build is planned next, and starts after groups C and D (0046, 0060).

## Anti-goals (a failure even if it works)
- An edition that failed its checks shown to visitors.
- Missing data shown as zero, a favourable value or a clean result (rule 7), including a walking route that wasn't found shown as "0 min".
- A searched postcode sent to an outside service or written to a log (0046).
- A source used before its licence record says "cleared".
- A source that silently stops updating while the site keeps showing its old copy as current.
- The founder's dashboard reachable from the internet.

## Constraints
- Free first, within the rules (house rule, founder 19 Nov 2026). The server is small and shared (0060); Neon storage costs about $0.35 per GB a month (0060).
- Python only (0049). New packages need the founder's approval: Dagster (`dagster`, `dagster-webserver`, Apache-2.0) is approved by the choice below, subject to the memory check; Valhalla runs as a container image, not a Python package.
- England only; other nations show "not yet covered" (rule 6), with a nation field kept in the data.

## Approaches considered
### The pipeline's scheduling and dashboard (DA-04)
| | What it gives | Cost |
|---|---|---|
| **Dagster on the server, if memory allows (chosen)** | Run history, logs per source, schedules, check results, a rollback launcher, all free | About 0.6 to 0.8 GB of memory all the time (measured in the spike, macOS); no login of its own; concepts to learn |
| Plain jobs on timers plus our own admin page (the fallback) | Lightest on memory | We build run history, retries and the dashboard ourselves |
| Prefect | Similar to Dagster | Same login and memory costs, weaker on editions |

A throwaway spike on 20 Nov 2026 (Dagster 1.13.31, two real sources: flood warnings and Birmingham crime) proved: editions, blocking checks (a bad edition never went live), the 15-minute schedule firing by itself, a rollback, and six tests in about 1.5 seconds. About 200 of its 330 lines (fetch, check, save, switch, roll back) were plain Python and SQL that work without Dagster, so the way out is cheap.

### Where the jobs run
- **Schedules on the server; GitHub Actions for the heavy builds (walking times, bus timetables), started automatically by the server through workflow dispatch (chosen; founder's choices 2 and 9).** GitHub's scheduled runs can start late or be dropped without a failure, and are switched off after 60 days without repository activity, so routine schedules don't belong there.
- All on GitHub, or all on the server (the walking-time build would compete with the live app): not chosen.

### Postcode lookup (DA-06)
- **Our own copy of the ONS Postcode Directory, loaded quarterly (chosen).**
- postcodes.io's public API: same ONS data, no fresher, no uptime promise, an unpublished fair-use limit, and searches sent to a third party.
- Self-hosted postcodes.io (MIT): private like our own copy, but another service with its own database to run and update on the small server.
- postcodes.io as the main route with our copy as the backup (the founder's proposal, weighed in the conversation): two routes to build, test and keep in step, with no gain, because our copy must be loaded anyway and the area data lives in the same database.

### Walking times (DA-08)
- **Valhalla (MIT), batch, rebuilt quarterly (chosen).**
- Valhalla on demand on the server: fresher, but a few GB of memory (an estimate) on the small server, and searched locations reach the engine.
- Straight-line estimates: misleading near rivers, railways and main roads.
- OSRM (BSD-2) and GraphHopper (Apache-2.0): heavier on memory; licences to re-confirm if ever reconsidered.

## What the founder decided (20 Nov 2026, prompt windows)
1. **Who sees versions:** "You only, admin screen" (over the agent's "You only, simple").
2. **Standard tool or our own:** the founder asked "should we be using a standard tooling or be creating a custom one and reinventing the wheels?" and "would we be able to test and ensure they run"; after the answers, "Try Dagster in a spike (Recommended)" and "Server; GitHub for heavy builds (Recommended)"; after the spike, "Dagster if memory allows (Recommended)".
3. **Dagster's dashboard login:** after asking "is there a way to authenticate dagster admin or not?": "VPN only" (over the agent's "VPN + Caddy password").
4. **Postcodes:** after asking about postcodes.io's availability, proposing "postcodes.io as the main option and then if it is down we have ONS data as backup", and asking about privacy, data reliability and update frequency: "ONS copy only (Recommended)".
5. **Unclear licences:** "Let us discuss this case by case, no blanket rule". Then, for each, the founder brought the publishers' own records and decided to use them under the Open Government Licence v3: the Environment Agency's Flood Map for Planning (the publisher's dataset record and data.gov.uk both say OGL; the catalogue's "No Licence Provided" is a metadata gap; the service's Ordnance Survey background map is separately restricted and not used); Defra's round 4 road, rail and airport noise maps (publisher records say OGL; copyright years 2023 and 2024; modelled for 2021 conditions); DfT's transport connectivity measure ("I would include it in City Explorer, using OGL v3 as the working licence and clearly labelling the metric experimental"; the file's "license: TBA" names no other licence); and the Bus Open Data Service ("Proceed with BODS for calculating scheduled buses per hour": DfT's catalogue lists OGL and its implementation guide allows commercial reuse, with attribution and an accuracy disclaimer). The records the founder cited (read 20 Nov 2026):
   - Flood zones: [publisher record](https://dsp.environment.data.gov.uk/dataset/04532375-a198-476e-985e-0579a0a11b47), [data.gov.uk](https://www.data.gov.uk/dataset/104434b0-5263-4c90-9b1e-e43b1d57c750/flood-map-for-planning-flood-zones1), [the catalogue entry with no licence](https://ckan.publishing.service.gov.uk/dataset/flood-map-for-planning-flood-zones1), [service terms](https://flood-map-for-planning.service.gov.uk/terms-and-conditions), [Ordnance Survey terms for its background map](https://flood-map-for-planning.service.gov.uk/os-terms).
   - Noise, round 4: [road](https://environment.data.gov.uk/dataset/562c9d56-7c2d-4d42-83bb-578d6e97a517), [rail](https://environment.data.gov.uk/dataset/3fb3c2d7-292c-4e0a-bd5b-d8e4e1fe2947), [airport](https://environment.data.gov.uk/dataset/dac9cba4-abe7-43bd-b8e9-8a83da52edd8), [Defra licensing guidance](https://environment.data.gov.uk/support/faqs/275874594/275874729).
   - DfT connectivity: [DfT publication scheme (Crown copyright, OGL)](https://www.gov.uk/government/organisations/department-for-transport/about/publication-scheme#crown-copyright), [the publication](https://www.gov.uk/government/publications/transport-connectivity-metric), [interpreting the scores](https://connectivity-tool-lite.dft.gov.uk/help/interpreting-connectivity-scores).
   - BODS: [DfT catalogue (licence: OGL)](https://findtransportdata.dft.gov.uk/dataset/bus-open-data---download-all-timetable-data--18335fb19c4), [implementation guide: use of published data and attribution](https://www.gov.uk/government/publications/bus-open-data-implementation-guide/bus-open-data-implementation-guide).
6. **Walking times:** "Valhalla, batch, quarterly (Recommended)".
7. **OpenStreetMap's share-alike:** "Accept share-alike if needed (Recommended)".
8. **First city for walking times:** "Let us yse sheffield for walking times" [sic] (over the agent's Birmingham).
9. **Approval for data builds:** "why does this need my approval [...] the more automated the better": the data builds run automatically, with the safety moved into the credential's limits and the pipeline's checks (see Running it).
10. **Neon's running cost:** after the builder check found the pipeline keeps Neon awake more than 0060 assumed: "Trim the wake-ups (Recommended)": Dagster's history in SQLite on the server, flood still every 15 minutes, 2 editions for big sources. Rough estimate, unmeasured: about $10 to $15 a month for Neon, within 0060's range and under its $25 alert; lower after choice 11 removed the 15-minute source (measured at build).
11. **Live flood warnings:** after asking "semms like the flood data is the one with the hightes frquesncy of evry 15 minutes, is it a dela breakef for the pilot" [sic] and "Amongts the other options showd we do flood data just asking" [sic]: "Link to GOV.UK (Recommended)". The pilot keeps no copy of live warnings; the flood row links to the official GOV.UK flood warnings service. Long-term flood risk (flood zones, risk by postcode, surface water) stays. This reverses DA-12 for the pilot; the specifications, fixtures, AI-03 cases and canvas boards that show the live row change in a follow-up pull request.

## The design

### Sources and editions (DA-04)
Every source follows the same steps, in a plain Python package (`vestagraph-pipeline`) that does not import Dagster:
1. **Fetch** the publisher's file or API response (no scraping, 0028), with the source's own adapter (0029).
2. **Keep the raw file** unchanged, with its download time and checksum. *Agent's call:* raw files go to a Cloudflare R2 bucket in the EU (R2's free tier is about 10 GB of storage a month, from memory; the builder confirms the free tier and whether an EU-located bucket is included on Cloudflare's R2 pricing and data-location pages, with the date read; the founder's Cloudflare account already exists), keeping the last 3 raw files per source; larger raw files (the OpenStreetMap extract, bus timetables) are kept only until their edition is live, then deleted.
3. **Tidy** into our structure, with each fact's official level (DA-14) and the source's edition date.
4. **Check** with that source's rules. Every source has at least: the expected columns or fields are present, values are in their allowed ranges or code lists, and the number of rows hasn't changed by more than a set share since the live edition (*agent's call:* 20% unless the source's register record says otherwise). Missing values stay missing (never zero). An empty answer is valid only where the source says so (for example, no planning applications nearby is a real answer).
5. **Save** as a new numbered edition: its own table in the `area` schema, plus a row in an `editions` table (source, edition number, fetched at, publisher's edition date, row count or unknown, raw file checksum, check results, status `candidate`, `live`, `failed` or `retired`).
6. **Switch live** only if every check passed: while holding a lock for that source (for example a PostgreSQL advisory lock keyed on the source id, held across check and switch, so two runs, or a run and a rollback, never switch the same source at once), one transaction repoints the source's `<source>_current` view to the new edition and marks the old one retired. A failed edition never goes live, and the live one stays.
7. **Roll back**: the same switch, to an earlier edition that passed its checks. Keep the last 3 passed editions of each source, but only 2 of the big ones (walking times, the postcode directory, bus timetable inputs), deleting older ones (founder's choice 10 below).

The area tools and the API read only the `_current` views. Every `_current` value is Cached in 0029's terms; once older than the source's allowed age it is labelled as that source's register record says.

**Calculated figures (rule 2):** the views hold tidied **inputs** only. Every calculated figure a visitor sees (crime counts within a distance, buses per hour, distances, priority results) comes from the tested `vestagraph_area` package, either when asked or precomputed by the pipeline calling that package's functions; SQL and PostGIS may select and filter inputs (for example, places within a distance) but never produce a shown figure. Walking times are an **input** from Valhalla, stored with their method and the OpenStreetMap date (as the register line DA-18 already treats them).

### Running it
- **If the server has at least about 1.5 GB of memory free** after the old app is retired (0060, measured in the group A build): Dagster runs on the server (webserver and daemon in containers, its run history in a SQLite file on the server, not in Neon, so Neon can sleep between jobs; the builder confirms against Dagster's deployment documentation that the webserver and daemon can share SQLite storage, and otherwise runs both in one container), calling the pipeline package. Its dashboard is reachable **only over the founder's WireGuard VPN** (founder: "VPN only"); telemetry and the newsletter prompt switched off. It is the founder's admin screen: each source with its runs, check results and schedule, and the rollback job.
- **Otherwise:** the same package runs on systemd timers, and a small admin page lists editions with a roll-back button, served **only on the WireGuard VPN** like Dagster (the founder's "VPN only"; never on the public app). That page then needs a canvas board and a specification before it is built.
- **Binding:** the dashboard's port (Dagster's or the fallback page's) binds only to the server's WireGuard interface address, never `0.0.0.0` (Docker's published ports bypass host firewall rules such as ufw). The launch check tries it from outside the VPN, both at the server directly and through Cloudflare.
- *Agent's call:* in either case, a short page listing each source's editions (number, dates, checks, status) is added only if the founder finds the Dagster history hard to read in use; the spike showed rollback is a typed form, not a button.
- **Schedules** come from each source's register record (for example crime monthly, the postcode directory quarterly; no pilot source refreshes faster than daily after choice 11).
- **The heavy builds** (walking times, and turning the bus timetables into the inputs for buses per hour) run on GitHub Actions' free standard runners. Dagster on the server starts them automatically when a new upstream edition appears (a new OpenStreetMap extract each quarter; new bus timetables), through GitHub's workflow-dispatch API (in the systemd fallback, a timer makes the same call), so GitHub's unreliable schedules are not used. No approval step (founder, 20 Nov 2026: "why does this need my approval [...] the more automated the better"). *Agent's call* for the bus timetables: they are large, so they follow the walking-time pattern rather than running on the small server.

### Knowing it ran
*Agent's call:* the pipeline checks results, not the scheduler. Each register record states how long may pass since the pipeline last **confirmed** the source: a fetch whose content passed every check (or matched an edition that already passed), whether or not it changed. A fetch that fails tidying, checks or the switch leaves the last-confirmed time unchanged, so a publisher returning broken files keeps the source late and the alert fires; failed checks also raise their own alert. The clock is not the publisher's data date, so a source published with a lag (police.uk crime runs about two months behind) is not always late (for example a daily source 3 days, a monthly source 45 days). The API exposes `/healthz/data`, which lists only source names with `fresh` or `late` (no data, no postcodes); it answers from a small state file the pipeline writes on the server after each run, never from a database query, so checks and outside callers never wake Neon; and the existing uptime workflow in the infrastructure repository checks it, so the founder gets an email when any source is late, whether the scheduler, Dagster or the server failed. That uptime workflow is a GitHub schedule, which can run late; it is a backstop for a failure that lasts hours, which is what it needs to catch. The site keeps showing a late source with its data date.

### Testing
- Each source's fetch, tidy and check code is tested in `make check` against saved sample files (synthetic or small real extracts with their licence recorded), including a malformed file, an empty file and a large drop in rows.
- The switch and roll-back logic is tested against a real PostgreSQL in tests (the spike's six tests are the model).
- Contract tests against the live sources run nightly, outside the merge gate (0029), and alert on format changes.

### The licence register (DA-05)
*Agent's call:* one record per source in `packages/fixtures/reference/source-register.json`, with a JSON Schema checked by the fixture validator. Each record: id, name, publisher, source URL, licence name and URL, the date the licence was read, the exact attribution text, restrictions (for example the EPC address fields), personal data (none, or what), status `cleared`, `open` or `blocked`, the feature switch it controls, update cadence and the allowed age (for alerts), and notes. The pipeline refuses to make a source live unless its record is `cleared`; About the data (AREA-25, AREA-44, CITY2-58 to CITY2-72) is served by the API from the register and the live editions' dates at request time (cached; the dates exist only at run time, so it is not a `make generate` output); Dagster's schedules read the cadence from it.
- The four sources the founder settled are `cleared` under OGL v3 with the conditions in decision 5 above; the agent re-reads each linked publisher page when writing its record and records the date.
- Every other source gets its record, read case by case (founder: "no blanket rule"). **Only the founder sets a status to `cleared`:** the agent reads the publisher's pages and brings each source to the founder in a prompt window, and the founder's answer is recorded in the record's notes; any that stays unclear stays undecided, and its feature stays switched off until then (the existing rule: each extra sits behind its own switch, and launch never waits for one).

### Postcode lookup (DA-06)
- The ONS Postcode Directory (ONSPD) is a pipeline source, loaded quarterly (ONS releases in February, May, August and November), checked and switched live like any other. Lookups are a read from our own table; searched postcodes never leave our system.
- **What a search shows:** a live English postcode returns its location and areas; a Welsh or Scottish one shows "not yet covered" (rule 6); a Northern Irish one (`BT`) shows "not yet covered" without needing Northern Ireland's data, which has its own commercial licence and is not loaded; Channel Islands and Isle of Man postcodes (GY, JE, IM) show "not yet covered", keyed on the directory's country code rather than the prefix (the builder confirms how the ONSPD codes them); a retired postcode says it was retired and when; an unknown one says "We don't know this postcode yet" (new postcodes can take up to a quarter to appear).
- Each postcode has one point (its centre, with ONS's quality marker); areas follow that point, so a postcode on a boundary takes the side its point is on, a limit stated on About the data.
- The ONSPD's licence and its OS and Royal Mail attribution lines are recorded in the register.

### Walking times (DA-08)
- **Engine:** Valhalla (MIT), its official container image, pinned.
- **Batch on GitHub Actions**, started automatically by Dagster each quarter after a new OpenStreetMap England extract (Geofabrik, about 1.6 GB today): build the graph, then use Valhalla's matrix service for each postcode's centre to the nearest places in each category within a straight-line pre-filter of 5 km, keeping the nearest 10 per category (*agent's call*, matching FE-19's card rules of up to 10 places within 5 km, so every place the card shows has a walking time; the Sheffield trial measures the cost, and the agent comes back to the founder if 5 km proves too costly). The job is split by postcode area across parallel jobs to fit the runners' limits (4 CPUs, 16 GB of memory, 14 GB of disk).
- **Results are pulled, not pushed** (after the pre-push review found that a database credential in GitHub could be reached by any code on `main`, including dependency updates that merge on green checks): the GitHub job uploads its result as a workflow artifact with a checksum; the server's pipeline downloads it, checks the checksum, loads it into its own incoming tables and checks it like any other source before it goes live. **No database credential lives in GitHub.** The server holds one GitHub token: fine-grained, this repository only, Actions read and write only (to start a build and download its artifact), with an expiry, kept in SOPS (0060). Changes to the build workflows are founder merges, like the release workflow (0060); the group B build plan adds them to `AGENTS.md`'s founder-merge list (itself a founder merge). A compromised dependency could still produce plausible but wrong figures, as it could on the server; the checks, the row-change limit and rollback are the guard. App releases still wait for the founder's approval (0060); this automation covers data builds only.
- **Destinations** come from official datasets where they exist (DfE schools, NaPTAN stops and stations) and from OpenStreetMap for everyday places and parks.
- **Missing routes:** "no walking route found" is stored as `no_route` with no time, distinct from `not_computed`; neither is ever shown as zero.
- **Shown with** the OpenStreetMap data date and "© OpenStreetMap contributors". *Agent's call* under the founder's "Accept share-alike if needed": we treat share-alike as applying (the safer reading, since no one is placed to rule it out), and publish each live edition of the walking-time table, and of places taken from OpenStreetMap, as a downloadable file under ODbL, attached to a GitHub release of this repository and linked from About the data.
- **One city first** (Sheffield; founder, 20 Nov 2026: "Let us yse sheffield for walking times" [sic]) to measure the build time and storage before all of England; the estimate today is 10 to 20 hours of computing and 2 to 4 GB of storage, both unmeasured.

### Scope of the build plan
*Agent's call:* the group B plan covers the pipeline package, Dagster, the licence register, the freshness check, postcode lookup, walking times (Sheffield first, then England), and two model sources end to end (the Environment Agency's flood risk by postcode, a batch file, and crime, a monthly source with a publishing lag). Every other source is then its own small ticket in the same pattern, taken from `docs/references/data-sources.md` and the register. The Dagster path is planned with a stop point at the group A memory measurement; the fallback admin page is designed and planned only if that measurement fails. Dagster's dashboard uses the WireGuard VPN the infrastructure repository already runs.

## Launch blockers group B adds
1. Every source the pilot shows has a register record marked `cleared`; any other source's feature is switched off.
2. Every source has its checks and has gone live once through the pipeline; one roll-back has been tried.
3. `/healthz/data` is watched by the uptime check, and a deliberately late source has raised an alert.
4. The ONSPD is loaded, and the six search outcomes (English, Welsh or Scottish, Northern Irish, Channel Islands or Isle of Man, retired, unknown) are tested.
5. Walking times are built for England, with `no_route` shown as "no walking route found".
6. The Dagster dashboard (or, in the fallback, the admin page) is reachable only over the VPN, checked from outside it.

## For group C (privacy), from this design
- New processors: Cloudflare R2 (raw files, no personal data); GitHub Actions (the walking-time and bus timetable builds, no personal data). Searched postcodes stay on our systems.
- The EPC lookup remains the one live call with personal data (DA-09); nothing in this pipeline stores personal data.

## Left to the builder
The pipeline package's layout, each source's exact check rules and allowed row change, the table and view names beyond the pattern above, the Dagster asset layout, the R2 bucket's settings within the free tier, Valhalla's settings (walking speed: Valhalla's default, recorded on About the data), the shard size for the walking-time build, and the alert wording. Also: GitHub-hosted jobs stop after 6 hours each (from memory; confirm on GitHub's limits page), so the England build is split into jobs that fit, and whether each job rebuilds the routing graph or reuses one built once; switching a `_current` view to an edition with different columns needs a drop and create in the same transaction (`CREATE OR REPLACE VIEW` cannot drop or rename columns); and the Neon storage estimate, itemised (two editions each of England's walking times and the postcode directory, plus Neon's 7-day restore history after bulk loads and 96 flood checks a day), checked against the $10 to $15 estimate.
