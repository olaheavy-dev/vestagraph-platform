@screen @buying @renting
Feature: City Explorer council page (one page per council: search, what it costs, rent or buy, your budget, charts and their captions, states, privacy)
  Question it answers: "What does it cost to live in this council area each month, to rent or to buy, and how do I get from the council down to a postcode?"
  Modes: both (and anyone, with no account; decisions 0046 and 0055)
  Added 17 Nov 2026 (PR C of the City Explorer plan, Task 14a; decisions 0053, 0054 and 0055; register lines FE-37, FE-43 to FE-45, FE-47, FE-48, FE-50, DA-21, BE-38, PD-19). The design is `docs/superpowers/specs/2026-11-15-city-explorer-design.md` (the council page sections); the neighbourhood result page is `city-explorer-neighbourhood.feature` (HOOD), and compare, share and print, what changed and the council tools are `city-explorer-part-2.feature` (CITY2); they are written in `city-explorer-neighbourhood.feature` and `city-explorer-part-2.feature`, not here.
  Fixtures: councils by code in `packages/fixtures/data/council-area.json` (inputs, each with its source) and `packages/fixtures/generated/council-result.json` (every calculated figure). The sample councils: E06999001 Northbridge (complete, unitary, three neighbourhoods), E06999002 Southvale (price start point not published), E07999001 Eastmere (district, formed 2023-04-01 from "East Westshire Borough", no published rent, one property type with no record, a method break in the affordability series) and E07999002 Westmere (district, nothing recorded: no council tax, rent, price, ratio, tenure or connectivity). The data names read "(synthetic)"; the boards print the same names with "(sample)", and every scenario here quotes the board's text. The postcode SV2 3AB belongs to E06999002.
  Figures: none typed here (AGENTS.md rule 2). A scenario that needs a figure names the council code and the generated field (the figure map below); the page quotes the number from the file.
  Where: the page for one council, titled with its name (for example "Northbridge Council area"; the boards show "Northbridge (sample)"). Boards, on the canvas page "Pilot · City Explorer" (design canvas version 407, each with its Dark twin): CouncilPage (phone), CouncilPageDesktop, CouncilBudgetValue (phone and desktop) and CouncilStates (26 states, phone width; the same messages sit in the desktop page's content area). The printout (CouncilPrint, FE-50), compare, what changed, About the data and the neighbourhood boards belong to the other City Explorer features.
  "The council search" (agent's call, open to the founder, 17 Nov 2026): no board draws a page of its own for searching councils. In these scenarios "the council search" is the landing page's one search box (FE-37, `01-landing.feature` LAND-14 to LAND-16), with the ambiguous, not-covered and not-found messages of CouncilStates shown where its result goes. "← Check another place" on a council page returns to the landing page with the box ready, and the landing footer's "Explore council areas" opens the same box (LAND-20).
  Rule 7: a missing figure is never shown as zero, a flat line, a favourable value or a clean result. A caption needs both end points. A difference needs both sides.
  Rule 4 and 0054: no ranking of councils, no "1st of N", no score drawn on a map, no combined score, no verdict words. The sentences under each chart are built by tested rules from the generated figures, never by AI.
  Sign-in: on this page the chat entry and Save lead to sign-in when signed out (AUTH-28 in `sign-in.feature` owns that scenario, for council E06999001; not repeated here).
  Wording status: the board texts quoted below are the canvas's. Three sentences have no board yet and are proposed wording, finalised before build: the "less" and the "about the same" patterns of the rent or buy sentence (DA-21 approved only the "more" pattern), and the "not comparable" caption for a change that spans a method break.
  Still to draw or generate (the scenarios are written; each carries a comment): the phone sheets for the neighbourhoods map, who rents and who owns, and transport connectivity (FE-43: the boards are not drawn yet, so CITY-25 and its siblings are `@ui` and say so); the coverage line's generator field (FE-44, issue #292, CITY-32).
  Data scenarios (no tag) check the facts in `council-area.json` and `council-result.json` with the council steps in docs/specs/README.md. Every other scenario is `@ui`, because the outcome is on the page, or is a rule on typed input that the server works out (`vestagraph_area`, 0053) and no sample council records.

  Board-to-scenario map (each board has a Dark twin that shows the same states; CITY-108):
    CouncilPage, phone: the header and the postcode box -> CITY-01, CITY-03; cost summary then topic rows -> CITY-23; the open House prices sheet -> CITY-24, CITY-64 to CITY-67; the other sheets -> CITY-25; band picker as a select -> CITY-27; Band D example, rent, price -> CITY-28, CITY-31; rent or buy -> CITY-34, CITY-38; budget empty -> CITY-55; neighbourhoods row -> CITY-87; How we got this -> CITY-91 to CITY-93
    CouncilPageDesktop: layout and wrap -> CITY-26; band chips -> CITY-27; the charts and their captions -> CITY-61 to CITY-86; neighbourhoods map, list and panel -> CITY-87 to CITY-90
    CouncilBudgetValue, phone and desktop: a typed budget -> CITY-56, CITY-57; the box's privacy line -> CITY-59
    CouncilStates 1 Loading -> CITY-94; 2 Council not found -> CITY-21; 3 Place in more than one council -> CITY-09, CITY-10; 4 Places sharing a name -> CITY-11, CITY-12; 5 London search -> CITY-13, CITY-14; 6 County search -> CITY-15, CITY-16; 7 Former council name -> CITY-17, CITY-18; 8 Series starts at a council merger -> CITY-98; 9 Not covered (Wales) -> CITY-19, CITY-20; 10 Postcode in another council -> CITY-04, CITY-05; 11 A source missing for this council -> CITY-52, CITY-53; 12 Provisional edition -> CITY-83; 13 Stale edition -> CITY-95; 14 Figure published only for the county -> CITY-96; 15 Broken series -> CITY-76 to CITY-78; 16 Council replaced -> CITY-97; 17 One side missing -> CITY-50, CITY-51; 18 No rate band -> CITY-39, CITY-40, CITY-41; 19 Working out -> CITY-47, CITY-49; 20 Couldn’t work this out -> CITY-48; 21 Invalid budget -> CITY-58; 22 Invalid deposit, rate or term -> CITY-42 to CITY-45; 23 Offline -> CITY-99; 24 All sources down -> CITY-100; 25 A property type not published -> CITY-70, CITY-71; 26 A type’s 12-month change not published -> CITY-72, CITY-73; a small loan's band (Review Focus 2) -> CITY-111; the all-eight-bands answer -> CITY-110

  Figure map (every figure a scenario mentions -> its ID; the page quotes the value, the scenario never types it). `council-result.json` figures are cited as <council code> / <path>; inputs as the field in `council-area.json`:
    population -> `council-area.json` <code> / population
    council tax for the band picked, a year and a month -> `council-result.json` <code> / bands / <band> / shownYearly and shownCouncilTax (inputs: `council-area.json` <code> / bands, the published yearly amounts)
    the eight bars -> <code> / bands / A to H / shownYearly and shownCouncilTax
    average rent -> `council-area.json` <code> / rentSeries, its newest point (period and status in <code> / rentOrBuy / rentPeriod and rentPointStatus)
    average price -> `council-area.json` <code> / priceSeries, its newest point (<code> / rentOrBuy / pricePeriod and pricePointStatus)
    the price of each type -> `council-area.json` <code> / priceSeries / byType, the newest point of each type
    rent side -> <code> / rentOrBuy / byBand / <band> / shownRentSide
    buy side, repayment, difference and its direction -> <code> / rentOrBuy / byBand / <band> / buySides / <product> / shownBuySide, shownRepayment, shownDifference, comparison
    rate, its band and month -> <code> / rentOrBuy / byBand / <band> / buySides / <product> / rateBand (input: `council-area.json` rateBands)
    example deposit and term -> `council-result.json` exampleInputs
    captions -> <code> / captions (rent, price, affordability, tenure) and <code> / priceByType (the four types), each with its `pattern`, `reason`, periods and values
    tenure shares -> <code> / tenureShares
    connectivity -> `council-area.json` <code> / connectivity
    neighbourhoods and their names -> <code> / neighbourhoods (label, code)
    the sources' dates and editions -> the `source` of each field in `council-area.json`
    the "N of M topics published" coverage line -> not generated yet (FE-44, #292)
    the typed budget, a typed deposit, rate or term -> the visitor's own input, never a record

  Required states (doc 03 §5; AGENTS.md rules 1, 4, 6 and 7; plan Review Focus 1 to 7):
    loading -> CITY-94
    empty: the budget box with nothing typed -> CITY-55
    ambiguous match: a place in several councils, places sharing a name, London, a county -> CITY-09 to CITY-16
    not covered: Wales, Scotland, Northern Ireland -> CITY-19, CITY-20
    not found -> CITY-21
    partial answer: a source missing, no rent, no council tax, a type not published, a start point not published -> CITY-50 to CITY-53, CITY-70 to CITY-73
    stale or provisional edition -> CITY-83, CITY-95
    source failed, offline -> CITY-99, CITY-100
    a broken series, a series that starts at a merger -> CITY-76 to CITY-78, CITY-98
    deposit of 100% or more, rate too high, term out of range -> CITY-42 to CITY-45
    a loan above the highest published band, a product with no rate at the deposit's band -> CITY-39 to CITY-41
    privacy and rate limits -> CITY-59, CITY-101 to CITY-105

  # The page: header, title and the postcode box (design spec, "The page", sections 1 and "Search and the postcode link").
  @ui
  Scenario: CITY-01 the header names the council, what it is, its population and the source
    Given the user has opened the council page for council "E06999001"
    When the page has loaded
    Then the page heading is the council's name followed by "(sample)", and the line under it reads "Council area (sample) · unitary council. Each fact says which area and which period it covers."
    And a line shows the population quoted from `council-area.json` for "E06999001" as "Population <n> (mid-2025 estimate, council area)" with the stamp "ONS mid-year population estimates"
    And no other figure sits in the header

  @ui
  Scenario: CITY-02 each council page has its own title and description and is in the sitemap
    Given the user has opened the council page for council "E06999001"
    When the page has loaded
    Then the browser title and the page description name the council and say it is a council area
    And the council's address is listed in the sitemap, and the neighbourhood pages are not (HOOD, 0055: neighbourhoods travel after the #)

  @ui
  Scenario: CITY-03 the postcode box opens the postcode result
    Given the user has opened the council page for council "E06999001"
    When the user types a postcode in the box labelled "Check a postcode here" and chooses "Check"
    Then the postcode result opens
    And the line under the box reads "Opens the postcode result; it says if the postcode is in another council area."

  # fixture: packages/fixtures/data/council-area.json `postcodes` (SV2 3AB belongs to E06999002); the search list in council-result.json carries it.
  Scenario: CITY-04 the postcode SV2 3AB belongs to Southvale, not Northbridge
    Then council search "SV2 3AB" has kind "council-for-postcode"
    And council search "SV2 3AB" lists council "E06999002"

  # The boards differ on this button: CouncilPage draws "Check" (CITY-03), CouncilStates board 10 draws "Search" (this scenario). Each scenario follows its own board; the founder picks one label when the build starts (reported in PR C).
  @ui
  Scenario: CITY-05 a postcode from another council says which council it is in and still opens
    Given the user has opened the council page for council "E06999001"
    When the user types "SV2 3AB" in the box labelled "Check a postcode here" and chooses "Search"
    Then it says "SV2 3AB is in Southvale (sample)" and "You searched from Northbridge (sample), but this postcode is in a different council area."
    And it says "We still open its result. Its council facts are for Southvale (sample), not Northbridge (sample)."
    And the one action "Open the result for SV2 3AB" opens the postcode result

  # Part 2 owns what the two buttons do (CITY2-). Here: they exist and are not a ranking.
  @ui
  Scenario: CITY-06 the header carries Compare and Share, which are part 2
    Given the user has opened the council page for council "E06999001"
    When the page has loaded
    Then the header shows "Compare" and "Share"
    And choosing them opens the compare and share features specified in `city-explorer-part-2.feature`

  # Search (FE-37; design spec "Search and the postcode link"; decision 0055 point 3).
  Scenario: CITY-07 a council name leads to that one council
    Then council search "Northbridge (synthetic)" has kind "council"
    And council search "Northbridge (synthetic)" lists council "E06999001"

  @ui
  Scenario: CITY-08 searching a council name opens its page with a way back to the search
    Given the user is on the council search
    When the user searches for "Northbridge (sample)"
    Then the page for council "E06999001" opens, titled with the council's name
    And the page has a link "← Check another place", which returns to the landing page's one search box

  Scenario: CITY-09 a place in two councils lists both
    Then council search "Eastmere Westmere Fields (synthetic)" has kind "choose"
    And council search "Eastmere Westmere Fields (synthetic)" lists council "E07999001"
    And council search "Eastmere Westmere Fields (synthetic)" lists council "E07999002"

  @ui
  Scenario: CITY-10 a place in more than one council asks the visitor to choose and never picks
    Given the user is on the council search
    When the user searches for "Eastmere Westmere Fields (sample)"
    Then the page says "Eastmere Westmere Fields (sample) is in more than one council area" and "Choose the council area you mean."
    And it says "We don’t pick one for you; each leads to that council’s own page."
    And it lists "Eastmere (sample)" and "Westmere (sample)", each as "Council area · Westshire (sample)", in the data's order, not a ranking
    And no council page has opened

  Scenario: CITY-11 two places called Newbury are both returned
    Then council search "Newbury (synthetic)" has kind "choose"
    And council search "Newbury (synthetic)" lists council "E07999001"
    And council search "Newbury (synthetic)" lists council "E06999002"

  @ui
  Scenario: CITY-12 places sharing a name are listed with their county and none is picked
    Given the user is on the council search
    When the user searches for "Newbury (sample)"
    Then the page says "More than one place is called Newbury (sample)" and "They are in different counties. Choose the one you mean."
    And it says "We list the county beside each so you can tell them apart; none is picked for you."
    And it lists "Newbury (sample), Westshire (sample)" with "Council area · Eastmere (sample) · West (sample)" and "Newbury (sample), Southshire (sample)" with "Council area · Southvale (sample) · South (sample)"
    And no council page has opened

  Scenario: CITY-13 the London stand-in lists its councils
    Then council search "Capital (synthetic)" has kind "choose"
    And council search "Capital (synthetic)" lists council "E06999001"
    And council search "Capital (synthetic)" lists council "E06999002"

  # Real London data comes at stage 5b (the board says so); the sample stands in with "Capital (synthetic)".
  @ui
  Scenario: CITY-14 a London search lists its councils and combines none
    Given the user is on the council search
    When the user searches for "Capital (sample)"
    Then the page says "Capital (sample) has more than one council" and "Greater Capital (sample) is made up of several council areas. Choose one."
    And it says "Each council has its own page; we don’t combine them."
    And it lists "Northbridge (sample)" and "Southvale (sample)", each as "Council area · Greater Capital (sample)"

  Scenario: CITY-15 a county name lists its district councils
    Then council search "Westshire (synthetic)" has kind "choose"
    And council search "Westshire (synthetic)" lists council "E07999001"
    And council search "Westshire (synthetic)" lists council "E07999002"

  @ui
  Scenario: CITY-16 a county search lists its districts and says the page is for one council
    Given the user is on the council search
    When the user searches for "Westshire (sample)"
    Then the page says "Westshire (sample) is a county with more than one council" and "Its district councils are listed. Choose one."
    And it says "Figures are published for each council area, so the page is for one council, not the whole county."
    And it lists "Eastmere (sample), Westshire (sample)" and "Westmere (sample), Westshire (sample)", each as "District council"

  Scenario: CITY-17 an old council name leads to the current council with a note
    Then council search "East Westshire Borough (synthetic)" lists council "E07999001" with note "former-name"
    And council "E07999001" has field "population" with status "recorded"

  @ui
  Scenario: CITY-18 an old council name says what the council is called now and goes to its page
    Given the user is on the council search
    When the user searches for "East Westshire Borough (sample)"
    Then the page says "East Westshire Borough (sample) is now Eastmere (sample)" and "The council was formed on 1 April 2023 and goes by its new name."
    And it says "You’re being taken to the current council’s page, which carries a line saying so."
    And the council page for "E07999001" shows "You searched for East Westshire Borough (sample). It is now called Eastmere (sample)." and the action "Go to Eastmere (sample) →"

  Scenario: CITY-19 a place in Wales is not covered
    Then council search "Afonbryn (synthetic)" has kind "not-covered"

  @ui
  Scenario: CITY-20 a place in Wales says not yet covered and shows no page (rule 6)
    Given the user is on the council search
    When the user searches for "Afonbryn (sample)"
    Then the page says "Not yet covered" and "Afonbryn (sample) is in Wales. Vestagraph covers England only for now."
    And it says "We show no page rather than the wrong rules or sources."
    And the action "What England-only means ↗" is the one action
    And a place in Scotland or Northern Ireland says the same

  # No sample council is called "Midvale": the typed text is the visitor's own, so no figure appears.
  @ui
  Scenario: CITY-21 a search that matches nothing says so and offers one action
    Given the user is on the council search
    When the user searches for "Midvale"
    Then the page says "We couldn’t find “Midvale”" and "No council area, town or village in England matches what you typed."
    And it says "Nothing is wrong with your search. It may be spelt another way, or be outside England."
    And the one action is "Search again"

  # FE-37 (amended 15 Nov 2026): one box on the landing page for a postcode or a town. The landing page's own scenarios (LAND, with the hero wording) are LAND-14 to LAND-20 in `01-landing.feature`; here the behaviour that reaches this page.
  @ui
  Scenario: CITY-22 the one search box sends a postcode to the area check and a place to a council page
    Given the user is on the landing page
    When the user types a town or council name in the one box and chooses "Search"
    Then a place that names one council opens that council's page
    And a place that names several councils asks the visitor to choose (CITY-10 to CITY-16)
    And a postcode typed in the same box opens the area check instead

  # Layout (FE-43; the phone page is a short cost-first summary, then one row per topic).
  @ui
  Scenario: CITY-23 on a phone the page is a cost summary then one row per topic
    Given the user has opened the council page for council "E06999001" on a phone (390 px wide)
    When the page has loaded
    Then it shows, in order, the header, the cost summary (council tax band, council tax, average rent, average price), rent or buy, the coverage line, your budget, then "Topics for this council"
    And "Topics for this council" says "One row for each. Tap a row to open its chart, its caption and its table."
    And it has one row each for "Council tax by band", "Private rents", "House prices", "Affordability ratio", "Who rents, who owns" and "Transport connectivity", then "Neighbourhoods" and "Rent or buy, in detail"
    And each row shows its area and period, and the figure quoted from the data where it has one

  @ui
  Scenario: CITY-24 a topic row opens its chart, caption and table in a sheet
    Given the user has opened the council page for council "E06999001" on a phone (390 px wide)
    When the user taps the row "House prices"
    Then a sheet opens titled "House prices" with the four property types and their captions (CITY-64)
    And it has "Show as table" and the source stamp "UK House Price Index"
    And Escape or the phone's Back closes the sheet and returns focus to the row

  # FE-43: the open House prices sheet is the one drawn (board CouncilPage). The sheets for Neighbourhoods and rent or buy in detail, Who rents, who owns and Transport connectivity are not drawn on the canvas yet; these scenarios wait for those boards and carry no wording beyond the row text above.
  @ui
  Scenario: CITY-25 the other topic rows open sheets like House prices (boards still to draw)
    Given the user has opened the council page for council "E06999001" on a phone (390 px wide)
    When the user taps the row "Who rents, who owns", "Transport connectivity", "Neighbourhoods" or "Rent or buy, in detail"
    Then a sheet opens with that topic's chart or map, its caption and its table or list, the same way as the House prices sheet (CITY-24)
    And its content is the same as the desktop page's section (CITY-63, CITY-80, CITY-82, CITY-87)

  @ui
  Scenario: CITY-26 on desktop the charts are open and the page stacks to the phone layout on a narrow window
    Given the user has opened the council page for council "E06999001" on desktop (1440 px wide)
    When the page has loaded
    Then the charts for council tax by band, private rents, house prices, the affordability ratio and who rents and who owns are open on the page, each with its caption
    And in a window narrower than about 760 px the same page stacks into the phone layout
    And nothing scrolls sideways at 320 to 390 px

  @ui
  Scenario: CITY-27 the council tax band is picked from chips on desktop and a select on a phone
    Given the user has opened the council page for council "E06999001"
    When the user looks at "Council tax band"
    Then desktop shows eight chips A to H, each at least 48 px, labelled "Council tax band (Band D is the example)"
    And a phone shows a select with "Band A" to "Band H" and "Band D (example)"
    And the band is changed with the keyboard

  # What it costs here (design spec section 2; FE-43).
  @ui
  Scenario: CITY-28 the council tax line starts on Band D and is labelled an example
    Given the user has opened the council page for council "E06999001"
    When the page has loaded
    Then the council tax line reads "Council tax, Band D (example)", with the yearly amount and the monthly amount quoted from `E06999001 / bands / D / shownYearly` and `shownCouncilTax`
    And under it "Council area · 2026 to 2027 · average for a two-adult dwelling, parish and adult social care charges included"
    And the line above the figures reads "Changing the band changes the council tax line, rent or buy and the budget check. The averages are for the council area."

  # The eight published band amounts are inputs (no band rule table, nothing derived from Band D; founder "Record all eight bands").
  Scenario: CITY-29 the band amounts are recorded for Northbridge and Southvale
    Then council "E06999001" has field "bands" with status "recorded"
    And council "E06999002" has field "bands" with status "recorded"

  @ui
  Scenario: CITY-30 on the example inputs, changing the band changes the council tax line and rent or buy with no request
    Given the user has opened the council page for council "E06999001" with no budget typed and the example inputs unchanged
    When the user picks another band
    Then the council tax line and the two sides of rent or buy change to that band's figures quoted from `E06999001 / bands / <band>` and `E06999001 / rentOrBuy / byBand / <band>` in the generated file
    And no request goes to the server for the change (the page already holds the example-input figures for all eight bands)

  # Agent's call, open to the founder (17 Nov 2026): the server's one answer covers all eight bands. Decision 0053 and CITY-56 keep every calculation out of the browser, so the within-or-above labels and the buy sides for a typed budget or edited inputs are not in the generated file; asking once per change and again per band would make every band pick wait.
  @ui
  Scenario: CITY-110 with a budget typed or inputs edited, the server's one answer covers all eight bands, so picking a band needs no new request
    Given the user has opened the council page for council "E06999001" with a budget typed or an input edited
    When the server's answer for those inputs has arrived
    Then that one answer holds the sides, the comparison and the within-or-above labels for all eight bands
    And picking another band shows that band's figures from the answer already received, with no new request and no calculation in the browser (decision 0053, CITY-56)
    And while the answer is pending the figures read "Working out…" as in CITY-47

  @ui
  Scenario: CITY-31 the average rent and the average price show their area, month and provisional status
    Given the user has opened the council page for council "E06999001"
    When the page has loaded
    Then "Average rent" shows its figure quoted from the newest point of `E06999001 rentSeries` as "a month", with "Council area · <rentPeriod> (provisional)"
    And "Average price" shows its figure quoted from the newest point of `E06999001 priceSeries`, with "Council area · <pricePeriod> (provisional)"
    And the months and the word "provisional" come from `E06999001 / rentOrBuy` (rentPeriod, rentPointStatus, pricePeriod, pricePointStatus)

  # FE-44: one line under the cost summary, counted from the topic rows' recorded statuses. Its generator field waits for issue #292 (rule 2), so the data step is not written yet.
  @ui
  Scenario: CITY-32 a coverage line says how many topics are published for this council
    Given the user has opened the council page for council "E06999001"
    When the page has loaded
    Then one line under the cost summary reads "<found> of <total> topics published for this council", with both numbers quoted from the council's generated coverage field (issue #292)
    And under it "Not published: " names each topic that is not, or "none"
    And there are no per-topic "what to check next" lines
    And a topic the source has no record for is counted as not published, never as found

  @ui
  Scenario: CITY-33 the council tax label says what the figure is
    Given the user has opened the council page for council "E06999001"
    When the user reads the council tax line and the "Council tax by band" chart
    Then it is the council area's average for a two-adult dwelling before discounts, parish charges varying, and the label says so
    And it is the published yearly amount; the monthly amount is that amount divided by 12 by tested code, never typed or worked out in the browser

  # Rent or buy, per month (design spec section 4; plan Review Focus 1, 2, 3, 7).
  @ui
  Scenario: CITY-34 rent or buy shows each side with its council tax and where the figures come from
    Given the user has opened the council page for council "E06999001" (Band D, the example inputs)
    When the user reads "Rent or buy, per month"
    Then "Rent" shows `E06999001 / rentOrBuy / byBand / D / shownRentSide` with "rent <rent> + council tax <council tax>"
    And "Buy · 2-year fixed" shows `shownBuySide` of the 2-year fixed with "repayment <repayment> + council tax <council tax>"
    And the line above reads "Example inputs, editable. The same council tax is on both sides, because whoever lives in a home normally pays it."
    And under each side "Council area · rent <rentPeriod> and price <pricePeriod> (both provisional)"
    And the council tax on the two sides is the same figure for the band picked

  Scenario: CITY-35 buying the average-priced home costs more a month than the average rent at Northbridge
    Then council "E06999001" at band "D" for product "2-year-fixed" has comparison "more"

  @ui
  Scenario: CITY-36 the difference sentence says how much more a month buying costs, in whole pounds
    Given the user has opened the council page for council "E06999001" (Band D, the example inputs)
    When the user reads under the two sides
    Then it reads "On these inputs, buying the average-priced home costs <difference> more a month than the average rent." with the difference quoted from `shownDifference` of the 2-year fixed (DA-21 approved the "more" pattern)
    And the money is in whole pounds, from the generated file

  # Proposed wording (no board yet): the spec's patterns "less" and "about the same as", each worked out by tested code. No sample council gives either, so there is no data scenario; the tested module covers both (plan Task 4).
  @ui
  Scenario: CITY-37 when buying costs less, the sentence says so
    Given a council whose generated comparison for the product is "less"
    When the user reads under the two sides
    Then it reads "On these inputs, buying the average-priced home costs <difference> less a month than the average rent."
    And the sentence does not say which is better, and does not say "cheaper"

  @ui
  Scenario: CITY-38 rent or buy says it is not the full cost and that the averages describe different homes
    Given the user has opened the council page for council "E06999001"
    When the user reads under rent or buy
    Then it says "This is repayment and council tax only; not the full cost of owning or renting."
    And "The averages describe different homes: the rent covers every size of rented home, the price every type sold."
    And "Example inputs: deposit <deposit>%, term <term> years, rate <rate>% (Bank of England, 2-year fixed, <loan band>% loan band, October 2026)", the deposit and term from `exampleInputs`, the rate and loan band from the 2-year fixed `rateBand`, labelled "example"
    And no sentence says whether to rent or to buy

  # Review Focus 2: the 5-year fixed is published only at some bands. A band is never borrowed from another band or product.
  Scenario: CITY-39 the 5-year fixed has no rate at the example deposit and the 2-year fixed has
    Then council "E06999001" at band "D" for product "5-year-fixed" has problem "rate-band-unavailable"
    And council "E06999001" at band "D" for product "2-year-fixed" has comparison "more"

  @ui
  Scenario: CITY-40 a product with no rate at the deposit says so and asks for a typed rate
    Given the user has opened the council page for council "E06999001" (the example deposit)
    When the user reads the "Buy · 5-year fixed" line
    Then it says "No published rate for this deposit size" with "Bank of England quoted rates, October 2026"
    And "We never borrow a rate from another deposit size or product. The 2-year fixed line still shows."
    And it offers "Type a rate to see this line" with a rate box in %
    And the rent side and the 2-year fixed side are unchanged

  # Review Focus 2, second half: a loan above the highest published band gives rate-band-unavailable on every buy side. No sample record has it (the board notes it reads the same as state 18), so this waits for the server check, tested in `vestagraph_area`.
  @ui
  Scenario: CITY-41 a deposit whose loan is above the highest published band leaves every buy side without a rate
    Given the user has opened the council page for council "E06999001"
    When the user types a deposit so small that the loan is above the highest published band
    Then every buy side says "No published rate for this deposit size" and offers "Type a rate to see this line"
    And the rent side stays
    And no rate is borrowed from another band

  # Review Focus 2, third rule (plan `docs/superpowers/plans/2026-11-15-city-explorer.md`): the bands mean "up to X% loan", so a small loan takes the lowest published band that covers it. The plan's worked example is a 50% loan taking the 60% band; no sample record has it, so it waits for the server check, tested in `vestagraph_area`. Added 17 Nov 2026 at the next free ID.
  @ui
  Scenario: CITY-111 a small loan takes the lowest published band that covers it and the note names that band
    Given the user has opened the council page for council "E06999001"
    When the user types a deposit whose loan is the plan's Review Focus example, a 50% loan
    Then the buy side uses the published rate of the lowest band that covers that loan, the 60% band in the plan's example
    And the rate note names that band: "Rate: the Bank of England’s quoted rate for a 2-year fixed at the <loan band>% loan band (a <deposit>% deposit), October 2026. Editable; a typed rate replaces it."
    And a band is never borrowed from another product, so a product with no rate at that band still says "No published rate for this deposit size"

  @ui
  Scenario: CITY-42 a deposit of 100% or more says no mortgage is needed and the rent side stays
    Given the user has opened the council page for council "E06999001"
    When the user types a deposit of 100% or more
    Then the deposit box shows "Deposit too large: no mortgage needed." with an icon and words, tied to the box
    And the buy sides and the difference sentence are hidden
    And the rent side stays, and no figure is shown as £0

  @ui
  Scenario: CITY-43 a rate above the highest allowed is refused with its limit
    Given the user has opened the council page for council "E06999001"
    When the user types a very large rate
    Then the rate box shows "Enter a rate from 0% up to 20%." (BE-38)
    And the buy sides and the difference sentence are hidden, the rent side stays, and nothing crashes

  @ui
  Scenario: CITY-44 a term outside 1 to 40 years is refused
    Given the user has opened the council page for council "E06999001"
    When the user types a term outside the allowed range
    Then the term box shows "Enter a term of 1 to 40 years."
    And the buy sides and the difference sentence are hidden, and the rent side stays

  @ui
  Scenario: CITY-45 while any input is wrong the buy sides and the sentence are hidden and the rent side stays
    Given the user has opened the council page for council "E06999001"
    When the user has typed a wrong deposit, rate or term
    Then it says "The buy sides and the sentence are hidden while an input is wrong; the rent side stays.", and the rent side shows with its council tax
    And a negative, empty or non-numeric value says what is wrong and shows no figure

  @ui
  Scenario: CITY-46 a typed rate replaces the published one and is labelled editable
    Given the user has opened the council page for council "E06999001"
    When the user types a rate that is allowed
    Then the buy sides use the typed rate in place of the Bank of England rate
    And the note reads "Rate: the Bank of England’s quoted rate for a 2-year fixed at the <loan band>% loan band (a <deposit>% deposit), October 2026. Editable; a typed rate replaces it."
    And a rate of 0% gives a repayment with no interest from the same tested module

  @ui
  Scenario: CITY-47 while a changed input is worked out its figures read "Working out…"
    Given the user has opened the council page for council "E06999001"
    When the user changes the deposit
    Then rent, "Buy · 2-year fixed" and "Buy · 5-year fixed" each read "Working out…" with "Waiting for the server"
    And no old figure shows beside the new deposit

  @ui
  Scenario: CITY-48 when the server cannot answer the figures read "Couldn’t work this out" with Retry
    Given the user has changed the deposit and the request fails, is refused or the device is offline
    When the answer does not arrive
    Then the figures are replaced by "Couldn’t work this out" and "The request didn’t go through. You may be offline, or have asked too many times in a short while."
    And "Your inputs are kept. No old figure is shown beside them."
    And the one action is "Retry"

  @ui
  Scenario: CITY-49 typing is debounced and only the newest answer is used
    Given the user types a new deposit while an earlier request is still waiting
    When both answers arrive, the older last
    Then the figures show the answer for the newest input, and the older answer is dropped
    And typing sends one request after a pause, not one per key

  # Review Focus 3: a council with no published rent gets the buy side only.
  Scenario: CITY-50 Eastmere has no published rent, so no rent side and no comparison
    Then council "E07999001" has field "rentSeries" with status "no-record-in-source"
    And council "E07999001" at band "D" has no rent side
    And council "E07999001" at band "D" for product "2-year-fixed" has no comparison

  @ui
  Scenario: CITY-51 one side missing shows the side that exists and says why the other is missing
    Given the user has opened the council page for council "E07999001"
    When the user reads "Rent or buy, per month"
    Then it says "ONS Price Index of Private Rents doesn’t publish a rent for Eastmere (sample)."
    And "Rent" reads "Not published" with "Council area · no rent in the source, so no figure and no budget label for this side"
    And "Buy · 2-year fixed" is still shown, with "Buying is still shown. With one side missing there is no difference sentence."
    And no rent figure, difference sentence or budget label for rent is drawn, and nothing is £0

  # Review Focus 6: the band's published amount is a gap, so there is no side, comparison or budget label.
  Scenario: CITY-52 Westmere has no council tax, so bands A and D have no side or comparison
    Then council "E07999002" has field "bands" with status "no-record-in-source"
    And council "E07999002" at band "D" has problem "council-tax-missing"
    And council "E07999002" at band "A" has problem "council-tax-missing"
    And council "E07999002" has field "rentSeries" with status "no-record-in-source"
    And council "E07999002" has field "priceSeries" with status "no-record-in-source"
    And council "E07999002" has field "population" with status "no-record-in-source"

  @ui
  Scenario: CITY-53 a council with sources missing names each missing source and shows no rent or buy
    Given the user has opened the council page for council "E07999002"
    When the page has loaded
    Then it says "These sources have nothing recorded for this council area." and "A missing figure is said to be missing; it is never shown as £0 or as a clean result."
    And "Average rent" reads "ONS Price Index of Private Rents doesn’t publish this for Westmere (sample)."
    And "Average price" reads "UK House Price Index doesn’t publish this for Westmere (sample)."
    And "Council tax" reads "MHCLG council tax levels doesn’t publish this for Westmere (sample)."
    And it says "Rent or buy needs council tax, so it isn’t shown for Westmere (sample)." and shows no side, no comparison and no budget label
    And the link "About the data →" ("How each source works: About the data →") is the one action

  # Your budget (design spec section 3; 0053's pattern).
  @ui
  Scenario: CITY-54 the budget box is optional and says what it does
    Given the user has opened the council page for council "E06999001"
    When the user reads "Your budget"
    Then it shows the box "Your monthly budget" with a "£" prefix
    And it says "Optional. It is only used to say “within your budget” or “above it” in rent or buy. Not stored, not shared, not in a printout."

  @ui
  Scenario: CITY-55 with the budget box empty there are no labels
    Given the user has opened the council page for council "E06999001" and has typed no budget
    When the user reads rent or buy
    Then no side says "within your budget" or "above it"
    And there is no message about the empty box

  @ui
  Scenario: CITY-56 a typed budget labels each side within your budget or above it
    Given the user has opened the council page for council "E06999001"
    When the user types a monthly budget
    Then the rent side and each buy side with a figure says "within your budget" or "above it", worked out by the server's tested budget check from the shown figures
    And the labels change with the band picked

  @ui
  Scenario: CITY-57 a side with no figure has no budget label
    Given the user has opened the council page for council "E07999001" and has typed a budget
    When the user reads rent or buy
    Then the "Rent" side, which is "Not published", has no label
    And the "Buy · 5-year fixed" side with no published rate has no label

  @ui
  Scenario: CITY-58 an invalid budget says what is wrong and shows no label
    Given the user has opened the council page for council "E06999001"
    When the user types text that is not a number in "Your monthly budget"
    Then the box shows "Enter your monthly budget as a number of pounds, using digits only." with an icon and words, tied to the box
    And "Until it is a number, no “within your budget” or “above it” label is shown. Rent or buy still works."
    And the action "Clear the box" empties it

  @ui
  Scenario: CITY-59 the budget and the rent or buy inputs go in the request body and are never stored or put in an address
    Given the user has typed a budget and changed the deposit, rate and term on the council page
    When the page asks the server to work out the labels and the figures
    Then the amounts travel only in the request body, never in the address or its query string
    And they are not written to any log, never stored on the server, and not kept in browser storage
    And they are not in a share link or in the printout (CITY2-)

  @ui
  Scenario: CITY-60 the budget stays while the visitor moves between pages in one tab and is gone after a reload
    Given the user has typed a budget on the council page
    When the user moves to a neighbourhood page and back, or to the postcode result and back, in the same tab
    Then the budget box still holds the value, held in the page's memory only
    And after a reload or in a new tab the box is empty

  # Charts and captions (design spec "Sections in order" 5 to 9; "Plain-words captions"; DA-21).
  @ui
  Scenario: CITY-61 council tax by band draws eight bars A to H from the published amounts
    Given the user has opened the council page for council "E06999001" on desktop
    When the user reads "Council tax by band"
    Then there is one bar for each of the bands A to H, each labelled with its yearly and monthly amounts quoted from `E06999001 / bands / <band> / shownYearly` and `shownCouncilTax`
    And the heading reads "Council area · 2026 to 2027 · a year, with the month beside it"
    And under it "Average for the council area, two adults, before discounts; parish charges vary. Bars start at £0. The band picked is marked by a border and a fill."
    And the band picked is marked by a border and a fill, not colour alone

  Scenario: CITY-62 the rent caption at Northbridge is a rise over 12 months
    Then council "E06999001" caption "rent" has pattern "trend-rose"

  @ui
  Scenario: CITY-63 private rents is a monthly line with its caption and the provisional months marked
    Given the user has opened the council page for council "E06999001" on desktop
    When the user reads "Private rents"
    Then a monthly line shows the series from `E06999001 rentSeries`, headed "Council area · monthly, <first month> to <last month>", the months quoted from `E06999001 rentSeries`
    And the caption reads "Average rent rose <amount> (<percent>%) in the 12 months to <period>. The latest <provisionalPoints> months are provisional and may change.", with the amount, the percent and the count quoted from `E06999001 / captions / rent` (values: amount, percent, provisionalPoints)
    And "Move along the months" shows a month's value with "provisional" where it is

  @ui
  Scenario: CITY-64 house prices draw four property types with their own patterns and labels
    Given the user has opened the council page for council "E06999001" on desktop
    When the user reads "House prices"
    Then four lines, "Detached", "Semi-detached", "Terraced" and "Flat", use a solid, a long-dash, a short-dash and a dotted stroke with direct labels (FE-47), so colour is never the only difference
    And the heading reads "Council area · monthly, <first month> to <last month> · average price of each property type", the months quoted from `E06999001 priceSeries`
    And "Move along the months" shows each type's average price for the month, "<latest month> · provisional", quoted from `E06999001 priceSeries / byType`

  Scenario: CITY-65 the detached caption at Northbridge is a rise and each type has its own caption
    Then council "E06999001" caption "price:detached" has pattern "trend-rose"
    And council "E06999001" caption "price:semiDetached" has pattern "trend-rose"
    And council "E06999001" caption "price:flat" has pattern "trend-rose"

  Scenario: CITY-66 the terraced caption at Northbridge is a fall
    Then council "E06999001" caption "price:terraced" has pattern "trend-fell"

  @ui
  Scenario: CITY-67 each type's caption names the type and its own change, and none compares types
    Given the user has opened the council page for council "E06999001" on desktop
    When the user reads under the house prices chart
    Then each type has a line "<Type>: average price rose <amount> (<percent>%) in the 12 months to <period>." quoted from `E06999001 / priceByType` (values, toPeriod)
    And the terraced line reads "fell" in place of "rose" (CITY-66)
    And "The latest <provisionalPoints> months are provisional and may change.", the count quoted from the `priceByType` caption's `provisionalPoints`
    And no sentence compares one type with another

  Scenario: CITY-68 the terraced caption at Eastmere is unchanged
    Then council "E07999001" caption "price:terraced" has pattern "trend-unchanged"

  @ui
  Scenario: CITY-69 an unchanged price says was unchanged
    Given the user has opened the house prices of council "E07999001"
    When the user reads the terraced caption
    Then it reads "Terraced: average price was unchanged in the 12 months to <period>." with the period quoted from the caption's values (toPeriod)
    And "unchanged" uses its stated threshold, not the threshold of "about the same" in rent or buy

  # Review Focus 4 (a missing point is a gap, not zero): a type a council has no figure for.
  Scenario: CITY-70 Eastmere has no record for flats
    Then council "E07999001" caption "price:flat" has pattern "missing"
    And council "E07999001" caption "price:flat" has reason "no-record-in-source"

  @ui
  Scenario: CITY-71 a property type with no record says so and draws no line and no zero
    Given the user has opened the house prices of council "E07999001"
    When the user reads the chart
    Then "Flat" reads "Not published" and has no line and no zero
    And the line "Flat: the UK House Price Index doesn’t publish this for Eastmere (sample)." replaces its change caption
    And the other three types draw as usual

  Scenario: CITY-72 Southvale has no start point for the price change
    Then council "E06999002" caption "price" has pattern "missing"
    And council "E06999002" caption "price" has reason "start-point-not-published"
    And council "E06999002" caption "price:detached" has reason "start-point-not-published"
    And council "E06999002" caption "price:flat" has reason "start-point-not-published"

  @ui
  Scenario: CITY-73 a type's 12-month change that is not published says so and its line has a visible gap
    Given the user has opened the house prices of council "E06999002"
    When the user reads the chart and the captions
    Then each type reads "<Type>: the UK House Price Index doesn’t publish this for Southvale (sample) in <start month>, so there is no 12-month change.", the month quoted from the input point `2025-08` (status `not-published`) in `council-area.json` E06999002 / priceSeries / points
    And each type's line stops before a dashed "?" slot for that month and restarts after it, with nothing drawn across it
    And each type still shows its latest value, "<latest month> · provisional"

  Scenario: CITY-74 the affordability caption at Northbridge is a rise
    Then council "E06999001" caption "affordability" has pattern "trend-rose"

  @ui
  Scenario: CITY-75 the affordability ratio is a yearly line with a caption that names both ends
    Given the user has opened the council page for council "E06999001" on desktop
    When the user reads "Affordability ratio"
    Then a yearly line shows the series from `E06999001 affordabilitySeries`, headed "Council area · yearly, year ending September, <first year> to <last year> · median house price to median earnings, workplace-based"
    And the caption reads "The ratio rose <amount>, from <first> in <first year> to <last> in <last year>." (DA-21), quoted from `E06999001 / captions / affordability`
    And "Move along the years" shows a year's ratio

  # The break is in the input; the generated captions for Eastmere's latest pair sit after it, so they are trends.
  Scenario: CITY-76 the Eastmere affordability series marks a change in method
    Then council "E07999001" series "affordabilitySeries" marks a method break
    And council "E07999001" caption "affordability" has pattern "trend-rose"

  @ui
  Scenario: CITY-77 a series with a method break is not joined across it
    Given the user has opened the affordability ratio of council "E07999001"
    When the user reads the chart
    Then it says "The way this is measured changed here, so the two parts are not comparable."
    And the line is drawn as two parts with no line across the break
    And the text alternative says the parts "are measured differently and are not comparable", with each part's end points quoted from the data and no first-to-last pairing

  # Review Focus 4: a change whose month 12 months earlier is missing, or that spans a break. No sample council produces a not-comparable caption, so this waits for a fixture (proposed wording).
  @ui
  Scenario: CITY-78 a change across a method break or with a missing earlier point shows no change figure
    Given a council whose latest two end points lie either side of a method break, or whose month 12 months earlier is not published
    When the user reads the caption
    Then it says only "not comparable" or "not published", and never a rise, a fall, an amount or a percentage
    And nothing is shown as zero or "unchanged"

  Scenario: CITY-79 the tenure caption at Northbridge is a single point
    Then council "E06999001" caption "tenure" has pattern "single-point"
    And council "E06999001" has field "tenure" with status "recorded"

  @ui
  Scenario: CITY-80 who rents and who owns is one bar for Census day with its rounding line
    Given the user has opened the council page for council "E06999001" on desktop
    When the user reads "Who rents, who owns"
    Then one stacked bar shows the five shares quoted from `E06999001 / tenureShares` (owned outright, owned with a mortgage or loan, rented from the council or a housing association, rented privately, other), headed "Council area · Census day, 21 March 2021 · share of households"
    And under it "Shares are rounded to one decimal place, so they may not add up to 100%." (FE-48)
    And the caption reads "In March 2021, <percent>% of households rented privately." quoted from `E06999001 / captions / tenure`

  Scenario: CITY-81 Northbridge has a transport connectivity figure
    Then council "E06999001" has field "connectivity" with status "recorded"

  @ui
  Scenario: CITY-82 transport connectivity shows the DfT scale and says it is relative, with no status beside it
    Given the user has opened the council page for council "E06999001" on desktop
    When the user reads "Transport connectivity"
    Then it shows "<score> on a scale of 0 to 100" quoted from `council-area.json` for "E06999001", with "Council area · Q4 2024 · 100 is the most connected on DfT’s scale"
    And it says "Relative, not absolute. DfT says scores should be interpreted relative to other areas."
    And no "provisional" or "Experimental Statistics" tag sits beside the figure (FE-45; the status is on About the data)

  @ui
  Scenario: CITY-83 provisional months are marked by the word, a dashed line and hollow marks, never colour alone
    Given the user has opened the council page for council "E06999001"
    When the user reads "Average rent"
    Then the figure shows "provisional" beside its month
    And "Provisional months may change when the source is revised. They are marked with the word, a dashed line and hollow marks, never colour alone."

  @ui
  Scenario: CITY-84 every chart has a table view, where a missing month reads "not published"
    Given the user has opened the council page for council "E06999002" on desktop
    When the user chooses "Show as table" under a chart
    Then the same figures show as a table, and a month the source does not publish reads "not published", never a blank or 0
    And the chart has a text alternative made of its caption and its values

  @ui
  Scenario: CITY-85 chart values show on tap and on keyboard focus, never on hover only
    Given the user has opened the council page for council "E06999001" on desktop
    When the user taps, or moves focus with the keyboard to, a point on a chart
    Then the value for that month or year shows, and the change is announced to a screen reader
    And hovering alone shows nothing the keyboard cannot reach

  @ui
  Scenario: CITY-86 the page has no ranking of councils, no score and no verdict word
    Given the user has opened the council page for council "E06999001"
    When the user reads the whole page
    Then it ranks no council, shows no "1st of N", no combined score and no score drawn on a map (0054)
    And no caption, label or sentence calls a figure "best", "better" or "cheaper", "high" or "low", "steep" or "sharp"
    And rent or buy gives no advice (CITY-38)

  # Neighbourhoods on the council page (design spec section 10); the neighbourhood's own page is `city-explorer-neighbourhood.feature` (HOOD).
  @ui
  Scenario: CITY-87 the neighbourhoods map has a list as the way in for keyboard and screen reader users
    Given the user has opened the council page for council "E06999001" on desktop
    When the user reads "Neighbourhoods"
    Then a map shows the neighbourhoods inside the council, with "Choose a neighbourhood" and a list naming each as "<larger area’s name> (<code>)" quoted from `E06999001 / neighbourhoods` (label)
    And the heading reads "Neighbourhood level · inside Northbridge (sample) council area · named by the larger area and its code"
    And the map shapes are not tab stops; the list is
    And the line "The map shows the <count> neighbourhoods in this sample for Northbridge (sample). It is not coloured by any figure." gives the count from the list

  @ui
  Scenario: CITY-88 choosing a neighbourhood opens a small panel with focus on its heading
    Given the user has opened the council page for council "E06999001" on desktop
    When the user chooses a neighbourhood from the list
    Then a panel opens with focus on its heading, reading "Neighbourhood in Northbridge (sample) council area", with the action "See this neighbourhood"
    And Escape, or Close, closes it and returns focus to the list
    And on a phone the Back button closes it

  @ui
  Scenario: CITY-89 the neighbourhood map is not coloured by any figure and names its sources
    Given the user has opened the council page for council "E06999001" on desktop
    When the user reads under the map
    Then no neighbourhood is coloured by a score, rank or figure (0054)
    And the source line names the Office for National Statistics under the Open Government Licence v.3.0, the OS data attribution and the House of Commons Library MSOA names under the Open Parliament Licence
    And "Boundary and name sources, under How we got this ↓" links to those stamps
    And the board's map drawing is a placeholder for our own street map tiles (FE-03, still to price)

  @ui
  Scenario: CITY-90 "See this neighbourhood" opens the neighbourhood page with the code after the hash
    Given the user has chosen a neighbourhood on the council page for council "E06999001"
    When the user chooses "See this neighbourhood"
    Then the neighbourhood result page opens (`city-explorer-neighbourhood.feature`), with the neighbourhood's code after the "#" in the address, so it never reaches the logs

  # How we got this (FE-24, FE-34; the stamps follow FE-33).
  @ui
  Scenario: CITY-91 "How we got this" says how the figures were made and that the data is sample
    Given the user has opened the council page for council "E06999001"
    When the user reads "How we got this"
    Then it says "Each figure says its area (here the council area) and its period."
    And "Monthly council tax is the published yearly amount divided by 12; repayments, differences and the sentences under each chart come from our tested rules, never from AI."
    And "Rent or buy shows repayment and council tax only; the average rent and the average price describe different homes. Months marked provisional may change."
    And "Sample data: every council, figure and neighbourhood is made up, shaped like the source named beside it."

  @ui
  Scenario: CITY-92 each topic has one line with its source stamp and a link to About the data
    Given the user has opened the council page for council "E06999001"
    When the user reads "How we got this"
    Then there is one line each for "Population", "Council tax", "Private rents", "House prices", "Affordability ratio", "Who rents, who owns", "Transport connectivity", "Neighbourhood boundaries and names" and "Mortgage rates"
    And each line carries its source stamp, as an icon, name and link (FE-33), with no dates or notes in the stamp
    And "How each source works, its date and its status: About the data →" opens About the data

  @ui
  Scenario: CITY-93 the page links to "Use in ChatGPT or Claude"
    Given the user has opened the council page for council "E06999001"
    When the user reads the end of the page
    Then "Use in ChatGPT or Claude →" opens that page (decision 0056)
    And the council page has no on-page AI chat (its "Ask about this area" entry goes to the signed-in workspace, AUTH-28)

  # The remaining states (CouncilStates boards 1, 13, 14, 16, 8, 23, 24).
  @ui
  Scenario: CITY-94 while a council loads the page says what it is doing and has no action
    Given the user has chosen the council page for "Northbridge (sample)"
    When the council's figures have not arrived
    Then the page says "Getting Northbridge (sample)…" and "Getting each topic from our stored copies of the sources."
    And "Topics appear as they arrive; nothing is shown as empty in the meantime."
    And there is no action, as on the postcode result

  # No sample record is stale, so the board shows no figure; this scenario waits for a stale fixture.
  @ui
  Scenario: CITY-95 an older edition says so and the figure stays readable
    Given a council whose stored copy of a source is older than it should be
    When the user opens its page
    Then the page says "Our copy of a source is older than it should be" and "A newer edition may be out. The figure on the page is unchanged and still readable."
    And "About the data shows when each source was last updated."
    And the action is "About the data", and the source stamp has no status word or date (FE-33)

  # No sample record holds a county figure or a county name for a council, so the board uses placeholders and draws no figure; this scenario waits for one.
  @ui
  Scenario: CITY-96 a figure published only for the county is labelled with its level and never presented as the council's
    Given a council whose figure the source publishes only for the county
    When the user reads that figure
    Then the page says "Published for the county, not this council" and "Some figures exist only for <county> county, which includes <council>."
    And the label reads "County · <county> · <period>"
    And the figure is never presented as the council's own, and the action is "What the county figure covers →"

  # No sample council has been replaced during the pilot; the board uses placeholders and draws no figure.
  @ui
  Scenario: CITY-97 a council replaced during the pilot says so and links to the new one
    Given a council that was replaced by another council during the pilot
    When the user opens the old council's page
    Then the page says "This council has been replaced" and "<old council> was replaced by <new council> on <date>."
    And "Its “what changed” records are dropped, with a note saying so, rather than shown as if nothing happened."
    And the action is "Go to <new council>’s page →"

  # No sample series starts at a council's formation date (Eastmere's formedOn is 2023-04-01 and none of its series starts then), so the board shows the message with a placeholder date and draws no figure; this scenario waits for one.
  @ui
  Scenario: CITY-98 a series that starts at a council merger draws no line across the formation date
    Given a council formed by a merger whose series starts when it was formed
    When the user reads that chart
    Then it says "This chart starts when the council was formed" and "A chart starts where its council starts. No line is drawn across the date the council was formed."
    And "Chart starts: <date the council was formed>" and "No line is drawn before this date."
    And nothing from before that date is joined on

  @ui
  Scenario: CITY-99 offline results stay and new searches and changed inputs wait
    Given the user has opened the council page for council "E06999001"
    When the device goes offline
    Then the page says "You’re offline" and "This device has no internet connection."
    And "Results already on screen stay; new searches and changed inputs wait until you’re back online."
    And the action is "Try again"

  @ui
  Scenario: CITY-100 when all sources are down every topic says it is not known right now
    Given our stored copies cannot be reached
    When the user opens the council page for council "E06999001"
    Then the page says "We can’t reach our stored copies right now" and "Every topic says “Not known right now” until our service recovers."
    And "Council tax", "Average rent", "Average price", "Affordability ratio", "Who rents, who owns" and "Transport connectivity" each read "Not known right now"
    And "The topics stay listed so you can see what we would show; nothing is shown as zero or as a clean result."
    And the action is "About the data"

  # Privacy (design spec Constraints; decisions 0014, 0046, 0053).
  @ui
  Scenario: CITY-101 typed place names, postcodes, budgets, the band and the rent or buy inputs are never stored or logged
    Given the user has typed a place name and a postcode, picked a band, typed a budget and changed the rent or buy inputs
    When the server has answered each request
    Then none of those values is stored, or written to a server, application, hosting or tracing log
    And analytics never records a form field (FE-05)
    And the privacy notice names them

  @ui
  Scenario: CITY-102 the council page's own address is an ordinary page view with the visitor's address dropped
    Given the user has opened the council page for council "E06999001" from a place-name search
    When the page view is logged
    Then the address of the page is logged as an ordinary page view, with the visitor's IP address dropped or anonymised before the log is written
    And the place name the visitor typed does not appear in the log

  @ui
  Scenario: CITY-103 nothing is in the query string
    Given the user has opened the council page for council "E06999001"
    When the user types a place, a postcode or a budget, picks a band or changes the rent or buy inputs
    Then the address has no query string, and a postcode may use only the fragment as decision 0046 allows

  @ui
  Scenario: CITY-104 no third party sees a page view
    Given the user has opened the council page for council "E06999001"
    When the page loads
    Then the boundary files, map tiles, fonts and the chart library come from our own hosting
    And the page makes no request to a third party (B28)

  @ui
  Scenario: CITY-105 the new endpoints carry the pilot's rate limits
    Given the user sends many budget, rent or buy, compare or place-name requests in a short while
    When the limit is passed
    Then the server refuses them, the page shows "Couldn’t work this out" with "Retry" (CITY-48), and no figure is shown beside the changed input

  # Accessibility (design spec Constraints).
  @ui
  Scenario: CITY-106 the page works by keyboard, with touch targets of at least 44 px and no sideways scrolling
    Given the user has opened the council page for council "E06999001"
    When the user uses only the keyboard, or a phone 320 to 390 px wide
    Then every control can be reached and used, with a visible focus
    And every touch target is at least 44 px
    And the page does not scroll sideways

  @ui
  Scenario: CITY-107 errors are tied to their inputs, changed figures are announced and motion is reduced when asked
    Given the user has opened the council page for council "E06999001"
    When the user types a wrong value, or changes an input
    Then each error message is tied to its input and uses an icon and words, not colour alone
    And a changed figure is announced to a screen reader
    And with reduced motion asked for, nothing animates

  @ui
  Scenario: CITY-108 every board has a dark twin and the display control changes the theme and text size
    Given the user has opened the council page for council "E06999001"
    When the user opens "Display" and chooses the dark theme
    Then every state above reads the same in the dark theme, in WCAG 2.2 AA contrast
    And the theme and text size are remembered on this device only, as on the postcode result

  # Split from CITY-37 (IDs are permanent): the "about the same" sentence, proposed wording.
  @ui
  Scenario: CITY-109 when buying costs about the same, the sentence says so with no figure
    Given a council whose generated comparison for the product is "about-the-same"
    When the user reads under the two sides
    Then it reads "On these inputs, buying the average-priced home costs about the same a month as the average rent." with no figure
    And the sentence does not say which is better, and does not say "cheaper"
