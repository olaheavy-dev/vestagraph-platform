# 0057: ChatGPT call details: anonymous totals only

**ID:** SE-05  
**Status:** Proposed (founder's choices made 15 Nov 2026 in prompt windows)  
**Date:** 2026-11-15  
**Stage:** 5b (before the public MCP server launches)  
**Applies, without changing:** [0014](0014-privacy-and-data-protection.md) (SE-02): "Keep nothing about anonymous visitors", with only anonymous counts, now applied to the tool calls the MCP server receives. [0051](0051-ai-in-the-public-pilot.md) and [0056](0056-no-on-page-chat-in-the-pilot.md) stand: no postcode, place name or tool argument in any log; rate limits a global and a per-host cap.

## Context
The pilot offers a public, read-only MCP server with the area and council tools, which visitors add to their own ChatGPT or Claude ([0051](0051-ai-in-the-public-pilot.md) points 1 and 4; [0056](0056-no-on-page-chat-in-the-pilot.md)). MCP, the Model Context Protocol, is the standard way an AI app connects to an outside service ([modelcontextprotocol.io](https://modelcontextprotocol.io)).

**What ChatGPT sends with each tool call.** Besides the tool's arguments, ChatGPT adds fields in the call's `_meta` part. OpenAI's reference page ([developers.openai.com/plugins/reference](https://developers.openai.com/plugins/reference), read 15 Nov 2026) lists:

| Field | OpenAI's description |
|---|---|
| `openai/subject` | "Anonymized user id sent to MCP servers for the purposes of rate limiting and identification" |
| `openai/session` | anonymised conversation id, for correlating tool calls in the same ChatGPT conversation |
| `openai/organization` | anonymised organisation id, "when available" |
| `openai/userLocation` | "Coarse location hint (city, region, country, timezone, longitude, latitude)" |
| `openai/userAgent` | "Optional, best-effort user agent hint" (a description of the device and app) |
| `openai/locale` | the requested language and region, for example `en-GB` |

The same page says the device hint and the location "are hints only; servers should never rely on them for authorization decisions and must tolerate their absence." The server must work the same when they are missing, and a missing value is counted as "not sent", never guessed (rule 7).

**Claude.** Anthropic's documentation does not say what Claude sends with a tool call beyond its arguments (research note, 15 Nov 2026: "not stated").

The question was what, if anything, to do with these fields.

## Options
### Option A: Keep 0014: anonymous totals only (recommended by the agent)
The server reads the location and language only to add one to anonymous daily totals, then drops every field. No ID, conversation, organisation, coordinates or device hint is stored or logged. 0014 stands as written.

### Option B: Log the fields for usage statistics for 90 days
Keep the user, conversation and organisation IDs and the city, region and country with each call for 90 days, then reduce them to anonymous totals. Counts distinct and returning users, but reverses 0014's "keep nothing about anonymous visitors" and makes the area-tools specification TOOLS-26 ("the server keeps no record of calls") untrue. It needs a recorded legitimate interests assessment, a deletion job and probably a DPIA before launch.

### Option C: Drop everything unread
The server ignores `_meta` entirely; usage is counted only by tool and day. Simplest, but gives no picture of where or in which language the tools are used.

## Recommendation
Option A. It keeps 0014's promise, adds almost no launch work and still shows reach by region and language.

## Decision
**Option A**, the founder's choice (15 Nov 2026, prompt window): **"Keep 0014: anonymous counts only (Recommended)"**, chosen after the agent showed that logging would reverse 0014, which says "keep nothing about anonymous visitors; only anonymous counts", and would change TOOLS-26. Device hint and language (same day, prompt window): **"Drop device, language as total (Recommended)"**.

**History.** Earlier the same day, in prompt windows, the founder had chosen Option B: "Log them for usage stats" (over the agent's recommended "Drop unread, never store"), "City as well" (keep city, region and country; drop time zone, latitude and longitude), "90 days (Recommended)" (then only anonymous totals) and "All three IDs" (user, conversation and organisation). Those answers were superseded the same day, once the conflict with 0014 was shown.

### What happens to each field
"Dropped" means the server removes the field before anything is written to any log, store, trace or error report, the way 0014 treats raw IP addresses.

| Field | What the server does |
|---|---|
| `openai/subject` (user ID) | Dropped. Not used for rate limits either. |
| `openai/session` (conversation ID) | Dropped |
| `openai/organization` (organisation ID) | Dropped |
| `openai/userLocation`: city, region and country | Read only to add one to the day's totals, then dropped |
| `openai/userLocation`: time zone, latitude, longitude | Dropped |
| `openai/userAgent` (device hint) | Dropped |
| `openai/locale` (language) | Read only to add one to the day's language total, then dropped |
| Tool arguments (postcode, place name, council, any typed text) | Never logged or stored (0051, 0056, 0014) |
| IP address | Never stored (0014: in memory only, for rate limiting) |
| Anything Claude, or a future ChatGPT version, sends that is not listed here | Dropped unread. A new field is used only after a new decision. |

### The totals
- **What is counted:** calls per day by tool, by host (ChatGPT, Claude, other) and outcome (answered, refused by a limit, error); calls per day by city, region and country (ChatGPT only; "not sent" when the location is missing); calls per day by language. Each total is counted separately, not crossed with the others, so no row combines tool, place and language.
- **City:** counted. Founder, 15 Nov 2026, prompt window: "City as well"; the agent had recommended "Region and country", following 0014's "Anonymous counts must not be detailed enough to identify a person".
- **Minimum count:** a total for a day below **10** is shown and stored as "fewer than 10". Founder, 15 Nov 2026, prompt window: "10 (Recommended)". No official threshold was found in the sources read, so this is our own rule.
- **Kept:** the totals have no end date, as 0014's anonymous counts.
- **Rate limits** stay a global cap and a per-host cap (0051). `openai/subject` is not used.

### Privacy points that still apply to a brief read
- **It is still processing.** UK GDPR Article 4(2) defines processing as "any operation… performed on personal data", including "collection", "consultation" and "use", with no exception for brief handling ([legislation.gov.uk: Article 4](https://www.legislation.gov.uk/eur/2016/679/article/4), read 15 Nov 2026). The user ID and a city-level location can be personal data: the ICO says an identifier that "distinguishes one individual from another" is personal data "regardless of whether it is possible to link the 'online' identity with a 'real world' named individual", and lists location data among identifiers ([ICO: identifiers and related factors](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/personal-information-what-is-it/what-is-personal-data/what-are-identifiers-and-related-factors/), read 15 Nov 2026). So receiving the fields and reading region, country and language to count them needs a lawful basis and privacy information, even though nothing about a person is kept.
- **Lawful basis:** legitimate interests (Article 6(1)(f)), the same basis 0014 part 1 is settling for IP addresses and logs. The ICO says the law does not require a written assessment "But you should do one anyway" ([ICO: applying legitimate interests in practice](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/legitimate-interests/how-do-we-apply-legitimate-interests-in-practice/), read 15 Nov 2026). One short paragraph in SE-02 part 1's assessment covers it; no separate assessment.
- **Anonymising is processing too:** the ICO's anonymisation pages could not be loaded on 15 Nov 2026 (the site timed out); read them before launch. Until then, not stated from a page read.
- **Privacy information:** the data comes from OpenAI, not from the person, so UK GDPR Article 14 applies ([legislation.gov.uk: Article 14](https://www.legislation.gov.uk/eur/2016/679/article/14), latest revised version, read 15 Nov 2026); its text read has no exception for brief processing. The privacy notice (SE-02 parts 1 and 2) says what ChatGPT sends, that we drop it and keep only anonymous totals, the purpose, the basis, the source and the right to object ([ICO: what privacy information should we provide?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/the-right-to-be-informed/what-privacy-information-should-we-provide/), read 15 Nov 2026). Since we cannot contact a ChatGPT user, it relies on Article 14(5)(a) ("the data subject already has the information": the how-to page shows it before anyone connects) and Article 14(5)(e) with 14(7) ("making the information available publicly": the public notice).
- **No longer needed:** a deletion job (nothing per call is stored) and a separate DPIA. The ICO's DPIA test is processing "likely to result in a high risk" ([ICO: when do we need to do a DPIA?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/when-do-we-need-to-do-a-dpia/), read 15 Nov 2026). Its "invisible processing" item (relying on the Article 14 disproportionate-effort exception) needs a DPIA only "where this processing is combined with any of the criteria from the European guidelines", and a brief read for counting meets none that the agent can see. Note SE-02's DPIA screening line: "If in any doubt, we would always recommend that you do a DPIA".
- **Transfers:** totals hold no personal data, so where they are stored raises no transfer question. Receiving the fields from OpenAI abroad: the ICO's transfers guide covers only transfers we initiate (not stated for receiving) ([ICO: international transfers, a guide](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/international-transfers-a-guide/), read 15 Nov 2026).

### What the "Use in ChatGPT or Claude" page says
In addition to what 0056 decision 2 requires, a short section, "What your app sends us":
- ChatGPT sends, with every tool call, an anonymised user ID, conversation ID and organisation ID (for work accounts), a rough location (city, region, country, time zone and approximate coordinates), a device hint and your language. ChatGPT chooses to send these; we don't ask for them.
- We keep none of it. We count calls by city, region, country and language per day, then drop everything. We never keep what you asked: no postcode, place name or other text.
- Claude does not document sending anything beyond the question's details; anything it sends is dropped the same way.
- A link to the privacy notice.

The wording is proposed and finalised with the page, which is re-checked against OpenAI's reference page before launch, because hosts change what they send.

## Consequences
- **0014 stands** and now explicitly covers MCP calls.
- **Small cities:** a daily total for a small city comes close to identifying someone, so the minimum count of 10 is what protects small cities, and it applies to every total that includes a city. TOOLS-26 ("the server keeps no record of calls") stays true.
- **Specification wording to check** when the specifications are next edited (no change made here): `docs/specs/pilot/area-tools.feature` TOOLS-26 could add "and the usage totals hold only daily counts by tool, host, outcome, city, region, country and language, with no ID"; TOOLS-25 could name the `_meta` IDs, coordinates and device hint among what never reaches a log; new scenarios for the totals, the "fewer than 10" rule and a missing location (rule 7).
- **Launch blockers added** (stage 5b gate): the drop-on-arrival filter with tests that no `_meta` ID, coordinate or device hint reaches a log, store, trace or error report; the privacy notice and how-to page sections above.
- **Running cost:** a few small counters per day; nothing measurable.
- **Revisit if** OpenAI changes the fields it sends, Anthropic documents fields for Claude, or the totals turn out not to answer the usage questions (any per-person record would need a new decision that changes 0014).

## Open points for the founder
None. The founder answered the last two (city totals, minimum count) on 15 Nov 2026.
