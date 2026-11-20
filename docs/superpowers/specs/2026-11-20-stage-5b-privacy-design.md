# Stage 5b, group C: privacy, and an anonymous chat first: design

**Date:** 20 Nov 2026. **Status:** approved by the founder, 20 Nov 2026 (prompt window, "Approve (Recommended)", which also accepts the agent's calls marked below; each can still be changed). Recorded in decision [0063](../../decisions/0063-pilot-privacy-and-anonymous-chat-first.md). Each founder answer below was given on 20 Nov 2026 in a prompt window unless marked typed; the agent's calls are marked and can be changed. **Decisions it follows:** [0014](../../decisions/0014-privacy-and-data-protection.md) (SE-02), [0046](../../decisions/0046-public-area-check-first.md), [0051](../../decisions/0051-ai-in-the-public-pilot.md), [0056](../../decisions/0056-no-on-page-chat-in-the-pilot.md), [0057](../../decisions/0057-chatgpt-call-details.md), [0058](../../decisions/0058-signed-in-chat-in-the-pilot.md), [0060](../../decisions/0060-pilot-foundation-hosting-and-database.md), [0061](../../decisions/0061-pilot-data-pipeline-postcodes-and-walking-times.md); register lines SE-02, SE-06 to SE-09, FE-05, IN-05.

## Intent and why
Group C was meant to settle the privacy work 0058's signed-in chat needed before launch: the lawful basis, a DPIA, access and deletion requests, the PECR check of sign-in cookies, and an email service for sign-in links. While choosing who is responsible for the data, the founder asked how to avoid that weight for what is, today, a portfolio project: "how can we avoid this soletrader thing, remove sign, just a porflio project? what are my options?" (typed). The answers below reshape the pilot: **the chat opens to everyone without sign-in, limited per IP address; sign-in, accounts and the email service wait until later.** The privacy work shrinks to what an anonymous site with an AI chat needs, and the account work becomes a checklist to finish before sign-in ever opens.

Why the anonymous chat (founder's reason from 0058, which still holds): the chat is the part of the pilot that shows AI-engineering and forward-deployed-engineer skills, and an anonymous chat is one anyone, including an employer, can try at once.

Success: the pilot launches lawfully with a finished Privacy notice (no "To be written before launch" placeholders), a written lawful-basis assessment and a short DPIA; the chat cannot drain the AI budget; and nothing a visitor types reaches an ordinary log.

## Goals
1. Settle who is responsible for the data (the controller), the contact route and the ICO fee position.
2. Set the anonymous chat's limits and abuse guard: per-IP daily limit, bot check.
3. Settle chat traces for anonymous visitors.
4. Set the lawful basis for each kind of processing, the DPIA, request handling and the PECR position.
5. Settle FE-05 (usage counts and feedback) for the pilot.
6. List what must be done before sign-in opens later.

## Non-goals
- The AI provider, framework, monthly cap in pounds and the AI test runner (group D: AI-01, AI-04, AI-09, AI-03, IN-05).
- The anonymous chat's screens, wording and scenarios (a design step after this, see "What is left").
- Sign-in, accounts, saved areas and chat history (deferred, below).
- Final legal wording of the Privacy notice (written in the build from this design; the founder's copy review approves it).

## Anti-goals (a failure even if it works)
- A visitor's typed text, searched postcode or IP address in an ordinary server, application or error log (0014, 0046).
- A placeholder in the live Privacy notice shown as if it were finished text (SE-07).
- A chat that keeps working with no limit when the bot check or the limiter fails (fail closed: if the limiter can't count, the chat pauses).
- One abuser using up the month's AI budget before any alert fires.
- Any data used for adverts, profiling or sale.

## Constraints
- Free first, within the rules (house rule). Python API and Next.js (0049); the founder's server in Germany behind Cloudflare, database on Neon Frankfurt (0060).
- UK GDPR and PECR; ICO guidance is the reference (sources below).
- 0014's rule stays: nothing kept about anonymous visitors except anonymous counts, now with one named exception (30-day traces, below).
- The AI provider may not train on chat text (0051's provider terms, "No training, short checks OK"), checked when AI-01 is chosen.

## Approaches considered

### Who handles personal data in the pilot (founder's main choice)
| Option | What it meant | Chosen? |
|---|---|---|
| Keep 0058: open sign-in and chat | All of group C now: accounts, DPIA, email service, requests | No |
| Sign-in behind a feature flag, owner-only or invite-only at launch | Chat only for the founder or invited people | No (the founder asked about it: "what if we have a feature flag that can gate chat behing a sign in or not, will this be a big change?") |
| **Anonymous chat, IP limits** | Anyone can chat without signing in; per-IP limit, bot check, monthly cap | **Chosen** (the founder asked "what of a fourth option of chst without sign in at all, can we use ip address to limit request, what does this affect" (typed), then chose it over the agent's recommendation "Flag, launch owner-only") |
| Private demo only | Nothing public | No |

Trade-offs the founder accepted: IP limits are rough (shared office or mobile IPs run out sooner; a VPN gives one person many IPs), so the bot check and the monthly cap (IN-05) carry more of the load; no history or saved areas; it reverses 0056 and 0014's "no AI calls per anonymous visitor" for the chat.

### Sign-in
**Chosen: "Defer sign-in until later (Recommended)"**, over "Build it, flag closed" and "Both open at launch". The pilot ships with no accounts; Better Auth, the account page, the email service, saved areas, chat history and the deletion jobs are built later. Their specifications and boards stay, marked for later. The founder (typed): "so if we later add signin as long as we are not commercial, no payment but wwe will start with anonymous first".

### Chat traces
**Chosen: "Words, kept 30 days"**, over the agent's recommendation "Metadata only" and "Words, kept 7 days". Traces hold the words and tool calls of anonymous chats, with no IP address, for 30 days, visible only to the founder, then deleted. Because there are no accounts, a trace can't be matched to a person, so it can't be deleted early on request; the Privacy notice says so plainly. The founder asked first: "do we still neeed sole trader with 30 days for this?" (typed); the answer was that the trace choice doesn't change who is responsible or the fee, only how much visitor text is held.

### Per-IP daily limit
**Chosen: "15 a day per IP (Recommended)"**, over 10 and 30. Same number as 0058's per-account cap.

### Bot check
**Chosen: "ALTCHA, self-hosted (Recommended)"**, over Cloudflare Turnstile and "Start with ALTCHA, switch if abused". Research on 20 Nov 2026 (official pages):
| | ALTCHA (self-hosted) | Cloudflare Turnstile |
|---|---|---|
| Cost | Free, no limits, MIT ([altcha.org](https://altcha.org/)) | Free, "Unlimited challenges" ([plans](https://developers.cloudflare.com/turnstile/plans/)) |
| Who sees visitor data | No one else: runs on our server | Cloudflare, which says it is "a data controller of Signals that we process to improve Turnstile's bot detection" ([privacy](https://www.cloudflare.com/turnstile-privacy-policy/)) |
| Cookies | "sets no cookies, does no fingerprinting" ([altcha.org](https://altcha.org/)) | Unclear for the web widget |
| Strength | Proof of work: slows bots, doesn't detect them | Detects bots |

**This choice approves the Python package `altcha`** ([altcha-lib-py](https://github.com/altcha-org/altcha-lib-py), MIT; register line). Cloudflare's free-plan rate limiting has "One rule", counted by "IP only" over 10 seconds ([docs](https://developers.cloudflare.com/waf/rate-limiting-rules/)), too coarse for a daily limit, so the API counts the 15 itself.

### Email service
Not needed while there is no sign-in. The 20 Nov 2026 research is kept for later (ranked: Scaleway Transactional Email, Amazon SES London or Frankfurt, Lettermint, Brevo; not recommended: Resend and Postmark, which store data in the US; sources in the research notes of this session, to be re-checked when sign-in is planned, as prices change).

## Decisions

### 1. Who is responsible, and contact
- **Controller:** the founder, as a private individual. Founder chose "You, as a sole trader (Recommended)"; the agent then corrected its framing: no business or HMRC registration is needed, because the controller role follows who decides what the site does with personal data, not a tax status.
- **Contact:** "privacy@ address on our domain (Recommended)": an address on the Vestagraph domain that forwards to the founder's inbox. *Agent's call:* Cloudflare Email Routing if its free forwarding fits (checked in the plan); a new service needs the founder's approval.
- **Address:** the founder chose "A PO Box or virtual address (Recommended)" for the ICO register; with no fee due (below) nothing goes on the register, so no PO Box is bought. *Agent's call, to confirm in the plan against ICO guidance:* the Privacy notice gives the founder's name and the privacy@ address as contact details, with no postal address.

### 2. ICO data protection fee: none while non-commercial
The founder took the ICO's [self-assessment](https://ico.org.uk/for-organisations/data-protection-fee/data-protection-fee-self-assessment/) on 20 Nov 2026 and answered "Not started trading", after reading its definition: "Under data protection law, you are considered to be trading if you're using personal information for commercial reasons, even if you're an individual and not part of an organisation." Result: "You don't need to pay a fee yet … Once you start trading you should retake this self assessment" and "You do not need to tell the ICO you're exempt." The founder (typed): "i don;t need to pay it seems". The agent's earlier view ("likely due") was too cautious and was corrected.
- **Retake the quiz before** any income, adverts, paid feature or company, and when sign-in opens (a cheap check). Tier 1 is £52 a year, £5 less by direct debit ([ICO FAQs](https://ico.org.uk/for-organisations/data-protection-fee/faqs-data-protection-fee-payment-and-online-registration/)).
- Grey area recorded: the pilot also shows the founder's skills to employers; the agent's reading is that this is personal career use, not commercial use of visitors' data. Not an ICO statement.

### 3. The anonymous chat
- **Alongside the search pages, prominently** (founder, after approving this design: "Alongside, prominent (Recommended)", over "Alongside, low-key" and "Chat replaces search", after asking "should we replace the whole ui search step with the anonymous chat or have it as another option?"): search stays the main way in and works when the chat is paused; the chat is offered beside the postcode box on the landing page and as "Ask about this area" on each result, opening with that area loaded.
- Anyone can use it without signing in. 15 messages per IP address per day, counted by the API, reset at midnight UK time (*agent's call*, as 0058). The counting rules from 0058 carry over where they fit (a stopped answer, a guard-stopped answer and Regenerate count; a failure on our side doesn't).
- **How IPs are counted (agent's call):** in memory on the API, as 0014 requires ("any short-lived raw use, such as rate limiting, is kept in memory only"). The pilot runs one API copy (0060). If more copies are ever run, the count moves to the database as a keyed hash of the IP, kept no longer than the day, which needs a new decision because it stores a pseudonymous identifier.
- **Fail closed:** if the limiter or bot check can't run, the chat pauses with the "Chat unavailable right now" state (0058 FE-66); the rest of the site keeps working.
- **Bot check:** ALTCHA before the first message of a chat and again after a set number of messages (*agent's call*; the number is set in the plan). Used ALTCHA proofs are stored until they expire, so one proof can't be replayed (ALTCHA's library doesn't do this itself).
- **Monthly cap:** IN-05's monthly cap in pounds (group D) is the hard backstop; reaching it shows "Chat is paused for this month, the area check still works" (0058 note).
- **No history:** the conversation lives only in the browser tab's memory; closing the tab ends it. Nothing is written to the device (no cookies, no local storage) for the chat.
- **What reaches the AI provider:** the visitor's messages and the tool results, never the IP address. The provider's terms must say no training on the text (0051), checked at AI-01.

### 4. Traces
Words and tool calls, no IP address, kept 30 days, founder-only, then deleted automatically. Ordinary logs and error reports never hold chat text, postcodes or IPs (0014, 0058). The AI test set (AI-03) never copies from traces without a later decision (0058 choice 9's agent's call, kept).
- **Sensitive details (builder check; founder: "Warning + scrub obvious details (Recommended)", over "Warning only" and "Switch traces to metadata only"):** visitors may type health, disability, family or money details, which UK GDPR treats as special category data (Article 9) where they concern health and similar, and we have no Article 9 condition for keeping them. So the chat screen shows a short line asking visitors not to share personal or health details (wording for the founder's copy review), and before a trace is saved a tested filter removes obvious identifiers (email addresses, phone numbers, card-like numbers). The filter can't catch everything; the DPIA records the leftover risk. *Agent's call:* the filter uses an established package if one fits (WW-25), brought to the founder with evidence; otherwise a small tested module.
- **Deletion wording (agent's call):** if traces are stored in Neon, deleted traces stay in Neon's 7-day history (0060), so the notice says "deleted after 30 days, and gone from backups within 7 more days". If group D chooses a hosted tracing tool, that tool's own retention and data location are checked first and the notice follows them; a tool that can't delete after 30 days doesn't qualify.
- **Access (agent's call):** the founder reads traces over the VPN only, as with the data dashboard (0061), or through the tracing tool's own login if group D picks a hosted one; no admin login is built in the pilot.

### 5. Lawful basis (agent's proposal, approved by the founder: "proposals are fine, go ahead")
| Processing | Personal data | Lawful basis |
|---|---|---|
| Serving pages; Cloudflare's proxy and its request analytics (0060) | IP address, browser details | Legitimate interests (running and securing the site) |
| Search inputs (postcode, place) for the area check and City Explorer | A postcode can hint where someone may move (0014) | Legitimate interests (giving the result the visitor asked for); never stored or logged |
| Per-IP limits (chat, energy certificate lookup) | IP address, in memory only | Legitimate interests (security, fair use, cost) |
| ALTCHA bot check | A proof from the visitor's browser, on our server only | Legitimate interests (security) |
| Chat messages sent to the AI provider | Whatever the visitor types | Legitimate interests (answering the visitor's question) |
| 30-day chat traces | Typed text, no IP | Legitimate interests (finding faults, watching cost and safety) |
| Report a problem counts; FE-05 counts; 0057's ChatGPT totals | None after counting (anonymous totals) | Not personal data once counted; the moment of reading 0057's fields is covered by legitimate interests |
| A privacy request by email | Name, email address, the request | Legal obligation (answering data-protection requests) |

Each legitimate-interests line gets a short written assessment (an LIA, the ICO's three-part test: purpose, necessity, balance; [ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/a-guide-to-lawful-basis/legitimate-interests/)), kept in the repository. This also lets the founder accept [0057](../../decisions/0057-chatgpt-call-details.md), which waited on its lawful basis.

### 6. DPIA
A short written DPIA before launch, covering the anonymous chat and its 30-day traces. The ICO lists "the novel application of existing technologies (including AI)" as a factor and says "If in any doubt, we would always recommend that you do a DPIA" ([ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/examples-of-processing-likely-to-result-in-high-risk/)). It covers: what visitors may type (including sensitive details they choose to share), the provider's retention and no-training terms, trace access and deletion, abuse, and the risks of the IP limit.

### 7. Requests from people
- Requests go to the privacy@ address; answered "without undue delay and at the latest within one month" ([ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/subject-access-requests/a-guide-to-subject-access/)).
- What we can and can't find: we hold no accounts and no IPs; traces can't be matched to a person, so the reply explains that, and that traces are deleted after 30 days. The Privacy notice says the same up front.
- Portability doesn't arise: it applies only to consent or contract ([ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-data-portability/)), and no line above uses them.

### 8. PECR (cookies and device storage)
- The pilot sets **no cookies**: no sign-in session, and ALTCHA sets none.
- The three "remember on this device" lists (recent postcodes SE-08, councils, priority limits SE-09) stay off until the visitor switches them on, which is their consent, kept at most 12 months (as decided).
- So **no cookie banner.** The Data (Use and Access) Act 2025's new statistics exception (in force 5 Feb 2026, [S.I. 2026/82](https://www.legislation.gov.uk/uksi/2026/82/made)) is not needed, because the FE-05 counts store nothing on the device.

### 9. FE-05: usage counts and feedback (agent's proposal; the founder's question "what would you want to know after a month?" is still open and can change it)
Only anonymous daily totals on our server, nothing stored on or read from the device: area checks, City Explorer views, chat messages, chats paused by the daily limit or the monthly cap, bot-check failures, and Report a problem by reason (FE-74's three shapes). Totals below 10 show as "fewer than 10", as 0057 does. No page analytics tool.

### 10. Before sign-in opens (later)
A checklist the sign-in plan must clear, from 0058 and this design: retake the ICO quiz; choose the email service (research above, re-checked); the lawful basis for accounts, chats and saved areas; update the DPIA; access, deletion and export handling for stored accounts; the PECR check of the sign-in session cookie (the ICO lists "authenticating the subscriber or user" as strictly necessary, [ICO](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-the-use-of-storage-and-access-technologies/what-are-the-exceptions/)); Neon's 7-day history in the deletion promise (0060); the Privacy notice update.

## What this changes in the records
- **New decision 0063 (SE-10)** records this design; **0058** is amended (sign-in, accounts, saved areas and history move from the pilot to later; the chat opens without sign-in); **0056** and **0014** are amended (AI calls for anonymous visitors in the chat, with these safeguards; one kept item, the 30-day traces); **0051**'s anonymous safeguards are the model.
- **Register:** SE-01 (sign-in moves to later), SE-02 (pilot parts settled here), SE-06 (email link: later), FE-05 (settled as above), a new line approving `altcha`, IN-05 (the monthly cap is now the anonymous chat's backstop).
- **Group A's plan** ([2026-11-20](../plans/2026-11-20-stage-5b-group-a-foundation.md)) and 0060's design lose Better Auth's routes and secrets.
- **Specifications:** `sign-in.feature`, `account.feature` and the signed-in parts of `workspace-chat.feature` are tagged for later; the Privacy notice scenarios (PRIV-01 to PRIV-19) are updated for an anonymous chat when the notice is written.
- **Status file** updated.

## Order of work (builder check; agent's call)
The provider (AI-01), the tracing tool (AI-09) and the monthly cap (IN-05) are group D's. So: the records changes are made now; the build plan for the limiter, ALTCHA, the trace filter and the log guards can be written now; the legitimate-interests assessments, the DPIA and the Privacy notice are drafted now and finished after group D, because they must name the AI provider and the tracing tool, where each stores data, and on what transfer terms. The DPIA also notes that a home-buying site is unlikely to be used by children (the ICO's Children's code applies where children are likely to use a service), with no age check.

## What is left
- **To the founder (open):** what to learn from the pilot's usage after a month (FE-05 may change); **where the founder's name appears** (founder: "Ask me again later"): the Privacy notice must name the controller, and repository rule 5 bars real personal data from committed files, so the options are a name filled in at deploy time from a private setting, or a recorded exception to rule 5; decided at the Privacy notice step, with the check that an email address alone meets the "contact details" requirement.
- **A design step for the anonymous chat's screens** (before planning its build): where the chat opens from on the public pages, the workspace layout without the sidebar's saved areas and past chats, the daily-limit and bot-check states, and the Privacy notice's new wording. The pilot gate (0052) passed with the signed-in chat's boards, so these boards and scenarios are new work, with the founder's copy review.
- **To the builder:** the ALTCHA re-check interval, the in-memory counter's shape, the trace store (group D picks the tracing tool, AI-09; it must delete traces automatically after 30 days), the LIA and DPIA text, the Privacy notice text, the privacy@ forwarding setup.
