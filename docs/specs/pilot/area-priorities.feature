@screen @buying @renting
Feature: Priorities (what matters to you, on an area result)
  Question it answers: "Does this area meet the limits I set for what matters to me, and where is that not known?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: the postcode-level sample area data, `packages/fixtures/data/postcode-area.json`
    (NB1 4XY normal, NB7 1RR sparse and failed flood); each result comes from
    `packages/fixtures/generated/area-result.json` (the tested `vestagraph_area` package, FE-38, and the
    server module of 0053); figures: none typed here.
  What it is: the visitor sets measurable limits (for example "a GP within a 15-minute walk"); each limit
    is listed on its own as meets, misses, not known or not known beyond the search (FE-22, FE-40). The
    result works fully without priorities; they are never a step before it (FE-40).
  Rule 2: no distance, time or count is typed in a scenario; the page quotes the nearest recorded distance
    from `area-result.json`; the search limit is `SEARCH_LIMIT_METRES` in
    `packages/vestagraph-area/src/vestagraph_area/priorities.py`, shown in the display unit by
    `vestagraph_area.distance.display_distance` (FE-27, FE-40); and the data
    scenarios check outcomes by postcode, priority ID and record ID.
  Rule 7: a gap is never a miss. A source that says "no record in this source" gives Not known; only a
    place that is recorded but beyond the limit gives Misses, and a missing walking time gives Not known,
    never a silent switch to straight-line distance (FE-40).
  Limits are sent in the request body to work out results, never stored or logged (FE-22, 0053).
  Required states (design docs/superpowers/specs/2026-11-14-first-design-batch-design.md, "Priorities";
    AGENTS.md rules 2, 4 and 7):
    meets, with the nearest place -> PRIO-01, PRIO-02
    misses, showing the nearest recorded place -> PRIO-03, PRIO-09
    not known, a gap in the source -> PRIO-04
    not known beyond the search -> PRIO-05, PRIO-10
    checking -> PRIO-11
    couldn't check, never a miss -> PRIO-14
    invalid limit, empty or not a number -> PRIO-07
    the ready-made limits and one panel at a time -> PRIO-06, PRIO-13
    no total, count or ranking -> PRIO-08
    not known on the page, never a miss -> PRIO-18
    privacy of the limits -> PRIO-12, PRIO-15, PRIO-16, PRIO-17, PRIO-19

  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY)
  Scenario: PRIO-01 the GP limit is met in the normal sample postcode
    Then area result "NB1 4XY" has priority "SAMPLE-PRIORITY-GP" with outcome "meets"
    And area result "NB1 4XY" has priority "SAMPLE-PRIORITY-GP" with nearest record "NB1-4XY-AREA-AMENITY-10"

  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY)
  Scenario: PRIO-02 the rail, primary school and broadband limits are met in the normal sample postcode
    Then area result "NB1 4XY" has priority "SAMPLE-PRIORITY-RAIL" with outcome "meets"
    And area result "NB1 4XY" has priority "SAMPLE-PRIORITY-RAIL" with nearest record "NB1-4XY-AREA-TRANSPORT-STOP-2"
    And area result "NB1 4XY" has priority "SAMPLE-PRIORITY-PRIMARY" with outcome "meets"
    And area result "NB1 4XY" has priority "SAMPLE-PRIORITY-PRIMARY" with nearest record "NB1-4XY-AREA-SCHOOL-1"
    And area result "NB1 4XY" has priority "SAMPLE-PRIORITY-BROADBAND" with outcome "meets"

  # fixture: packages/fixtures/generated/area-result.json (NB7 1RR)
  Scenario: PRIO-03 the sparse postcode misses the primary school and broadband limits
    Then area result "NB7 1RR" has priority "SAMPLE-PRIORITY-PRIMARY" with outcome "misses"
    And area result "NB7 1RR" has priority "SAMPLE-PRIORITY-PRIMARY" with nearest record "NB7-1RR-AREA-SCHOOL-1"
    And area result "NB7 1RR" has priority "SAMPLE-PRIORITY-BROADBAND" with outcome "misses"

  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY, NB7 1RR)
  Scenario: PRIO-04 a childcare limit is not known for both sample postcodes
    Then area result "NB1 4XY" has priority "SAMPLE-PRIORITY-CHILDCARE" with outcome "not-known"
    And area result "NB7 1RR" has priority "SAMPLE-PRIORITY-CHILDCARE" with outcome "not-known"

  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY, NB7 1RR)
  Scenario: PRIO-05 a hospital limit is not known beyond the search for both sample postcodes
    Then area result "NB1 4XY" has priority "SAMPLE-PRIORITY-HOSPITAL" with outcome "not-known-beyond-search"
    And area result "NB7 1RR" has priority "SAMPLE-PRIORITY-HOSPITAL" with outcome "not-known-beyond-search"

  @ui
  Scenario: PRIO-06 the priorities sheet and panel list the ready-made limits
    Given the result for a sample postcode is open
    When the visitor opens "Set priorities" (a sheet on a phone, a panel on desktop, FE-26)
    Then the ready-made limits are listed: GP surgery, pharmacy, primary school, secondary school, railway station, bus stop, supermarket, park or green space, childcare provider, hospital, broadband speed
    And each has an editable number and unit
    And each has a line saying what it uses: walking time, straight-line distance or predicted speed

  @ui
  Scenario: PRIO-07 an empty or non-numeric limit shows its message and is not sent
    Given the priorities sheet is open
    When the visitor leaves a limit empty or types text that is not a number
    Then a message appears under that box saying what to enter
    And nothing is sent to check that limit

  @ui
  Scenario: PRIO-08 each result is listed on its own with no total
    Given the visitor has set several limits on a sample postcode
    When the results are shown
    Then each priority is listed with its own result
    And no total, count of met priorities, ranking, score or "better area" appears anywhere (FE-22)

  @ui
  Scenario: PRIO-09 a miss shows the nearest recorded place
    Given the visitor sets a limit that a recorded place does not meet
    When the result is shown
    Then it reads "Misses your limit" followed by the nearest recorded distance quoted from `area-result.json`
    And the distance follows the country's display units (FE-27)

  @ui
  Scenario: PRIO-10 a limit past the search says so
    Given the visitor sets a limit beyond the search distance
    When the result is shown
    Then it reads "Not known beyond 3.1 miles" (the label FE-40 fixes; the distance is `SEARCH_LIMIT_METRES` shown by `display_distance`, never typed on the page)
    And it does not read as a miss or as met (FE-40)

  @ui
  Scenario: PRIO-11 checking state
    Given the visitor changes a limit
    When the check is under way
    Then "Checking your priorities…" is shown and announced to screen readers
    And the old result is not shown meanwhile

  @ui
  Scenario: PRIO-12 limits are sent only to work out results
    Given the visitor has set limits
    When the limits are sent to be checked
    Then they travel with the postcode only to work out results and are never stored or logged (0053)

  @ui
  Scenario: PRIO-13 closing the priorities sheet returns focus
    Given the priorities sheet is open
    When the visitor presses Escape or the phone's Back
    Then the sheet closes
    And focus returns to "Set priorities" or "Edit", whichever opened it

  @ui
  Scenario: PRIO-14 a failed check is never shown as a miss
    Given the visitor changes a limit
    When the check fails
    Then "Couldn't check this · Try again" is shown
    And it is never shown as a miss

  @ui
  Scenario: PRIO-15 remembering limits is off by default
    Given the priorities sheet is open
    Then "Remember these on this device" is off by default

  @ui
  Scenario: PRIO-19 remembered limits come back from the browser only
    Given the visitor turns on "Remember these on this device"
    When the visitor returns on a later visit
    Then the limits come back from the browser
    And they were not sent to be stored (0053)

  @ui
  Scenario: PRIO-16 a shared link never carries limits
    Given the visitor has set limits
    When the visitor shares the result link
    Then the link does not carry the limits

  @ui
  Scenario: PRIO-17 limits travel only in the request body
    Given the visitor has set limits
    When the limits are sent to be checked
    Then they are in the request body only, never in a query string or an address that reaches a log (0053)

  @ui
  Scenario: PRIO-18 a priority that is not known reads Not known, never a miss
    Given a priority whose topic has "no record in this source"
    When the result is shown
    Then it reads "Not known"
    And it never reads "Misses your limit" (FE-40, rule 7)
