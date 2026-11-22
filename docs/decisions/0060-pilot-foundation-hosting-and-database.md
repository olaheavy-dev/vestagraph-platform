# 0060: The pilot's foundation: the app on the founder's server, the database on Neon

**ID:** IN-07 (with register lines IN-01 to IN-05, DA-03 and BE-02)  
**Status:** Accepted (founder, 19 Nov 2026, prompt windows; the design approved with "Approve (Recommended)")  
**Date:** 2026-11-19  
**Stage:** 5b (group A of the stage 5b decisions)  
**Amends (no older text is rewritten):** [0022](0022-cost-first-hosting.md) for the database only: the database goes to a paid managed service (Neon) rather than the founder's server. 0022's order stays for everything else. Adds a dated note to [0046](0046-public-area-check-first.md) on Cloudflare's own logs.  
**Design:** [`2026-11-19-stage-5b-foundation-design.md`](../superpowers/specs/2026-11-19-stage-5b-foundation-design.md), which holds the options, sources, every founder answer and every agent's call.

## Context
The pilot gate passed on 19 Nov 2026. Stage 5b starts with 17 open decisions, and the founder chose to take them in four groups, one at a time: "A first, then B, C, D (Recommended)" (A: foundation; B: data; C: privacy and accounts; D: AI). This record settles group A.

The pilot is public and stores personal data: email addresses, chat text and saved areas ([0058](0058-signed-in-chat-in-the-pilot.md)). 0022 (written for a private prototype) put the API, PostgreSQL with PostGIS and background jobs on the founder's existing server. The server is in Germany (EEA); its current state was read on 19 Nov 2026 from the founder's private infrastructure repository and is recorded there, not in this public repository. The launch blockers below are what it must meet first.

## Options (summary; the design has the full table and sources)
- **Database on the founder's server:** £0 extra and next to the API, but we build and test encrypted backups; each app keeps its own copy.
- **Neon (chosen), Frankfurt:** managed PostgreSQL with PostGIS, pay per use with no minimum ($0.106 per compute-unit hour, $0.35 per GB a month on the Launch plan, read 19 Nov 2026), undo up to 7 days, up to 100 projects.
- **DigitalOcean, Frankfurt:** $15.15 a month fixed, daily backups and 7-day undo, several apps sharing 1 GB of memory.
- Split personal data onto Neon's free tier; Supabase; Aiven's free tier; Scaleway: dropped or not pursued (reasons in the design).

## Decision
The founder's words, 19 Nov 2026 (prompt windows):
1. **The app runs on the founder's existing server:** "Yes, use it (Recommended)".
2. **The database:** after asking for the pros and cons, Neon's capacity and pricing, whether it could serve other projects, the cost for Vestagraph alone, other options and how DigitalOcean differs: "Several projects", then "Neon Frnakfurt for now we can compare cost later if cost sky rockets" [sic].
3. **Deploys:** "Approve each release (Recommended)".
4. **Budget:** "Alert now, full cap after AI (Recommended)".
5. **Secrets:** "Encrypted in the infra repo (Recommended)" (SOPS with age).
6. **Traffic:** "Proxy through Cloudflare (Recommended)".
7. **Capacity:** retire the founder's app that is being wound down, first (its name stays out of this public repository); then "Delete now, no notice" for its data, with one last confirmation before deletion.
8. **Cloudflare's own logs:** "Accept, name it, keep none (Recommended)".
9. **The private infrastructure repository:** "Agents merge after proper review and tests if applicable, nothing must be broken".

So:
- **Where things run (IN-01, IN-02):** Next.js (with Better Auth), the FastAPI API and the background jobs run as containers on the founder's server in Germany behind Caddy, with Cloudflare proxying `vestagraph.com`.
- **Database (DA-03):** PostgreSQL with PostGIS on **Neon, Frankfurt region, Launch plan**, one Vestagraph project; personal and public data in separate schemas (0058); size capped (starting at 0.25 compute units) and a 7-day undo window (agent's calls).
- **Infrastructure as code (IN-03):** in the founder's private infrastructure repository (Terraform and Ansible); this repository keeps only its own container and Compose files with placeholders (0022).
- **Releases and environments (IN-04):** a merge builds images tagged by commit on GHCR; the founder approves a release in a protected GitHub environment, which tags that image `production`; the server follows only that tag. Environments: the founder's laptop and live. Secrets: SOPS with age in the private infrastructure repository.
- **Spending (IN-05, part 1):** a Neon spending alert (about $25 a month) and a Hetzner billing alert now; the monthly cap in pounds is set after groups C and D.
- **API contract (BE-02):** FastAPI's generated OpenAPI description, committed; OpenTelemetry in the code (0025), with the trace destination chosen in group D.

## Consequences
- **Running cost:** Neon, about $5 to $21 a month for Vestagraph at the capped size plus storage (an estimate; it depends on traffic and group B's data size). The server's cost is unchanged.
- **Launch blockers** (from the design): the app being wound down is deleted; secrets encrypted; the approved release and a rollback work; no IP address or searched postcode in Caddy's or the app's logs and no postcode in Cloudflare's (checked with a test search); Cloudflare proxy on; no real IP addresses in the infrastructure documentation; one Neon restore tried; the spending alert and uptime check live.
- **For group C (privacy):** Neon, Hetzner and Cloudflare are processors to name; check each one's terms, company location and any transfer outside the UK and EEA; Neon's 7-day history keeps deleted data for up to 7 days, so 0058's deletions complete after that.
- Doc 04 §6's "PostgreSQL with PostGIS on the existing server before paying for a managed database" no longer applies to the pilot.
- **Revisit if** Neon's monthly cost climbs well past the estimate (founder: "we can compare cost later if cost sky rockets"), a restore fails, or group C finds a transfer problem with a provider.

## Dated note, 20 Nov 2026: the build plan
The group A build plan is [`2026-11-20-stage-5b-group-a-foundation.md`](../superpowers/plans/2026-11-20-stage-5b-group-a-foundation.md). While writing it, the agent found that the founder's other apps use DNS-only Cloudflare records, so the server's address is already public and proxying Vestagraph alone does not hide it (the design said it would). The founder's choices (prompt window, 20 Nov 2026):
- **The server's address:** "Lock and proxy all apps" (over the agent's "Lock Vestagraph only"): Caddy answers Vestagraph only for requests from Cloudflare's address ranges, and the other apps move to proxied records too.
- **Secrets after a reboot:** "Re-run after reboot (Recommended)": secrets reach the containers as files in a memory-only folder (Docker keeps environment variables in plain text on disk); the decryption key stays only on the founder's machine, so the secrets step is run again after each reboot.
- **How to build:** "Subagent-driven (Recommended)".

**Note, 20 Nov 2026 ([0063](0063-pilot-privacy-and-anonymous-chat-first.md), accepted by the founder):** sign-in leaves the pilot, so Better Auth's routes, tables and secrets are not part of the pilot's foundation; they return when sign-in opens.

**Note, 22 Nov 2026 (group A build, founder: "Separate live image (Recommended)"):** the release does not move a tag on the commit-tagged image. `publish` writes `sha-<commit>` tags to `vestagraph-placeholder` with `GITHUB_TOKEN`; only the approved `release` job writes the separate live image `vestagraph-placeholder-live:production`, with a token held as the `production` environment's secret, so a workflow on another branch cannot move what the server runs. See the [group A plan](../superpowers/plans/2026-11-20-stage-5b-group-a-foundation.md).
