# Energy certificate by certificate number (pilot): design

**Date:** 18 Nov 2026. **Status:** approved by the founder, 18 Nov 2026 (prompt window, "Approve (Recommended)"). **Decisions:** DA-09 (13 Nov 2026, "Certificate number (Recommended)"); 18 Nov 2026 "Draw the EPC now; sale later (Recommended)" (status item 5b). **Stage:** boards and specification before the pilot gate (0052); the build is stage 5b.

## Intent and why
The pilot shows an area. The design benchmark re-run ([2026-11-16](../../reviews/2026-11-16-design-benchmark.md)) still rates it worse than the competitor on facts about the home itself, and the competitor shows "the energy certificate with upgrade costs" ([comparison](../../reviews/2026-11-13-competitor-report-comparison.md)). A visitor who has a home in mind can find its certificate number on GOV.UK's free [Find an energy certificate](https://www.gov.uk/find-energy-certificate) service, type it in, and see that certificate's open facts in Vestagraph's own clear format, with sources, beside the area facts. Success: a visitor understands the home's rating, its estimated running costs and the suggested improvements, knows how old the certificate is and what it cannot tell them, and nothing about the home's address is shown, stored or logged.

## Goals
- One page, **Check an energy certificate**, that looks up one domestic certificate by its 20-digit number and shows its open (OGL v3.0) facts.
- Every figure is **quoted** from the certificate as an input (AGENTS rule 2): ratings, scores, the certificate's own running-cost estimates, indicative improvement costs and typical savings.
- Clear states for every way a lookup can go wrong, and for facts an older certificate does not hold.
- Canvas boards (light and dark, phone and desktop, plus the printout) and a specification file before the pilot gate.

## Non-goals (pilot)
- Finding a certificate by address or postcode (needs the restricted address data; DA-06, DA-09).
- Saving a certificate to an account, or the signed-in chat looking one up (founder, 18 Nov 2026: "Not in the pilot (Recommended)"). The page behaves the same signed in or not and stores nothing.
- Any figure we calculate: no total yearly cost, no "you would save £X", no comparison with an average home or the area ("Full, plus our comparisons" was not chosen). Comparisons can come later through the cost engine.
- Non-domestic certificates (CEPC) and display energy certificates (DEC).
- A valuation or past sale for the home (BE-34, stage 6).

## Anti-goals (a failure even if it works)
- Showing, storing or logging the address, postcode or UPRN-derived address text, or implying the certificate belongs to the postcode the visitor searched before.
- The certificate number in a URL, a log line, an error report or analytics (decision 0014).
- Calling a home, rating or improvement good, bad, safe or recommended in our own voice (rule 4); rewording the register's ratings into a score of our own.
- A missing fact shown as zero, blank or a favourable value (rule 7).
- Presenting the certificate's cost estimates as the household's bills.

## Constraints (checked 18 Nov 2026)
- **Source:** the MHCLG energy certificate register, `GET /api/certificate?certificate_number=<20 digits>` ([fetch certificate data](https://get-energy-performance-data.communities.gov.uk/api-technical-documentation/fetch-certificate-data)); a bearer token for Vestagraph through GOV.UK One Login; limit 6,000 requests per 5 minutes per IP address and token, HTTP 429 above it ([technical documentation](https://get-energy-performance-data.communities.gov.uk/api-technical-documentation)).
- **Licence:** every field except the address and postcode fields is OGL v3.0; address data may be used "solely for specific purposes related to the energy performance of buildings" ([licensing restrictions](https://get-energy-performance-data.communities.gov.uk/guidance/licensing-restrictions)). So the adapter drops `address_line_*`, `post_town` and `postcode` on receipt and they never leave it; matching the certificate to a searched postcode is not done.
- **Personal data:** address-level certificate data is personal data ([data protection requirements](https://get-energy-performance-data.communities.gov.uk/guidance/data-protection-requirements)); the certificate number identifies one home, so it is treated like a postcode (0014): never in a URL or log, and the privacy notice (SE-02) names the processing.
- **Shape varies:** the response "will vary depending on the type of certificate and the schema" (RdSAP 17.0 to 21.0.1, SAP 12.0 to 19.2.0; [JSON samples](https://github.com/communitiesuk/epb-data-warehouse/tree/main/spec/fixtures/json_samples)). Several fields are codes (for example `property_type`, `built_form`, `improvement_details.improvement_number`) that need official code-to-words tables.
- **Validity:** "An EPC is valid for 10 years"; ratings run "from A (best) to G (worst)" ([GOV.UK](https://www.gov.uk/buy-sell-your-home/energy-performance-certificates)). Quoting the register's own "best" and "worst" scale ends is the source's wording, not ours.
- **Nations:** the register covers England and Wales; the pilot is England only (rule 6). A certificate whose `country_code` is not England shows "not yet covered" for that nation.
- **Outside services** go through an adapter labelled Live, Cached, Fallback or Unavailable (0029); live-service tests stay out of the merge gate.

## Approaches
- **Chosen: live lookup, store nothing** (founder, 18 Nov 2026: "Yes, live lookup, store nothing (Recommended)"). One register call per search through an adapter; the address fields are dropped at once; nothing is kept after the response. Code tables are small versioned data files, each with its official source. For the boards and specifications now, a synthetic sample certificate with its own JSON Schema joins the fixtures, and every figure on the boards is quoted from it.
- **Rejected: cache certificates in our database.** Keeps personal data we do not need and adds retention rules.
- **Rejected: bulk download of the register.** The address licence forbids general use, and it is a large store of personal data.

## What the founder decided (18 Nov 2026, prompt windows)
1. **Where:** "Own page, linked from results (Recommended)": its own page, reached from a new "Check this" energy row on the area result and from the landing page; not a box inside the area result, because that would imply the certificate belongs to the searched postcode.
2. **What it shows:** "Full certificate facts (Recommended)": ratings now and potential; the certificate's own running-cost estimates; each part of the home with its description and star ratings; suggested improvements with indicative cost and typical saving; all quoted, labelled as estimates and not bills, with the date and status.
3. **Signed in:** "Not in the pilot (Recommended)".
4. **Approach:** as above.

## The page (proposal; the boards settle the look)
```
Check an energy certificate                         [Sample data]
Certificate number  [____-____-____-____-____]  (Search)
Find yours on GOV.UK ↗
Flat · 55 m² · inspected 4 Apr 2025 · valid until Apr 2035
Energy rating   E 50  →  C 72 potential          [EPC register ↗]
Running costs (the certificate's estimates, not your bills)
  Heating   £366 a year → £250   Hot water …   Lighting …
The home, part by part
  Walls  Cavity wall, as built, no insulation   ★★☆☆☆   …
Suggested improvements (the certificate's, in its order)
  1  Low energy lighting   £220 – £250   typical saving £139 a year
How we got this · About the data
```
(Figures above are illustrative; the boards quote the synthetic sample.)

## States
Each needs a board and a scenario:
1. Empty page (before a search), with the GOV.UK link and a one-line note that the number is on the certificate and on Find an energy certificate.
2. Number wrongly formatted (not 20 digits after removing spaces and dashes): an inline error before any lookup.
3. Checking (skeleton, no spinner, FE-64).
4. Found, current certificate.
5. Found, older than 10 years: shown, with "This certificate is more than 10 years old" and its date.
6. Found, replaced by a newer certificate, or cancelled, as the register marks it (`status`): shown with that status, and for a replaced one a pointer to look for the newer certificate on GOV.UK.
7. A non-domestic certificate or display energy certificate number: "This page covers home energy certificates only."
8. A certificate for Wales: "Wales is not yet covered."
9. Not found.
10. Register unavailable or over its limit: "Not known right now", with the GOV.UK link (rule 7).
11. A fact missing from an older certificate: "Not on this certificate" in that row, never blank or zero.
Plus the printout (like the area printout, ending with its sources page) and dark versions of every screen board.

## What is left to the builder (the agent's calls, open to the founder)
- **Address of the page:** `/energy-certificate`, with the number never in the path, query string or `#` fragment; it lives only in the page's state and the request body. So the result cannot be bookmarked or shared as a link; the printout is the way to keep it. *Agent's call.*
- **Entry points:** the "Check this" energy row (added by the plan, below) opens this page (the GOV.UK link moves onto the page); the landing gets a link under the search box or in the footer (the boards decide). *Agent's call.*
- **The sample:** one synthetic certificate shaped like RdSAP 21.0.1 (the newest domestic schema in the samples), plus a second, older-schema sample with missing facts for state 11, and samples for states 5 to 8. No real certificate number or address is used; the sample numbers are obviously synthetic.
- **Code tables:** property type, built form, tenure, star ratings and improvement descriptions, each from an official source cited in the data file (the SAP and RdSAP specifications or the register's own published lookups); a code with no table entry shows "Not on this certificate", never the raw code.
- **Data contract (from the builder check):** the sample fixture is Vestagraph's normalised contract, the shape the page receives after the adapter: whole pence for money (0036), a source on every value, and an explicit missing status for "Not on this certificate" (rule 7), following `packages/fixtures/README.md`; the boards quote it. A raw-register-shaped sample (with obviously fake address fields, to test that the adapter drops them) is a stage 5b build task, not part of the boards. *Agent's call.*
- **Validity is calculated (from the builder check):** "valid until" and "more than 10 years old" are calculated outputs (rule 2), so they come from a small tested function with independently worked cases (exactly 10 years, a 29 February date) and a cited rule line ("valid for 10 years", GOV.UK, with its effective date), written to a generated file the boards quote. Which date the 10 years run from (the certificate's registration or inspection date) is confirmed against the official source before the function is written; the boards' "today" is the fixtures' snapshot date. *Agent's call.*
- **The "Check this" energy row (from the builder check):** no specification or `pilot-topics.json` entry has it yet (only the pilot design's list of official checks, line 138). The plan adds it to the registry, `area-topics.feature`'s Check this scenarios and the printout's list, opening this page; its wording joins the copy review. *Agent's call.*
- **Code tables (from the builder check):** they are real official data, so they live in their own versioned reference folder with source URL and effective date (rule 3), not in `packages/fixtures/data/` (synthetic only). Before the gate they hold only the codes the samples use, marked partial; the full tables for every schema in scope are a 5b build task. They are words for codes, not tax, legal, tenancy or privacy rules, so they are not on the founder-merge list. *Agent's call.*
- **The public MCP server** gets no certificate tool: 0051 limits it to area data. *Agent's call.*
- **Wording:** all page wording is proposed and goes to the founder's copy review before the gate.
- **Reused patterns:** source stamp (FE-33), How we got this (FE-34), About the data (one entry for the register), display settings, the feedback kit (FE-64), distances not used.

## Records this changes
- DA-09 gains a dated note pointing here; the pilot design (`2026-11-13-pilot-area-ai-design.md`, line 46) already lists the exception.
- The site plan (`.design/prototype/INFORMATION_ARCHITECTURE.md`) gains the page and its entry points.
- `docs/references/data-sources.md` (EPC register) gains the endpoint, rate limit and schema notes above.
- `docs/planning/status.md` item 5b points to this design and its plan.
