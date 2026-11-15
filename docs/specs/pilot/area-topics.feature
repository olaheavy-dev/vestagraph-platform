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
  Scenario: TOPIC-03 on desktop a topic opens as a panel in place of the map
    Given the result for a sample postcode is open on desktop
    When the visitor opens a topic
    Then a panel opens beside the list in place of the map
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

  @ui
  Scenario: TOPIC-19 Flood shows no map until flood outlines are recorded
    Given the result for "NB1 4XY" is open
    When the visitor opens "Flood"
    Then no map is shown for the topic until flood outlines are recorded (FE-25)

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

  @ui
  Scenario: TOPIC-12 a route-only topic says it is not yet covered
    Given the result for a sample postcode is open
    When the visitor opens a topic we only link to
    Then it reads "Not yet covered" with its official link
    And no facts are shown for it
