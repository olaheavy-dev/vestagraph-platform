# 0057: Usage logging for ChatGPT calls to the area tools

**ID:** SE-05  
**Status:** Proposed (founder's choices made 15 Nov 2026 in prompt windows; the device hint and language are defaults for the founder to confirm; the legitimate interests assessment and the DPIA screening are still to do)  
**Date:** 2026-11-15  
**Stage:** 5b (before the public MCP server launches)  
**Would amend, once accepted (no older text is rewritten):** [0014](0014-privacy-and-data-protection.md) (SE-02)'s starting position that an anonymous visitor's use is kept "nothing linked to the person", with only anonymous counts: for tool calls that arrive from ChatGPT, a pseudonymous record is kept for 90 days, as below. 0014's other rules, and the rule in [0051](0051-ai-in-the-public-pilot.md) and [0056](0056-no-on-page-chat-in-the-pilot.md) that no postcode, place name or tool argument is ever logged, stand unchanged.

## Context
The pilot offers a public, read-only MCP server with the area and council tools, which visitors add to their own ChatGPT or Claude ([0051](0051-ai-in-the-public-pilot.md) points 1 and 4; [0056](0056-no-on-page-chat-in-the-pilot.md)). MCP, the Model Context Protocol, is the standard way an AI app connects to an outside service ([modelcontextprotocol.io](https://modelcontextprotocol.io)). The server's rate limits are a global cap and a per-host cap (0051 point 3).

**What ChatGPT sends with each tool call.** Besides the tool's arguments, ChatGPT adds fields in the call's `_meta` part. OpenAI's reference page ([developers.openai.com/plugins/reference](https://developers.openai.com/plugins/reference), read 15 Nov 2026) lists:

| Field | OpenAI's description |
|---|---|
| `openai/subject` | "Anonymized user id sent to MCP servers for the purposes of rate limiting and identification" |
| `openai/session` | anonymised conversation id, for correlating tool calls in the same ChatGPT conversation |
| `openai/organization` | anonymised organisation id, "when available" |
| `openai/userLocation` | "Coarse location hint (city, region, country, timezone, longitude, latitude)" |
| `openai/userAgent` | "Optional, best-effort user agent hint" (a description of the device and app) |
| `openai/locale` | the requested language and region, for example `en-GB` |

The same page says the device hint and the location "are hints only; servers should never rely on them for authorization decisions and must tolerate their absence." So the server must work the same when they are missing, and a missing value is recorded as missing, never guessed (rule 7).

**Claude.** Anthropic's documentation does not say what Claude sends with a tool call beyond its arguments (research note, 15 Nov 2026: "not stated").

**Why this needs a record.** 0014 keeps nothing about an anonymous visitor's use except anonymous counts. Keeping a user ID, a conversation ID and a city with each call is a record about a person (see "Is this personal data?" below), so it changes 0014's starting position and needs a lawful basis, privacy information and a retention rule before launch.

## Options
### Option A: Drop the extra fields unread, never store them (recommended by the agent)
The server ignores everything in `_meta`; usage is measured only with 0014's anonymous counts (for example calls per day per tool). No personal data from ChatGPT is kept, so no legitimate interests assessment, no deletion job and nothing new in the privacy notice beyond saying the fields are dropped. The cost: no count of distinct users, returning users or conversations, and no picture of where users are.

### Option B: Use the user ID for rate limits only, held in memory
`openai/subject` is used as a per-user rate-limit key (OpenAI offers it for this), kept only in memory or as an expiring anonymised key, as 0014 already allows for IP addresses; nothing is written to a log. Fairer limits per person, still no stored record, but no usage statistics either.

### Option C: Log the fields for usage statistics, with limits (the founder's choice)
Keep the IDs and a coarse location with each call for a fixed period to learn how the tools are used, drop the precise fields on arrival, then reduce the record to anonymous totals.

## Recommendation
The agent recommended Option A ("Drop unread, never store"): it keeps 0014's promise and adds no launch work. It offered Option C with the limits below as the alternative.

## Decision
**Option C**, the founder's choice. Founder's answers, 15 Nov 2026, in prompt windows (quoted as chosen):
1. **Whether to keep the fields:** "Log them for usage stats". The agent's recommended option, "Drop unread, never store", was offered and declined.
2. **Location:** "City as well": keep the city, region and country; drop the time zone, latitude and longitude on arrival.
3. **How long:** "90 days (Recommended)", then only anonymous totals (for example calls per week per region).
4. **Which IDs:** "All three IDs": keep the user, conversation and organisation IDs.
5. **Not yet decided:** the device hint (`openai/userAgent`) and the language (`openai/locale`). **Default, founder to confirm:** drop the device hint on arrival; keep the language only as an anonymous total (calls per day per language), never in the per-call record. This was the agent's earlier recommended option.

### What is kept and what is dropped on arrival
"On arrival" means the server removes the field before anything is written to any log, store, trace or error report, the same way 0014 treats raw IP addresses.

| Field | ChatGPT calls | Claude calls |
|---|---|---|
| Time of the call | Kept, to the hour (*default, founder to confirm*; enough for weekly totals) | Counted only |
| Tool name and outcome (answered, refused by a limit, error) | Kept | Counted only |
| Host (ChatGPT or Claude) | Kept | Counted only |
| `openai/subject` (user ID) | Kept | not sent (not documented) |
| `openai/session` (conversation ID) | Kept | not sent (not documented) |
| `openai/organization` (organisation ID) | Kept when sent; recorded as missing otherwise | not sent (not documented) |
| `openai/userLocation`: city, region, country | Kept when sent; recorded as missing otherwise | not sent (not documented) |
| `openai/userLocation`: time zone, latitude, longitude | **Dropped on arrival** | not sent (not documented) |
| `openai/userAgent` (device hint) | **Dropped on arrival** (*default, founder to confirm*) | not sent (not documented) |
| `openai/locale` (language) | Daily total per language only (*default, founder to confirm*) | not sent (not documented) |
| Tool arguments (postcode, place name, council, any typed text) | **Never logged or stored** (0051, 0056, 0014) | **Never logged or stored** |
| IP address | Never stored (0014: in memory only, for rate limiting) | Never stored |

For Claude, nothing beyond 0014's anonymous counts is kept, because Anthropic documents nothing extra. If Anthropic later documents identifying fields, a new decision chooses what to do with them; until then the server drops any undocumented field unread.

The per-call record never holds a tool argument, so it never shows which postcode or council a person asked about; the tool name says only what kind of question it was.

### Retention and deletion
- **Per-call records:** kept for **90 days** from the call, then deleted by a scheduled job that runs at least daily. The job and a test that proves a 91-day-old record is gone are launch blockers.
- **Before deletion:** records are reduced to **anonymous totals** with no ID of any kind, for example calls per week per region, per tool and per host, and distinct users per week as a single number. Totals keep region and country, not city (*default, founder to confirm*), so that a total cannot point at one person (0014: "Anonymous counts must not be detailed enough to identify a person"). The totals have no end date.
- **Backups and logs:** any backup or hosting log that might hold a per-call record follows the same 90-day limit, or the record is kept out of it.
- The ICO says the law sets no fixed period, so "it is up to you to justify this, based on your purposes for processing", and that where identification is no longer needed "you should anonymise the data" ([ICO: storage limitation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/), read 15 Nov 2026). The justification for 90 days goes in the LIA below.

### Is this personal data?
Yes, treated as personal data in our hands:
- The ICO says an online identifier is personal data where it "distinguishes one individual from another", "regardless of whether it is possible to link the 'online' identity with a 'real world' named individual", and lists location data among identifiers ([ICO: identifiers and related factors](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/personal-information-what-is-it/what-is-personal-data/what-are-identifiers-and-related-factors/), read 15 Nov 2026). `openai/subject` is a stable ID that tells one ChatGPT user from another.
- OpenAI calls the IDs "anonymized", but OpenAI can link them back to an account. The ICO says pseudonymised data "is personal data in the hands of someone who holds the additional information", and "may be anonymous information" for a recipient without it, depending on whether others could still identify people ([ICO: pseudonymisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/pseudonymisation/), read 15 Nov 2026). Because the record also holds a city, an organisation ID and times, and OpenAI describes the ID as being for "identification", this record treats it as personal data. Whether the ICO would see this exact combination as anonymous for us: not stated.

### Lawful basis: legitimate interests, with the assessment to complete
The proposed basis is **legitimate interests** (UK GDPR Article 6(1)(f)). Consent would need a prompt before the first call, which an MCP server has no screen for. The ICO's three-part test ([ICO: what is the legitimate interests basis?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/legitimate-interests/what-is-the-legitimate-interests-basis/), read 15 Nov 2026) is "Do you have a legitimate interest…?", "Is your use… necessary for that purpose?" and "Do the person's interests, rights or freedoms override the legitimate interest…?". The ICO says the law does not require a written legitimate interests assessment (LIA) "But you should do one anyway", "You should record your LIA and the outcome", and do it "before you start using the personal information" ([ICO: applying legitimate interests in practice](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/legitimate-interests/how-do-we-apply-legitimate-interests-in-practice/), read 15 Nov 2026).

**LIA outline (to complete and record before launch):**
1. **Purpose.** Learn how the free tools are used: how many distinct people and conversations use them, whether people come back, which tools help, and which parts of the country they reach, so the pilot can be improved, kept within budget and judged against its goals, and so a later commercial decision has evidence. The ICO gives analytics "to improve their products and services" as an example where legitimate interests may be considered ([ICO: when can we rely on legitimate interests?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/legitimate-interests/when-can-we-rely-on-legitimate-interests/), read 15 Nov 2026).
2. **Necessity.** The weakest part, to be answered honestly in the LIA: 0014's anonymous counts already answer "how many calls, which tools". Distinct and returning users and conversations need the IDs; reach by area needs the location. The organisation ID's need (telling work accounts from personal ones) is the hardest to justify and is an open point below. The ICO says data must be "limited to what is necessary" and "You must not collect personal data on the off-chance that it might be useful in the future" ([ICO: data minimisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/), read 15 Nov 2026).
3. **Balancing.** Against: people may not expect their ChatGPT to send a stranger an ID and their city, and the ICO says legitimate interests is unlikely to fit where data is used "in ways people are not aware of and don't expect" (same page as point 1). For: no names, no arguments (so no postcode or place asked about), coarse location only, 90 days, no sharing, no marketing, no profiling, no decisions about anyone, and the "Use in ChatGPT or Claude" page explains it before anyone connects.
4. **Right to object.** The ICO says people "have the right to object to processing on the basis of legitimate interests", and the right "must be explicitly brought to people's attention clearly and separately" ([ICO: what else do we need to consider?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/legitimate-interests/what-else-do-we-need-to-consider/); [ICO: what privacy information should we provide?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/the-right-to-be-informed/what-privacy-information-should-we-provide/), both read 15 Nov 2026). A ChatGPT user cannot see their own `openai/subject`, so we cannot find their records from a request. UK GDPR Article 11 says a controller that cannot identify the person need not collect more information just to do so, and must tell them where possible ([legislation.gov.uk: Article 11](https://www.legislation.gov.uk/eur/2016/679/article/11), read 15 Nov 2026). How we honour an objection is an open point.

### Privacy information this requires
The data comes from OpenAI, not from the person, so UK GDPR Article 14 applies ([legislation.gov.uk: Article 14](https://www.legislation.gov.uk/eur/2016/679/article/14), latest revised version, read 15 Nov 2026). The privacy notice (SE-02 parts 1 and 2) gains a section on the MCP server that says, in plain language:
- who we are and how to contact us;
- what we receive from ChatGPT with each tool call (the six fields above) and that Claude, as far as Anthropic documents, sends nothing extra;
- what we keep (the table above), what we drop on arrival, and that tool arguments are never kept;
- the purpose (usage statistics) and the lawful basis (legitimate interests), naming the interest;
- the source: OpenAI's ChatGPT, which sends these fields itself;
- that we keep per-call records for 90 days, then only anonymous totals;
- who else receives them (our hosting provider, as processor; nobody else), and where they are stored, with the safeguard if outside the UK (see "Transfers" below);
- the person's rights, with the right to object stated "clearly and separately", what we can and cannot do given Article 11, the right to complain to us (Article 14(2)(da), in force from 19 June 2026 according to the legislation.gov.uk timeline) and to the ICO, with its contact details;
- that no automated decisions or profiling are made.

**When it must be given.** Article 14(3) requires the information "within a reasonable period… but at the latest within one month". We have no way to contact a ChatGPT user. Two routes exist: Article 14(5)(a), "the data subject already has the information", if the "Use in ChatGPT or Claude" page shows it before anyone connects; and Article 14(5)(e), where providing it "is impossible or would involve a disproportionate effort", which under Article 14(7) needs appropriate measures "including by making the information available publicly". Whether either route fits someone who connects from a shared URL without seeing our page: not stated in the official sources read. The MCP server's own description (which hosts show when connecting) will also link the privacy notice.

### What the "Use in ChatGPT or Claude" page will say
In addition to what 0056 decision 2 already requires (each app's steps, what any risky setting means, that the host app sees what it sends to us and what we return under its own terms, a link to the privacy notice), a short section, "What your app sends us and what we keep":
- ChatGPT sends, with every tool call, an anonymised user ID, conversation ID and organisation ID (for work accounts), a rough location (city, region, country, time zone and approximate coordinates), a device hint and your language. We did not choose this; ChatGPT does it.
- We keep the three IDs and your city, region and country, with the tool used and the hour, for 90 days to count how the tools are used, then only anonymous totals. We drop the time zone, coordinates and device hint as they arrive, and we count languages only as totals.
- We never keep what you asked: no postcode, place name or other text you or your assistant sent.
- Claude does not document sending anything beyond the question's details, and we keep only anonymous counts for Claude.
- How to object, and the link to the privacy notice.

The wording is proposed and finalised with the page; the page is re-checked against OpenAI's reference page before launch, because hosts change what they send.

### DPIA
A data protection impact assessment (DPIA) is required where processing is "likely to result in a high risk". The ICO's list includes "Invisible processing" (data not obtained from the person where giving Article 14 information "would prove impossible" or "involve disproportionate effort") and "Tracking" ("tracking an individual's geolocation or behaviour"); each requires a DPIA "where this processing is combined with any of the criteria from the European guidelines". Among those nine criteria are "Systematic monitoring" and "Matching or combining datasets"; "In most cases, a combination of two of these factors indicates the need for a DPIA", and "If in any doubt, we would always recommend that you do a DPIA" ([ICO: when do we need to do a DPIA?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/when-do-we-need-to-do-a-dpia/), read 15 Nov 2026). The LIA is also "a potential trigger for a DPIA" (ICO applying legitimate interests page above).

Whether a 90-day record of a pseudonymous ID with a city counts as "tracking" or "systematic monitoring" under the ICO's list: not stated. **Agent's recommendation:** write a short DPIA before launch, since relying on Article 14(5)(e) would be "invisible processing" and the ICO recommends one "if in any doubt". A DPIA screening, at minimum, is a launch blocker.

### Transfers
The ICO defines a restricted transfer as "a transfer of personal information to a separate organisation located outside the UK" that we initiate, including giving an overseas processor access ([ICO: international transfers, a guide](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/international-transfers-a-guide/), read 15 Nov 2026). Receiving data from OpenAI's servers abroad: the guide does not address it (not stated). Storing the records with a hosting provider outside the UK would be a restricted transfer by us, needing an adequacy decision or another safeguard named in the privacy notice. The hosting choice is still open (IN-02; the pilot design assumes Cloudflare), so the storage location and its safeguard are settled with IN-02 before launch.

## Consequences
- **Running cost:** a small store for 90 days of per-call rows and the totals, plus a daily deletion job; expected to fit the hosting's free or lowest tier at pilot volumes (not yet measured; checked against the IN-05 monthly cap).
- **New launch blockers** (added to the 5b gate, backlog 38d): the privacy notice section above; the recorded LIA; a DPIA screening (and the DPIA if it says so); the deletion job with its test; the "drop on arrival" filter with tests that the time zone, coordinates, device hint and every tool argument never reach a log, store, trace or error report; the "Use in ChatGPT or Claude" page section.
- **Specifications to change** when this record is accepted: `docs/specs/pilot/area-tools.feature` TOOLS-26 ("the server keeps no record of calls") and its outline line on what the rate-limit store holds; new scenarios for the kept fields, the dropped fields, missing fields (rule 7) and the 90-day deletion.
- **0014 (SE-02)** gains this as part of its pilot parts; its ICO fee check (0014, "Still to decide") should count this processing.
- **Rules unchanged:** no tool argument, postcode or place name in any log (0051, 0056, 0014); IP addresses in memory only (0014); rate limits stay a global and per-host cap (0051) unless the founder adds a per-user cap (open point 4).
- **Founder merges this record** (`AGENTS.md`, "When merging": new or changed privacy rule tables).
- **Revisit if** OpenAI changes the fields it sends, Anthropic documents fields for Claude, the LIA or DPIA finds the balance fails, the hosting choice puts storage outside the UK without a safeguard, or the totals turn out to answer the usage questions without per-call records.

## Open points for the founder
1. **Device hint and language** (default above): drop the device hint; keep the language only as a daily total. Confirm or change.
2. **Smaller defaults in this record:** call time kept to the hour, and totals kept by region and country (not city). Confirm or change.
3. **Organisation ID:** the LIA's necessity test is hardest for it. Keep it as chosen, or keep only "work account: yes or no"?
4. **Rate limits:** use `openai/subject` also as a per-user rate-limit key (OpenAI's stated purpose), in addition to 0051's global and per-host caps? Default: no change to 0051's limits.
5. **Objections:** since we cannot find a person's records without their ID, the proposed answer is: say so in the notice (Article 11), stop the processing for anyone who disconnects, and delete within 90 days anyway. Accept, or ask for more (for example a way to send us an ID)?
6. **Privacy information timing:** rely on the how-to page and the server description (Article 14(5)(a)), with the public notice as the fallback (Article 14(5)(e) and (7)), and run the DPIA because of it.
7. **OpenAI's own terms:** whether OpenAI's developer or app terms limit what a server may do with these fields was not checked (this record used only ICO and legislation sources); check before launch.
