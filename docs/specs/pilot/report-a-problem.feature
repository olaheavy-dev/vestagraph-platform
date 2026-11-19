@screen @buying @renting
Feature: Report a problem with this fact (a reason, counted per fact per day, never a person)
  Question it answers: "Can I tell Vestagraph that a fact looks wrong, out of date or missing, without giving anything about myself?"
  Modes: both (and anyone, with no account; decisions 0014 and 0046)
  Added 19 Nov 2026 (pilot design batch, PR 1; design `docs/superpowers/specs/2026-11-19-pilot-design-batch-design.md`, section "4. Report a problem with this fact"; plan Tasks 1 and 2; register lines FE-05 (amended), FE-74, DA-12; pilot design `2026-11-13-pilot-area-ai-design.md` goal 7; decisions 0014, 0053). Founder's choices, 19 Nov 2026: "Pick a reason (Recommended)" and "Also City Explorer". The count's data contract is `packages/fixtures/schema/problem-report-counts.schema.json` with the sample `packages/fixtures/data/problem-report-counts.json` (plan Task 1, FE-74).
  Fixtures: the sample counts `packages/fixtures/data/problem-report-counts.json` (the data scenarios quote it by topic, record ID and area code; no count is typed here), and for the gap scenario the sample's sparse postcode NB7 1RR (`area-result.json`). Rule 2: a count's value is never typed or shown in a scenario; the counts are internal and are not on any page (REPORT-28).
  Where it appears (founder's choice 5, and the agent's call for the signed-in chat's side panel, open to the founder): on each fact in a topic's detail (sheet or panel) on the area result (REPORT-01), on compare (REPORT-02), on City Explorer's council page and council compare detail (REPORT-03) and neighbourhood page (REPORT-04), and in the signed-in chat's side panel, which shows the full area result (REPORT-05). Where it does not: summary lines (REPORT-06), the energy certificate page (REPORT-07), the area card and the compare table in the chat (REPORT-08) and the ChatGPT and Claude widget (REPORT-09).
  Rule 7: a gap (the record's own gap line, "Not known right now", "Not yet covered") can be reported too, and "Missing something" is its natural reason (REPORT-11).
  0014: nothing is stored on the visitor's device; "Reported" lives in the page's memory only (REPORT-16).
  Boards: `ReportProblem` (phone cards and the desktop panel; area topic detail) with `ReportProblemDark`, in the canvas section 'Pilot 8 · Compare, share, report', and `CouncilReportProblem` with `CouncilReportProblemDark` on the page 'Pilot · City Explorer' (section City Explorer 4); canvas version 1795107206-3e0d, 19 Nov 2026. Compare's detail with its links is on `ComparePhone` and `CompareDesktop`. REPORT-04 (a neighbourhood fact) and REPORT-05 (the chat's side panel) follow REPORT-01's anatomy and have no board of their own.
  Wording status: approved by the founder (design, 19 Nov 2026): the reasons "Wrong", "Out of date", "Missing something" and "Report a problem". Proposed, for the founder's copy review before build: "Thanks. We count reports for each fact to see what needs checking. We can't reply." (REPORT-15), "What's wrong with this fact?" (the heading of the choices, REPORT-12), "Reported" (REPORT-16), "Couldn't send. Try again." (REPORT-17, REPORT-19) and "You're offline. Try again when you're back online." (REPORT-18), and "Cancel" on the choices (REPORT-14). The design marks these as the agent's wording.
  One state needs a sample record that does not exist: the fact count (REPORT-21) is keyed by the SOURCE's own public identifier for a place or zone (a school URN, a NaPTAN stop code, a flood warning area code), and no sample record carries one; the sample uses a made-up code and the gap is tracked as `noticed` issue #349. Every other data scenario quotes the sample counts. A state with no sample (the failures) is a page behaviour, so it is `@ui`.
  Data scenarios (no tag) check the sample counts with the report steps in docs/specs/README.md. Every other scenario is `@ui`, because the outcome is on the page or in a request.

  Required states (design "States to cover"; AGENTS.md rule 7 and 0014):
    link on a fact -> REPORT-01 to REPORT-05; not on summary lines or elsewhere -> REPORT-06 to REPORT-09; a gap reportable -> REPORT-10, REPORT-11
    choices open -> REPORT-12 to REPORT-14
    sent -> REPORT-15, REPORT-16
    failed -> REPORT-17
    offline -> REPORT-18
    rate limited -> REPORT-19
    what is sent and checked -> REPORT-20, REPORT-31
    the three count shapes -> REPORT-21 to REPORT-24 (a fact with a record ID, a fact that points to one address or a gap, a council or neighbourhood figure)
    never a postcode, a time, free text or an address -> REPORT-25 to REPORT-27
    kept 90 days, internal only -> REPORT-28, REPORT-29
    keyboard, size, dark twin -> REPORT-30

  # ---- Where it appears ----

  @ui
  Scenario: REPORT-01 each fact in a topic detail on the area result has "Report a problem"
    Given the result for "NB1 4XY" is open
    When the visitor opens a topic's detail (a sheet on a phone, a panel on desktop), for example "Schools"
    Then each fact in the detail has its own small "Report a problem" link, after the fact and before its source stamp
    And the link is a button with an accessible name that names the fact

  @ui
  Scenario: REPORT-02 each fact in a compare detail has "Report a problem" for its own postcode
    Given the visitor has compared "NB1 4XY" and "NB7 1RR" and opened the "Schools" detail
    When the visitor reads each postcode's facts in the detail
    Then each fact has its own "Report a problem", and a report from one postcode's fact is about that fact only (COMPARE-35)

  @ui
  Scenario: REPORT-03 City Explorer's council page facts and council compare details have "Report a problem"
    Given the visitor has opened the council page for council "E06999001", and a council compare detail (CITY2-01 onwards)
    When the visitor reads a council figure or a fact in a sheet, for example the council tax by band
    Then each has "Report a problem", and a report from council compare is about the figure of the council it sits under
    And the council printout carries no link (it is paper)

  @ui
  Scenario: REPORT-04 City Explorer's neighbourhood page facts have "Report a problem"
    Given the visitor has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the visitor reads a neighbourhood fact
    Then each fact has "Report a problem", and a report is about that neighbourhood's fact, never an address

  @ui
  Scenario: REPORT-05 the signed-in chat's side panel topic details have the link, because the side panel shows the full area result
    Given a signed-in visitor has opened an area result in the chat's side panel (WCHAT)
    When the visitor opens a topic's detail in the panel
    Then each fact has "Report a problem" as on the area result (REPORT-01), and a report sent from the panel is counted as the same fact's (agent's call, open to the founder)
    And a report from a signed-in visitor is counted exactly as an anonymous one: the account, session and cookie are not read for the count, not logged and not kept, and the rate limit does not key on the account beyond memory (agent's call, pre-push security review, open to the founder)

  # ---- Where it does not appear ----

  @ui
  Scenario: REPORT-06 the summary lines have no link
    Given the result for "NB1 4XY" is open
    When the visitor reads the rows of the result
    Then no row's summary line has "Report a problem" (it is only in a topic's detail), and no row has a second tap target for it

  @ui
  Scenario: REPORT-07 the energy certificate page has no link
    Given the visitor has opened a certificate on "/energy-certificate" (ENERGY-01 onwards)
    When the visitor reads the page
    Then no "Report a problem" appears on it, because it shows one certificate's own record and not an area fact

  @ui
  Scenario: REPORT-08 the area card and the compare table in the chat have no link
    Given a signed-in visitor has an area card and a compare table in the chat
    When the visitor reads the card, its expanded dialog and the table
    Then none has "Report a problem" (the chat's widgets are compact cards, not the area result)

  @ui
  Scenario: REPORT-09 the ChatGPT and Claude widget has no link
    Given an area result is shown in ChatGPT or Claude by the widget (0056)
    When the visitor reads it
    Then there is no "Report a problem", and the widget sends nothing to the report count

  # Gaps (design: "Missing something" is the natural reason).
  # fixture: packages/fixtures/generated/area-result.json (NB7 1RR)
  Scenario: REPORT-10 the sparse sample has gaps a visitor could report
    Then area result "NB7 1RR" has topic "flood" with outcome "not-known"
    And area result "NB7 1RR" has topic "green-space" with outcome "not-covered"
    And postcode record "NB7-1RR-AREA-SOLD-PRICE-1" has status "no-record-in-source"

  @ui
  Scenario: REPORT-11 a gap can be reported, and "Missing something" is its natural reason
    Given the result for "NB7 1RR" is open
    When the visitor opens the "Sold nearby" detail, where its source has no record, and chooses "Report a problem"
    Then the link is there on a record's own gap line (for example "No sold prices nearby in this source"), on "Not known right now" and on "Not yet covered", as on a fact, and the three reasons are offered
    And the report is counted by topic and council only, with no record ID (REPORT-22)

  # ---- The choices ----

  @ui
  Scenario: REPORT-12 the tap opens three fixed choices and Cancel
    Given a fact's "Report a problem" is shown
    When the visitor chooses it
    Then three choices open under the heading "What's wrong with this fact?" (proposed wording), "Wrong", "Out of date" and "Missing something", with "Cancel" (proposed wording), and nothing is sent yet
    And no text field is offered, because a report has no free text

  @ui
  Scenario: REPORT-13 choosing a reason sends the report behind the invisible bot check
    Given the three choices are open
    When the visitor chooses "Out of date"
    Then the report is sent with the reason "out-of-date" behind the invisible bot check (0014 part 1), with no question for the visitor
    And "Wrong" sends "wrong" and "Missing something" sends "missing-something", and no other reason exists

  @ui
  Scenario: REPORT-14 Cancel closes the choices and sends nothing
    Given the three choices are open
    When the visitor chooses "Cancel", or presses Escape
    Then the choices close, focus returns to the "Report a problem" link, and nothing is sent or remembered

  # ---- Sent ----

  @ui
  Scenario: REPORT-15 after sending, the page says thanks and that we can't reply
    Given the visitor has chosen a reason and the report was sent
    When the page answers
    Then it says "Thanks. We count reports for each fact to see what needs checking. We can't reply." (proposed wording, for the founder's copy review), announced to a screen reader
    And it does not say the fact was changed, checked or fixed

  @ui
  Scenario: REPORT-16 "Reported" stays on that fact until the page is closed and nothing is stored on the device
    Given a report was sent for a fact
    When the visitor reads the fact again, then closes the page and opens it again
    Then the fact shows "Reported" (proposed wording) until the page is closed, kept in the page's memory only
    And after the page is reopened the fact shows "Report a problem" again, and nothing was written to the browser (no cookie, storage or cache), because "already reported" on this device would need PECR consent

  # ---- Failures ----

  @ui
  Scenario: REPORT-17 a failed send says "Couldn't send. Try again." and the choices stay available
    Given the visitor has chosen a reason and the bot check failed or the server answered with an error
    When the page answers
    Then it says "Couldn't send. Try again." (proposed wording) and the fact is not marked "Reported"
    And the choices can be opened again, and no free text or detail of the failure is shown

  @ui
  Scenario: REPORT-18 offline says so and the report is not queued
    Given the visitor has chosen a reason and the device is offline
    When the page answers
    Then it says "You're offline. Try again when you're back online." (proposed wording) and the fact is not marked "Reported"
    And nothing is held on the device to send later

  @ui
  Scenario: REPORT-19 a rate limit gives the same wording as a failure, so it reveals nothing
    Given the visitor has reached the report rate limit (its number is set at build within the pilot caps; not yet decided; tracked with the other pilot rate limits, DA-35 and 0056, a launch blocker)
    When the visitor chooses a reason
    Then the page says "Couldn't send. Try again." exactly as in REPORT-17, with no mention of a limit, a count or a time
    And no IP address or client key is kept to apply the limit beyond a short time in memory, as for the other limits (DA-35, 0056 for the mechanism only; 0014)

  # ---- What is sent ----

  @ui
  Scenario: REPORT-20 the request carries the fact and the reason, never the postcode
    Given the visitor reports a fact on the result for "NB1 4XY"
    When the report is sent
    Then the request body holds the source, the topic, the fact's record ID only where REPORT-21 allows one, the council and the reason, and nothing else
    And it holds no date: the server stamps the day itself (Europe/London) when it counts, so a client cannot back-date or future-date a count
    And it holds no postcode (the area is the council's code), is not in a query string, and is not written to a server, application, hosting or tracing log
    And the record ID is the SOURCE's own public identifier for that place or zone (a school URN, a NaPTAN stop code, a flood warning area code), never Vestagraph's record `id`, which holds the postcode (agent's call, pre-push security review, open to the founder)

  @ui
  Scenario: REPORT-31 the server accepts only values it served on that page
    Given the page served the topic, the figure, the council or area code and the record IDs of the facts on it
    When a report arrives whose topic, source, figure, area code or record ID is not one the server served on that page, or whose topic is not a counted topic of the registry
    Then it is refused silently with the same wording as a failure ("Couldn't send. Try again.", REPORT-17), and nothing is stored or logged
    And a value the client made up (an address, a name, a postcode, a very long ID) never reaches a count, because the count's contract allows known keys only (`problem-report-counts.schema.json`)

  # ---- The three count shapes (design section 4; data contract of plan Task 1) ----

  # fixture: packages/fixtures/data/problem-report-counts.json (the fact count: a flood warning area, no address)
  # fixture needed: #349 (no sample record carries a source's own identifier; the sample's SYNTHETIC-FWA-001 is made up)
  # Only a topic whose records are public facilities or official zones may carry a record ID: getting-around (a stop; not bus departures), everyday-places (a GP surgery, a hospital, a pharmacy or another public place; not childcare, which is home-based), schools and flood (a flood warning area; not flood risk by postcode). Every other topic, and a record worked out from the postcode, is counted by topic and council only (REPORT-22). The ID is the source's own identifier, never Vestagraph's record `id`.
  Scenario: REPORT-21 a fact with a record ID that names a public place or zone is counted by topic, record and reason
    Then the problem report counts hold a fact count for topic "flood" with record "SYNTHETIC-FWA-001" and reason "out-of-date"

  # fixture: packages/fixtures/data/problem-report-counts.json (sold prices and planning point to one address or site). Every topic off REPORT-21's list (places of worship, crime, broadband, air quality, radon, council tax, affordability, deprivation, transport connectivity, green space) and a gap with no record have the same shape (design section 4), which the schema allows and the sample does not hold a separate count for; the step cannot tell them apart.
  Scenario: REPORT-22 a fact that points to one address, or is not on the record ID list, is counted by topic and council with no record ID
    Then the problem report counts hold an area count for topic "sold-nearby" with reason "wrong" and no record ID
    And the problem report counts hold an area count for topic "planning-nearby" with reason "missing-something" and no record ID

  # fixture: packages/fixtures/data/problem-report-counts.json (a council figure and a neighbourhood figure, public area codes)
  Scenario: REPORT-23 a council or neighbourhood figure is counted by the figure's name and the area's public code
    Then the problem report counts hold a figure count for "council-tax-band-d" at level "council" for area "E06999001"
    And the problem report counts hold a figure count for "deprivation" at level "neighbourhood" for area "E01999011"

  # fixture: packages/fixtures/data/problem-report-counts.json
  Scenario: REPORT-24 every count has one of the three fixed reasons
    Then every problem report count has one of the three fixed reasons

  # ---- What is never stored ----

  # fixture: packages/fixtures/data/problem-report-counts.json
  Scenario: REPORT-25 no count holds a postcode or an address
    Then no problem report count has a "postcode" field
    And no problem report count has a "address" field

  # fixture: packages/fixtures/data/problem-report-counts.json
  Scenario: REPORT-26 no count holds a time finer than the day, free text, a client key or an IP address
    Then every problem report count date is a day with no time
    And no problem report count has a "time" field
    And no problem report count has a "comment" field
    And no problem report count has a "clientKey" field
    And no problem report count has a "ipAddress" field

  # fixture: packages/fixtures/data/problem-report-counts.json
  Scenario: REPORT-27 no count is a per-report row
    Then no problem report count has a "reportId" field
    And no problem report count has a "userId" field
    And no two problem report counts share the same key
  # The key is the date, the shape fields (topic, record ID, council or figure, area code and level) and the reason, so five reports of one fact on one day are one count.

  # fixture: packages/fixtures/data/problem-report-counts.json
  Scenario: REPORT-28 counts are kept for 90 days
    Then the problem report counts are kept for 90 days

  @ui
  Scenario: REPORT-29 the counts stay internal and are never shown on the site
    Given counts exist for a fact
    When any visitor reads that fact, its detail or any page
    Then no count, no "reported N times" and no list of reports is shown, and nothing of the counts is published
    And publishing them would need its own decision (small-number rules, SE-05)
    And the founder reads a count as a signal only, to decide what to check; one actor can inflate it (the bot check and rate limit only slow that), so no decision rests on a count alone

  @ui
  Scenario: REPORT-30 Report a problem works by keyboard, with 44 px targets and a dark twin
    Given the visitor has opened a topic detail on a phone and on desktop
    When the visitor works through the link, the choices, Cancel and the answer by keyboard
    Then every control can be reached and used, each at least 44 px tall, the focus is visible and returns to the link, and nothing scrolls sideways at 390 px
    And the dark twin shows the same states in WCAG 2.2 AA contrast
