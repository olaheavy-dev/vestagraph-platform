@screen @buying @renting
Feature: At a glance (the first thing on an area result)
  Question it answers: "What do I need to know about this area first, and what is left for me to find out?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: the postcode-level sample area data, `packages/fixtures/data/postcode-area.json`
    (NB1 4XY normal, NB7 1RR sparse and failed flood, NB9 9ZZ unknown); the counts, questions and coverage
    come from `packages/fixtures/generated/area-result.json` (the tested `vestagraph_area` package, FE-38)
    and the topic registry `packages/fixtures/data/pilot-topics.json`; figures: none typed here.
  What it is: the block at the top of the result (FE-22): how many topics were found, how many are not
    known, how many questions to ask, a "Things to check in person" link that shows no count (FE-41), a
    coverage line, and "What matters to you · Set priorities". Each count opens the list of its items.
  Rule 2: no count, distance or coverage figure is typed in a scenario; the page quotes them from
    `area-result.json`, and the data scenarios check outcomes by postcode, topic key and record ID.
  Found means the source answered, including "no record in this source" and "none found within the radius";
    not known means our stored copy failed or is unavailable; topics we only link to, and the family view, are
    left out of the coverage total, as is a topic outside the covered area (FE-38).
  Questions to ask come from gaps, one per gap, de-duplicated by topic and text (FE-39 as built), from a
    reviewed template; "Things to check in person" comes from a fixed, reviewed list per topic from
    `pilot-topics.json`, except the family view, which keeps its list in its own sheet (FE-39).
  Required states (design docs/superpowers/specs/2026-11-14-first-design-batch-design.md, "At a glance";
    AGENTS.md rules 2, 4 and 7):
    every counted topic found -> GLANCE-01, GLANCE-02
    some topics not known, with a question for the gap -> GLANCE-03, GLANCE-04
    sparse area, topics left out of the coverage total -> GLANCE-05
    the block's order and contents -> GLANCE-06
    each count opens its items; a count of zero has nothing to list -> GLANCE-07, GLANCE-10
    check in person, a fixed reviewed list -> GLANCE-08
    narrow phone layout and tap targets -> GLANCE-09
    unknown postcode, never shown as empty topics -> AREA-05 (14-check-an-area.feature)

  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY)
  Scenario: GLANCE-01 every counted topic of the normal sample postcode is found
    Then area result "NB1 4XY" has topic "getting-around" with outcome "found"
    Then area result "NB1 4XY" has topic "everyday-places" with outcome "found"
    Then area result "NB1 4XY" has topic "places-of-worship" with outcome "found"
    Then area result "NB1 4XY" has topic "schools" with outcome "found"
    Then area result "NB1 4XY" has topic "planning-nearby" with outcome "found"
    Then area result "NB1 4XY" has topic "flood" with outcome "found"
    Then area result "NB1 4XY" has topic "crime" with outcome "found"
    Then area result "NB1 4XY" has topic "sold-nearby" with outcome "found"
    Then area result "NB1 4XY" has topic "broadband" with outcome "found"
    Then area result "NB1 4XY" has topic "air-quality" with outcome "found"
    Then area result "NB1 4XY" has topic "radon" with outcome "found"
    Then area result "NB1 4XY" has topic "council-tax-by-band" with outcome "found"
    Then area result "NB1 4XY" has topic "housing-affordability" with outcome "found"
    Then area result "NB1 4XY" has topic "deprivation" with outcome "found"
    Then area result "NB1 4XY" has topic "transport-connectivity" with outcome "found"
    Then area result "NB1 4XY" has topic "green-space" with outcome "found"

  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY)
  Scenario: GLANCE-02 the normal sample postcode asks a question for each gap
    Then area result "NB1 4XY" asks the gap question for record "NB1-4XY-AREA-AMENITY-6"
    And area result "NB1 4XY" asks the gap question for record "NB1-4XY-AREA-FLOOD-1"

  # fixture: packages/fixtures/generated/area-result.json (NB7 1RR)
  Scenario: GLANCE-03 the sparse postcode's flood, radon and transport connectivity are not known
    Then area result "NB7 1RR" has topic "flood" with outcome "not-known"
    And area result "NB7 1RR" has topic "radon" with outcome "not-known"
    And area result "NB7 1RR" has topic "transport-connectivity" with outcome "not-known"

  # fixture: packages/fixtures/generated/area-result.json (NB7 1RR)
  Scenario: GLANCE-04 the sparse postcode asks a question for its missing amenity and its failed radon lookup
    Then area result "NB7 1RR" asks the gap question for record "NB7-1RR-AREA-AMENITY-2"
    And area result "NB7 1RR" asks the gap question for record "NB7-1RR-AREA-RADON-1"

  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY, NB7 1RR)
  Scenario: GLANCE-05 topics we only link to, the family view and a not-covered topic are left out of the coverage total
    Then area result "NB1 4XY" leaves topic "council-tax-band-home" out of the coverage total
    Then area result "NB1 4XY" leaves topic "mobile-by-network" out of the coverage total
    Then area result "NB1 4XY" leaves topic "noise" out of the coverage total
    Then area result "NB1 4XY" leaves topic "ground-and-mining" out of the coverage total
    Then area result "NB1 4XY" leaves topic "family-view" out of the coverage total
    Then area result "NB7 1RR" leaves topic "council-tax-band-home" out of the coverage total
    Then area result "NB7 1RR" leaves topic "mobile-by-network" out of the coverage total
    Then area result "NB7 1RR" leaves topic "noise" out of the coverage total
    Then area result "NB7 1RR" leaves topic "ground-and-mining" out of the coverage total
    Then area result "NB7 1RR" leaves topic "family-view" out of the coverage total
    And area result "NB7 1RR" has topic "green-space" with outcome "not-covered"
    And area result "NB7 1RR" leaves topic "green-space" out of the coverage total

  @ui
  Scenario: GLANCE-06 At a glance comes first on the result
    Given the result for a sample postcode is open
    When the page has loaded
    Then At a glance is the first block, before the topics
    And it shows the found, not known and questions to ask counts, each quoted from `area-result.json`
    And it shows "Things to check in person →" with no count
    And it shows the coverage line quoted from `area-result.json`
    And it ends with "What matters to you · Set priorities"
    And no score, band, verdict or total of priorities appears

  @ui
  Scenario: GLANCE-07 each count opens the list of its items
    Given the result for a sample postcode is open
    When the visitor opens a count
    Then the list of that count's items opens, each item opening its topic

  @ui
  Scenario: GLANCE-10 a count of zero says there is nothing to list and has no link
    Given the result for a sample postcode is open
    When a count is zero
    Then it says there is nothing to list
    And it has no link

  @ui
  Scenario: GLANCE-08 Things to check in person opens the reviewed list
    Given the result for a sample postcode is open
    When the visitor opens "Things to check in person →"
    Then the fixed reviewed list per topic from `pilot-topics.json` is shown, except the family view, which keeps its list in its own sheet (FE-39)
    And the list is the same for every postcode and is not written by AI

  @ui
  Scenario: GLANCE-09 At a glance fits a 320 px screen
    Given the result for a sample postcode is open at a width of 320 px
    When At a glance is shown
    Then the tiles stack into one column with no sideways scroll
    And every tap target is at least 44 px
