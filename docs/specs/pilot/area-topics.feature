@screen @buying @renting
Feature: Topic sheet and panel (one topic of an area result, opened from its row)
  Question it answers: "What does the source say about this one topic, which area does it cover, and what is left for me to check?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: the postcode-level sample area data, `packages/fixtures/data/postcode-area.json`
    (NB1 4XY normal, NB7 1RR sparse and failed flood); distances and walking times come from
    `packages/fixtures/generated/area-result.json` (the tested `vestagraph_area` package, FE-38);
    figures: none typed here.
  What it is: one anatomy for four kinds of topic (a list of places, figures for an area, an
    official ranking or standard, and a warning; design spec, "The four kinds"); route-only topics show
    "Not yet covered" (TOPIC-12). A phone shows it as a bottom sheet, desktop as a panel beside the list in place of the
    map, one at a time (FE-26). Every topic opens in the same order (B29).
  Scenarios are grouped by topic, so IDs are not in numeric order.
  Rule 2: no distance, time, count or date is typed in a scenario; the page quotes values from the records
    named by ID in `postcode-area.json` and from `area-result.json`.
  Rule 7: a gap is named and never reads as zero, "none", a miss or a clean result. The search distance
    beside a gap label is the display-unit distance (miles): the search limit `SEARCH_LIMIT_METRES` in `packages/vestagraph-area/src/vestagraph_area/priorities.py`, shown in the display unit, miles, by `vestagraph_area.distance.display_distance` (DA-20, B2); `area-result.json` does not hold it.
  Required states (design docs/superpowers/specs/2026-11-14-first-design-batch-design.md;
    AGENTS.md rules 2, 4 and 7):
    gap, "no record in this source" with its search distance -> TOPIC-09, TOPIC-10
    stale record, the date is the fact and stays shown, no status word -> TOPIC-05, TOPIC-23
    failed copy, our stored copy of a source is missing or failed (AREA-07, FE-38) -> TOPIC-25 (TOPIC-20 is withdrawn)
    no map, topics with no places or never mapped -> TOPIC-06, TOPIC-08, TOPIC-19, TOPIC-21, TOPIC-12
    the shared order of every topic -> TOPIC-01
    phone sheet and desktop panel behaviour -> TOPIC-02, TOPIC-03, TOPIC-15, TOPIC-16
    Schools -> TOPIC-04, TOPIC-13, TOPIC-14
    Recorded crime -> TOPIC-06, TOPIC-21, TOPIC-22
    Deprivation -> TOPIC-07
    Flood -> TOPIC-08, TOPIC-17, TOPIC-18, TOPIC-19
    Explain this, reviewed text or not yet available -> TOPIC-11, TOPIC-24
    route-only topic -> TOPIC-12
    design pass, 16 Nov 2026 (canvas version 405; plan docs/superpowers/plans/2026-11-16-benchmark-design-pass.md Task 6b; DA-22 to DA-31, FE-69):
      Radon (counted; 1 km square; indicative, not definitive; UKradon link) -> TOPIC-26 to TOPIC-29
      Broadband as the gigabit-capable share of premises, no full-fibre claim -> TOPIC-30, TOPIC-31
      council-wide rent inside Housing affordability, from the council by link -> TOPIC-32 to TOPIC-34
      Check this rows (long-term flood risk, Article 4 and tree preservation orders, council tax band of a home, mobile, coal mining, noise), never implying a check -> TOPIC-35 to TOPIC-39
      the energy certificate of a home row, which opens its own page and shows no result -> TOPIC-41
      the map layers each topic draws -> TOPIC-40

  @ui
  Scenario: TOPIC-01 every topic opens in the same order
    Given the result for a sample postcode is open
    When the visitor opens any topic
    Then the topic shows, in this order: title and headline (the row's own line), your priority result if one is set, facts with the area each covers, the map where the topic has places, gaps, what to do next, Explain this, source stamps (B29)

  @ui
  Scenario: TOPIC-02 on a phone a topic opens as a bottom sheet with Close
    Given the result for a sample postcode is open on a phone
    When the visitor opens a topic
    Then a bottom sheet opens with a "Close" control

  @ui
  Scenario: TOPIC-15 Escape or Back closes the sheet and focus returns to the row
    Given a topic sheet is open on a phone
    When the visitor presses Escape or the phone's Back
    Then the sheet closes
    And focus returns to the row that opened it

  @ui
  Scenario: TOPIC-16 the open topic has its own link
    Given a topic is open
    Then the "#" part of the address names that topic, as it does the postcode (AREA-03), so the link opens the result with that topic open (B14)

  # Withdrawn: it read "failed copy" as copying a link to the clipboard, which no decision or board designs.
  # The real state, our stored copy of a source failing, is TOPIC-25. The ID is kept and never reused.
  @ui @withdrawn
  Scenario: TOPIC-20 a failed copy of the topic link says so
    Given a topic is open
    When the visitor copies the topic's link and the copy fails
    Then a message says the link could not be copied
    And the link is still shown so the visitor can copy it by hand

  @ui
  Scenario: TOPIC-25 a topic whose stored source copy failed reads Not known right now
    Given the result for "NB7 1RR" is open
    When the visitor opens "Flood"
    Then the facts read "Not known right now"
    And it says this is not the same as no warning (DA-12)
    And no warning status from an old copy is shown (AREA-07, FE-38)

  @ui
  # Changed 17 Nov 2026 (Codex review of the design-pass specifications): the desktop result keeps the map in its header, so an opened topic replaces the right column (AREA-43; FE-26 note, agent's call, approved by the founder on 18 Nov 2026: "Keep all (Recommended)").
  Scenario: TOPIC-03 on desktop a topic opens as a panel in place of the right column
    Given the result for a sample postcode is open on desktop
    When the visitor opens a topic
    Then a panel opens beside the list in place of the right column (Check in person and places), and the map stays in the header (AREA-43)
    And only one topic is open at a time (FE-26)
    And focus moves to the panel's heading

  @ui
  Scenario: TOPIC-04 the Schools topic lists each school with its facts
    Given the result for "NB1 4XY" is open
    When the visitor opens "Schools"
    Then each school is listed with its phase and type quoted from its school record in `postcode-area.json` (`NB1-4XY-AREA-SCHOOL-1` and `-2`), and its distance and walking time quoted from `area-result.json`
    And each school shows its inspection date and framework

  @ui
  Scenario: TOPIC-13 the Schools topic quotes the admissions figures from their records
    Given the result for "NB1 4XY" is open
    When the visitor opens "Schools"
    Then the admissions figures are quoted from records "NB1-4XY-AREA-SCHOOL-DEMAND-1" and "NB1-4XY-AREA-SCHOOL-DEMAND-2"

  @ui
  Scenario: TOPIC-14 the desktop Schools panel has its own small map
    Given the result for "NB1 4XY" is open on desktop
    When the visitor opens "Schools"
    Then the panel shows its own small map of the schools

  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY)
  Scenario: TOPIC-05 the school inspection record is stale
    Then postcode record "NB1-4XY-AREA-SCHOOL-INSPECTION-1" has status "stale"

  @ui
  Scenario: TOPIC-23 a stale inspection keeps its date shown
    Given the result for "NB1 4XY" is open
    When the visitor opens "Schools"
    Then the inspection date of record "NB1-4XY-AREA-SCHOOL-INSPECTION-1" stays shown as the fact
    And no status word or badge (such as Old or stale) is shown beside it; the source's date is on About the data (FE-33, FE-35)

  @ui
  Scenario: TOPIC-06 Recorded crime shows counts by month and category
    Given the result for "NB1 4XY" is open
    When the visitor opens "Recorded crime"
    Then counts by month and category are quoted from records "NB1-4XY-AREA-CRIME-1" and "NB1-4XY-AREA-CRIME-2"

  @ui
  Scenario: TOPIC-22 Recorded crime says the area it covers and names the neighbourhood team
    Given the result for "NB1 4XY" is open
    When the visitor opens "Recorded crime"
    Then the area covered reads "within 1 mile"
    And the neighbourhood team is named

  @ui
  Scenario: TOPIC-21 Recorded crime is never shown on a map
    Given the result for "NB1 4XY" is open
    When the visitor opens "Recorded crime"
    Then no map is shown for the topic (B5)

  @ui
  Scenario: TOPIC-07 Deprivation quotes the decile and rank in one sentence about the neighbourhood
    Given the result for "NB1 4XY" is open
    When the visitor opens "Deprivation"
    Then one sentence quotes the decile and rank from record "NB1-4XY-AREA-DEPRIVATION-RANK-1"
    And the sentence says which end is most deprived
    And it says "compared with other neighbourhoods"
    And it says it describes the neighbourhood, not this street or home (decision 0054, DA-17)

  @ui
  Scenario: TOPIC-08 Flood warnings say when we last checked
    Given the result for "NB1 4XY" is open
    When the visitor opens "Flood"
    Then the warnings from record "NB1-4XY-AREA-FLOOD-1" read "when we last checked, at" followed by the time of that check

  @ui
  Scenario: TOPIC-17 Flood links to the long-term risk service
    Given the result for "NB1 4XY" is open
    When the visitor opens "Flood"
    Then the long-term flood risk link is shown

  @ui
  Scenario: TOPIC-18 Flood quotes the properties-by-likelihood counts from their record
    Given the result for "NB1 4XY" is open
    When the visitor opens "Flood"
    Then the properties-by-likelihood counts are quoted from record "NB1-4XY-AREA-FLOOD-RISK-POSTCODE-1"

  # Note, 16 Nov 2026 (FE-68, DA-22; design pass): flood outlines are a layer of the 2D street map on the Map screen (MAP-13, MAP-19); the Flood panel board still says "No map yet" (canvas follow-up: issue #314).
  @ui
  Scenario: TOPIC-19 the Flood panel draws no map of its own
    Given the result for "NB1 4XY" is open
    When the visitor opens "Flood"
    Then the Flood panel draws no map of its own; flood outlines are on the Map screen's 2D map (MAP-19)

  @ui
  Scenario: TOPIC-09 a "no record in this source" gap shows its search distance
    Given a topic has a gap where the source holds no record
    When the visitor opens the topic
    Then the gap shows its label, for example "No supermarket found within <the search distance> in this source"
    And the search distance is quoted from the search limit `SEARCH_LIMIT_METRES` in `packages/vestagraph-area/src/vestagraph_area/priorities.py`, shown in the display unit, miles, by `vestagraph_area.distance.display_distance` (DA-20, B2)
    And it never reads as zero or as a clean result

  @ui
  Scenario: TOPIC-10 What to do next lists the gap question and every check-in-person item
    Given a topic has a gap and fixed check-in-person items
    When the visitor opens the topic
    Then "What to do next" lists the gap question
    And it lists every check-in-person item for the topic (FE-39)

  # No sample explanation texts exist yet (one written, one missing): noticed issue #342.
  @ui
  Scenario: TOPIC-11 Explain this shows the reviewed text when it exists
    Given a topic with reviewed explanation text is open
    When the visitor looks at Explain this
    Then it shows that reviewed text

  @ui
  Scenario: TOPIC-24 Explain this without reviewed text says it is not yet available
    Given a topic with no reviewed explanation text is open
    When the visitor looks at Explain this
    Then it reads "Explanation not yet available"
    # No "Ask more about this" link in the pilot: there is no chat to open (AI-12, decision 0056, 15 Nov 2026).
    # 16 Nov 2026 (0058, FE-58): the chat is back for signed-in users and "Ask more about this" returns for everyone, except under an explanation that is not yet available (WCHAT-55, WCHAT-76, WCHAT-105).

  # Changed 16 Nov 2026 (design pass, FE-69): these rows now read "Check this: we haven't checked it" with what the thing is, why it matters and the official link (TOPIC-35 to TOPIC-39); the Noise row also says road noise is a map layer (TOPIC-38). They sit under the heading "Not yet covered here".
  @ui
  Scenario: TOPIC-12 a route-only topic says it is not yet covered
    Given the result for a sample postcode is open
    When the visitor opens a topic we only link to
    Then it sits under "Not yet covered here" and reads "Check this: we haven't checked it" (TOPIC-37, TOPIC-38) with its official link
    And no facts are shown for it

  # ---- Design pass, 16 Nov 2026: new topics and rows (canvas version 405) ----

  # Radon (DA-23, DA-31, FE-69). Wording approved by the founder with the remedy examples dropped; the record's label ("Radon potential, the 1 km square around this postcode (synthetic)") stays proposed until the next wording review (DA-31 note).
  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY NB1-4XY-AREA-RADON-1, grid-square level of 1000 m)
  Scenario: TOPIC-26 the normal sample postcode has a recorded radon band for its 1 km square
    Then postcode record "NB1-4XY-AREA-RADON-1" has status "recorded"
    And area result "NB1 4XY" has topic "radon" with outcome "found"

  @ui
  Scenario: TOPIC-27 the Radon topic quotes the band as published for the 1 km square
    Given the result for "NB1 4XY" is open
    When the visitor opens "Radon"
    Then the fact reads "Radon potential: " followed by the class and "edition" quoted from record "NB1-4XY-AREA-RADON-1" as published
    And the area it covers reads "The 1 km square around this postcode"
    And the limit reads "Indicative, not definitive: the class is the highest found anywhere in this 1 km square, not a test of this home. Only a measurement in the home gives its radon level. A low class does not mean no radon."
    And the link "Get a radon report for an address from UKradon (paid) ↗" is shown
    And the source stamp is "BGS and UKHSA" (the short name was approved by the founder on 18 Nov 2026, FE-69)
    And no per-home radon level, verdict or "safe" or "low risk" label is shown

  @ui
  Scenario: TOPIC-28 the Radon topic asks one question and lists two reviewed checks
    Given the result for "NB1 4XY" is open
    When the visitor opens "Radon"
    Then "What to do next" lists the check in person "Ask the owner or landlord whether radon has been measured in the home, and ask to see the result." and "Ask whether anything has been fitted to reduce radon."
    And the gap question "Has radon been measured in the home, and what was the result?" appears in Questions to ask only when radon is not known for the postcode (FE-39, FE-69)

  # fixture: packages/fixtures/data/postcode-area.json (NB7 1RR NB7-1RR-AREA-RADON-1, source-failed)
  Scenario: TOPIC-29 a failed radon lookup is not known and asks its question
    Then postcode record "NB7-1RR-AREA-RADON-1" has status "source-failed"
    And area result "NB7 1RR" has topic "radon" with outcome "not-known"
    And area result "NB7 1RR" asks the gap question for record "NB7-1RR-AREA-RADON-1"

  # Broadband coverage replaces the predicted-speed record ("Replace it now", DA-28, DA-31). The limit text beyond DA-28's phrase is proposed (DA-31 section 3).
  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY recorded; NB7 1RR no record in this source)
  Scenario: TOPIC-30 broadband coverage is recorded for the normal postcode and has no record for the sparse one
    Then postcode record "NB1-4XY-AREA-BROADBAND-COVERAGE-1" has status "recorded"
    And postcode record "NB7-1RR-AREA-BROADBAND-COVERAGE-1" has status "no-record-in-source"

  @ui
  Scenario: TOPIC-31 Broadband is the gigabit-capable share of premises and makes no full-fibre claim
    Given the result for "NB1 4XY" is open
    When the visitor opens "Broadband"
    Then the fact reads "Gigabit-capable broadband available at " followed by the percentage, "of all premises" or "of residential premises", and the snapshot month in brackets, all quoted from record "NB1-4XY-AREA-BROADBAND-COVERAGE-1"
    And the area it covers reads "This postcode"
    And the limit reads "The share of premises in this postcode where providers say gigabit-capable broadband is available. It can't say whether a home has full fibre or a working connection, or what speed you would get."
    And no download speed, full-fibre claim or "fast" or "slow" label is shown
    And a postcode with no record reads "No broadband coverage figure for this postcode in this source", never zero (rule 7)

  # Council-wide rent (DA-29, DA-30). The figure is never copied: it is read from `council-result.json` through the council code of record NB1-4XY-AREA-COUNCIL-RENT-1 (`councils[code == councilCode]`, rent caption `toValue` and `toPeriod`, `rentOrBuy.rentPointStatus`), and "provisional" comes from that status.
  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY recorded, NB7 1RR no record in this source)
  Scenario: TOPIC-32 council rent is recorded for the normal postcode and has no record for the sparse one
    Then postcode record "NB1-4XY-AREA-COUNCIL-RENT-1" has status "recorded"
    And postcode record "NB7-1RR-AREA-COUNCIL-RENT-1" has status "no-record-in-source"

  @ui
  Scenario: TOPIC-33 Housing affordability shows the council-wide rent, labelled, with a City Explorer link
    Given the result for "NB1 4XY" is open
    When the visitor opens "Housing affordability"
    Then a second line reads "Council-wide average private rent: " followed by the monthly figure, the month and "provisional" where its status says so, all quoted from `council-result.json` for the council named by record "NB1-4XY-AREA-COUNCIL-RENT-1" and never copied or typed (DA-30)
    And the area it covers reads "Council area: " followed by the council's name
    And it says "A council-wide average, not this street. It does not say what any one home would rent for."
    And the link "See " followed by the council's name and " in City Explorer →" opens that council's City Explorer page (DA-29)
    And the source stamp is "Office for National Statistics"

  @ui
  Scenario: TOPIC-34 a missing council rent reads as a gap, never zero
    Given the result for "NB7 1RR" is open
    When the visitor opens "Housing affordability"
    Then the rent line reads "No average private rent for this area in this source"
    And when the rent caption in `council-result.json` is missing the rent shows "Not known", never a figure (DA-31 section 1.2)
    And it shares the affordability question rather than asking a second one

  # "Check this" rows (DA-22, DA-24, DA-26, DA-28; FE-69 "Approve as written"): what it is, why it matters, a link to the official service, no data of ours and nothing implying we checked.
  @ui
  Scenario: TOPIC-35 the long-term flood risk row says we haven't checked it
    Given the result for "NB1 4XY" is open
    When the visitor reads the Flood row
    Then a row marked "Check this" reads "Long-term flood risk" with "We haven't checked this. The official service covers rivers and the sea, surface water, reservoirs and groundwater where data is available, and shows the risk of an area, not a specific property." and the link "Check your long-term flood risk (gov.uk) ↗"
    And it shows no result, status or colour for the home or postcode

  @ui
  Scenario: TOPIC-36 planning shows an Article 4 and tree preservation orders row
    Given the result for "NB1 4XY" is open
    When the visitor reads the Planning nearby row
    Then a row marked "Check this" reads "Article 4 directions and tree preservation orders" with "We haven't checked these. An Article 4 direction can remove some building work a homeowner could otherwise do without planning permission, and a tree preservation order protects particular trees. The council holds both." and the link "Find your council's planning team ↗"
    And no result is shown for this address, and "no result does not mean no constraint" is never contradicted (DA-24)

  @ui
  Scenario: TOPIC-37 the topics we only link to read Check this under "Not yet covered here"
    Given the result for a sample postcode is open
    When the visitor reads "Not yet covered here"
    Then it says "We haven't checked these for this postcode. Each one says what it is and links to the official place to check."
    And "Council tax band of a home" reads "Check this: we haven't checked it" with "The council tax band of an exact address. It sets that home's council tax charge." and the link "Check the council tax band of a home (gov.uk) ↗"
    And "Mobile by network" reads "Check this: we haven't checked it" with "How strong each network's mobile signal is at an address. It matters if you rely on calls or mobile data at home." and the link "Ofcom's coverage checker ↗" (DA-28)
    And "Ground and mining" reads "Check this: we haven't checked it" with "Whether a home is in an area affected by past coal mining. It can matter for the ground the home sits on." and the link "Check if a property is affected by coal mining (gov.uk) ↗" (DA-26)
    And none of them (Noise: TOPIC-38) shows a fact, a count or a status for the postcode

  # The founder approved the Noise row's "Check this for a home" wording in the FE-69 window, then the agent corrected the rail sentence on the same day (rule 1; FE-69 agent correction).
  @ui
  Scenario: TOPIC-38 the Noise row says road noise is a map layer and does not say there is no rail noise
    Given the result for "NB1 4XY" is open
    When the visitor reads the Noise row
    Then it reads "Check this for a home" and "Road noise is shown as a layer on the map (modelled for 2021, not measured). The source has no record of rail noise for this postcode. That does not mean there is no rail noise. For a home, check in person." with the link "Government road and rail noise mapping (gov.uk) ↗"
    And it does not read "rail noise isn't in this source"
    And no noise level, decibel figure or band is shown for the home

  @ui
  Scenario: TOPIC-39 no Check this row implies that we checked anything
    Given the result for a sample postcode is open
    When the visitor reads any row marked "Check this"
    Then the row says "We haven't checked" or "Check this: we haven't checked it", or, for noise, "Check this for a home"
    And it shows no tick, no colour for a result, no "clear", "safe", "verified" or "approved", and no count (rules 4 and 7)
    And it is left out of At a glance's counts and of the coverage total (GLANCE-05)
    And its link says it goes to an official service and carries no postcode unless it says so (AREA-18)

  # fixture: packages/fixtures/data/pilot-topics.json (the layers each topic lists under `mapLayers`)
  Scenario: TOPIC-40 each topic lists the map layers it draws on the 2D map
    Then topic "flood" draws map layer "flood-zones"
    And topic "flood" draws map layer "surface-water"
    And topic "planning-nearby" draws map layer "listed-buildings"
    And topic "planning-nearby" draws map layer "conservation-areas"
    And topic "noise" draws map layer "road-noise"
    And topic "noise" draws map layer "rail-noise"

  # Added 18 Nov 2026 (energy certificate design, `docs/superpowers/specs/2026-11-18-energy-certificate-design.md`). All the wording of this row was approved by the founder on 19 Nov 2026 (copy review, "Approve as written (Recommended)"). The page is specified in `energy-certificate.feature` (ENERGY); the registry row is `energy-certificate-home` in `packages/fixtures/data/pilot-topics.json`.
  @ui
  Scenario: TOPIC-41 the energy certificate row opens its own page and shows no result for the postcode
    Given the result for "NB1 4XY" is open
    When the visitor reads "Not yet covered here" and opens "Energy certificate of a home"
    Then the row reads "Check this: we haven't checked it" with "The energy certificate of a home: its rating, the certificate's own running-cost estimates and suggested improvements. You need the certificate number." and the link "Check an energy certificate" opens "/energy-certificate", beside the official link "Find an energy certificate (gov.uk) ↗"
    And no rating, cost, status or colour is shown on the row, the postcode is not sent to the page, and the row is left out of At a glance's counts and of the coverage total (GLANCE-05)
