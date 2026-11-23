# 0068: Vestagraph's server is a DigitalOcean Droplet in London, shared with one other project

**ID:** IN-09 (amends register lines IN-02 and IN-08)  
**Status:** Accepted (founder, 23 Nov 2026, prompt window: "DigitalOcean London now"; the server was created by the founder the same day)  
**Date:** 2026-11-23  
**Stage:** 5b (group A)  
**Amends (no older text is rewritten):** [0067](0067-own-server-in-london-and-neon-london.md): the London server is a DigitalOcean Droplet, not an OVHcloud VPS-2, and it is shared with one of the founder's other projects. 0067's other choices stand: Neon in London, the Hetzner server keeping the founder's remaining projects, the move of the placeholder first. Neon's timing is unchanged (the start of the group B build, `docs/planning/status.md`).  
**Evidence:** DigitalOcean's own pages, cited below (read 23 Nov 2026); memory measured on the Hetzner server the same day; the founder's private infrastructure repository for the server's details.

## Context
0067 chose an OVHcloud VPS-2 in London, but on 23 Nov 2026 OVH had no Linux VPS in stock in any European datacentre, and the founder chose to wait with a stock watch. Later the same day the founder wrote: "I am thinking we move vestagraph and [one of the founder's other projects] to digital ocean , will 4gb be enough for tehse two and [the two remaining projects] stay on hetzner, investigate" [sic; project names replaced, because this repository does not name the founder's other projects].

**Memory for the two apps on one 4 GB server** (the agent's estimate, 23 Nov 2026):

| Part | Memory | Source |
|---|---|---|
| Operating system and Docker | about 0.4 GB | measured on the Hetzner server |
| Caddy and two Watchtower instances | about 0.1 GB | measured (Caddy 35 MB, Watchtower 18 to 28 MB each) |
| Vestagraph's Next.js site | 0.15 to 0.3 GB | a Next.js site on the Hetzner server measured 149 MB |
| Vestagraph's API (FastAPI, LangGraph) | 0.2 to 0.35 GB | estimate |
| Dagster (group B) | 0.6 to 0.8 GB | the 20 Nov 2026 spike ([0061](0061-pilot-data-pipeline-postcodes-and-walking-times.md)) |
| The other project's site and API | 0.4 to 0.7 GB | estimate (a Next.js site and a FastAPI API) |
| **Total** | **about 1.9 to 2.7 GB of 4 GB** | |

This holds only if both apps keep their databases in Neon, not on the server: a database and a vector store on the server would add about 0.3 to 0.8 GB (estimate).

**DigitalOcean, from its own pages (read 23 Nov 2026):**
- Basic Droplet, Regular CPU, 2 vCPU, 4 GB, 80 GB SSD, 4 TB transfer: **$24 a month**; UK VAT of 20% is added, so **$28.80** ([Droplet pricing](https://www.digitalocean.com/pricing/droplets), [UK tax](https://docs.digitalocean.com/platform/billing/taxes/gbr/)). The 8 GB size is $48.
- London (LON1) offers Basic Droplets with no capacity warning ([regional availability](https://docs.digitalocean.com/platform/regional-availability/)).
- Cloud Firewalls are free, allow 50 rules per firewall and 1,000 sources per rule, and take IPv4 and IPv6 ranges, so Cloudflare's ranges on TCP 443 fit in one rule ([limits](https://docs.digitalocean.com/products/networking/firewalls/details/limits/)).
- 99.99% monthly uptime per Droplet, with service credits ([SLA](https://www.digitalocean.com/sla/cpu-droplets)).
- A resize of CPU and memory only keeps the disk, can be undone, and needs the Droplet powered off ([resize](https://docs.digitalocean.com/products/droplets/how-to/resize/)).
- A data processing agreement with EU Standard Contractual Clauses and a UK addendum, relying first on the Data Privacy Framework with its UK Extension ([DPA](https://www.digitalocean.com/legal/data-processing-agreement)). It does not promise that data stays in the chosen region.
- The free metrics agent supports memory alerts ([monitoring](https://docs.digitalocean.com/products/monitoring/)).

## Options
- **DigitalOcean London now (chosen):** $28.80 a month including VAT; managed firewall for IPv4 and IPv6, 99.99% uptime commitment, mature Terraform provider, the UK.
- **Wait for OVH, with a deadline (the agent's recommendation):** £8.88 a month for 8 GB once in stock; free until then.
- **Hetzner CPX22, Germany:** $28.31 a month including VAT and IPv4; one provider for everything.

The agent pointed out that DigitalOcean costs about the same as the Hetzner CPX22 the founder had called "too expensive" earlier the same day, and about two and a half times the OVH price (£8.88, about $11 to $12, for twice the memory).

## Decision
**DigitalOcean London now** (founder, 23 Nov 2026, prompt window, over "Wait for OVH, with a deadline (Recommended)" and "Hetzner CPX22 Germany now").

So:
- **The server:** a Basic Regular Droplet, 2 vCPU, 4 GB, 80 GB, in London (LON1), Ubuntu 24.04 LTS, IPv4 and IPv6, the free metrics agent, no paid backups (both apps' data lives in Neon and the code and images on GitHub), key-only SSH. The founder created it on 23 Nov 2026; its address and account details stay in the private infrastructure repository.
- **Shared:** Vestagraph and one of the founder's other projects run on it. Each keeps its database in its own Neon project, not on the server. The Hetzner server keeps the founder's remaining projects.
- **The setup** is planned in the private infrastructure repository: a Cloud Firewall managed by Terraform (TCP 443 from Cloudflare's ranges only, the WireGuard port, SSH closed once the VPN works), a memory alert, and the existing Ansible plays. The Terraform token is scoped to droplets (read), firewalls, monitoring and tags, expires after 90 days, and is held only as a GitHub secret.
- **Two layers in front of the app:** the Cloud Firewall lets only Cloudflare reach TCP 443, and the Caddy origin lock from 0060 stays as the second layer; a host firewall on the Droplet is optional.
- **The OVH stock watch** in the infrastructure repository is removed in the Phase 22 work.

## Consequences
- **Running cost:** $28.80 a month including VAT from 23 Nov 2026, on top of the Hetzner server. Daily backups would add 30% if they are ever wanted.
- **Merging:** this record adds a running cost, so the founder merges its pull request (AGENTS.md, "Founder merges these").
- **DigitalOcean's data processing agreement** is an addendum to its terms of service, so it needed no separate signature (the agent's reading of the [DPA page](https://www.digitalocean.com/legal/data-processing-agreement); group C confirms it).
- **Founder to-dos:** renew the DigitalOcean token before it expires (90 days from 23 Nov 2026, so by 21 Feb 2027).
- **For group C (privacy):** DigitalOcean replaces OVHcloud as the server's processor once Vestagraph runs there. DigitalOcean is a US company: the DPIA and the Privacy notice cover the transfer basis (the Data Privacy Framework's UK Extension, then the UK addendum) and that the DPA does not promise to keep data in London.
- **Revisit if** memory stays above about 80% (resize to 8 GB, $48 plus VAT), the other project needs more than its share, or group C finds a problem with the transfer basis.
