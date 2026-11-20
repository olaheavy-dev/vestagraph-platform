# 0061: The pilot's data: an edition pipeline, a licence register, our own postcode copy and batch walking times

**ID:** DA-38 (with register lines DA-04, DA-05, DA-06 and DA-08)  
**Status:** Accepted (founder, 20 Nov 2026, prompt windows; the design approved with "Approve (Recommended)")  
**Date:** 2026-11-20  
**Stage:** 5b (group B of the stage 5b decisions)  
**Amends (no older text is rewritten):** the pilot's earlier assumption that postcodes come from postcodes.io (`docs/references/data-sources.md`): the pilot uses its own copy of the ONS Postcode Directory instead.  
**Design:** [`2026-11-20-stage-5b-data-design.md`](../superpowers/specs/2026-11-20-stage-5b-data-design.md), which holds the options, the spike's results, every founder answer and every agent's call.

## Context
Group A ([0060](0060-pilot-foundation-hosting-and-database.md)) settled where the pilot runs. Group B settles its data: about 40 official and open sources that every area figure comes from (the area tools read only our cached copies, [0046](0046-public-area-check-first.md)). The founder asked on 14 Nov 2026 for "proper and robust system design for data ingestion from the sources, process them into structure format, saving them, monitoring and viewing their versions" [sic]. No source had a licence record yet, four had official pages that disagreed, and the pilot's postcode lookup assumed a third-party service.

## Options (summary; the design has the full comparison)
- **Pipeline tool:** Dagster (chosen, if the server's memory allows), plain jobs on timers with our own admin page (the fallback), Prefect. A throwaway spike on 20 Nov 2026 ran Dagster with two real sources: editions, blocking checks, a self-firing 15-minute schedule, a rollback and six tests worked; it used about 0.6 to 0.8 GB of memory all the time and has no login of its own.
- **Where jobs run:** schedules on the server and heavy builds on GitHub Actions (chosen); all on GitHub (scheduled runs can be late or dropped); all on the server.
- **Postcodes:** our own ONS copy (chosen); postcodes.io's public API; postcodes.io with our copy as backup; self-hosted postcodes.io.
- **Walking times:** Valhalla in a quarterly batch (chosen); Valhalla on demand; straight-line estimates; OSRM or GraphHopper.

## Decision
The founder's words, 20 Nov 2026 (prompt windows):
1. **Versions view:** "You only, admin screen".
2. **Standard tool or our own:** the founder asked "should we be using a standard tooling or be creating a custom one and reinventing the wheels?" and "would we be able to test and ensure they run"; then "Try Dagster in a spike (Recommended)", "Server; GitHub for heavy builds (Recommended)", and after the spike "Dagster if memory allows (Recommended)".
3. **Dagster's dashboard:** after asking "is there a way to authenticate dagster admin or not?": "VPN only".
4. **Postcodes:** after proposing "postcodes.io as the main option and then if it is down we have ONS data as backup" and asking about privacy, reliability and update frequency: "ONS copy only (Recommended)".
5. **Unclear licences:** "Let us discuss this case by case, no blanket rule"; the founder then cleared the Environment Agency's flood zones, Defra's round 4 noise maps, DfT's transport connectivity measure ("using OGL v3 as the working licence and clearly labelling the metric experimental") and the Bus Open Data Service ("Proceed with BODS for calculating scheduled buses per hour") under the Open Government Licence v3, citing the publishers' own records (in the design).
6. **Walking times:** "Valhalla, batch, quarterly (Recommended)"; first city: "Let us yse sheffield for walking times" [sic].
7. **OpenStreetMap's share-alike:** "Accept share-alike if needed (Recommended)".
8. **Approval for data builds:** "why does this need my approval [...] the more automated the better".
9. **Neon's cost:** "Trim the wake-ups (Recommended)".
10. **Live flood warnings:** after asking "semms like the flood data is the one with the hightes frquesncy of evry 15 minutes, is it a dela breakef for the pilot" [sic] and "Amongts the other options showd we do flood data just asking" [sic]: "Link to GOV.UK (Recommended)".

So:
- **Pipeline (DA-04):** every source is fetched, its raw file kept, tidied, checked and saved as a numbered edition; it goes live only if every check passes, by one switch of its `_current` view, and rolls back by the same switch. The core is a plain Python package, independent of Dagster. Dagster schedules it on the server, with its history in SQLite on the server and its dashboard reachable only over the founder's WireGuard VPN, **if at least about 1.5 GB of memory is free** after group A retires the old app; otherwise systemd timers run the same package and a small admin page, also reachable only over the VPN, replaces the dashboard. Heavy builds (walking times, bus timetables) run on GitHub Actions, started automatically by the server; their results are pulled by the server as workflow artifacts and checked like any other source, so no database credential lives in GitHub; founder merges for the build workflows and the pipeline's checks replace an approval step. A freshness check emails the founder when any source is older than its allowed age. Calculated figures still come only from `vestagraph_area` (rule 2); walking times are a sourced input (DA-18).
- **Flood warnings:** the pilot keeps no copy of live flood warnings; the flood row links to the official GOV.UK service, and long-term flood risk stays. This reverses DA-12 for the pilot; the specifications, fixtures, AI-03 cases and canvas boards change in a follow-up pull request. No pilot source now refreshes faster than daily.
- **Licence register (DA-05):** one record per source in `packages/fixtures/reference/source-register.json`, schema-checked; nothing goes live unless its record is `cleared`, and only the founder sets `cleared`, case by case; About the data, the alerts and the schedules read it. Other sources are settled case by case.
- **Postcodes (DA-06):** our own copy of the ONS Postcode Directory, loaded quarterly; searches never leave our systems. Wales and Scotland show "not yet covered", and so do Northern Ireland, whose data is not loaded (separate commercial licence), and the Channel Islands and Isle of Man. Retired and unknown postcodes say so.
- **Walking times (DA-08):** Valhalla (MIT), batch each quarter on GitHub Actions, up to 5 km and the nearest 10 places per category (FE-19), Sheffield first; "no walking route found" is never zero; shown with the OpenStreetMap date and credit; the table is published under ODbL, treating share-alike as applying.

## Consequences
- **Running cost:** Neon about $10 to $15 a month (a rough estimate, unmeasured; within 0060's range and its $25 alert); Cloudflare R2's free tier for raw files; GitHub Actions free for this public repository.
- **New packages approved by this decision:** `dagster`, `dagster-webserver` (Apache-2.0), subject to the memory check; Valhalla's official container image (MIT).
- **Launch blockers:** every shown source `cleared`; every source live once through the pipeline and one rollback tried; a late source has raised an alert; the six postcode outcomes tested; walking times built for England; the dashboard (or the fallback page) reachable only over the VPN.
- **For group C (privacy):** Cloudflare R2 and GitHub Actions handle no personal data; searched postcodes stay on our systems; the energy certificate lookup remains the only live call with personal data (DA-09).
- **Revisit if** the server lacks the memory for Dagster, the 5 km walking-time build costs too much in the Sheffield trial, Neon's bill passes the alert, or a publisher contradicts a licence the founder cleared.
