@screen @buying @renting
Feature: Compare two postcodes (two area results side by side, topic by topic)
  Question it answers: "How do these two postcodes line up, topic by topic, with each side's own source and gaps, and nothing worked out between them?"
  Modes: both (and anyone, with no account; decision 0046)
  Added 19 Nov 2026 (pilot design batch, PR 1; design `docs/superpowers/specs/2026-11-19-pilot-design-batch-design.md`, section "1. Compare two postcodes"; plan Task 2; decisions 0004, 0014, 0053, 0054; register lines FE-20, FE-22, FE-33, FE-34, FE-40, FE-41, FE-73, PD-21). Founder's choice, 19 Nov 2026: "Topic by topic (Recommended)". The way in is the area result (`area-glance.feature`, `area-topics.feature`); the council version is `city-explorer-part-2.feature` (CITY2-01 to CITY2-32), whose patterns this feature mirrors. Report a problem on compare's topic details is `report-a-problem.feature` (REPORT-01 onwards).
  Fixtures: the postcode-level sample area data, `packages/fixtures/data/postcode-area.json` (NB1 4XY normal, NB7 1RR sparse, with a failed flood source, NB9 9ZZ unknown), `packages/fixtures/data/homes.json` (WALES-1 outside England), and the generated `packages/fixtures/generated/area-result.json` (NB1 4XY and NB7 1RR). The compare scenarios draw NB1 4XY first and NB7 1RR second, because the sparse postcode shows gaps well.
  Figures: none typed here (AGENTS.md rule 2). Every count, line and outcome is quoted by record path from `area-result.json`: <postcode> / glance / found, notKnown, coverageFound, coverageTotal; <postcode> / topics / <key> / outcome (the topics in the file's order, the registry order of `pilot-topics.json`). The summary line of each topic is the same text the area result shows (FE-20); `area-result.json` carries the outcome of each topic and the page builds the line from that topic's records, as it does on the area result, so compare adds no figure of its own. Compare works out nothing between the two postcodes.
  Rule 4 and 0054: compare shows the two postcodes in the order the visitor picked them. It never sorts, ranks or totals them, names no "better" or "worse" postcode, and works out no difference between them ("2 more schools"). The only words about the two sides are each side's own facts.
  Rule 7: a gap on one side is never blank, zero or a clean result. Three cases, each with the area result's own approved wording: a topic whose source holds no record reads that record's own gap line (TOPIC-09, AREA-47, for example "No sold prices nearby in this source"; the topic still counts as found); a topic whose source is down reads "Not known right now" (AREA-07); a topic outside the covered area reads "Not yet covered". "Not known" is the label of an outcome (a not-known count, a priority), never a replacement for a record's own gap line.
  Rule 6: a postcode outside England reads "Not yet covered" on its own side (AREA-01, AREA-08).
  Boards: `ComparePhone`, `CompareDesktop` and `CompareStates`, each with a `…Dark` twin, in the canvas section 'Pilot 8 · Compare, share, report' on the page 'Pilot · public area check' (checked against canvas version 1795107206-3e0d, 19 Nov 2026). Wording below that is not marked "approved" is the design's or the area result's own wording.
  Wording status: approved wording is reused from the area result (AREA-04, AREA-05, AREA-07, AREA-08, AREA-30, PRIO) and from compare councils (CITY2-04, CITY2-27). Proposed wording, for the founder's copy review before build: the compare page's heading, subtitle and the empty second-postcode line "Add a second postcode to see the two side by side." (drawn on `CompareStates` card 1; COMPARE-01, COMPARE-03), "Compare with another postcode" and "Share this comparison" on the area result and compare (COMPARE-01, COMPARE-29), and the "How we got this" note (COMPARE-28). Each is marked "proposed" at its scenario.
  Data scenarios (no tag) check the sample data with the area result steps in docs/specs/README.md. Every other scenario is `@ui`, because the outcome is on the page, in the browser or in what the server logs.

  Board-to-scenario map (drawn in plan Task 3; each board has a Dark twin, COMPARE-36):
    Compare, phone and desktop: the way in -> COMPARE-01, COMPARE-02; the postcode boxes and Swap -> COMPARE-03, COMPARE-16, COMPARE-17; At a glance for each -> COMPARE-08, COMPARE-09, COMPARE-10; priorities -> COMPARE-18 to COMPARE-21; the rows -> COMPARE-11 to COMPARE-13; a row's two details -> COMPARE-14; gaps -> COMPARE-22 to COMPARE-27; no ranking -> COMPARE-15; How we got this -> COMPARE-28; Share this comparison -> COMPARE-29 to COMPARE-31; offline -> COMPARE-32; too many checks -> COMPARE-39; privacy -> COMPARE-33; Report a problem in a detail -> COMPARE-35; keyboard, size, no sideways scroll -> COMPARE-34; dark twin -> COMPARE-36; no Print -> COMPARE-37

  Required states (design "States to cover"; AGENTS.md rules 1, 4, 6 and 7):
    empty second postcode -> COMPARE-03
    invalid -> COMPARE-04
    not England -> COMPARE-05, COMPARE-06
    unknown -> COMPARE-07
    a source down on one side -> COMPARE-24, COMPARE-25 (the failed flood source of NB7 1RR, a real sample record)
    a topic missing on one side -> COMPARE-22, COMPARE-23, COMPARE-26, COMPARE-27 (no record in the source; not covered)
    offline -> COMPARE-32
    too many checks (rate limit) -> COMPARE-39
    swapped -> COMPARE-16
    the same postcode twice -> COMPARE-17
    priorities not set -> COMPARE-18; priorities set -> COMPARE-19, COMPARE-20, COMPARE-21
    shared link -> COMPARE-29 to COMPARE-31
    loading: compare loads both results as the area result does (AREA-06) -> COMPARE-11
    privacy -> COMPARE-33
    no state in this feature needs a new sample record, but the sample's own content has one open question: NB7 1RR's Planning line is test text (fixture issue #348, COMPARE-13; a content choice to decide before build or at the gate's `noticed` triage). Every other state is quoted from an existing record.

  # The way in (design: from the result, this postcode first, as council compare CITY2-02). Heading and subtitle are proposed wording.
  @ui
  Scenario: COMPARE-01 "Compare with another postcode" on the area result opens compare with this postcode first
    # Drawn on ShareStates and, since 19 Nov 2026 (canvas version 424), in the header of the four Result · Check an area boards (AreaResult, AreaResultDesktop and their Dark twins).
    Given the result for "NB1 4XY" is open
    When the visitor chooses "Compare with another postcode" (proposed wording)
    Then compare opens with "NB1 4XY" as the first postcode and an empty box for the second, which is never filled in for the visitor
    And the page heading reads "Compare two areas" (proposed wording) with the line "Two postcodes side by side, in the order you picked them. Vestagraph doesn’t rank areas or pick a winner: each row shows each postcode’s own facts." (proposed wording)
    And above it a link goes back to the result for "NB1 4XY"

  # The exact form of the route is left to the builder (design); the rule is fixed here.
  @ui
  Scenario: COMPARE-02 compare has its own address with both postcodes after the #
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor reads the address
    Then both postcodes are after the "#" (proposed form "/compare#NB1 4XY,NB7 1RR", the exact form left to the builder)
    And the query string holds no postcode (AREA-03)

  # CompareStates card 1 draws this state; its line is proposed wording, like CITY2-05.
  @ui
  Scenario: COMPARE-03 before a second postcode is entered compare shows no rows and no figure
    Given the visitor has opened compare from the result for "NB1 4XY"
    When no second postcode has been entered
    Then only the first postcode and the empty box are shown, with the plain line "Add a second postcode to see the two side by side." (proposed wording, drawn on `CompareStates` card 1)
    And no row, no count and no priority result is shown for a postcode that was not entered, and nothing is shown as zero

  @ui
  Scenario: COMPARE-04 an invalid second postcode shows the search's own message on that side only
    Given the visitor has opened compare from the result for "NB1 4XY"
    When the visitor enters an incomplete postcode as the second postcode
    Then the inline message of AREA-04 is shown under the second box, and no search is made for it
    And the first postcode's side stays as it was

  # Home "WALES-1" stands in for a postcode outside England: postcode-area.json is England only (rule 6).
  Scenario: COMPARE-05 a postcode outside England is not yet covered on its own side
    Then home "WALES-1" has coverage "not-yet-covered"

  @ui
  Scenario: COMPARE-06 a postcode outside England reads "Not yet covered" on its side and compare works for the other
    Given the visitor has opened compare from the result for "NB1 4XY"
    When the visitor enters the postcode of home "WALES-1" as the second postcode
    Then that side shows the "Not yet covered" card of AREA-08, with no topic shown as empty, and no row shows a figure for it
    And the first postcode's At a glance and details stay as they were

  # fixture: packages/fixtures/data/postcode-area.json (NB9 9ZZ, the unknown postcode)
  @ui
  Scenario: COMPARE-07 an unknown second postcode shows only that it wasn't found
    Given the visitor has opened compare from the result for "NB1 4XY"
    When the visitor enters a well-formed postcode that the sample data doesn't know, "NB9 9ZZ"
    Then that side shows "We couldn't find that postcode" as AREA-05 does, and no topic row shows empty or a clean result for it
    And the first postcode's side stays as it was

  # At a glance for each (FE-22, FE-41): each side's own counts, never a difference.
  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY, NB7 1RR)
  Scenario: COMPARE-08 each postcode's topic outcomes come from its own result
    Then area result "NB1 4XY" has topic "flood" with outcome "found"
    And area result "NB7 1RR" has topic "flood" with outcome "not-known"
    And area result "NB7 1RR" has topic "radon" with outcome "not-known"
    And area result "NB7 1RR" has topic "transport-connectivity" with outcome "not-known"
    And area result "NB7 1RR" asks the gap question for record "NB7-1RR-AREA-BUS-DEPARTURES-1"
    And area result "NB1 4XY" asks the gap question for record "NB1-4XY-AREA-FLOOD-1"

  @ui
  Scenario: COMPARE-09 At a glance is shown for each postcode with its own counts
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor reads the top of the page
    Then each postcode has its own At a glance with its "found", "not known" and "Questions to ask" counts, quoted from `area-result.json` <postcode> / glance / found and notKnown and the number of entries in questions (FE-22, FE-41), and its coverage line from coverageFound and coverageTotal
    And no count, line or word says which postcode has more, fewer or better

  @ui
  Scenario: COMPARE-10 each side's Things to check in person shows no count, as on the result
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor reads each side's At a glance
    Then "Things to check in person" is a link on each side with no count (FE-41), and each side's questions come from its own `glance` / `checkInPerson`
    And the two sides' questions are not merged, compared or de-duplicated across postcodes

  # The rows: every pilot topic in the area result's order, both summary lines.
  @ui
  Scenario: COMPARE-11 every counted topic is one row, in the area result's order, loading as skeletons
    Given the visitor has entered both postcodes and the results are still loading
    When the results arrive
    Then each topic of `area-result.json` <postcode> / topics is one row, in that file's order (the registry order of `pilot-topics.json`), and while loading each row shows a skeleton and no row shows as empty (AREA-06)
    And the order never changes with the postcodes, the priorities or the figures
    And the "Check this" rows, the route-only topics and the energy certificate row are not on compare: each is a link or a check about one home, not a fact about a postcode, and only the topics the registry marks `counted: false` in `pilot-topics.json` are left out; a topic that is not covered for one postcode (the Green space of "NB7 1RR") stays a row and reads "Not yet covered" on that side (COMPARE-26, COMPARE-27) (agent's call, open to the founder)

  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY, NB7 1RR)
  Scenario: COMPARE-12 the two samples have a result for each counted topic, with the same topic keys
    Then area result "NB1 4XY" has topic "getting-around" with outcome "found"
    And area result "NB7 1RR" has topic "getting-around" with outcome "found"
    And area result "NB1 4XY" has topic "schools" with outcome "found"
    And area result "NB7 1RR" has topic "schools" with outcome "found"
    And area result "NB1 4XY" has topic "sold-nearby" with outcome "found"
    And area result "NB7 1RR" has topic "sold-nearby" with outcome "found"
    And area result "NB1 4XY" has topic "council-tax-by-band" with outcome "found"
    And area result "NB7 1RR" has topic "council-tax-by-band" with outcome "found"

  @ui
  Scenario: COMPARE-13 each row shows the topic's name and both postcodes' summary lines, each labelled with its postcode
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor reads a row, for example "Schools"
    Then the row shows the topic's name once, and each postcode's summary line with its postcode beside it (stacked on a phone, in two columns on desktop)
    And each side carries the same text the area result shows for that postcode (FE-20), built from the postcode's own topic records: the summary line, every extra gap line (for example "Childcare: no record in this source" under Everyday places), the "Not known right now" sentences, and the area line ("From the postcode centre", "Council area: Fellshire", "Neighbourhood: Northbridge Fells 001"), so a gap is never dropped and each figure says which area it covers
    # Fixture issue #348: NB7 1RR's Planning line is test text in the sample; deciding it is a content choice before build.
    And compare adds no word or figure of its own

  @ui
  Scenario: COMPARE-14 tapping a row opens both details one after the other, each with its own source stamp
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor taps the "Schools" row
    Then a sheet (phone) or a panel (desktop) opens with the first postcode's detail and then the second postcode's, in that order, each in the topic sheet's usual anatomy (TOPIC-01)
    And each detail carries its own source stamp and date (FE-33), and the two are never merged into one list or one figure

  # Never ranked, sorted, totalled or differenced (rule 4, design "Never").
  @ui
  Scenario: COMPARE-15 compare never sorts, ranks, totals, colours as better or worse, or works out a difference
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor reads every row, count, line and detail on the page
    Then no row is sorted or filtered by a figure, no postcode is ranked or totalled, and no colour or icon marks a side better or worse
    And none of the words "more", "fewer", "better" or "worse" appears about a comparison between the two postcodes, and no number is the difference between them
    And no sentence like "2 more schools" or "3 minutes closer" appears

  # Swap (as CITY2-04).
  @ui
  Scenario: COMPARE-16 Swap swaps the two columns and changes nothing else
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor chooses Swap
    Then "NB7 1RR" is the first postcode and "NB1 4XY" the second, every row shows each postcode's own line unchanged, and the address changes order only (COMPARE-02)
    And no row is re-sorted, no label changes and the priorities, if set, stay as they were

  @ui
  Scenario: COMPARE-17 the same postcode on both sides compares without any verdict
    Given the visitor has opened compare from the result for "NB1 4XY"
    When the visitor enters "NB1 4XY" as the second postcode
    Then compare shows the same rows on both sides, each with the same line, and says nothing about the two being identical, the same or a duplicate
    And the page does not refuse, correct or reorder the entry, and no extra search is shown

  # Priorities on compare (design: carry over in the page's memory, changeable here with the same controls; works fully without; FE-40).
  @ui
  Scenario: COMPARE-18 with no priorities set, compare shows the entry to set them and works fully without
    Given the visitor has set no priorities and has compared "NB1 4XY" and "NB7 1RR"
    When the visitor reads the top of the page
    Then a "What matters to you · Set priorities" entry is shown (FE-40), and every row and At a glance count works without it
    And no priority result is shown for either postcode

  @ui
  Scenario: COMPARE-19 priorities set on the result carry over in the page's memory and can be changed on compare
    Given the visitor has set limits on the result for "NB1 4XY" and then chosen "Compare with another postcode"
    When the second postcode is entered
    Then each postcode shows its own result for each limit (meets, misses, not known or not known beyond the search), each limit listed on its own with no total and no ranking (PRIO-08)
    And the limits can be changed on compare with the same controls as on the result, and they are kept in the page's memory only, never in the address or on the device

  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY, NB7 1RR)
  Scenario: COMPARE-20 the sample's ready-made limits give each postcode its own outcome
    Then area result "NB1 4XY" has priority "SAMPLE-PRIORITY-GP" with outcome "meets"
    And area result "NB7 1RR" has priority "SAMPLE-PRIORITY-PRIMARY" with outcome "misses"
    And area result "NB7 1RR" has priority "SAMPLE-PRIORITY-CHILDCARE" with outcome "not-known"
    And area result "NB7 1RR" has priority "SAMPLE-PRIORITY-HOSPITAL" with outcome "not-known-beyond-search"

  @ui
  Scenario: COMPARE-21 a priority that is not known on one side reads Not known there, never a miss
    Given the visitor has set a limit and has compared "NB1 4XY" and "NB7 1RR"
    When a limit is not known for one postcode, for example the childcare limit of "NB7 1RR"
    Then that postcode's side reads "Not known" for the limit, as PRIO-18 sets, and the other side reads its own outcome
    And neither side is compared with the other, and no total of limits met is shown

  # Gaps (rule 7; design "Gaps").
  # fixture: packages/fixtures/data/postcode-area.json (NB7-1RR-AREA-SOLD-PRICE-1 no record in the source; NB1-4XY-AREA-SOLD-PRICE-1 recorded)
  Scenario: COMPARE-22 a topic NB7 1RR has no record for, and NB1 4XY has
    Then postcode record "NB1-4XY-AREA-SOLD-PRICE-1" has status "recorded"
    And postcode record "NB7-1RR-AREA-SOLD-PRICE-1" has status "no-record-in-source"
    And postcode record "NB7-1RR-AREA-BROADBAND-COVERAGE-1" has status "no-record-in-source"
    And area result "NB7 1RR" has topic "sold-nearby" with outcome "found"

  @ui
  Scenario: COMPARE-23 a topic one side has no record for reads that record's own gap line on that side
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor reads the "Sold nearby" row
    Then the "NB7 1RR" side reads the record's own gap line as on the area result (TOPIC-09, AREA-47), quoted from the label of `NB7-1RR-AREA-SOLD-PRICE-1` in `postcode-area.json` without "(synthetic)", and the "NB1 4XY" side shows its own line
    And the topic still counts as found in "NB7 1RR"'s At a glance, and a topic whose outcome is not known (radon or transport connectivity of "NB7 1RR") reads "Not known right now" as COMPARE-25 says
    And nothing is shown as zero, blank or a clean result, and no sentence compares the two

  # fixture: packages/fixtures/data/postcode-area.json (NB7-1RR-AREA-FLOOD-1 source-failed)
  Scenario: COMPARE-24 the failed flood source of the sparse sample is down for NB7 1RR only
    Then postcode record "NB7-1RR-AREA-FLOOD-1" has status "source-failed"
    And area result "NB1 4XY" has topic "flood" with outcome "found"
    And area result "NB7 1RR" has topic "flood" with outcome "not-known"
    And area result "NB7 1RR" has topic "radon" with outcome "not-known"
    And area result "NB7 1RR" has topic "transport-connectivity" with outcome "not-known"

  # A down source reads "Not known right now" (AREA-07), as the corrected design and FE-73 say; "Unavailable" is withdrawn.
  @ui
  Scenario: COMPARE-25 a source that is down on one side reads what the result reads, and the other side still shows
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor reads the "Flood" row, where our stored copy of the flood source for "NB7 1RR" failed
    Then that side reads "Not known right now" with "We don't hold a current copy of this source" (AREA-07), no "Try again", and its official link where one exists
    And the "NB1 4XY" side shows its own flood line, and every other row on both sides still shows

  # fixture: packages/fixtures/data/postcode-area.json (NB7-1RR-AREA-GREEN-SPACE-1 not-covered)
  Scenario: COMPARE-26 a topic outside the covered area on one side is left out of that side's coverage
    Then postcode record "NB7-1RR-AREA-GREEN-SPACE-1" has status "not-covered"
    And area result "NB7 1RR" has topic "green-space" with outcome "not-covered"
    And area result "NB7 1RR" leaves topic "green-space" out of the coverage total
    And area result "NB1 4XY" has topic "green-space" with outcome "found"

  @ui
  Scenario: COMPARE-27 a topic not yet covered on one side reads "Not yet covered" there and is not counted
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor reads the "Green space" row
    Then the "NB7 1RR" side reads "Not yet covered" and the "NB1 4XY" side shows its own line
    And the topic is left out of "NB7 1RR"'s coverage total (GLANCE-05), and no side reads as zero or a clean result

  @ui
  Scenario: COMPARE-28 "How we got this" appears once on the page and says nothing is ranked
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor reads "How we got this"
    Then there is one note for the whole page (FE-34), saying both columns come from the same sources and editions, that gaps are shown as gaps, and that nothing is ranked or worked out between them (proposed wording, for the founder's copy review)
    And it links to About the data, where each source's limits are

  # Share this comparison (as CITY2-32; PRIO-16 extended).
  @ui
  Scenario: COMPARE-29 "Share this comparison" carries both postcodes after the # and never the limits
    Given the visitor has compared "NB1 4XY" and "NB7 1RR" and set limits
    When the visitor chooses "Share this comparison" (proposed wording)
    Then the link carries both postcodes, in that order, after the "#", and nothing stored is used to make it
    And the link carries no limit, display setting or open topic, and no query string (PRIO-16, PRIO-17)
    And the control behaves as the area result's Share does (SHARE-01 to SHARE-04)

  @ui
  Scenario: COMPARE-30 a shared link with spaces, lower case or one invalid postcode runs both searches as typed would
    Given a shared compare link holds "nb1 4xy" and a postcode that is incomplete
    When the visitor opens it
    Then both postcodes are searched as if typed, so spaces and lower case are accepted (as AREA-03 and the search accept them), and the incomplete side shows the search's own message of AREA-04 on that side only
    And the valid side shows its own At a glance and rows, and nothing is stored or logged to open the link, except the Recent postcodes list when the visitor has turned it on (RECENT-07)

  @ui
  Scenario: COMPARE-31 a shared compare link opens with no limits
    Given a shared compare link and a visitor who has set no limits
    When the visitor opens it
    Then compare shows the "set what matters to you" entry (COMPARE-18) and no priority result
    And the limits of whoever shared it are never in the link (PRIO-16)

  @ui
  Scenario: COMPARE-32 offline, the results already shown stay and a new postcode waits
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the device goes offline
    Then the page says "You’re offline" and "This device has no internet connection." and "Results already on screen stay; new searches and changed inputs wait until you’re back online." (the approved wording of CITY2-27 and CITY-99; no "Try again", which AREA-30 offers only on the result), and the results already on screen stay unchanged
    And a new second postcode is held until the device is back online, and no row for it is shown as empty

  @ui
  Scenario: COMPARE-33 the two postcodes and the limits are never in a query string, a log or an error report
    Given the visitor has compared "NB1 4XY" and "NB7 1RR" and set limits
    When the server has answered the compare request
    Then the postcodes and the limits travel in the request body only, and none is stored or written to a server, application, hosting or tracing log, or to an error report
    And nothing is in the query string, and analytics never records a postcode or a limit (0014, 0053, FE-05)

  @ui
  Scenario: COMPARE-34 compare works by keyboard, with 44 px targets and no sideways scrolling
    Given the visitor has opened compare on a phone and on desktop
    When the visitor works through the page by keyboard
    Then every control (the two boxes, Swap, "Set priorities", the rows, the details, Share this comparison and the jump list) can be reached and used, each at least 44 px tall, and nothing scrolls sideways at 390 px
    And focus moves into a detail when it opens and back to its row when it closes, and a screen reader hears each line with its row and its postcode

  # The pointer to REPORT: compare's details carry the link (founder's choice 5); the summary lines do not.
  @ui
  Scenario: COMPARE-35 each fact in a compare detail has "Report a problem", and the summary lines do not
    Given the visitor has opened the "Schools" detail on compare
    When the visitor reads each fact in the detail
    Then each fact has its own "Report a problem" link, as REPORT-01 and REPORT-02 specify, and the summary lines on the rows do not

  @ui
  Scenario: COMPARE-36 every compare board has a dark twin and the display control changes the theme and text size
    Given the visitor has opened compare on a phone and on desktop
    When the visitor chooses "Display" and picks the dark theme and a larger text size
    Then the page shows the same rows, counts, gaps and states as the light board, in the dark twin's colours (WCAG 2.2 AA contrast) and at the chosen size
    And the theme and text size are remembered on this device only, as on the result

  @ui
  Scenario: COMPARE-37 compare offers no Print
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor looks for a way to print
    Then no Print control is offered, because the area printout covers one postcode (a compare printout is a later idea, doc 05)

  # The design's "Jump to" list (design section 1, "Top of the page"); added after the review, so it takes the next ID.
  @ui
  Scenario: COMPARE-38 the jump list names each row in the area result's order and sorts nothing
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the visitor opens the topic jump list at the top of the page
    Then it lists the same topics as the rows, in the same order as `area-result.json` <postcode> / topics (COMPARE-11), and choosing one moves to its row
    And it is never sorted or filtered by a figure or an outcome, and it has no count or marker on any entry

  # Rate limit (the area result's own state; compare asks the same service for each postcode).
  @ui
  Scenario: COMPARE-39 too many checks keeps the results already shown and offers one action
    Given the visitor has compared "NB1 4XY" and "NB7 1RR"
    When the service says too many checks have been made
    Then the page says "Too many checks just now" with "This connection has checked a lot of postcodes in a short time." and "Your results so far are still on screen. Checks open again shortly." (the area result's approved wording, AREA-29, as drawn on the `CompareStates` board), and offers "Try again in a minute"
    And the rows already shown stay, no row shows as empty, and no limit, count or time is revealed
