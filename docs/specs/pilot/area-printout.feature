@screen @buying @renting
Feature: Area summary printout (the designed report, "Print or save as PDF")
  Question it answers: "Can I take this area check away on paper, and trust it as much as the screen?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: the postcode-level sample area data, `packages/fixtures/data/postcode-area.json`
    (NB1 4XY normal, NB7 1RR sparse and failed flood and radon), the topic registry
    `packages/fixtures/data/pilot-topics.json` and `packages/fixtures/generated/area-result.json`;
    figures: none typed here.
  What it is: the designed report of register line FE-21, made in the browser (FE-06; AREA-17): a cover, At a
    glance on page 1 with its map, a contents page listing every topic, the questions to ask and the things to
    check in person, one page per topic, the "Not yet covered" and "Check this" rows with their official links
    printed in full, "How we got this" pages (FE-34) and a closing "Sources and credits" page with dates only
    (FE-33). Where the on-screen result has something to open, the printout has nothing to open, so it prints
    that text on a page of its own.
  Redrawn 16 Nov 2026 (the benchmark design pass, canvas version 405, board `AreaExport`, 22 pages; plan
    docs/superpowers/plans/2026-11-16-benchmark-design-pass.md Task 4 "As drawn"). Agent's calls, approved by the
    founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)"): the printout lists every topic in `pilot-topics.json` (every topic, counted or not, DA-31; none
    dropped silently, a missing one prints as "Not known"), and the sources page gives dates only, following
    FE-33's later amendment ("Dates only, no notes") over the plan's "date and status". The printout has no
    dark twin, by design. The printout's Family view, route-only and method lines were proposed wording, approved by
    the founder on 18 Nov 2026 (FE-69, "Approve as written (Recommended)").
  The cover is page 1 of the printout; At a glance is on it (PRINT-01, PRINT-02).
  Rule 2: no count, distance, date or page number is typed in a scenario; the page quotes them from
    `area-result.json` and the records named by ID, and page numbers are worked out by the print layout.
  Rule 7: a topic whose data is not known prints as "Not known", with the reason, and never as zero, a favourable
    value or a clean result.
  Required states (AGENTS.md rules 2, 4 and 7; FE-21, FE-33, FE-34, FE-42, FE-69):
    the cover, with the date and where each source's date is -> PRINT-01
    At a glance on page 1, with its map and the numbered badges -> PRINT-02, PRINT-03
    contents listing every topic, none dropped -> PRINT-04, PRINT-05
    questions to ask and check in person -> PRINT-06, PRINT-07
    a page per topic -> PRINT-08
    Not yet covered and Check this rows, official links printed in full -> PRINT-09, PRINT-10
    How we got this -> PRINT-11
    Sources and credits, dates only, credit lines only from the sources list -> PRINT-12, PRINT-13
    the Not known state example -> PRINT-14, PRINT-15
    print rules: 12 pt, greyscale, no arrows on printed stamps, footers -> PRINT-16, PRINT-17, PRINT-18, PRINT-19
    privacy and what is never printed -> PRINT-20
    the energy certificate row listed under "Not yet covered here", with its page address printed in full -> PRINT-21

  # Cover (FE-21; AREA-12 and AREA-20 keep the "Sample data" and made-at rules for the example and for any other postcode).
  @ui
  Scenario: PRINT-01 the cover shows the postcode, the area, the date and where the source dates are
    Given the user has checked the sample postcode "NB1 4XY"
    When the user chooses "Print or save as PDF"
    Then the cover shows the brand mark, the postcode and the area name quoted from `postcode-area.json`, and the title "Area summary"
    And it shows "Sample data: a made-up town" and the time the summary was made, marked "(example time)" for the example postcode (AREA-12), and for any other postcode the real time it was made without "Sample data" (AREA-20)
    And it says "Each source's date is on page " followed by the page of the "Sources and credits" page, worked out by the print layout

  # FE-21 and FE-42 (dated note, 16 Nov 2026): the cover's map follows the same rings; its badges sit beside the pins, never over them (MAP-16). Crime and flood are not mapped (MAP-12, MAP-13).
  @ui
  Scenario: PRINT-02 At a glance is on page 1 with its map and key
    Given the user has chosen "Print or save as PDF" for the sample postcode "NB1 4XY"
    When the user reads page 1
    Then the 3D map in FE-42's style (MAP-14), numbered, shows the places with a key (postcode centre, getting around, shops, health, schools, parks, places of worship)
    And a line under it says the rings show straight-line distance from the postcode centre, not a walking route, names the 500 m and 1 mile rings and the search limit quoted from `display_distance`, says "Numbers match the topic pages", lists any place that is "Not on the map", says "Crime and flood are not mapped" and carries "Map data © OpenStreetMap contributors"
    And below the map At a glance shows the found of total line, the found, "Not known: <count> topics" and "Questions to ask: <count>" counts quoted from `area-result.json`, with the pages of the questions and of the check-in-person lists, and "Things to check in person" with no count (FE-41)
    And it shows the same four facts as the desktop At a glance (AREA-38, AREA-39), each with its source name and no ↗ (PRINT-18)
    And no score, band, verdict or total of priorities is printed

  @ui
  Scenario: PRINT-03 numbered badges sit beside the pins and the numbers match the topic pages
    Given the user has chosen "Print or save as PDF" for the sample postcode "NB1 4XY"
    When the user looks at the cover map and a topic page
    Then each number sits beside its pin and no badge covers an icon (MAP-16)
    And the same number appears beside the same place on its topic page, for example in Getting around and Schools

  # fixture: packages/fixtures/data/pilot-topics.json (the registry: every topic, counted or not; the counted ones are in `area-result.json`)
  # The contents are generated from the registry. Counted topics are checked here by outcome; the topics we only link to are checked by GLANCE-05.
  Scenario: PRINT-04 counted topics print found, not known or not covered, never dropped (registry: PRINT-05)
    Then area result "NB1 4XY" has topic "getting-around" with outcome "found"
    And area result "NB1 4XY" has topic "radon" with outcome "found"
    And area result "NB1 4XY" has topic "housing-affordability" with outcome "found"
    And area result "NB7 1RR" has topic "radon" with outcome "not-known"
    And area result "NB7 1RR" has topic "flood" with outcome "not-known"
    And area result "NB7 1RR" has topic "transport-connectivity" with outcome "not-known"
    And area result "NB7 1RR" has topic "green-space" with outcome "not-covered"
    And area result "NB1 4XY" leaves topic "noise" out of the coverage total

  @ui
  Scenario: PRINT-05 "In this summary" lists every topic in the registry with its page
    Given the user has chosen "Print or save as PDF" for the sample postcode "NB1 4XY"
    When the user reads the contents page
    Then every topic in `pilot-topics.json` is listed in registry order with the page it is on, including the topics we only link to ("Not yet covered: check this") and the Family view ("Regrouped from places listed")
    And a topic with data reads "Facts", and a topic with no data would read "Not known" with the reason, never be dropped
    And the page says "Every topic is listed, none left out." and "Missing information is never shown as zero."
    And "Questions to ask", "Check in person", "How we got this" and "Sources and credits" are listed with their pages
    And the page numbers are worked out by the print layout and are the same as the pages' own numbers

  @ui
  Scenario: PRINT-06 the questions to ask have room to write
    Given the user has chosen "Print or save as PDF" for a sample postcode
    When the user reads the Questions to ask page
    Then each question is quoted from `area-result.json` (`glance.questions`), with the topic it belongs to and that topic's page named under it, and room to write the answer
    And a postcode with no question says there is nothing to list

  # Check in person: the fixed reviewed lists per topic (FE-39), the same text and order as the screen (GLANCE-08), with a tick box for each (FE-41: no count).
  @ui
  Scenario: PRINT-07 the check-in-person pages list every reviewed check by topic with a tick box
    Given the user has chosen "Print or save as PDF" for a sample postcode
    When the user reads the Check in person pages
    Then every topic in `pilot-topics.json` that has a list prints its reviewed list, including Radon, the council tax, noise, mobile and ground and mining lists
    And each line has a tick box and the pages read "These checks are written in advance for each topic, not made up for this postcode"
    And no count of checks is printed (FE-41), and the lists are the same for every postcode

  @ui
  Scenario: PRINT-08 each topic has a page of its own, with its facts, the area they cover and its source
    Given the user has chosen "Print or save as PDF" for the sample postcode "NB1 4XY"
    When the user reads the topic pages
    Then each topic prints its title, the area its facts cover, its facts and its source name, quoted from the records named by ID in `postcode-area.json` and from `area-result.json`
    And Broadband, Radon and Housing affordability print their facts as on the screen: the gigabit-capable share, the radon class and edition for the 1 km square with "Indicative, not definitive: not a test of this home.", and the council-wide rent with "A council-wide average, not this street." (TOPIC-27, TOPIC-31, TOPIC-33)
    And the topic pages carry no "What this doesn't tell you" block: each topic's limits are on the "How we got this" pages (FE-34)
    And Recorded crime and Flood print no map (MAP-12, MAP-13)

  # "Not yet covered here" page (FE-69 "Approve as written (Recommended)" for the row labels and descriptions). Each row's URL is printed in full because a printed page has nothing to tap.
  @ui
  Scenario: PRINT-09 the Not yet covered and Check this rows print what it is, why it matters and the official address
    Given the user has chosen "Print or save as PDF" for the sample postcode "NB1 4XY"
    When the user reads the "Not yet covered here" page
    Then it says "We haven't checked these for this postcode. Each one says what it is and links to the official place to check."
    And "Council tax band of a home", "Mobile by network", "Noise" and "Ground and mining" each print the wording of TOPIC-37 and TOPIC-38 and the official address in full, for example "https://www.gov.uk/council-tax-bands"
    And the Noise row says "Road noise is a layer on the map in Vestagraph online (modelled for 2021, not measured); it isn't printed here. The source has no record of rail noise for this postcode. That does not mean there is no rail noise. For a home, check in person."
    And nothing on the page implies that we looked up this address

  @ui
  Scenario: PRINT-10 the Check this rows inside a topic print their address in full too
    Given the user has chosen "Print or save as PDF" for the sample postcode "NB1 4XY"
    When the user reads the Planning nearby, Flood and Radon pages
    Then the Article 4 directions and tree preservation orders row (TOPIC-36) prints "Find your council's planning team" with its address in full
    And the long-term flood risk row (TOPIC-35) prints "Check your long-term flood risk (gov.uk)" with its address in full
    And the radon link prints "Get a radon report for an address from UKradon (paid)" with its address in full
    And a short note on the last page lists the pages of every "Check this" row

  # FE-34: the printout "already worked this way": method and limits on closing pages. The sentences added to the opening paragraph and the printout's route-only and Family view lines were approved by the founder on 18 Nov 2026 (FE-69).
  @ui
  Scenario: PRINT-11 "How we got this" gives each topic's method and limits after the topic pages
    Given the user has chosen "Print or save as PDF" for the sample postcode "NB1 4XY"
    When the user reads the "How we got this" pages
    Then an opening paragraph says what is specific to this search: distances are straight-line from the postcode centre, when flood warnings were last checked and that the warning check is not a flood risk check, the wider areas named under each fact (the neighbourhood, the council area and the 1 km square for radon), that rows marked "Check this" link to an official service and this address has not been looked up there, that counts come from tested rules and never from AI, and that every place is a made-up example for the sample postcode
    And each topic then prints its source names, its method line and its "Doesn't tell you" line, quoted from the topic's records and limits
    And a "Not yet covered here" block says which topics we hold no data for and, for Noise, that we hold only a modelled road-noise map layer, not shown in print, and that the source has no record of rail noise for this postcode, which does not mean there is no rail noise
    And Housing affordability's limits include "A council-wide average, not this street. It does not say what any one home would rent for."

  # FE-33 (founder, 14 Nov 2026: "Dates only, no notes"): the sources page has dates and no status words. A source we hold no current copy of says "We hold no current copy" instead of a date; the flood source shows when we last checked (AREA-25).
  @ui
  Scenario: PRINT-12 Sources and credits gives each source's data date and no status word
    Given the user has chosen "Print or save as PDF" for the sample postcode "NB1 4XY"
    When the user reads the "Sources and credits" page
    Then it lists each source the printout used in a table of source, data date and credit, the dates quoted from the records named by ID in `postcode-area.json`
    And the flood source reads its data date and "last checked at" with the time of the check, as About the data does (AREA-25)
    And no status word (Cached, Fallback, Old or Unavailable) appears, and a source we hold no current copy of reads "We hold no current copy" instead of a date
    And it lists the sources the design pass added, with their dates only: Ofcom's Connected Nations postcode data, the BGS and UKHSA Indicative Atlas of Radon and the ONS Price Index of Private Rents (AREA-44)

  # Credit lines are the licence's required text (DA-05, the licence register, is not started), so the lines on the board are proposed wording until it is. Rule 1: nothing is invented.
  @ui
  Scenario: PRINT-13 every credit line comes from the sources list and none is invented
    Given the user has chosen "Print or save as PDF" for a sample postcode
    When the user reads the Credit column
    Then each credit is the exact credit the source's licence requires, as held in the sources list, and "Each source's required credit is printed here." is said once
    And a source with no recorded credit line shows its own name only, and no credit is written for a source that is not in the list
    And the credits include the OpenStreetMap contributors line under the Open Database Licence where OpenStreetMap places are printed (DA-25)

  # fixture: packages/fixtures/data/postcode-area.json (NB7 1RR NB7-1RR-AREA-FLOOD-1 and NB7-1RR-AREA-RADON-1, source-failed)
  # The board's NB7 1RR example is a specimen page marked "State example, not part of the NB1 4XY printout".
  Scenario: PRINT-14 the postcode with a failed flood lookup has its flood record as not known
    # Radon's failed record and outcome are checked once, in TOPIC-29.
    Then postcode record "NB7-1RR-AREA-FLOOD-1" has status "source-failed"
    And area result "NB7 1RR" has topic "flood" with outcome "not-known"

  @ui
  Scenario: PRINT-15 a topic whose data is not known prints its own page with the reason and no zero
    Given the user has chosen "Print or save as PDF" for the sample postcode "NB7 1RR"
    When the user reads the Flood and Radon pages
    Then each prints "Not known right now", "We don't hold a current copy of this source." and "The lookup failed, so this is not known right now."
    And Flood warnings add "This is not the same as no warning." and a link line to the GOV.UK long-term flood risk checker printed in full
    And the "Doesn't tell you" line says a failed lookup does not mean there is no flood risk
    And the Questions to ask page includes the flood question and "Has radon been measured in the home, and what was the result?" (TOPIC-28)
    And nothing prints as zero, "none", a clean result or a favourable value (rule 7)

  # AGENTS.md rules, doc 04 §9 stage 5b design quality bar, FE-21 ("readable in black and white") and the plan's Task 4 acceptance.
  @ui
  Scenario: PRINT-16 every printed line is at least 12 pt
    Given the user has chosen "Print or save as PDF" for a sample postcode
    When the page is printed on A4
    Then no text on any page is smaller than 12 pt, including the source stamps, the footers and the credit lines

  @ui
  Scenario: PRINT-17 the printout is readable in greyscale
    Given the user has chosen "Print or save as PDF" for a sample postcode
    When the page is printed in black and white
    Then no meaning is carried by colour alone: charts, the decile boxes, the bars and the map key use shape, position, labels or fill that stay different in greyscale
    And every bar shows its count or distance at its end, and the decile charts mark this neighbourhood's decile with a dark box and say so in words
    And Recorded crime's "Not listed" cells say what they mean in the page's own words

  # FE-33 scope (founder, 14 Nov 2026, "One per list or topic (Recommended)"): "printed stamps carry no ↗". A printed page has nothing to tap, so a source is its name and a link is its address in full.
  @ui
  Scenario: PRINT-18 printed source stamps carry no arrow and links are printed as addresses
    Given the user has chosen "Print or save as PDF" for a sample postcode
    When the user looks at a source stamp and a link on a printed page
    Then the stamp shows the source's icon and name with no "↗", and the source name is not styled as a button
    And a link prints its text with its full address underneath, as in PRINT-09 and PRINT-10

  @ui
  Scenario: PRINT-19 every page, including the cover (page 1), has the same footer with its page number
    Given the user has chosen "Print or save as PDF" for the sample postcode "NB1 4XY"
    When the user looks at the foot of any page, the cover being page 1
    Then it reads "Vestagraph · area summary for " followed by the postcode, "sample data" for the example postcode, the made-at time, and "Page " followed by the page number and "of" the number of pages, both worked out by the print layout (a specimen page is footed "State example" and "not part of" the postcode's printout)

  @ui
  Scenario: PRINT-20 the printout makes no verdict and keeps the privacy line
    Given the user has chosen "Print or save as PDF" for a sample postcode
    When the user reads the whole printout
    Then it contains no score, band, ranking, "safe", "verified", "approved" or verdict about a home or the area, and no AI-written text
    And the last page says "Privacy: this summary was made in your browser. Vestagraph didn't store your search." (AREA-17)
    And for the sample postcode it says that every place, figure and date is a made-up example from a made-up town

  # Added 18 Nov 2026 (energy certificate design). All the wording of this row was approved by the founder on 19 Nov 2026 (copy review, "Approve as written (Recommended)"). Its on-screen version is TOPIC-41.
  @ui
  Scenario: PRINT-21 the printout lists the energy certificate row under "Not yet covered here"
    Given the user has chosen "Print or save as PDF" for a sample postcode
    When the user reads the "Not yet covered here" page
    Then "Energy certificate of a home" is listed there, as "Check this: we haven't checked it", with the official address https://www.gov.uk/find-energy-certificate printed in full
    And it prints no rating, cost or certificate number, and it is not counted in At a glance or in the coverage total
