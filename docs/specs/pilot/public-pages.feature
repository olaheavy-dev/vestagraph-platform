@screen @buying @renting
Feature: How it works, Privacy and Accessibility (the pilot's three public pages)
  Question it answers: "What is Vestagraph, what does it do with my data, and how accessible is it?"
  Modes: both (and anyone, with no account; decisions 0014 and 0046)
  Added 19 Nov 2026 (pilot design batch, PR 2, plan Task 5; design `docs/superpowers/specs/2026-11-19-pilot-design-batch-design.md`, sections 5 to 7; decisions 0014, 0053, 0056, 0057, 0058; register lines DA-09, DA-35, FE-11, FE-74, SE-02, SE-07, SE-08, SE-09).
  Where: `/how-it-works`, `/privacy` and `/accessibility`, linked from the footer on every page and, for "How it works", from the landing's "How it works" section (LAND-25, LAND-26 in `screens/01-landing.feature`). The footer labels are the landing boards': "How it works", "About the data", "Privacy notice", "Accessibility" (HOWTO-31).
  Fixtures: none. The three pages are static text; they quote no figure (AGENTS.md rule 2).
  Boards: on the canvas page "Pilot · public area check", section "Pilot 9 · Public pages" (design canvas version 437, version id 1795257784-6087; the four Privacy boards redrawn on 21 Nov 2026 for the anonymous chat: the other boards were last drawn at version 425): HowItWorks (desktop, 1440 wide) and HowItWorksPhone (390), Privacy and PrivacyPhone, Accessibility and AccessibilityPhone, each with a Dark twin. Every string below that is not a quote from a record is the agent's proposed wording. The Landing boards (Landing, LandingDark, LandingPhone, LandingPhoneDark) draw LAND-25 and LAND-26: the footer reads "How it works", "About the data", "Privacy notice", "Accessibility" and "Use in ChatGPT or Claude" (HOWTO-31), and the How it works section ends with the link "More on how it works". Each placeholder is drawn in one style, a dashed, hatched slate box with a "Placeholder" label above its exact text (a "Draft" label for PRIV-11's draft line); where a scenario lists several placeholders in one sentence, the board draws one box for the group, labelled with what it covers. No illustration is drawn (HOW-11 allows at most one).
  Launch blocker (design `docs/superpowers/specs/2026-11-21-anonymous-chat-design.md`, section 5; decisions 0063, 0064, 0065; register lines SE-10, SE-11): the chat does not go public until the Privacy notice states every fact in PRIV-04, PRIV-08, PRIV-13, PRIV-14, PRIV-20 and PRIV-21 (the controller, the purposes and lawful basis, the transfer to the US and its safeguard, the keeping periods, withdrawing consent, the right to complain to the ICO). PRIV-04 is the one scenario that names the controller (0065). Check PRIV-14's complaint wording against current law before launch: legislation.gov.uk's Article 13(2)(d) now reads "the Commission under section 165 of the 2018 Act" (the Data (Use and Access) Act 2025 may rename the ICO); unverified.
  Wording status: the agent's proposed wording, for the founder's copy review before build. The facts on each page are quoted from their records (listed per scenario); the words around them are proposed. Two kinds of text are fixed by the founder's decision SE-07 and are never rewritten: the legal-part placeholder "To be written before launch (SE-02)" and the contact placeholder "Contact details to be added before launch". Accessibility's results placeholder "To be completed after testing, before launch" is from the design (section 7).
  Rule 1 and SE-07: no legal position is stated that no record decides. The controller, the lawful basis, the keeping periods, the rights, withdrawing consent and the right to complain are stated only where 0063, 0064 or 0065 decide them (PRIV-04, PRIV-13, PRIV-14, PRIV-20, PRIV-21); everything else stays a placeholder. A placeholder is shown plainly as a placeholder, never styled as finished text. Rule 4 and 0054: no page calls an area, council or home "verified", "safe" or "approved", and none gives a score, rating or verdict.
  Facts decided on 21 Nov 2026 for the anonymous chat (0063, 0064, 0065), no longer placeholders: who the controller is and how to contact them (PRIV-04); the lawful basis and purposes for the chat (PRIV-20); the AI provider and the keeping periods (PRIV-13, PRIV-21); the bot check (ALTCHA, PRIV-08); the rights, withdrawing consent and the right to complain (PRIV-14). Sign-in, accounts, saved areas and chat history wait until later (0063 point 2), so no sign-in cookie is in the pilot. Facts still undecided, shown as placeholders and not invented: the lawful basis for the other kinds of processing (0057 only proposes legitimate interests for ChatGPT call fields); the legal retention wording around the periods that are decided elsewhere (FE-74's 90 days, 0057's totals with no end date, SE-08 and SE-09's 12 months); hosting and security (PRIV-19); the accessibility test method, date and results.

  Board-to-scenario map (each board has a Dark twin showing the same wording; HOW-14, PRIV-17, A11Y-09):
    HowItWorks (desktop) and HowItWorksPhone: header and sections -> HOW-01 to HOW-11; links -> HOW-04, HOW-08, HOW-09, HOW-12; layout -> HOW-13
    Privacy and PrivacyPhone: header and the placeholder style -> PRIV-01, PRIV-02, PRIV-03; each section -> PRIV-04 to PRIV-14, PRIV-18, PRIV-19, PRIV-20, PRIV-21; links -> PRIV-15; layout, keyboard -> PRIV-16
    Accessibility and AccessibilityPhone: A11Y-01 to A11Y-08
    Landing footer and "How it works" link -> LAND-25, LAND-26

  Required states (doc 03 §5; AGENTS.md rules 1, 4 and 7):
    loading, empty, ambiguous match, not covered, not found, stale, source failed, offline: not applicable (three static pages that hold no search and no stored data; they are part of the site)
    placeholder sections (Privacy) -> PRIV-02, PRIV-03, PRIV-14
    untested (Accessibility) -> A11Y-02, A11Y-03, A11Y-04
    privacy: PRIV-04 to PRIV-13, PRIV-18, PRIV-20, PRIV-21
    accessibility of the pages themselves: HOW-13, PRIV-16, A11Y-08, A11Y-09

  # ---- How it works (design section 5) ----

  @ui
  Scenario: HOW-01 the page opens with its title and what it is for
    Given the user is on the landing page
    When the user opens "How it works" from the footer
    Then the page "/how-it-works" opens with the heading "How it works"
    And a line under it says what the page is for, in plain words (proposed wording: "What Vestagraph is, where its facts come from and what it will never do.")

  @ui
  Scenario: HOW-02 the page has seven sections, in the design's order
    Given the user has opened "How it works"
    When the user reads the page from the top
    Then the section headings are, in this order: "What Vestagraph is", "Where the facts come from", "What it never does", "What “Not known” and the source stamp mean", "Explain this", "Use in ChatGPT or Claude" and "Report a problem"
    And there are no other sections (the headings are proposed wording; the order and the topics are the design's)

  @ui
  Scenario: HOW-03 "What Vestagraph is" says it shows facts about an area in England, each with its source and date
    Given the user has opened "How it works"
    When the user reads "What Vestagraph is"
    Then it says that Vestagraph shows facts about an area in England, each with where it came from and its date, and that it needs no account to check an area
    And it says other parts of the UK show "Not yet covered" (rule 6)

  @ui
  Scenario: HOW-04 "Where the facts come from" links About the data
    Given the user has opened "How it works"
    When the user reads "Where the facts come from"
    Then it says the facts come from named official and open sources, and links "About the data"
    And "About the data" opens the list of sources and their dates (AREA-44), and the page names no source or date of its own (rule 1)

  @ui
  Scenario: HOW-05 "What it never does" says no verdicts, no scores, and missing data is never shown as zero
    Given the user has opened "How it works"
    When the user reads "What it never does"
    Then it says Vestagraph never says a place or a home is "safe", never scores or ranks places, and never gives a verdict, so the choice stays the visitor's (rules 4 and 7; 0054)
    And it says missing data is never shown as zero, a favourable value or a clean result

  # FE-33: the stamp is the source's icon, name and link only. "Not known right now" and "Not yet covered" are the records' own gap lines.
  @ui
  Scenario: HOW-06 "What “Not known” and the source stamp mean" explains the gap line and the stamp
    Given the user has opened "How it works"
    When the user reads "What “Not known” and the source stamp mean"
    Then it says "Not known right now" means we hold no figure for that fact and have not guessed one, and "Not yet covered" means we do not cover that place or that topic yet, so Wales, Scotland and Northern Ireland are not covered yet (rule 6; AREA-01, NEAR-04) and a topic can also be not covered for a place in England, as the Green space of "NB7 1RR" is (COMPARE-26, COMPARE-27, fixture record `NB7-1RR-AREA-GREEN-SPACE-1`)
    And it says the source stamp on a fact shows where the fact came from, with a link to the source

  # AI-12: Explain this is pre-written, reviewed text; no live AI.
  @ui
  Scenario: HOW-07 "Explain this" is described as pre-written, reviewed text, not AI
    Given the user has opened "How it works"
    When the user reads "Explain this"
    Then it says each "Explain this" is a short text written in advance and reviewed by a person, and is not written by an AI at the time you read it
    And a topic with no reviewed text says it is not yet available (TOPIC-24)

  @ui
  Scenario: HOW-08 the "Use in ChatGPT or Claude" section links the how-to page
    Given the user has opened "How it works"
    When the user reads "Use in ChatGPT or Claude" and chooses its link
    Then it says, in one or two lines, that you can connect your own ChatGPT or Claude to Vestagraph's public area and council facts, and "Use in ChatGPT or Claude" opens (HOWTO-01)
    And the page names no host setting or plan (those are HOWTO-18 to HOWTO-28's, and are not known until tested)

  # The Report a problem control sits on a fact in a topic's detail (FE-74), so it has no page of its own to link to.
  @ui
  Scenario: HOW-09 the "Report a problem" section says what the control does and what is counted
    Given the user has opened "How it works"
    When the user reads "Report a problem"
    Then it says a fact's detail has a "Report a problem" link with three choices, "Wrong", "Out of date" and "Missing something", with no free text and no reply
    And it says we only count reports for each fact to see what needs checking, and links "Privacy notice" for what is kept (PRIV-07)

  @ui
  Scenario: HOW-10 the page uses no verdict words
    Given the user has opened "How it works"
    When the user reads the whole page
    Then it never calls an area, council or home "verified", "safe" or "approved" and shows no score, rating or ranking (rule 4), except where a sentence says Vestagraph never does (HOW-05)

  # Optional: one illustration at most, in the isometric style (FE-10). If one is added it is recorded in docs/assets/README.md first (rule 5).
  @ui
  Scenario: HOW-11 the page has at most one illustration, with a text alternative
    Given the user has opened "How it works"
    When the user looks at the page
    Then there is at most one illustration, in the isometric style (FE-10), with an alternative text that says what it shows or marked as decoration
    And if there is one, it is recorded in `docs/assets/README.md`

  @ui
  Scenario: HOW-12 the page links back, and is linked from the footer and the landing
    Given the user has opened "How it works"
    When the user chooses "← Back to Vestagraph"
    Then the landing page opens
    And "How it works" is in the footer of every page (HOWTO-31) and is reached from the landing's "How it works" section (LAND-25)

  @ui
  Scenario: HOW-13 the page works by keyboard, with 44 px targets, on a phone and on desktop
    Given the user has opened "How it works" on a phone (390 px wide) and on desktop
    When the user works through the page by keyboard
    Then every link can be reached and used in reading order, each button and standalone link at least 44 px tall (a link inside a sentence is exempt, as WCAG 2.2 success criterion 2.5.8 allows for inline targets), with the focus visible, and nothing scrolls sideways at 390 px
    And the heading order is one level-1 heading and the seven sections as level-2 headings

  @ui
  Scenario: HOW-14 the dark twin shows the same wording
    Given the user has chosen the dark theme
    When the user opens "How it works"
    Then the same sections and wording show, with text and links in WCAG 2.2 AA contrast

  # ---- Privacy (design section 6; SE-07) ----

  # SE-07 (founder, 19 Nov 2026): every section the notice needs is drawn, filled with facts already decided; the legal parts are placeholders. The page is a draft until SE-02 is written; it never claims to be the final notice.
  @ui
  Scenario: PRIV-01 the page opens with its title and says it is not final
    Given the user is on the landing page
    When the user opens "Privacy notice" from the footer
    Then the page "/privacy" opens with the heading "Privacy notice"
    And a line under it says the notice is unfinished and that the parts marked "To be written before launch (SE-02)" are not yet written (proposed wording)

  @ui
  Scenario: PRIV-02 the sections are in the design's order (with "Hosting and security", PRIV-19, added after "The chat"; section renamed from "Signed-in accounts and chat" on 21 Nov 2026, 0063)
    Given the user has opened "Privacy notice"
    When the user reads the page from the top
    Then the section headings are, in this order: "Who we are", "What we collect and what we never collect", "Remembering things on your device", "Report a problem counts", "The bot check", "Rate limits", "Links to other sites", "Maps", "Using Vestagraph in ChatGPT or Claude", "Energy certificate numbers", "The chat", "Hosting and security", "Your rights" and "Contact"
    And the headings are proposed wording; the topics and their order are the design's

  # SE-07: "The page never shows a placeholder as finished text."
  @ui
  Scenario: PRIV-03 every legal part reads exactly "To be written before launch (SE-02)", shown plainly as a placeholder
    Given the user has opened "Privacy notice"
    When the user looks for the controller details, the lawful basis, the retention wording and the rights wording
    Then each of them reads exactly "To be written before launch (SE-02)", except that the decided periods quoted in their own sections (PRIV-06, PRIV-07, PRIV-11, PRIV-13) stay as quoted, and only the legal wording around them is the placeholder (so each of PRIV-06, PRIV-07 and PRIV-11 also carries a placeholder for its lawful basis, retention wording or consent position); the parts written on 21 Nov 2026 are not placeholders: the controller (PRIV-04), the bot check (PRIV-08), the chat (PRIV-13, PRIV-20, PRIV-21) and the rights and contact (PRIV-14); the other still-undecided parts, such as "Hosting and security" (PRIV-19), stay placeholders
    And each is shown in a visibly different style from finished text (a labelled box, not body text) and is never worded as if it were final, and no legal position is stated anywhere that no record decides (rule 1)

  # Design section 5 and decision 0065 (21 Nov 2026): UK GDPR Article 13(1)(a) requires "the identity and the contact details of the controller". The founder chose to write their name in the notice (an exception to rule 5, 0065). The name is written here and nowhere else in this file.
  @ui
  Scenario: PRIV-04 "Who we are" names Vestagraph, the controller by name, and privacy@vestagraph.co.uk
    Given the user has opened "Privacy notice"
    When the user reads "Who we are"
    Then it says what Vestagraph is in one line (the same facts as HOW-03)
    And it names the controller as Sunkanmi Olawuwo, a private individual (0063 point 6, 0065)
    And it gives privacy@vestagraph.co.uk as the contact (0063 point 6, 0065; Article 13(1)(a))
    And it names no company and no postal address (none is decided)

  # 0014 (starting position; keep nothing about anonymous visitors), 0053 (limits in the request body only, never logged, never stored), 0014's logs rule.
  @ui
  Scenario: PRIV-05 "What we collect and what we never collect" quotes the decided facts
    Given the user has opened "Privacy notice"
    When the user reads "What we collect and what we never collect"
    Then it says that what you type, a postcode or a place name, is only used to show your result, and that it travels in the part of the link after the "#" or in the body of a request, never in a query string or an address that reaches a log (0014 for the search; the pilot design 2026-11-13 and the pilot design batch, section 6, for the "#" and the body)
    And it says searches are not kept against you, and we keep only anonymous counts, for example the number of checks per day (0014)
    And it says the limits you set in priorities are sent in the body of a request to work out the comparison, are not kept and are not logged (0053)
    And it names the City Explorer inputs: the place name or postcode you type, your budget, the council tax band you pick, and the deposit, mortgage rate and term in the rent or buy section; it says none of them is stored or written to a server, application, hosting or tracing log, that analytics never records a form field, and that the amounts travel only in the request body, never in the address or its query string, and are not in a share link or a printout (CITY-101, CITY-59, CITY-103; 0055)
    And it says IP addresses are dropped or anonymised before logs are written (0014)
    And the lawful basis and the retention wording each read exactly "To be written before launch (SE-02)"

  # SE-08 and SE-09: Recent postcodes and remembered priority limits at most 12 months; the councils' setting is the same (CITY2-46, CITY2-54). 0014 and 0053: off by default, PECR consent. Theme and text size are stored nowhere (FE-23, DISP-05).
  @ui
  Scenario: PRIV-06 "Remembering things on your device" names its three "remember on this device" choices, kept only in your browser
    Given the user has opened "Privacy notice"
    When the user reads "Remembering things on your device"
    Then it names "Remember postcodes on this device", "Remember councils on this device" and "Remember these on this device" (the limits you set in priorities), each off until you turn it on, each its own choice (0014; 0053; PRIO-15, PRIO-19)
    And it says the lists of postcodes and councils are kept only in your browser and are never sent to us, that remembered limits are also kept only in your browser and are sent only when you check, to work out the comparison, and are never stored or logged by us (0053; PRIO-17, PRIO-20), that you can clear or turn off a list at any time, and that an entry is kept at most 12 months, older entries being dropped automatically (SE-08 for postcodes, CITY2-54 for councils, SE-09 for limits, PRIO-20)
    And the lawful basis and the consent position (PECR) read exactly "To be written before launch (SE-02)" (0014 leaves the PECR check to decide)
    And it names no other thing stored on your device, because theme and text size are stored nowhere (FE-23, DISP-05) and the sign-in session cookies are a separate section (PRIV-13)

  # FE-74: the reasons, the shapes and internal only; the never-stored list and the 90 days are the pilot design 2026-11-13 goal 7, the pilot design batch section 4 and REPORT-26, REPORT-28.
  @ui
  Scenario: PRIV-07 "Report a problem counts" says what is counted, for how long, and that nothing identifies you
    Given the user has opened "Privacy notice"
    When the user reads "Report a problem counts"
    Then it says a report is counted per day, with the source, the topic or the figure, the area or the fact's public record ID and the reason ("Wrong", "Out of date" or "Missing something"), and there is no free text (FE-74)
    And it says the postcode, a row for each report, a time finer than the day, and any client key or IP address are never stored, that the counts are kept 90 days (the pilot design batch, section 4; REPORT-26, REPORT-28), and that they are used only by us to see what needs checking and are never published (FE-74)
    And the lawful basis and the retention wording around the 90 days read exactly "To be written before launch (SE-02)"

  # 0063 point 4 and BE-42 (20 Nov 2026), FE-86 (21 Nov 2026): ALTCHA, self-hosted, runs on the chat's consent tap. Replaces the 2026-11-13 wording for the chat. Report a problem also sits behind the bot check (REPORT-13); ALTCHA is decided only for the chat, so the provider for Report a problem stays a placeholder unless a record decides it.
  @ui
  Scenario: PRIV-08 "The bot check" says ALTCHA runs on the chat's consent tap, and names the bot check for Report a problem
    Given the user has opened "Privacy notice"
    When the user reads "The bot check"
    Then it says that for the chat the check is ALTCHA, a proof-of-work check that your device runs and that is checked on our own server, so no outside company sees you (0063 point 4; BE-42)
    And it says the chat's check runs when you tap "Agree and start chat", and again after a set number of messages (FE-86), sets no cookies and stores nothing on your device (0063)
    And it says that when you report a problem a bot check also runs (REPORT-13), and its provider reads exactly "To be written before launch (SE-02)" unless a record decides it
    And the retention wording, if the check keeps anything beyond used proofs until they expire (BE-42), reads exactly "To be written before launch (SE-02)"

  # DA-35, 0056 and 0014: an IP address held briefly in memory, never logged.
  @ui
  Scenario: PRIV-09 "Rate limits" says requests are counted per anonymised client and the energy certificate lookup by IP address, in memory, never logged
    Given the user has opened "Privacy notice"
    When the user reads "Rate limits"
    Then it says that to stop one visitor copying the whole dataset, we count requests to the website per anonymised client key, kept briefly and never written to a log (0056; the pilot design 2026-11-13, Abuse line), and that the energy certificate lookup is counted by IP address, held in memory only (DA-35; 0014)
    And it says calls from ChatGPT or Claude are limited by an overall cap and a cap for each app, not for each person (0057, 0051)
    And it says an IP address can be personal data, and the lawful basis reads exactly "To be written before launch (SE-02)"

  # FE-11: each outbound link names its destination and says when it carries the postcode; nothing is sent until the click.
  @ui
  Scenario: PRIV-10 "Links to other sites" says which links carry the postcode and that nothing is sent until you click
    Given the user has opened "Privacy notice"
    When the user reads "Links to other sites"
    Then it says some links in an area check carry the postcode to another site, that each link says so before you click, and that nothing is sent until you click (FE-11; 0014)
    And it names the sites that receive the postcode when a link is clicked, as the area check's links do (AREA-18), including Google Maps and its satellite view, "Google will see this postcode" (FE-11), and the page does not say "for example", as if Google were the only one
    And the full list of sites that receive the postcode is a placeholder reading "To be written before launch (SE-02)" until the build fixes which links carry the postcode (FE-11 lets any site that accepts it)
    And it says the links open with no referrer (`rel="noreferrer"`) and never pass through our logs

  # 0056 decision 2 and 0057: the host's own terms; what hosts send; anonymous totals; the record is Proposed.
  @ui
  Scenario: PRIV-11 "Using Vestagraph in ChatGPT or Claude" says the host's terms apply and what we keep
    Given the user has opened "Privacy notice"
    When the user reads "Using Vestagraph in ChatGPT or Claude"
    Then it says your own ChatGPT or Claude does the AI work under its own terms, and Vestagraph's server only returns sourced facts (0056)
    And it says ChatGPT may send, with a tool call, an anonymised user ID and conversation ID, an anonymised organisation ID when there is one, a rough location, a device hint and your language, that we do not ask for these, and that Claude sends nothing documented beyond the question's details (0057)
    And it says we keep none of it, count calls per day by tool, host, outcome, city, region, country and language, and never keep what you asked (0057), with any daily total below 10 shown as "fewer than 10", and that the totals have no end date (0057)
    And the section carries a visible line that its wording is a draft to be confirmed before launch, because 0057 (SE-05) is still Proposed (proposed wording: "Draft wording, to be confirmed before launch (0057).")
    And the lawful basis and the retention wording around the totals read exactly "To be written before launch (SE-02)" (0057 only proposes legitimate interests and chooses none)

  # DA-09: never logged; open building fields only; the design says never stored. DA-35: the lookup limit is keyed by IP address, not by the certificate number.
  @ui
  Scenario: PRIV-12 "Energy certificate numbers" says the number is never stored or logged
    Given the user has opened "Privacy notice"
    When the user reads "Energy certificate numbers"
    Then it says that when you enter a certificate number, we send the number to the government's energy certificate register to fetch that certificate, and the number is never logged and never stored (DA-09; 0014; the pilot design batch, section 6)
    And it says the lookup limit is counted in memory by IP address and never by the certificate number (DA-35)
    And it says only the certificate's open building fields are shown, never the address or postcode fields (DA-09)
    And the lawful basis reads exactly "To be written before launch (SE-02)"

  # 0063 (20 Nov 2026; sign-in waits until later, point 2), 0064 (20 Nov 2026: provider, 14 days, Neon, LangSmith EU) and the design's section 5. Replaces 0058's account, 12-month, 24-month and 30-day wording, which no longer applies in the pilot.
  @ui
  Scenario: PRIV-13 "The chat" says there is no sign-in, who handles your messages, where and for how long
    Given the user has opened "Privacy notice"
    When the user reads "The chat"
    Then it says there is no sign-in in the pilot: no account, saved area or chat history is kept, and the chat works without one (0063 point 2)
    And it says your messages, including any health or similar details you type, go to Anthropic, which processes them in the US or "global", deletes them within 30 days, and keeps content its systems flag for up to 2 years (0064; the DPA's UK Addendum is the safeguard for the transfer, Article 13(1)(f))
    And it says the words of real chats are kept 14 days in our own Neon database (London), with the identifier filter and the consent receipt, then deleted, and gone from Neon's 7-day history a week later (0064, 0063 point 5)
    And it says traces without the words go to LangSmith (LangChain) in its EU region (the Netherlands), as a processor of trace data only (0064)
    And it says the IP address is used in memory for the day's count of 15 messages and is never stored (0063 point 3)
    And it says special category details, such as health details, are handled only on your explicit consent, given when you tap "Agree and start chat" (0063 point 5; UK GDPR Article 9(2)(a))
    And it says the chat sets no cookies and stores nothing on your device (0063)
    And it says the AI model that writes chat answers may not use your chats for training (0064 point 3, "No training on our content")

  # Design sections 5 and 7: Article 7(3) and 13(2)(c) (withdrawing consent), 13(2)(d) (the right to complain), UK GDPR Article 11(2) (acting when the trace can be found). Source: https://www.legislation.gov.uk/eur/2016/679/article/13, read 21 Nov 2026. The other rights (access, deletion, objection) wait for SE-02.
  @ui
  Scenario: PRIV-14 "Your rights" and "Contact" give privacy@vestagraph.co.uk, withdrawing consent and the ICO
    Given the user has opened "Privacy notice"
    When the user reads "Your rights" and "Contact"
    Then "Contact" gives privacy@vestagraph.co.uk, the same contact as "Who we are" (PRIV-04)
    And "Your rights" says you can withdraw your consent at any time: stop using the chat, and email privacy@vestagraph.co.uk to have kept words deleted
    And it says we find a kept chat case by case: if you give enough to find it, we act on it (UK GDPR Article 11(2); 0063 point 5)
    And it says you have the right to complain to the ICO and links https://ico.org.uk/make-a-complaint/
    And the other rights wording, such as access, deletion and objection, reads exactly "To be written before launch (SE-02)" until it is written

  @ui
  Scenario: PRIV-15 the page links back and to the related pages
    Given the user has opened "Privacy notice"
    When the user chooses "← Back to Vestagraph"
    Then the landing page opens
    And the sections on ChatGPT or Claude and on links to other sites link "Use in ChatGPT or Claude" (HOWTO-16, HOWTO-17) and "About the data", and "Privacy notice" is in the footer of every page

  @ui
  Scenario: PRIV-16 the page works by keyboard, with 44 px targets, on a phone and on desktop
    Given the user has opened "Privacy notice" on a phone (390 px wide) and on desktop
    When the user works through the page by keyboard
    Then every link can be reached and used in reading order, each at least 44 px tall, with the focus visible, and nothing scrolls sideways at 390 px
    And a placeholder box is read by a screen reader as text, with its words "To be written before launch (SE-02)" and not hidden behind a style

  @ui
  Scenario: PRIV-17 the dark twin shows the same sections, with the placeholders still plain
    Given the user has chosen the dark theme
    When the user opens "Privacy notice"
    Then the same sections and wording show in WCAG 2.2 AA contrast, and each placeholder is still visibly different from finished text

  # Decision 0059 (DA-37): the basemap comes from OpenFreeMap's public servers. The section sits after "Links to other sites" (PRIV-02). Added after PRIV-17 so no ID moves.
  @ui
  Scenario: PRIV-18 "Maps" says each map view sends your IP address and the map area to OpenFreeMap
    Given the user has opened "Privacy notice"
    When the user reads "Maps"
    Then it says the map's background tiles come from OpenFreeMap, a map service run by a company other than us, and that map data is requested only when you choose "Show map" (FE-75), and then your browser asks OpenFreeMap for the tiles for the area on screen, which is the area around the postcode you checked, so OpenFreeMap receives your IP address and that area, under its own policy (0059)
    And it says OpenFreeMap says it uses no cookies, no keys and no accounts, and its privacy policy (read 19 Nov 2026) says it does not store IP addresses in its access logs, that an error log may include the IP address and the address requested, that if it detects abuse or a security threat it may switch IP logging on for up to 30 days to investigate, and that server logs are deleted after 7 days (after at most 30 days for a security incident) (0059)
    And it says OpenFreeMap's policy says it may use Cloudflare as a CDN, and that Cloudflare may collect certain information under its own privacy policy (0059)
    And our own lawful basis and retention wording read exactly "To be written before launch (SE-02)" (0059: the policy and terms are read again before launch)
    And it says that if the map cannot load, the facts still show (MAP-27)

  # Added after review (19 Nov 2026): 0014 says the notice covers what hosting and security services handle. Hosting (IN-02) was undecided then; 0060 (19 Nov 2026) chose Hetzner, Neon and a Cloudflare proxy (0067, 23 Nov 2026: an OVHcloud server and Neon, both in London), and the wording is written with the privacy work (SE-02), so this stays a placeholder until then. Added after PRIV-18 so no ID moves.
  @ui
  Scenario: PRIV-19 "Hosting and security" is a placeholder, so the list of recipients does not read as complete
    Given the user has opened "Privacy notice"
    When the user reads "Hosting and security", which sits after "The chat" (PRIV-02)
    Then it reads exactly "To be written before launch (SE-02)", shown as a placeholder (PRIV-03), and names no host, security service or retention (the wording waits for SE-02)

  # Added 21 Nov 2026 (anonymous chat design, section 7; decisions 0063, 0064): Article 13(1)(c) and 13(2)(a). Added after PRIV-19 so no ID moves.
  @ui
  Scenario: PRIV-20 the chat's purposes and lawful basis are stated for each processing
    Given the user has opened "Privacy notice"
    When the user reads "The chat"
    Then for each processing it says its purpose and its lawful basis (Article 13(1)(c)): answering your questions and the day's limit and bot check are on legitimate interests (0063 point 9, with a written assessment for each); keeping chat words 14 days to fix problems is on legitimate interests; special category details such as health details are on your explicit consent (Article 9(2)(a)); answering privacy requests is on legal obligation (0063 point 9)
    And it says anonymous daily counts are not personal data (0063 point 9)
    And no lawful basis is stated for a processing that no record decides (rule 1)

  @ui
  Scenario: PRIV-21 the chat's keeping periods are stated
    Given the user has opened "Privacy notice"
    When the user reads "The chat"
    Then it states each keeping period (Article 13(2)(a)): Anthropic deletes within 30 days and keeps flagged content up to 2 years; our Neon table keeps the words 14 days and Neon's history 7 days more; LangSmith keeps its traces, which have no words, 14 days (0064); the IP address is not kept (PRIV-13)
    And it names no period that no record decides (rule 1), and gives no keeping period for the chat's daily totals (none is decided); Report a problem's 90 days are PRIV-07's

  # ---- Accessibility (design section 7) ----

  @ui
  Scenario: A11Y-01 the page states the target as WCAG 2.2 level AA
    Given the user is on the landing page
    When the user opens "Accessibility" from the footer
    Then the page "/accessibility" opens with the heading "Accessibility"
    And it says the aim is to meet WCAG 2.2 level AA and links the standard ([W3C](https://www.w3.org/TR/WCAG22/))
    And it says "aim" or "target", not that the aim is met

  @ui
  Scenario: A11Y-02 the page says the site has not been tested yet
    Given the user has opened "Accessibility"
    When the user reads the status
    Then it says Vestagraph has not been tested yet, in the words "has not been tested yet"

  @ui
  Scenario: A11Y-03 the test results and known issues are a placeholder
    Given the user has opened "Accessibility"
    When the user looks for the test results and known issues
    Then they read exactly "To be completed after testing, before launch"
    And the placeholder is shown plainly as a placeholder, not as finished text, and names no tool, date, score, result or issue (rule 1)

  # Rule 1: no conformance claim before a test.
  @ui
  Scenario: A11Y-04 the page never claims conformance
    Given the user has opened "Accessibility"
    When the user reads the whole page
    Then it never says the site "conforms", "complies", "is compliant", "is accessible to everyone" or "meets" WCAG, and states no conformance level as achieved

  @ui
  Scenario: A11Y-05 the contact route stays a placeholder (the Privacy notice's contact is a privacy route only)
    Given the user has opened "Accessibility"
    When the user looks for how to report an accessibility problem
    Then it reads exactly "Contact details to be added before launch", with no email address, form or phone number (the Privacy notice's contact, PRIV-14, is a privacy route only, so this stays a placeholder until an accessibility contact is decided)

  @ui
  Scenario: A11Y-06 the page names no enforcement or complaints route, because none is decided
    Given the user has opened "Accessibility"
    When the user reads the page
    Then it names no regulator, no complaints procedure and no legal duty (no record decides one; rule 1)

  @ui
  Scenario: A11Y-07 the page links back and is linked from the footer
    Given the user has opened "Accessibility"
    When the user chooses "← Back to Vestagraph"
    Then the landing page opens
    And "Accessibility" is in the footer of every page (HOWTO-31)

  @ui
  Scenario: A11Y-08 the page works by keyboard, with 44 px targets, on a phone and on desktop
    Given the user has opened "Accessibility" on a phone (390 px wide) and on desktop
    When the user works through the page by keyboard
    Then every link can be reached and used in reading order, each at least 44 px tall, with the focus visible, and nothing scrolls sideways at 390 px

  @ui
  Scenario: A11Y-09 the dark twin shows the same wording, with the placeholder still plain
    Given the user has chosen the dark theme
    When the user opens "Accessibility"
    Then the same wording shows in WCAG 2.2 AA contrast, and the placeholder is still visibly different from finished text
