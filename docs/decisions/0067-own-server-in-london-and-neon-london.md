# 0067: Vestagraph moves to its own server in London when stock allows, and Neon goes to London

**ID:** IN-08 (amends register lines IN-02 and DA-03)  
**Status:** Accepted (founder, 23 Nov 2026, prompt windows: "Yes, plan it (Recommended)", then "Wait, with an automatic stock watch (Recommended)")  
**Date:** 2026-11-23  
**Stage:** 5b (group A)  
**Amends (no older text is rewritten):** [0060](0060-pilot-foundation-hosting-and-database.md): the app will no longer run on the founder's existing server in Germany once the London server can be ordered, and the Neon project is created in London, not Frankfurt. Everything else in 0060 stands (Neon on the Launch plan, release approval, SOPS and age, the Cloudflare proxy and lock, the budget alerts, the private infrastructure repository).  
**Evidence:** the founder's private infrastructure repository (`wiki/log.md`, 22 and 23 Nov 2026) for the server's state and the console checks; the provider pages cited below. This record is the design: there is no separate spec file.

## Context
0060 put the app on the founder's existing server, a Hetzner CX23 (2 vCPU, 4 GB) in Germany. On 22 Nov 2026 a resize to CX33 (4 vCPU, 8 GB) failed for lack of capacity and switched every site off for about 4 minutes. On 23 Nov 2026 the retry found the console refusing CX33 and CX43 outright ("Not available. Please choose another location or type."), so nothing was switched off.

The founder then said the founder's other projects will soon share that server, and asked to "start plan for vestgarp on its own server" [sic]. The agent checked, in the founder's Hetzner console (23 Nov 2026), what a new server would cost: every Cost-Optimized type (CX, and Arm CAX: "Temporarily not available") could not be ordered in any location, so the cheapest new 4 GB server was a CPX22 in Germany at $28.31 a month including VAT and the IPv4 address. The founder: "this is too expensive", and asked for other options, locations and providers. Hetzner has no UK location.

The Neon project does not exist yet (group A plan, Task 10). Founder, 23 Nov 2026: "Database has not been created yet, we are still in planning phase". Neon offers AWS Europe (London), `aws-eu-west-2`, with Postgres, and a project's region cannot be changed after it is created ([Neon regions](https://neon.com/docs/introduction/regions), page updated 18 Nov 2026, read 23 Nov 2026).

## Options (read 23 Nov 2026 on each provider's own pages; prices per month)
- **OVHcloud VPS-2, London (chosen):** 4 vCores, 8 GB, 75 GB NVMe, 1 Gbps, unlimited traffic, daily backup of the previous 24 hours included; £7.40 excluding VAT with no commitment (about £8.88 including VAT), £7.03 on 6 months, £6.29 on 12 months, no setup fee ([UK VPS page](https://www.ovhcloud.com/en-gb/vps/); OVH's public order catalogue for the GB store, plan `vps-2027-model2`, one price for every location). The smaller VPS-1 (2 vCores, 4 GB, 40 GB) is £3.90 excluding VAT.
- **DigitalOcean, London:** 2 vCPU, 4 GB, 80 GB for $24; a managed cloud firewall and a mature Terraform provider, so the easiest to run ([pricing page](https://www.digitalocean.com/pricing/droplets)).
- **Netcup VPS 500, Germany:** 2 vCPU, 4 GB, 64 GB; €9.50 including VAT on a 12-month contract, €7.03 on 24 months ([VPS page](https://www.netcup.com/en/server/vps)).
- **Hetzner CPX22, Germany:** $28.31 including VAT and IPv4; the cheaper CX23 (about $7.79) when it can be ordered again, with no date.
- **Contabo, UK or Germany:** cheapest plan 4 vCPU, 8 GB; the UK surcharge and setup fee could not be read (unverified).
- **Oracle Cloud Always Free (Arm):** £0, but Oracle "may reclaim" instances that stay mostly idle for 7 days, and the home region is fixed for good: not dependable for a public pilot.
- **Stay on the one Hetzner server:** free for now, but the other projects are coming to it, and it cannot grow.

What OVH states about the VPS range ([VPS special conditions](https://contract.eu.ovhapis.com/1.0/pdf/Conditions_Particulieres_VPS-gb.pdf), [UK GDPR data protection agreement](https://contract.eu.ovhapis.com/1.0/pdf/OVH_Data_Protection_Agreement-gb.pdf), [Edge Network Firewall guide](https://docs.ovhcloud.com/en/guides/bare-metal-cloud/dedicated-servers/firewall-network), [Terraform `ovh_vps`](https://registry.terraform.io/providers/ovh/ovh/latest/docs/resources/vps)):
- "suitable for both pre-production and production"; host resources are shared between customers' servers (like Hetzner's CX); 99.9% availability for these ranges, with small service credits that start from an incident ticket.
- Docker runs on standard VPS (not "Local Zone" VPS); anti-DDoS is included; IPv6 is included.
- The Edge Network Firewall is IPv4 only and holds at most 20 rules per address, so the Cloudflare-only lock lives in the server's own firewall (as it already does in Caddy on the Hetzner server).
- An upgrade is one click without reinstalling, but only "provided that the resources are available"; a downgrade means a new server.
- A UK GDPR Article 28 agreement with OVH Limited; OVH does not move the data out of the chosen datacentre without the customer's approval.
- Terraform can order, reinstall and import a VPS; ordering needs a default payment method on the account.

## Decision
The founder's words, 23 Nov 2026 (prompt windows and typed answers):
1. **Location:** "check availability of a new server, do they have uk locations, if not stick with germany, then lets move now". Hetzner has no UK location; the founder then asked "Should we move to digital ocean as it is in london or hetzner in germany", and, after learning Neon has London, chose the UK for both.
2. **Provider:** after asking "what are the pros and cons of OVHcloud vs Digital ocean?" and "confirm ovh is a good fit, would work for us and the cost does not mean lower quality": **OVHcloud**.
3. **Size:** after asking "how much is ovh 8gb?": the 8 GB **VPS-2**, because "AT THE END OF THE DAY OTHER PROJECTS MIGHT JOIN VESTGRAPH" [sic], and the agent advised that an upgrade later depends on spare capacity, as the Hetzner resize showed.
4. **Two servers:** after asking "are we gogin to be able to manage tow servers successfully?" [sic] and whether one of the founder's other projects should move to the new server too: the agent advised keeping the other projects on the Hetzner server for now, and the founder approved the plan that said so (point 5).
5. **The whole plan:** "Yes, plan it (Recommended)", for: an OVHcloud VPS-2 in London becomes Vestagraph's server now, with room for other projects to join later; Neon in London; the founder's other projects stay on Hetzner for now.
6. **Out of stock:** when the founder came to order, OVH's order page said "No location available at the moment", and OVH's public order rules (read 23 Nov 2026) showed no Linux VPS in stock in any European datacentre, in any size (VPS-2 and VPS-3 in London offered Windows only). After asking "what are the advantages of digital ocean": "Wait, with an automatic stock watch (Recommended)" (over DigitalOcean London at about £19 a month, Hetzner CPX22 at $28.31 and Netcup on a 12-month contract).

So:
- **Where the app runs (IN-02):** the Next.js site, the FastAPI API and the background jobs run as containers on an **OVHcloud VPS-2 in London** once it can be ordered with Linux. **Until then the app stays on the Hetzner server in Germany**, and a stock watch in the private infrastructure repository (every 6 hours, no secrets) opens an issue, which emails the founder, when the VPS-2 is in stock in London. On the new server the app runs behind Caddy and the Cloudflare proxy; the server is paid monthly with no commitment at first. Other projects may join this server later, each one checked for memory first. The Hetzner server keeps the founder's other projects.
- **Database (DA-03):** Neon, **AWS Europe (London), `aws-eu-west-2`**, Launch plan, created at the group A plan's Task 10 on the founder's account. Neon is created in London even while the app is still in Germany: the database does not exist yet, its region cannot change later, and the extra distance (about 15 ms a round trip, an estimate) does not matter before real users arrive. Agent's call: check at that step that PostGIS and the Launch plan's prices are the same in London, and stop and ask if not.
- **The Cloudflare-only lock** sits in the server's own firewall (nftables or ufw: the build plan picks one) and in Caddy; OVH's edge firewall may add the IPv4 rules if it accepts address ranges (unverified).
- **The group A tasks do not wait for stock:** Tasks 10 to 12 (Neon, the restore drill, the release, rollback and log checks) run on the Hetzner server now, and are repeated on the new server when it arrives.
- **The placeholder** moves to the new server first and proves the release, rollback, log check and lock there; then the Hetzner copy of the placeholder, its Caddy block, Watchtower and secrets are removed in the same piece of work.
- **The server's address and account details** stay in the private infrastructure repository, never here (0060).

## Consequences
- **Running cost:** nothing new until the server is ordered; then about £8.88 a month including VAT for the server (about £7.55 on a 12-month commitment, to consider once the pilot settles). The Hetzner server's cost is unchanged. Neon's estimate in 0060 is unchanged, subject to the Task 10 check.
- **Merging:** this record adds a running cost, so the founder merges its pull request (AGENTS.md, "Founder merges these").
- **Founder to-dos:** create the OVHcloud account (UK store) with a payment method and accept the data processing agreement; the agent checks the checkout total against the figures above before the founder pays. Create the Neon project in London at Task 10.
- **For group C (privacy):** the Privacy notice and the DPIA name the processors that actually host the app when the pilot opens: OVHcloud (OVH Limited, UK), Neon (AWS London) and Cloudflare if the London server is running by then; Hetzner (Germany) instead of OVHcloud if it is not. The proposed sentence in `docs/specs/pilot/public-pages.feature` now says the Neon database is in London and goes into the founder's copy review.
- **Two servers to look after:** the infrastructure repository runs the same Ansible plays and checks against both; the OVH server gets its own Terraform folder and state, so a change to one cannot touch the other.
- **Revisit if** the OVH server's shared CPU proves too slow, OVH cannot upgrade it when needed, group C finds a problem with OVH's terms, or Hetzner's cheaper types return and the founder wants one provider again.

**Note, 23 Nov 2026 ([0068](0068-shared-server-on-digitalocean-london.md), accepted by the founder):** the London server is a DigitalOcean Droplet (4 GB, $24 a month plus VAT), not an OVHcloud VPS-2, created by the founder the same day and shared with one of the founder's other projects; the OVH-specific parts of this record (the cost, the OVH account to-do, the Terraform folder, the processor named for group C, the revisit conditions, the server's own firewall as the only network lock, and the stock watch, removed in the Phase 22 work) are replaced by 0068, and one of the founder's other projects now shares the London server. Neon in London, the placeholder moving first, the Caddy lock and the repeated checks stand.
