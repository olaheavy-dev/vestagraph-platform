# Stage 5b, group A: the foundation (hosting, database, deploys, secrets): design

**Date:** 19 Nov 2026. **Status:** approved by the founder, 19 Nov 2026 (prompt window, "Approve (Recommended)", which also accepts the agent's calls marked below; each can still be changed). Recorded in decision [0060](../../decisions/0060-pilot-foundation-hosting-and-database.md). **Decisions it follows:** [0022](../../decisions/0022-cost-first-hosting.md) (cost-first hosting, amended here for the database), [0046](../../decisions/0046-public-area-check-first.md) (stage 5b decisions first; searched postcodes never reach logs), [0058](../../decisions/0058-signed-in-chat-in-the-pilot.md) (one database for accounts, chats and saved areas; Better Auth; the API holds no per-user state), [0059](../../decisions/0059-pilot-basemap-from-openfreemap.md) (Cloudflare already named in the privacy notice for maps). **Stage:** 5b, the decisions before the build.

**Note, 22 Nov 2026 ([0063](../../decisions/0063-pilot-privacy-and-anonymous-chat-first.md), accepted by the founder 20 Nov 2026):** sign-in leaves the pilot, so Better Auth is not part of the pilot's foundation: no Better Auth sign-in routes in the Next.js container, no Better Auth tables, and no Better Auth secret or keys in the secrets file. The text below is kept as approved; read its Better Auth parts (the stack, the "Where things run" table, the secrets list and the build plan's list) as returning only when sign-in opens. The `personal` schema stays, for the chat words kept 14 days in our own Neon table ([0064](../../decisions/0064-pilot-chat-ai-multi-agent-claude-langsmith.md) note).

## Intent and why
The pilot gate passed on 19 Nov 2026, and stage 5b starts with its open decisions (17 of them). The founder chose to take them in four groups, one at a time: **A, the foundation**, then B (data), C (privacy and accounts) and D (AI). Group A comes first because hosting decides the running cost, where personal data is stored and what gets logged, and the other groups build on it.

The pilot is public and stores **personal data** (email addresses, chat text, saved areas, 0058). So the foundation must be safe and cheap: no visitor's searched postcode or IP address reaches a log (0046), personal data can be restored after a mistake, and a bad change never reaches users without the founder seeing it.

Success: the register lines IN-01 to IN-05, DA-03 and BE-02 are settled (IN-05 in part), and the build plan can list the foundation's tasks and launch blockers without going back to the founder.

## Goals
1. Say where each part of the pilot runs, and why (IN-01, IN-02, DA-03).
2. Say how a change gets from a merged pull request to the live site (IN-04).
3. Say how secrets are kept (IN-04) and how the infrastructure is described in code (IN-03).
4. Set how spending is watched until the full monthly cap is set (IN-05, part 1).
5. Fix the problems 0022 listed with the founder's server, before Vestagraph deploys there.
6. List the launch blockers group A adds.

## Non-goals
- The data pipeline, source licences, postcode lookup and walking-time routing (group B).
- The privacy notice text, lawful basis, DPIA, access requests, the cookie check, the email-sending service and analytics (group C). Group A only records what group C must cover.
- The AI framework trial, the AI provider and the evaluation tooling (group D), and the tracing tool for chat traces (0058's 30-day traces).
- The full monthly budget cap in pounds (IN-05 part 2): set after groups C and D, when the email and AI costs are known.
- Building anything. This is a design; the build is planned next.

## Anti-goals (a failure even if it works)
- A searched postcode or a visitor's IP address in any server, application or Caddy log of ours (0014, 0046).
- Personal data that can't be restored after a mistake, or a restore that has never been tried.
- A merged change reaching the live site without the founder's approval.
- A searched postcode in Cloudflare's own logs (Cloudflare's IP analytics are accepted, decision 10 below).
- A secret in the public repository, or lying in plain files on the server.
- A server address, hostname, credential or private repository path in a tracked file (0022, `AGENTS.md`).
- A running cost with no alert on it.

## Constraints
- **Free first, within the rules** (house rule, founder 19 Nov 2026) and **cost first** (0022): a paid service only where it earns its cost; this design records why the database is one.
- The Vestagraph repository stays public-safe (0022): it holds only its own deployment files (container builds, a Compose file with placeholders). Server details and secrets live in the founder's private infrastructure repository.
- The pilot's stack is fixed by earlier decisions: Next.js frontend with Better Auth for sign-in (0048, 0058), FastAPI API in Python (0049), PostgreSQL with PostGIS (doc 04), and the API keeps no per-user state in memory (0058).
- UK GDPR: where personal data is stored, and by whom, goes into the privacy notice and the DPIA (group C). The EEA is treated as adequate by the UK.

## The founder's server today
The founder's existing virtual server at Hetzner in Germany (EEA) runs apps as containers behind Caddy. Its current state, including where it stands on 0022's five problems, was read on 19 Nov 2026 from the private infrastructure repository and is recorded there, not here (this repository is public). The launch blockers below are the conditions it must meet before Vestagraph goes live.

## Approaches considered

### Database (DA-03)
| | Cost | Backups and undo | Where | Notes |
|---|---|---|---|---|
| **The founder's server** | £0 extra | We would build nightly encrypted dumps and test restores | Germany, next to the API | Matches 0022 and doc 04; we own updates and backups; each app keeps its own copy |
| **Neon** (chosen, Frankfurt) | Pay per use, no minimum: $0.106 per compute-unit hour, $0.35 per GB a month (Launch plan) | Undo to any moment within a history window of up to 7 days | Frankfurt or London | Up to 100 projects; idle projects sleep and cost little; size can be capped |
| **DigitalOcean** | $15.15 a month, fixed (1 CPU, 1 GB memory, 10 GB disk) | Daily backups and undo within 7 days | Frankfurt or London | Predictable; several apps share one cluster's memory |
| **Neon free tier, personal data only** (split) | £0 | 6-hour history | London | Two databases, against 0058's one database; dropped |
| **Supabase** | Free tier pauses after a week and keeps no backups; Pro from $25 | — | London | Dropped: free tier unfit for real users |
| **Aiven free, Scaleway** | Aiven free: 1 GB, no backups kept; Scaleway: not confirmed (pages blocked) | — | EU | Not pursued |

Sources (read 19 Nov 2026): [Neon pricing](https://neon.com/pricing), [Neon regions](https://neon.com/docs/introduction/regions), [Neon compute sizes](https://neon.com/docs/manage/computes), [Neon PostGIS](https://neon.com/docs/extensions/postgis), [DigitalOcean pricing](https://www.digitalocean.com/pricing/managed-databases), [DigitalOcean PostgreSQL features](https://docs.digitalocean.com/products/databases/postgresql/details/features/), [DigitalOcean regions](https://docs.digitalocean.com/platform/regional-availability/), [Supabase pricing](https://supabase.com/pricing), [Aiven free PostgreSQL](https://aiven.io/free-postgresql-database), [Hetzner billing FAQ](https://docs.hetzner.com/cloud/billing/faq/).

**Estimated Neon cost for Vestagraph alone:** at the smallest size (0.25 compute units, 1 GB memory, about 2.7 cents an hour awake), about $5 a month if awake 4 hours a day, $8 at 8 hours, and $21 if always awake, including about 5 GB of storage. The real figure depends on traffic and the size of the area data (group B).

### Deploys (IN-04)
- **Approve each release (chosen):** a merge builds the image; a GitHub Actions job deploys it only after the founder approves in a protected GitHub environment.
- Auto-deploy on every merge (as the other apps do): rejected; nothing stops a bad change reaching personal data.
- Staging auto-deploy, live approved: safest, but two copies on a small shared server.

### Secrets (IN-04)
- **SOPS with age, encrypted in the private infrastructure repository (chosen):** decrypted only at deploy.
- GitHub environment secrets written to the server's `.env` at deploy: simpler, but the file on the server stays plain.
- Plain `.env` files (today's state): rejected for an app holding personal data.

### Address and traffic
- **Cloudflare proxy (chosen):** hides the server's address, absorbs traffic floods, allows rate limits at the edge. *(Correction, 20 Nov 2026: the founder's other apps' DNS-only records already publish the server's address, so the proxy hides it only once those apps are proxied too and Caddy refuses direct requests; founder: "Lock and proxy all apps", dated note on 0060.)*
- DNS only: one fewer company sees visitors' traffic, but the server's address is not hidden.

### Capacity
- **Retire the founder's app that is being wound down first (chosen):** frees memory and removes another app's user data from the server.
- Measure and upgrade if needed; upgrade now: not chosen.

## What the founder decided (19 Nov 2026, prompt windows)
1. **Order of stage 5b decisions:** "A first, then B, C, D (Recommended)".
2. **The founder's existing server runs the app:** "Yes, use it (Recommended)".
3. **Database:** after asking for the pros and cons, how many databases Neon's price allows, whether it could serve other projects, its capacity, other options, the cost for Vestagraph alone, and how DigitalOcean's pricing differs and whether it is in Germany: "Several projects" (the database service may later serve the founder's other projects too), then "Neon Frnakfurt for now we can compare cost later if cost sky rockets" [sic].
4. **Deploys:** "Approve each release (Recommended)".
5. **Budget:** "Alert now, full cap after AI (Recommended)".
6. **Secrets:** "Encrypted in the infra repo (Recommended)".
7. **Cloudflare:** "Proxy through Cloudflare (Recommended)".
8. **Capacity:** "Retire [the founder's app being wound down] first" (the app's name is left out of this public repository, as `AGENTS.md` requires for the founder's other projects).
9. The playback of this design: "Right, write it up (Recommended)".
10. **Cloudflare's own logs** (after the builder check asked whether 0046's "never reach server, application or hosting logs" covers them; Cloudflare keeps request analytics with IP addresses, no postcodes, for about 31 days on the free plan, [security events](https://developers.cloudflare.com/waf/analytics/security-events/), [changelog](https://developers.cloudflare.com/changelog/post/2026-10-02-30-days-analytics-on-every-plan/)): "Accept, name it, keep none (Recommended)". Cloudflare is a named processor; we never export or copy its logs; our own server, Caddy and app logs stay free of IP addresses. Recorded as a dated note on 0046.
11. **Work in the private infrastructure repository:** "Agents merge after proper review and tests if applicable, nothing must be broken" (a standing approval for that repository, over the agent's recommendation that the founder merges each change).
12. **The app being wound down:** "Delete now, no notice". The agent confirms once more with the founder just before the deletion runs, because it cannot be undone.

## The design

### Where each part runs (IN-01, IN-02, DA-03)
| Part | Runs on |
|---|---|
| Next.js frontend, with Better Auth's sign-in routes | A container on the founder's server |
| FastAPI API (area tools, chat, daily cap, deletion jobs) | A container on the founder's server |
| Background jobs (group B decides their shape) | Containers on the founder's server |
| PostgreSQL with PostGIS: personal data and public area data in separate schemas (0058) | **Neon, Frankfurt region, Launch plan** (pay per use), one Vestagraph project |
| Map tiles | OpenFreeMap (0059), unchanged |
| DNS, TLS at the edge, traffic proxy | Cloudflare (proxied records for Vestagraph) |
| Caddy | The founder's server, routing to the Vestagraph containers |

- **Neon settings:** autoscaling capped at a small top size (start at 0.25 compute units; raise only with a recorded reason); the history (undo) window set to 7 days; PostGIS installed with `CREATE EXTENSION`; the app connects over TLS. *Agent's call:* the cap and the 7-day window.
- **Amends 0022 for the database only:** 0022's order (free, then the founder's server, then paid) still applies to everything else. The database goes to a paid managed service because the founder wants one managed home for several projects with built-in undo, and chose to compare costs again if they climb.

### From merge to live (IN-04)
*Agent's call (after the builder check: the server's firewall rightly blocks GitHub's runners from logging in, so the server pulls rather than GitHub pushing):*
1. A pull request builds and tests the images (no push).
2. A merge to `main` builds the images and pushes them to GitHub's container registry (GHCR, public: the repository is public and the images hold no secrets), tagged with the commit (`sha-<commit>`), never `latest`.
3. A release job waits on a protected GitHub environment (`production`) for the founder's approval, then adds the tag `production` to that exact image. It needs only the repository's own token; *(Note, 22 Nov 2026: changed to a separate live image `vestagraph-placeholder-live` written with a token held as the `production` environment's secret, so a workflow on another branch cannot move it; see the group A plan.)* no server access and no decryption key live in the public repository.
4. On the server, Watchtower watches **only** the `production` tag of Vestagraph's images and pulls it (it never follows `main`). A check of `/healthz` (reporting the commit) after the pull confirms the release.
5. Rollback is moving `production` back to an earlier commit's image through the same approved job.
6. Database schema changes run when the new container starts, before it serves traffic (the migration tool is a build choice).
7. Secrets reach the server from the private infrastructure repository (Ansible decrypts the SOPS files) when they change, not on each release.

*Agent's call:* environments are the founder's laptop and live only; no staging copy (the founder chose approval over staging). The live address is `vestagraph.com` (already registered at Cloudflare, IN-06); `vestagraph.co.uk` redirects to it.

*Agent's call:* the build plan starts with a minimal placeholder app (a health page only) to prove the release, the rollback and the log check (launch blockers 3 and 4) before the app shell (#86) exists. Building starts once groups B to D are decided (0046: decisions first).

### Secrets (IN-04)
- Vestagraph's live secrets (database connection string, Better Auth secret and keys, later the AI and email keys) are stored encrypted with SOPS and age in the private infrastructure repository and decrypted only at deploy.
- No plain copies or `.env` backups are left in working folders.
- The Vestagraph repository commits only `.env.example` with placeholder names. *(Correction, 20 Nov 2026, build plan: secrets reach the containers as files, so the repository commits `deploy/secrets.example`, names only.)*
- Provider tokens used by the deploy job are scoped to the job and the `production` environment.

### Infrastructure as code (IN-03)
- *Agent's call:* the Cloudflare records, the server's firewall and the Caddy route are added in the private infrastructure repository's existing Terraform and Ansible. The Neon project is created in Terraform if a maintained provider fits, otherwise by hand with its settings written in the infrastructure repository. Bicep stays only for any Azure parts (0022).

### Logs and IP addresses (0014, 0046)
- Cloudflare proxies Vestagraph's address; Caddy's Vestagraph route writes no access log, or one with the client address and the URL removed. Searched postcodes travel in the URL fragment or the request body, never the query string (0046).
- The containers' own logs carry no IP address, postcode or chat text. Chat traces are group D's (0058).
- Cloudflare sees visitors' IP addresses, as it already may for maps (0059), and keeps its own request analytics for about 31 days; the founder accepted this (decision 10 above): Cloudflare is a named processor, and we never export or copy its logs. Group C names it in the privacy notice for the site's traffic as well. Searched postcodes never reach Cloudflare's logs because they are not in the URL path or query string.

### Rate limiting
- *Agent's call:* a per-visitor limit at Cloudflare's edge or in Caddy for the public area endpoints, plus the 15-messages-a-day account cap kept in the database (0058). The numbers are set in the build plan.

### Monitoring and spending (0022 problem e, IN-05 part 1)
- *Agent's call:* an uptime check every few minutes on `/healthz` (a scheduled GitHub Actions job, as the server already uses for another app), alerting the founder by email; Neon's and Hetzner's built-in graphs; billing alerts at Neon (its spending notifications, about $25 a month for Vestagraph) and Hetzner.
- The full monthly cap in pounds is set after groups C and D (IN-05 part 2).

### The API contract (BE-02)
- *Agent's call:* FastAPI's generated OpenAPI description is the contract; it is committed, and the frontend's types are generated from it. Breaking changes need a version step. The observability foundation (0025) for the API is OpenTelemetry in the code; where traces are sent is group D's choice.

### Work in the private infrastructure repository (before Vestagraph deploys)
Agents do this work under that repository's own `AGENTS.md` and may merge after a proper review and its tests, with nothing broken (founder's standing approval, decision 11 above). Nothing from it is copied into this repository.
1. Retire the app being wound down: delete its data with no notice (decision 12), after one last confirmation from the founder, and remove its containers and records.
2. Move Vestagraph's secrets to SOPS with age (and, where it helps, the other apps).
3. Check that the infrastructure documentation holds no real IP addresses.
4. Add the Vestagraph Caddy route without IP logging, the proxied Cloudflare records and the deploy user's narrow permissions.
5. Check the memory and disk use after the retirement; resize only if needed.

## Launch blockers group A adds
1. The app being wound down is retired and its data deleted.
2. Vestagraph's secrets are encrypted (SOPS with age); no plain copies remain.
3. Watchtower follows only the approved `production` tag for Vestagraph, and the approved release works, including a rollback.
4. No IP address or searched postcode appears in Caddy's or the app's logs, and no postcode in Cloudflare's (checked with a test search).
5. Cloudflare proxies Vestagraph's address.
6. The infrastructure documentation holds no real IP addresses.
7. A Neon restore to an earlier moment has been tried once, on a branch, and written up.
8. The Neon spending alert (or its stand-in) and the uptime check are live.

## For group C (privacy), from this design
- Name Neon (database, Frankfurt), Hetzner (server, Germany) and Cloudflare (traffic proxy) as processors; confirm each one's data processing terms, company location and any transfers outside the UK and EEA.
- Retention: Neon's 7-day history holds deleted data for up to 7 days; 0058's deletions are only complete after that.

## Left to the builder
- The container layout and Compose file, the migration tool, the health check details, the rate-limit numbers, how Better Auth and the API connect to Neon (pooled connection or direct), handling the first slow request after Neon sleeps, and the exact Terraform or manual steps, within the decisions above.
