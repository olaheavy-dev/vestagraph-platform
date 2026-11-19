@screen @buying @renting
Feature: City Explorer neighbourhood page (facts published for one neighbourhood, labelled with their level, and the way on to a postcode)
  Question it answers: "I have no postcode yet: what is published for this neighbourhood, and how do I get from here to a postcode?"
  Modes: both (and anyone, with no account; decisions 0046 and 0055)
  Added 17 Nov 2026 (PR C of the City Explorer plan, Task 14b; decisions 0053, 0054 and 0055; register lines FE-45, FE-46, FE-48, DA-14, DA-21, PD-19). The design is `docs/superpowers/specs/2026-11-15-city-explorer-design.md` ("Neighbourhood result page"). The council page is `city-explorer.feature` (CITY); compare, share and print, what changed and the City Explorer About the data board are `city-explorer-part-2.feature` (CITY2).
  Fixtures: the neighbourhoods of each council, listed by their LSOA code, in `packages/fixtures/data/council-area.json` (each fact with its level and source; `councils[].neighbourhoods[].facts`) and in `packages/fixtures/generated/council-result.json` (`councils[].neighbourhoods`: label and tenure shares). The sample neighbourhoods: E01999011 "Northbridge Centre (synthetic) (011A)", E01999012 and E01999013 in Northbridge E06999001; E01999021 in Southvale E06999002; E01999031 "Eastmere Green" in Eastmere E07999001, whose deprivation fact has no record in its source; Westmere E07999002 has none. The data names read "(synthetic)"; the boards print the same names with "(sample)", and every scenario quotes the board's text. The boards draw one neighbourhood, Northbridge Centre, so its scenarios name that code; the address uses the short code ("011A").
  Figures: none typed here (AGENTS.md rule 2). The connectivity score and decile, and the deprivation decile, rank and number of areas, are published inputs recorded with their source in `council-area.json`; a scenario cites them by field and the page quotes them. The tenure shares are calculated outputs of `council-result.json`, cited by neighbourhood code. A scenario never types a number.
  Where: the neighbourhood result page, titled "<larger area's name> (<code>)" and reached from the council page's neighbourhoods map or list (CITY-90). Boards, on the canvas page "Pilot · City Explorer" (design canvas version 407, each with its Dark twin): NeighbourhoodPage (phone, 390) and NeighbourhoodPageDesktop (1440, a fluid page, the map beside the facts). Both draw the same sample neighbourhood.
  Address: the neighbourhood travels after the "#", for example `/council/northbridge#n=011A`, so it never reaches our logs (founder, 15 Nov 2026, "Code after # (Recommended)"; as postcodes, decision 0046). A neighbourhood page is therefore never in the sitemap or a search engine; council pages are (CITY-02).
  Rule 7: a fact the source has no record for is never shown as zero, a favourable value or a clean result. Topics that need a postcode say so and are never worked out from the neighbourhood's centre.
  Rule 4 and 0054: no ranking of neighbourhoods, no "1st of N", no combined score, no score drawn on a map, no verdict words. What is allowed is the official deprivation rank and decile and DfT's own decile, quoted as published with 0054's notes ("relative, not absolute"; "describes the neighbourhood, not a street").
  Wording status: the board texts quoted below are the canvas's. Not drawn on any board, so proposed wording, approved by the founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)") (issue #318 stays open until the boards are drawn), finalised before build: a neighbourhood fact the source has no record for (HOOD-14), an address whose code matches no neighbourhood (HOOD-37) and the page's loading, offline and all-sources-down messages (HOOD-38). Not generated yet: the neighbourhood tenure sentence (issue #294, HOOD-19) and the At a glance counts (a noticed issue, like the council coverage line, FE-44, #292; HOOD-07). The map drawing on both boards is a placeholder for our own street map tiles (FE-03, still to price), and the boundary year in the credit is the placeholder "[year of the boundary edition]" because no data file holds it.
  Price lines by property type (FE-47, BE-37): the neighbourhood page draws no price, rent or council tax figure of its own (HOOD-26 says so). The four price lines are on the council page (CITY-64 to CITY-73) and each council's four averages are in compare (CITY2-09 to CITY2-11).
  Data scenarios (no tag) check the facts in `council-area.json` and `council-result.json` with the council steps in docs/specs/README.md. Every other scenario is `@ui`, because the outcome is on the page.

  Board-to-scenario map (each board has a Dark twin that shows the same states; HOOD-41):
    NeighbourhoodPage, phone: header and title -> HOOD-02 to HOOD-04; the postcode box -> HOOD-05; At a glance -> HOOD-06, HOOD-07; Published for this neighbourhood: Transport connectivity -> HOOD-08 to HOOD-11, Deprivation -> HOOD-12 to HOOD-16, Who rents, who owns -> HOOD-17 to HOOD-20; Needs a postcode -> HOOD-21 to HOOD-23; Council area facts -> HOOD-24 to HOOD-26; Where it sits -> HOOD-27 to HOOD-29; How we got this -> HOOD-30 to HOOD-33; links at the foot -> HOOD-34
    NeighbourhoodPageDesktop: the same rows, with the map beside the facts -> HOOD-03, HOOD-27
    CouncilReportProblem (the council board; a neighbourhood fact follows its anatomy, with no board of its own): Report a problem on a neighbourhood fact -> HOOD-42 (REPORT-04)
    Not on a board: the states -> HOOD-36 to HOOD-38; privacy and accessibility -> HOOD-39, HOOD-40; the Dark twins -> HOOD-41
    Not on any board and not a scenario here: "price lines by property type" (see above); the council tools for ChatGPT and Claude belong to `area-tools.feature`.

  Figure map (every figure a scenario mentions -> where it comes from; the page quotes the value, the scenario never types it):
    connectivity score and decile -> `council-area.json` <council code> / neighbourhoods / <LSOA code> / facts / connectivity / value (score, decile), with its level and source (edition, period)
    deprivation decile, rank and number of areas -> `council-area.json` <council code> / neighbourhoods / <LSOA code> / facts / deprivation / value (decile, rank, ofAreas, edition), quoted as published
    tenure shares (five) -> `council-result.json` <council code> / neighbourhoods / <LSOA code> / tenureShares (input counts: `council-area.json` facts / tenure / value)
    the neighbourhood tenure sentence -> not generated yet (issue #294); until then its percentage is the privateRented share above
    neighbourhood names and codes -> `council-result.json` <council code> / neighbourhoods (label, code)
    the council's population -> `council-area.json` <council code> / population
    the At a glance counts -> not generated yet (noticed issue #339)
    the typed postcode -> the visitor's own input, never a record

  Required states (doc 03 §5; AGENTS.md rules 1, 4, 6 and 7):
    loading -> HOOD-38
    empty: no facts at all for a neighbourhood -> not a sample case; a fact with no record -> HOOD-13, HOOD-14
    ambiguous match: not applicable (the code in the address names one neighbourhood; a code that matches none -> HOOD-37)
    not covered: Wales, Scotland and Northern Ireland have no neighbourhood page (council page CITY-19, CITY-20)
    not found -> HOOD-37
    partial answer: a fact with no record, the topics that need a postcode, a council with no neighbourhoods -> HOOD-13, HOOD-14, HOOD-21 to HOOD-23, HOOD-36
    stale or provisional edition: no edition tag sits beside a figure (FE-45; the status is on About the data, CITY2-65, CITY2-69); a stale edition would use the council page's wording (CITY-95) and waits for a stale fixture
    source failed, offline -> HOOD-38
    privacy -> HOOD-03, HOOD-39

  # The page: header, title, address and the postcode box (design spec, "Neighbourhood result page").
  Scenario: HOOD-01 Northbridge lists Northbridge Centre by its larger area's name and code
    Then council "E06999001" lists neighbourhood "E01999011" with label "Northbridge Centre (synthetic) (011A)"

  @ui
  Scenario: HOOD-02 the header names the neighbourhood and the council area it sits in
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the page has loaded
    Then the page heading reads "Northbridge Centre (sample) (011A)", quoted from `E06999001 / neighbourhoods` (label)
    And the line under it reads "Neighbourhood in Northbridge (sample) council area. Tap a topic for its details and source. Each fact says which area it covers and when."
    And above it the link "← About Northbridge (sample) council area" opens the council page for "E06999001"

  @ui
  Scenario: HOOD-03 the neighbourhood is in the address after the hash, so it never reaches the logs
    Given the user has chosen "See this neighbourhood" for "E01999011" on the council page for council "E06999001" (CITY-90)
    When the neighbourhood page opens
    Then the address is the council's address followed by "#n=" and the neighbourhood's short code, for example "/council/northbridge#n=011A"
    And no neighbourhood name or code is in the path or the query string, and opening that address again opens the same page

  @ui
  Scenario: HOOD-04 on desktop the map sits beside the facts and on a phone it follows them
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the page is shown at desktop width and then at phone width
    Then at desktop width the page shows the header "Check an area" and "City Explorer", and the map sits beside the facts
    And at phone width the page is one column and "Where it sits" follows "Council area facts"

  @ui
  Scenario: HOOD-05 the postcode box opens the postcode result and says if it is in another council
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user types a postcode in the box labelled "Postcode", under "Have a postcode from a listing?", and chooses "Check"
    Then the postcode result opens
    And the line under the box reads "Opens the postcode result for it. It says if the postcode is in another council area."

  # At a glance follows the postcode area result: counts of topics, no figures in the tiles (so no rank or decile appears without its notes).
  @ui
  Scenario: HOOD-06 At a glance counts the topics found and the topics that need a postcode, with no figure in the tiles
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "At a glance"
    Then two tiles read "Found" with "topics" and "See them →", and "Needs a postcode" with "topics" and "See them →"
    And no connectivity score, decile, deprivation rank or share is in a tile

  # The counts have no generator field yet (noticed issue #339, as FE-44, #292, for the council page), so no data step.
  @ui
  Scenario: HOOD-07 the At a glance line gives the counts and says each fact has its area and date
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "At a glance"
    Then the line reads "<found> of <total> topics have facts for this neighbourhood; <needing> need a postcode. Each fact says which area it covers and when, further down.", with the three numbers quoted from the neighbourhood's generated coverage field (not generated yet)
    And the numbers are the rows drawn under "Published for this neighbourhood" and "Needs a postcode"

  # Transport connectivity (DfT, neighbourhood level). FE-45: the DfT status is on About the data only.
  Scenario: HOOD-08 Northbridge Centre has a published transport connectivity figure at neighbourhood level
    Then council "E06999001" neighbourhood "E01999011" has fact "connectivity" with status "recorded"
    And council "E06999001" neighbourhood "E01999011" has fact "connectivity" at level "neighbourhood"

  @ui
  Scenario: HOOD-09 the connectivity score is quoted on DfT's scale with its area, quarter and edition
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "Transport connectivity", headed "Neighbourhood level · <period>", the period quoted from the connectivity fact's `source` (period)
    Then it shows "Connectivity" and "<score> on a scale of 0 to 100" quoted from `council-area.json` for "E06999001" / "E01999011" (connectivity score)
    And the line under it reads "Neighbourhood · Northbridge Centre (sample) (011A) · <period> (edition <edition>) · 100 is the most connected on DfT’s scale"
    And no "provisional" or "Experimental Statistics" tag sits beside the figure (FE-45)

  @ui
  Scenario: HOOD-10 the connectivity decile is quoted as published with its direction
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "Transport connectivity"
    Then it shows "Connectivity decile" and the decile quoted from `council-area.json` for "E06999001" / "E01999011" (connectivity decile)
    And the line under it reads "Neighbourhood · Northbridge Centre (sample) (011A) · <period> · decile 10 is the most connected tenth of areas, decile 1 the least connected tenth"
    # The research did not confirm the decile columns in the real DfT file; the build checks they exist before the page quotes a decile.

  @ui
  Scenario: HOOD-11 transport connectivity says it is relative, not absolute, and describes the neighbourhood, not a street
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "Transport connectivity"
    Then it says "Relative, not absolute. DfT says scores should be interpreted relative to other areas, and a decile compares areas with each other. It describes the neighbourhood, not a street."
    And the source stamp reads "DfT transport connectivity metric"

  # Deprivation (the official rank and decile, quoted as published; 0054).
  Scenario: HOOD-12 Northbridge Centre has a published deprivation rank and decile at neighbourhood level
    Then council "E06999001" neighbourhood "E01999011" has fact "deprivation" with status "recorded"
    And council "E06999001" neighbourhood "E01999011" has fact "deprivation" at level "neighbourhood"

  Scenario: HOOD-13 Eastmere Green has no deprivation record in its source
    Then council "E07999001" neighbourhood "E01999031" has fact "deprivation" with status "no-record-in-source"
    And council "E07999001" neighbourhood "E01999031" has fact "connectivity" with status "recorded"

  # Proposed wording, approved by the founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)") (no board draws a neighbourhood fact with no record): it follows the council page's missing-source rule (CITY-52, CITY-53).
  @ui
  Scenario: HOOD-14 a deprivation fact with no record says so and shows no decile, no rank and no zero
    Given the user has opened the neighbourhood page for neighbourhood "E01999031" of council "E07999001"
    When the user reads "Deprivation"
    Then the row says the source has no record for this neighbourhood (wording to be drawn before build)
    And no decile, no rank, no "of" count and no zero is shown, and the connectivity row still shows its figures

  @ui
  Scenario: HOOD-15 the deprivation decile and the published rank are quoted as the source gives them
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "Deprivation", headed "Neighbourhood level · one edition, as published"
    Then it shows "Deprivation decile" with the decile quoted from `council-area.json` for "E06999001" / "E01999011" (deprivation decile), and "Neighbourhood · Northbridge Centre (sample) (011A) · sample edition"
    And it shows "Published rank" as "<rank> of <ofAreas>" quoted from the same record (rank and ofAreas), with the same area line
    And the source stamp reads "English Indices of Deprivation"

  @ui
  Scenario: HOOD-16 the deprivation rank and decile carry 0054's notes and say we do not rank
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "Deprivation"
    Then it says "Relative, not absolute. A rank compares neighbourhoods with each other; it says nothing about how deprived any one is in itself."
    And it says "Describes the neighbourhood, not a street. It does not describe this home or this street."
    And it says "Quoted as published (decile 1 is the most deprived 10% of neighbourhoods nationally). We do not rank neighbourhoods or add a score."

  # Who rents, who owns (Census 2021, TS054, neighbourhood level; FE-48).
  Scenario: HOOD-17 Northbridge Centre has tenure shares at neighbourhood level
    Then council "E06999001" neighbourhood "E01999011" has tenure shares
    And council "E06999001" neighbourhood "E01999011" has fact "tenure" at level "neighbourhood"

  @ui
  Scenario: HOOD-18 who rents and who owns is one bar for Census day with its five shares
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "Who rents, who owns", headed "Neighbourhood level · Census day, 21 March 2021 · share of households"
    Then one bar shows five shares quoted from `E06999001 / neighbourhoods / E01999011 / tenureShares`: "Owned outright", "Owned with a mortgage or loan", "Rented from the council or a housing association", "Rented privately" and "Other"
    And "Show as table" gives the same five shares as a table
    And the source stamp reads "Census 2021, TS054"

  @ui
  Scenario: HOOD-19 the neighbourhood tenure sentence is the single-point sentence for March 2021
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads under the bar
    Then the sentence reads "In March 2021, <percent>% of households rented privately." (DA-21)
    And <percent> is quoted from the neighbourhood's generated caption field once it exists (issue #294); until then it is the "privateRented" share of `E06999001 / neighbourhoods / E01999011 / tenureShares`, and the sentence is never typed

  @ui
  Scenario: HOOD-20 under every tenure bar one line says the shares are rounded
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads under the bar
    Then one line reads "Shares are rounded to one decimal place, so they may not add up to 100%." (FE-48)
    And the line carries no figure

  # Needs a postcode (the topics that depend on exactly where a home is; never worked out from the neighbourhood's centre).
  @ui
  Scenario: HOOD-21 four topics say they need a postcode and why
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "Needs a postcode"
    Then it says "These depend on exactly where a home is, so we do not work them out from the neighbourhood’s centre."
    And four rows are listed: "Getting around" ("Bus stop and station distances"), "Everyday places" ("Shops, GP surgery and pharmacy distances"), "Flood risk" ("Long-term flood risk by postcode") and "Sold prices nearby" ("Recent sales close to a postcode")

  @ui
  Scenario: HOOD-22 each of the four rows says to check a postcode and jumps to the postcode box
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user chooses the row "Flood risk"
    Then the row reads "Check a postcode in this neighbourhood to see this"
    And focus moves to the box labelled "Postcode"
    And the same holds for "Getting around", "Everyday places" and "Sold prices nearby"

  @ui
  Scenario: HOOD-23 no distance, flood risk or sold price is shown for a neighbourhood
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads the whole page
    Then no distance, no flood risk and no sold price appears, and no postcode is picked to stand for the neighbourhood

  # Council area facts (labelled with the council, not the neighbourhood; DA-14).
  @ui
  Scenario: HOOD-24 the population is labelled with the council, not the neighbourhood
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "Council area facts", headed "Council area level · labelled with the council, not the neighbourhood"
    Then it shows "Population" quoted from `council-area.json` for "E06999001" (population), with "Council area · Northbridge (sample) · mid-2025 estimate"
    And the source stamp reads "ONS mid-year population estimates"

  @ui
  Scenario: HOOD-25 the page links to the council's rents, prices and council tax
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user chooses "See rents, prices and council tax for Northbridge (sample) →"
    Then the council page for "E06999001" opens

  @ui
  Scenario: HOOD-26 the neighbourhood page draws no rent, price or council tax of its own
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads the whole page
    Then no rent, house price, price by property type or council tax figure is shown for the neighbourhood
    And those figures stay on the council page, labelled with the council (CITY-31, CITY-64 to CITY-73)

  # Where it sits (the neighbourhood's place on the council map; the map is not coloured by any score, 0054).
  @ui
  Scenario: HOOD-27 the map shows where the neighbourhood sits and is not coloured by any figure
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "Where it sits", headed "Neighbourhood level · inside Northbridge (sample) council area"
    Then a map shows the neighbourhood inside the council area
    And no area is coloured by a score, rank, decile or figure (0054)
    And the line under it reads "Map drawing is a placeholder for our own street map tiles. It is not coloured by any figure." on the board only, the real map carrying our own tiles (FE-03)

  @ui
  Scenario: HOOD-28 the map names its boundary and name sources
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads under the map
    Then the source line reads "Source: Office for National Statistics licensed under the Open Government Licence v.3.0. Contains OS data © Crown copyright and database right [year of the boundary edition]. Neighbourhood names: House of Commons Library MSOA names, under the Open Parliament Licence."
    And "Boundary and name sources, under How we got this ↓" links to those stamps
    # The board shows "[year of the boundary edition]" as a placeholder; the real page prints the edition's year from its source record.

  @ui
  Scenario: HOOD-29 the page links back to the neighbourhood's place on the council page map
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user chooses "Show on the council page map, Northbridge (sample) →"
    Then the council page for "E06999001" opens at its neighbourhoods map

  # How we got this (FE-24, FE-34; one closing section, as the postcode area result).
  @ui
  Scenario: HOOD-30 "How we got this" says each fact has its level and period and that nothing is ranked or combined
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "How we got this"
    Then it reads "Each fact says its level (here the neighbourhood, or the council area for the population line) and its period. The deprivation rank and decile are quoted as the government publishes them, with their notes; we do not rank neighbourhoods and we do not combine facts into a score. Topics that need a postcode are not worked out from the neighbourhood’s centre. The percentages come from our tested rules, never from AI. Sample data: every council, neighbourhood and figure is made up, shaped like the source named beside it."

  @ui
  Scenario: HOOD-31 each fact has one line with its source stamp
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "How we got this"
    Then one line each is listed for "Transport connectivity", "Deprivation", "Who rents, who owns", "Population (council area)" and "Neighbourhood boundaries and names"
    And their stamps read "DfT transport connectivity metric", "English Indices of Deprivation", "Census 2021, TS054", "ONS mid-year population estimates", "ONS boundaries and licence" and "House of Commons Library MSOA names"

  @ui
  Scenario: HOOD-32 the four postcode topics are listed as needing a postcode, not as facts
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads "How we got this"
    Then "Getting around", "Everyday places", "Flood risk" and "Sold prices nearby" are each listed with "Needs a postcode"
    And none has a source stamp, because nothing is quoted for the neighbourhood

  @ui
  Scenario: HOOD-33 "How we got this" links to About the data
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user chooses "How each source works, its date and its status: About the data →"
    Then the City Explorer About the data page opens (`city-explorer-part-2.feature`, CITY2-58)

  @ui
  Scenario: HOOD-34 the page links to Use in ChatGPT or Claude
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user chooses "Use in ChatGPT or Claude →"
    Then the how-to page opens (decision 0056)
    And the page has no on-page chat (0056)

  # Never (design spec): a picked postcode standing for the neighbourhood, a combined score, a ranking of neighbourhoods.
  @ui
  Scenario: HOOD-35 the page has no ranking of neighbourhoods, no score and no verdict word
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads the whole page
    Then it ranks no neighbourhood, shows no "1st of N", no combined score and no score drawn on a map (0054)
    And no caption, label or sentence of ours calls a figure "best", "better", "good", "high", "low", "safe" or "approved"
    And the only rank is the official deprivation rank, quoted as published with its notes (HOOD-16)

  # States. No board draws these for a neighbourhood: the behaviour is specified, the wording follows the council page's states where it exists and is finalised before build.
  Scenario: HOOD-36 Westmere has no neighbourhoods, so no neighbourhood page can be opened for it
    Then council "E07999002" lists no neighbourhoods

  @ui
  Scenario: HOOD-37 an address whose code matches no neighbourhood of the council says so and offers the council page
    Given the user opens the address of council "E06999001" followed by "#n=" and a code that matches none of its neighbourhoods
    When the page has loaded
    Then it says in plain words that no neighbourhood has that code (wording to be drawn before build, as the council page's "Council not found")
    And the one action opens the council page for "E06999001"
    And no other neighbourhood's page opens in its place

  @ui
  Scenario: HOOD-38 while a neighbourhood loads, offline or with every source down the page says so and stays honest
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the page is loading, the device goes offline, or our stored copies cannot be reached
    Then each case shows the council page's message for it (CITY-94, CITY-99, CITY-100), worded for a neighbourhood before build
    And no fact is shown as zero or as a clean result

  # Privacy and accessibility (design spec Constraints; decisions 0014, 0046, 0053).
  @ui
  Scenario: HOOD-39 the typed postcode is never stored or logged and no third party sees a page view
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user types a postcode in the box and chooses "Check"
    Then the postcode is not stored or written to any log, and analytics never records the box (FE-05)
    And boundary files, map tiles, fonts and the chart library are served from our own hosting, so no third party sees the page view (B28)

  @ui
  Scenario: HOOD-40 the page works by keyboard with touch targets of at least 44 px and no sideways scrolling
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user works through the page by keyboard, and then on a phone
    Then every control can be reached and used by keyboard, and each is at least 44 px tall
    And the page does not scroll sideways, and errors are tied to their inputs

  @ui
  Scenario: HOOD-41 every board has a dark twin and the display control changes the theme and text size
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user chooses "Display" and picks the dark theme and a larger text size
    Then the page shows the same facts, notes and states as the light board, in the dark twin's colours and at the chosen size

  # Added 19 Nov 2026 (pilot design batch, PR 1; founder's choice, "Also City Explorer"; register line FE-74). The behaviour, states, wording and counts are `report-a-problem.feature` (REPORT-04, REPORT-23); this scenario only points the neighbourhood page at it.
  @ui
  Scenario: HOOD-42 each neighbourhood fact has "Report a problem", as REPORT-04 sets
    Given the user has opened the neighbourhood page for neighbourhood "E01999011" of council "E06999001"
    When the user reads each fact published at neighbourhood level
    Then each has "Report a problem" (REPORT-04), and a report is counted by the figure's name and the neighbourhood's public code, never an address (REPORT-23)
    And a fact shown at council level on the page is reported as the council's (REPORT-03)
