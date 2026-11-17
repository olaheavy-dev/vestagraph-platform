@screen @buying @renting
Feature: City Explorer part 2 (compare two councils, share and print, what changed since your last visit, About the data)
  Question it answers: "How do two councils compare side by side, can I take this council away on paper or as a link, what is newer since I last looked, and where does each fact come from?"
  Modes: both (and anyone, with no account; decisions 0046, 0055 and 0056)
  Added 17 Nov 2026 (PR C of the City Explorer plan, Task 14b; decisions 0053, 0054, 0055 and 0056; register lines FE-33, FE-45, FE-47, FE-48, FE-50, DA-12, DA-21, BE-37, PD-19). The design is `docs/superpowers/specs/2026-11-15-city-explorer-design.md` ("Reasons to return, part 2": compare, share or print, what changed). The council page is `city-explorer.feature` (CITY), its header carries "Compare" and "Share" (CITY-06); the neighbourhood page is `city-explorer-neighbourhood.feature` (HOOD). The council tools for ChatGPT and Claude (decision 0056) belong to `area-tools.feature` and are not repeated here.
  Fixtures: councils by code in `packages/fixtures/data/council-area.json` (inputs, each with its source) and `packages/fixtures/generated/council-result.json` (every calculated figure). The sample councils: E06999001 Northbridge (complete), E06999002 Southvale (price start point not published, so no 12-month price change), E07999001 Eastmere (no published rent) and E07999002 Westmere (nothing recorded: no council tax). The data names read "(synthetic)"; the boards print the same names with "(sample)", and every scenario quotes the board's text. The compare boards draw Northbridge and Southvale, in that order.
  Figures: none typed here (AGENTS.md rule 2). A scenario that needs a figure names the council code and the generated field (the figure map below); the page quotes the number from the file, in whole pounds from the generator's whole-pound fields (BE-37). Compare works out nothing between the two councils: each council's own figure is shown, and "more" appears only where `council-result.json` holds that council's own comparison.
  Where: compare opens from the council page's "Compare" (CITY-06); share and print from "Share" and from the compare page; what changed sits at the top of a council page under the council's name; About the data is linked from "How we got this" on the council and neighbourhood pages. Boards, on the canvas page "Pilot · City Explorer" (design canvas version 407): CouncilCompare (phone) and CouncilCompareDesktop; CouncilPrint (the A4 printout, light only, FE-50, no Dark twin); CouncilWhatChanged (phone, three states) and CouncilWhatChangedDesktop; CouncilAboutData. Every board other than CouncilPrint has its Dark twin.
  Rule 7: a missing figure is never shown as zero, a flat value, a favourable value or a clean result. A difference needs both sides.
  Rule 4 and 0054: compare shows two councils side by side in the order the visitor picked them. It never sorts, ranks or totals them, has no "cheaper" or winner label and no calculated difference between the two councils.
  Wording status: the board texts quoted below are the canvas's. Not drawn on any board, so proposed wording that is finalised before build: the council "Share a link" control and its confirmation (CITY2-30 to CITY2-32; the boards show only the buttons "Share" and "Share this comparison"), a compare page before a second council is picked (CITY2-05), a council with a gap picked in compare (CITY2-22, CITY2-24), the offline message in compare (CITY2-27) and the note for a replaced council's records (CITY2-57). The "was" figure, the newer edition's name and date and the "revised" label in what changed are placeholders on the boards, because no sample record has an earlier edition or a revision (CITY2-48, CITY2-49). The dates on the About the data board are quoted from the sources research (`docs/reviews/2026-11-16-city-explorer-sources.md`); the page quotes them from the sources' own records once the generator carries them. The Share control's address for a shared comparison (where the two councils go) is not decided in the design spec; CITY2-32 fixes only what the address never holds.
  Data scenarios (no tag) check the facts in `council-area.json` and `council-result.json` with the council steps in docs/specs/README.md. Every other scenario is `@ui`, because the outcome is on the page or in the browser.

  Board-to-scenario map (each board has a Dark twin that shows the same states, except the printout; CITY2-29, CITY2-43):
    CouncilCompare, phone, and CouncilCompareDesktop: header, subtitle and the three controls -> CITY2-01 to CITY2-06; What it costs here -> CITY2-07 to CITY2-11; Rent or buy, per month -> CITY2-12 to CITY2-17; Council tax by band -> CITY2-19, CITY2-20; no ranking -> CITY2-18; gaps -> CITY2-21 to CITY2-24; How we got this and the stamps -> CITY2-25, CITY2-26; privacy and accessibility -> CITY2-27 to CITY2-29; Share this comparison and Print -> CITY2-32, CITY2-33
    The council header's Share -> CITY2-30, CITY2-31
    CouncilPrint, cover and page 1 -> CITY2-34 to CITY2-37; page 2 -> CITY2-38 to CITY2-40; page 3 -> CITY2-41; footer -> CITY2-42; light only and legibility -> CITY2-43, CITY2-44; a council with a gap -> CITY2-45
    CouncilWhatChanged, phone: 1 Consent off -> CITY2-46, CITY2-47; 2 Consent on, a newer edition and a revised month -> CITY2-48 to CITY2-51; 3 After Clear -> CITY2-52; the list kept and its stamps -> CITY2-50, CITY2-51; turning off, the 12 months, skipped editions -> CITY2-53 to CITY2-55
    CouncilWhatChangedDesktop: the same three states, at the top of the council page -> CITY2-56; a replaced council (no board) -> CITY2-57
    CouncilAboutData: header and intro -> CITY2-58; one row each -> CITY2-59 to CITY2-67, all rows -> CITY2-68; the DfT status only here -> CITY2-69; rows open and close -> CITY2-70; where it is linked from -> CITY2-71; theme and keyboard -> CITY2-72
    Not on a board and not a scenario here: the council tools for ChatGPT and Claude (`area-tools.feature`).

  Figure map (every figure a scenario mentions -> its ID; the page quotes the value, the scenario never types it). `council-result.json` figures are cited as <council code> / <path>; inputs as the field in `council-area.json`:
    council tax, a band, a year and a month -> <code> / bands / <band> / shownYearly and shownCouncilTax (inputs: `council-area.json` <code> / bands)
    average rent and its month -> `council-area.json` <code> / rentSeries, its newest point (period and status: <code> / rentOrBuy / rentPeriod and rentPointStatus)
    average price and its month -> `council-area.json` <code> / priceSeries, its newest point (<code> / rentOrBuy / pricePeriod and pricePointStatus)
    the price of each type -> `council-area.json` <code> / priceSeries / byType, the newest point of each type; its caption -> <code> / priceByType (pattern, reason, periods, values)
    rent side, buy side, repayment, difference and its direction -> <code> / rentOrBuy / byBand / <band> / shownRentSide, buySides / <product> / shownBuySide, shownRepayment, shownDifference, comparison
    the example deposit and term -> `council-result.json` exampleInputs
    the rate, its loan band and month -> <code> / rentOrBuy / byBand / <band> / buySides / <product> / rateBand
    captions -> <code> / captions (rent, price, affordability, tenure), each with its pattern, reason, periods and values
    tenure shares -> <code> / tenureShares
    the population -> `council-area.json` <code> / population
    the sources' editions, periods and statuses -> the `source` of each field in `council-area.json`
    an earlier edition's figure, a revised month, the newer edition's name -> not in any record yet (CITY2-48, CITY2-49 wait for a fixture)
    the compare choice, the band, a budget -> the visitor's own input, never a record

  Required states (doc 03 §5; AGENTS.md rules 1, 4, 6 and 7; plan Review Focus 1 to 7):
    loading: compare and what changed load with the council page (CITY-94)
    empty: no second council picked -> CITY2-05; what changed with the setting off -> CITY2-46; with nothing kept after Clear -> CITY2-52
    ambiguous match: not applicable (the compare board lists three of the four sample councils, Northbridge, Southvale and Eastmere; a place name is searched on the council search, CITY-09 to CITY-16)
    not covered: not applicable (a council outside England is not offered; CITY-19, CITY-20)
    not found: a council that cannot be found is the council page's state (CITY-21)
    partial answer: a council with no rent, a council with no council tax, a price type with no 12-month change, no rate for a product -> CITY2-10, CITY2-11, CITY2-15, CITY2-16, CITY2-21 to CITY2-24, CITY2-45
    stale or provisional edition: provisional months marked in each row -> CITY2-08, CITY2-14; a newer edition and a revised month -> CITY2-48, CITY2-49
    source failed, offline -> CITY2-27
    consent: the what-changed setting is off until turned on (PECR) -> CITY2-46, CITY2-47
    privacy -> CITY2-28, CITY2-31, CITY2-32, CITY2-54

  # Compare two councils (design spec, "Compare two councils"; 0054: never ranked).
  @ui
  Scenario: CITY2-01 the compare page says it shows two councils side by side and ranks none
    Given the user has opened compare from the council page for council "E06999001"
    When the page has loaded
    Then the page heading is "Compare councils" and above it the link "← Back to Northbridge (sample)" opens the council page for "E06999001"
    And the line under it reads "Two councils side by side, in the order you picked them. Vestagraph doesn’t rank councils or pick a winner: each row shows each council’s own published figure."

  # The first council is the one the visitor came from: the board's back link names it. The design spec does not say it in so many words.
  @ui
  Scenario: CITY2-02 choosing Compare on a council page opens compare with that council first
    Given the user has opened the council page for council "E06999001"
    When the user chooses "Compare" in the header (CITY-06)
    Then compare opens with "Northbridge (sample)" as the first council
    And the second council waits for the visitor's pick, which is never chosen for them

  @ui
  Scenario: CITY2-03 each council is picked from a list of the sample councils, in the data's order
    Given the user has opened compare from the council page for council "E06999001"
    When the user opens the lists "First council" and "Second council"
    Then each lists "Northbridge (sample)", "Southvale (sample)" and "Eastmere (sample)", in the data's order, not a ranking (the canvas boards CouncilCompare and CouncilCompareDesktop list these three; Westmere, with nothing recorded, is not drawn in a list)
    And no list is sorted or filtered by a figure

  @ui
  Scenario: CITY2-04 swapping the two councils swaps the columns and changes nothing else
    Given the user has picked "Northbridge (sample)" first and "Southvale (sample)" second
    When the user picks "Southvale (sample)" as the first council and "Northbridge (sample)" as the second
    Then every row shows Southvale's figure first and Northbridge's second, each figure unchanged
    And no row is re-sorted and no label changes

  # No board draws the page before a second council is picked: proposed wording, finalised before build (as the council page's empty states).
  @ui
  Scenario: CITY2-05 before a second council is picked compare shows no rows and no figure
    Given the user has opened compare from the council page for council "E06999001"
    When no second council has been picked
    Then the rows wait for the pick, with a plain line saying to pick a second council (wording to be drawn before build)
    And no row shows a figure for a council that was not picked, and nothing is shown as zero

  @ui
  Scenario: CITY2-06 the council tax band is picked once and changes every council tax row and rent or buy
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user changes the "Council tax band" from "Band D (example)" to another band
    Then the council tax rows and rent or buy of both councils show the figures for that band, quoted from each council's <code> / bands / <band> and rentOrBuy / byBand / <band>
    And no figure is worked out in the browser (rule 2)

  # What it costs here: each row holds both councils' own figures, in the order picked.
  @ui
  Scenario: CITY2-07 What it costs here gives each row both councils' own council tax, rent and price
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads "What it costs here"
    Then it says "Council area figures for each council. Band D is the example band; changing the band changes the council tax rows and rent or buy."
    And the rows "Council tax, Band D (example)", "Average rent" and "Average price" each hold both councils' figures, quoted from each council's `bands`, `rentSeries` and `priceSeries`
    And the council tax row shows a year and a month for each council, as the council page does (CITY-28)

  @ui
  Scenario: CITY2-08 each figure says its area and its period, with the provisional months marked
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads the "Average rent" and "Average price" rows
    Then each council's figure carries "Council area" and its own month, quoted from `rentOrBuy` rentPeriod and pricePeriod, with "(provisional)" where rentPointStatus or pricePointStatus says so
    And the two councils' months are never presented as the same month unless the records say so

  @ui
  Scenario: CITY2-09 average price by property type gives each council's four types side by side
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads "Average price by property type"
    Then "Detached", "Semi-detached", "Terraced" and "Flat" each hold both councils' average price for that type, quoted from `priceSeries` / `byType` (BE-37)
    And Northbridge's figure carries its own 12-month sentence quoted from `E06999001 / priceByType` (for example "average price rose … in the 12 months to <pricePeriod>", the period quoted from `E06999001 / priceByType` (values), or "fell" for the terraced type, as that caption's pattern says)
    And no figure or caption compares one type with another, or one council with the other

  Scenario: CITY2-10 Southvale has no 12-month price change for any type
    Then council "E06999002" caption "price:detached" has reason "start-point-not-published"
    And council "E06999002" caption "price:semiDetached" has reason "start-point-not-published"
    And council "E06999002" caption "price:terraced" has reason "start-point-not-published"
    And council "E06999002" caption "price:flat" has reason "start-point-not-published"

  @ui
  Scenario: CITY2-11 a council with no 12-month price change says why and draws no change
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads the property type rows for Southvale
    Then Southvale shows its price for each type and "The UK House Price Index doesn’t publish this for Southvale (sample) in August 2025, so there is no 12-month change." (DA-21), and no rise, fall, amount or percentage
    And on a phone the line "Each type is the average price of that type in that council, as the UK House Price Index publishes it." sits under the four groups, and on desktop "The four property types are each council’s own published average, side by side, with no difference between councils and no ranking."

  # Rent or buy (design spec section 4; DA-21): both councils on the same example inputs, each with its own council tax.
  @ui
  Scenario: CITY2-12 rent or buy says the inputs are the same for both councils and where the council tax goes
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads "Rent or buy, per month"
    Then it says "Example inputs, the same for both councils. The same council tax is on both sides, because whoever lives in a home normally pays it."
    And the line reads "Deposit <depositPercent>% (example)", "Term <termYears> years (example)" and "Rate <rate>% (Bank of England, 2-year fixed, <maxLoanToValuePercent>% loan band, <month>)", quoted from `council-result.json` exampleInputs and `E06999001 / rentOrBuy / byBand / D / buySides / 2-year-fixed / rateBand`

  Scenario: CITY2-13 both Northbridge and Southvale have a buy side that costs more than their own rent
    Then council "E06999001" at band "D" for product "2-year-fixed" has comparison "more"
    And council "E06999002" at band "D" for product "2-year-fixed" has comparison "more"

  @ui
  Scenario: CITY2-14 each council's rent and 2-year fixed rows show its own parts and its own periods
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads the rows "Rent" and "Buy · 2-year fixed"
    Then each council shows its total a month with "rent <rent> + council tax <tax>" on the rent row and "repayment <repayment> + council tax <tax>" on the buy row, quoted from `shownRentSide`, `shownRepayment`, `shownCouncilTax` and `shownBuySide`
    And each council's line reads "Council area · rent <rentPeriod> and price <pricePeriod> (both provisional)" from its own `rentOrBuy` rentPeriod and pricePeriod, so the two are not read as same-month figures

  Scenario: CITY2-15 neither council has a 5-year fixed rate at the example deposit
    Then council "E06999001" at band "D" for product "5-year-fixed" has problem "rate-band-unavailable"
    And council "E06999002" at band "D" for product "5-year-fixed" has problem "rate-band-unavailable"

  @ui
  Scenario: CITY2-16 a product with no rate says so for each council and borrows no rate
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads the row "Buy · 5-year fixed"
    Then each council's cell reads "No published rate for this deposit size"
    And no figure is shown for it and no rate from another band or product is used

  @ui
  Scenario: CITY2-17 buying compared with renting is each council's own sentence and no difference between councils
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads "Buying compared with renting, in each council"
    Then each council's cell shows "<difference> more a month" and "On these inputs, buying that council’s average-priced home costs £<difference> more a month than its average rent.", quoted from that council's own `shownDifference` and `comparison` (DA-21)
    And under the rows "This is repayment and council tax only; not the full cost of owning or renting. The averages describe different homes."

  @ui
  Scenario: CITY2-18 compare never sorts, ranks or totals the two councils
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads the whole page
    Then no row is sorted by a figure and no council is labelled "cheaper", "better", "best" or a winner
    And no difference, total or ratio between the two councils is shown, and the councils stay in the order picked (0054)

  @ui
  Scenario: CITY2-19 council tax by band gives each council's eight bands, a year with the month beside it
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads "Council tax by band"
    Then it says "Council area · 2026 to 2027 · a year, with the month beside it. Average for the council area, two adults, before discounts."
    And "Band A" to "Band H" each hold both councils' amount a year and a month, quoted from each council's `bands` (shownYearly, shownCouncilTax)

  @ui
  Scenario: CITY2-20 on desktop each group of rows is a table, with the councils in the order picked
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)" on desktop
    When the user reads "What it costs, two councils", "Rent or buy, two councils" and "Council tax by band, two councils"
    Then each is a table whose first heading reads "Council, in the order you picked" with the two councils' names as column headings
    And a screen reader hears each figure with its row and its council

  # Gaps in compare. No board draws a gap council in compare: the cells follow the council page's own missing wording (CITY-50 to CITY-53) and no new text is invented.
  Scenario: CITY2-21 Eastmere has no published rent, so no rent side and no comparison at Band D
    Then council "E07999001" has field "rentSeries" with status "no-record-in-source"
    And council "E07999001" at band "D" has no rent side
    And council "E07999001" at band "D" for product "2-year-fixed" has no comparison

  @ui
  Scenario: CITY2-22 a council with no rent shows its buy side and says its rent is missing
    Given the user has picked "Northbridge (sample)" and "Eastmere (sample)"
    When the user reads "Rent or buy, per month"
    Then Eastmere's rent cell says its rent is not published, in the council page's wording (CITY-50, CITY-51; wording to be confirmed on a compare board)
    And Eastmere's buy side stays, with no "more" sentence for it, and nothing is shown as £0

  Scenario: CITY2-23 Westmere has no published council tax at any band
    Then council "E07999002" at band "D" has problem "council-tax-missing"
    And council "E07999002" has field "bands" with status "no-record-in-source"

  @ui
  Scenario: CITY2-24 a council with no council tax has no side, no comparison and no zero in compare
    Given the user has picked "Northbridge (sample)" and a council whose council tax is not recorded, as Westmere "E07999002" is (the board's lists do not offer Westmere; this holds if the lists come to offer it)
    When the user reads the council tax and rent or buy rows
    Then that council's cells say what the council page says for a missing source (CITY-52, CITY-53; wording to be confirmed on a compare board)
    And no rent side, buy side, comparison or council tax figure is shown for that council, and nothing is shown as £0

  @ui
  Scenario: CITY2-25 "How we got this" in compare says each figure's area and period and that nothing is ranked
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads "How we got this"
    Then it reads "Each figure says its area (here the council area) and its period. Council tax is the published yearly amount for the band; the monthly amount is that yearly amount divided by 12. Rent or buy shows repayment and council tax only, on the example inputs, with the same council tax on both sides; the average rent and the average price describe different homes. The two councils are shown side by side in the order you picked, never sorted or ranked, and no figure is worked out between them. Months marked provisional may change. Sample data: every council and figure is made up, shaped like the source named beside it."

  @ui
  Scenario: CITY2-26 each group of rows carries the stamps of its sources, and each council has an Open link
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user reads under each group
    Then "What it costs here" ends with the stamps "MHCLG council tax levels", "ONS Price Index of Private Rents" and "UK House Price Index"
    And "Rent or buy, per month" ends with "Bank of England quoted rates", "ONS Price Index of Private Rents", "UK House Price Index" and "MHCLG council tax levels", and "Council tax by band" ends with "MHCLG council tax levels"
    And on a phone "Open Northbridge (sample)" and "Open Southvale (sample)" open each council's page

  # The offline message is the council page's (CITY-99); no compare board draws it.
  @ui
  Scenario: CITY2-27 offline, the compare results stay and a new pick waits
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the device goes offline
    Then the page says "You’re offline" and "This device has no internet connection." and "Results already on screen stay; new searches and changed inputs wait until you’re back online." (CITY-99)
    And a new pick or band is held until the device is back online

  @ui
  Scenario: CITY2-28 the two councils picked and the band are never stored or logged and never in the address
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)" and a band
    When the server has answered the compare request
    Then the councils and the band travel in the request body only, and none is stored, or written to a server, application, hosting or tracing log
    And nothing is in the query string, and analytics never records a control (FE-05)

  @ui
  Scenario: CITY2-29 compare works by keyboard, with 44 px targets, no sideways scrolling and a dark twin
    Given the user has opened compare on a phone and on desktop
    When the user works through the page by keyboard
    Then every control can be reached and used, and each is at least 44 px tall, and nothing scrolls sideways
    And the display control changes the theme and the text size, and each board's dark twin shows the same rows (decision 0049, canvas Dark twins)

  # Share (design spec: "Share a link": the council in the address, nothing stored; never the budget or edited inputs).
  # No board draws the council Share control opening; the boards show the buttons "Share" (council header) and "Share this comparison" (compare). Proposed behaviour, finalised before build.
  @ui
  Scenario: CITY2-30 Share on a council page offers a link to the council and a printable summary
    Given the user has opened the council page for council "E06999001"
    When the user chooses "Share" in the header
    Then the choices are a link to the council and the printable summary (the proposed wording is finalised before build)
    And no account is needed

  @ui
  Scenario: CITY2-31 a shared council link carries the council and nothing the visitor typed
    Given the user has typed a budget, picked a band and changed the deposit, rate and term on the council page for council "E06999001"
    When the user copies the council link from "Share"
    Then the link is the council's own address and nothing is stored to make it
    And it holds no budget, band, deposit, rate or term, and no query string

  @ui
  Scenario: CITY2-32 "Share this comparison" carries the two councils and never the band, a budget or an edited input
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)" and a band
    When the user chooses "Share this comparison"
    Then the link opens compare with those two councils, in that order, and nothing is stored to make it
    And it holds no budget and no edited input, and no query string (the place of the two councils in the address is decided at build)

  @ui
  Scenario: CITY2-33 Print on the compare page opens the printout of a council
    Given the user has picked "Northbridge (sample)" and "Southvale (sample)"
    When the user chooses "Print"
    Then the browser's print dialog opens on the printable council summary, which is for one council at a time and has no comparison in it
    And the printout is the one specified from CITY2-34 (the design spec's printable summary reuses the designed report, FE-21)

  # The council printout (board CouncilPrint, A4, three pages). FE-50: light only, no dark version. It uses the example inputs only and never the budget.
  @ui
  Scenario: CITY2-34 the printout's cover names the council, what it is and the population, and says sample data
    Given the user has chosen the printable summary for council "E06999001"
    When the printout is shown
    Then page 1 begins with "vestagraph" and "Northbridge (sample)"
    And the line under it reads "Council area summary · England · unitary council · population <n> (mid-2025 estimate, council area)", quoted from `council-area.json` for "E06999001" (population)
    And a stamp reads "SAMPLE DATA"

  @ui
  Scenario: CITY2-35 the printout says which example inputs it used even if the screen showed others, and prints no budget
    Given the user has changed the deposit, rate and term and typed a budget on the council page for council "E06999001"
    When the user prints the summary
    Then page 1 reads "Example inputs used on this page: deposit <depositPercent>%, term <termYears> years, mortgage rate <rate>% (Bank of England quoted rate, 2-year fixed, <maxLoanToValuePercent>% loan band, <month>), council tax Band D. If the screen showed other inputs, this printout still uses these example inputs. Your budget is not printed. Nothing here is saved by Vestagraph.", quoted from `council-result.json` exampleInputs and `E06999001 / rentOrBuy / byBand / D / buySides / 2-year-fixed / rateBand`
    And no edited input and no budget appears anywhere on it

  @ui
  Scenario: CITY2-36 page 1 prints What it costs here with the council tax, rent and price and their periods
    Given the user has chosen the printable summary for council "E06999001"
    When the user reads page 1 under "What it costs here"
    Then "Council tax, Band D (example)", "Average rent · council area · <rentPeriod> (provisional)" and "Average price · council area · <pricePeriod> (provisional)" each show their figure, quoted from `bands`, `rentSeries` and `priceSeries`
    And the line under them reads "Council area · council tax 2026 to 2027, rent <rentPeriod> and price <pricePeriod> (both provisional)"

  @ui
  Scenario: CITY2-37 page 1 prints rent or buy with the example inputs, its limits and the 5-year fixed gap
    Given the user has chosen the printable summary for council "E06999001"
    When the user reads page 1 under "Rent or buy, per month"
    Then the lines "Rent", "Buy · 2-year fixed" and "Buy · 5-year fixed" show "rent <rent> + council tax <tax>", "repayment <repayment> + council tax <tax>" and "No published rate for this deposit size", quoted from `E06999001 / rentOrBuy / byBand / D`
    And the sentence "On these inputs, buying the average-priced home costs £<difference> more a month than the average rent. This is repayment and council tax only; not the full cost of owning or renting. The rent covers every size of rented home, the price every type sold." quotes `shownDifference`
    And "Example inputs only; the deposit and term are examples, not advice."

  @ui
  Scenario: CITY2-38 page 2 prints the eight council tax bands, a year and a month for each
    Given the user has chosen the printable summary for council "E06999001"
    When the user reads page 2 under "Council tax by band"
    Then "Band A" to "Band H" each show "<yearly> a year · <monthly> a month", quoted from `E06999001 / bands / <band>` (shownYearly, shownCouncilTax)
    And the line reads "Council area · 2026 to 2027 · average for the council area, two adults, before discounts; parish charges vary."

  @ui
  Scenario: CITY2-39 page 2 prints "How the figures changed" from the generated captions
    Given the user has chosen the printable summary for council "E06999001"
    When the user reads page 2 under "How the figures changed"
    Then it prints the rent sentence, the four property type sentences ("Detached:", "Semi-detached:", "Terraced:", "Flat:") and the house price to earnings ratio sentence, each quoted from `E06999001 / captions` and `E06999001 / priceByType`
    And "The latest 2 months are provisional and may change." follows the rent sentence and "The latest 12 months of each price are provisional and may change." follows the types

  @ui
  Scenario: CITY2-40 page 2 prints who rents and who owns with its rounding line
    Given the user has chosen the printable summary for council "E06999001"
    When the user reads page 2 under "Who rents, who owns"
    Then it shows the five shares quoted from `E06999001 / tenureShares`, "Shares are rounded to one decimal place, so they may not add up to 100%." (FE-48), and "Council area · Census day, 21 March 2021 · share of households."
    And the single-point sentence "In March 2021, <percent>% of households rented privately." quotes `E06999001 / captions / tenure`

  @ui
  Scenario: CITY2-41 page 3 prints How we got this and each source's edition, period and status
    Given the user has chosen the printable summary for council "E06999001"
    When the user reads page 3
    Then it reads "How we got this" with "Each figure says its area (here the council area) and its period. Council tax is the published yearly amount for the band; the monthly amount is that yearly amount divided by 12. Rent or buy shows repayment and council tax only, on the example inputs, with the same council tax on both sides; the average rent and the average price describe different homes. Months marked provisional may change. Sample data: every council and figure is made up, shaped like the source named beside it."
    And it lists "Population", "Council tax", "Private rents", "House prices", "Affordability ratio", "Who rents, who owns" and "Mortgage rates", each with its source stamp and "Edition: … · Period: … ·" and its status, quoted from that field's `source` in `council-area.json`
    And it closes "Each source’s edition, period and status are listed above. This printout uses the example inputs only and does not include your budget. Sample data: every council and figure is made up."

  @ui
  Scenario: CITY2-42 every printed page has the same footer with its page number
    Given the user has chosen the printable summary for council "E06999001"
    When the user reads the foot of each page
    Then each reads "vestagraph · sample data · Northbridge (sample)" with "Page 1 of 3", "Page 2 of 3" and "Page 3 of 3"

  # FE-50: the printout is paper, so it has no dark version, as the area printout has none.
  @ui
  Scenario: CITY2-43 the printout is light only, even from the dark theme
    Given the user has chosen the dark theme in "Display" and is on the council page for council "E06999001"
    When the user chooses to print the summary
    Then the printout is drawn in the light colours, and there is no dark printout and no dark twin of the board (FE-50)

  @ui
  Scenario: CITY2-44 every printed line is at least 12 pt and the printout is readable in greyscale
    Given the user has chosen the printable summary for council "E06999001"
    When the user prints it in greyscale
    Then every printed line is at least 12 pt (as PRINT-16 in `area-printout.feature`)
    And every figure, label and provisional mark is still readable, and no meaning is carried by colour alone (B23)

  @ui
  Scenario: CITY2-45 a council with a gap prints the gap as not published and never as zero
    Given the user has chosen the printable summary for council "E07999001"
    When the user reads the pages
    Then Eastmere's missing rent is printed as not published, in the council page's wording (CITY-50), with no rent side and no "more" sentence, and nothing is printed as £0
    And the printout makes no verdict about the council and carries no ranking (0054)

  # What changed since your last visit (design spec: off until "Remember councils on this device" is turned on; PECR consent, like Recent postcodes).
  # Needs the PECR check before build. The browser stores the councils viewed and the edition dates seen, and picks which published figures to quote; it does no arithmetic (rule 2).
  @ui
  Scenario: CITY2-46 what changed is off by default and says nothing is kept
    Given the user has opened the council page for council "E06999001" for the first time
    When the user reads "What changed since your last visit"
    Then it says "Off. Vestagraph only says what is newer once you turn this on." and the setting "Remember councils on this device" has the action "Turn on"
    And it says "Nothing is kept while this is off."
    And the consent text reads "This keeps a short list of the councils you view and the editions you saw, so Vestagraph can say what is newer next time. It is a short browsing history. It stays in this browser and is never sent to us. Anyone using this device can see it. It is kept until you clear it, at most 12 months. Turning this off clears it."

  @ui
  Scenario: CITY2-47 nothing is stored in the browser while the setting is off
    Given the setting "Remember councils on this device" is off
    When the user views council pages for "E06999001" and "E06999002"
    Then no list of councils and no edition date is written to the browser
    And no record of the visit is sent to us

  @ui
  Scenario: CITY2-48 with the setting on, a newer edition quotes both figures from the generated file
    Given the setting is on and the user has seen the council page for council "E06999001" before
    When a newer edition of the average rent has been published since the last visit
    Then the panel shows "Average rent · Northbridge (sample)" and "£<newest figure> a month in <month> (provisional), was £<earlier figure> in <earlier month>", both quoted from the generated file
    And under it "Council area · newer edition: <the newer edition’s name and date>." and "The browser picks which published figures to quote; it does no arithmetic, so no difference is shown."
    # Waits for a fixture: no sample record has an earlier edition, so the board draws the "was" figure and the newer edition's name and date as placeholders, not invented numbers.

  @ui
  Scenario: CITY2-49 a month revised since the last visit quotes the newest figure for both months and says revised
    Given the setting is on and the user has seen the council page for council "E06999001" before
    When a month the user saw has been revised
    Then the panel shows "Average rent, <month> · Northbridge (sample)" with "Newest published figure £<figure> a month (provisional)" and the word "revised"
    And it quotes the newest published figure for both months, and shows no difference
    # Waits for a fixture: the sample data has provisional months but no revision record; the board's "revised" label and earlier figure are placeholders.

  @ui
  Scenario: CITY2-50 with the setting on, a list shows what is kept on this device
    Given the setting is on and the user has viewed the council pages for "E06999001" and "E06999002"
    When the user reads the panel
    Then it says "On. Records are kept until you clear them, at most 12 months, and only on this device."
    And "Kept on this device" lists "Councils viewed: Northbridge (sample), Southvale (sample)" and "Editions seen: <the rent edition>; <the price data edition>", with the editions quoted from the rent and price sources' `source` edition in `council-area.json`
    And the same consent text as the setting's is shown with the action "Clear"

  @ui
  Scenario: CITY2-51 the sources of the figures are stamped under the panel
    Given the setting is on and the panel shows a newer edition
    When the user reads under the panel
    Then the stamps "ONS Price Index of Private Rents" and "UK House Price Index" are shown for the figures it quotes

  @ui
  Scenario: CITY2-52 Clear deletes the list at once and the setting stays on
    Given the setting is on and a list is kept
    When the user chooses "Clear"
    Then the panel says "Cleared. The list of councils and editions is deleted from this device." and "Still on, with nothing kept. Councils you view from now on are listed here again."
    And the list is gone from the browser, and "Turning the setting off also clears the list." is shown

  @ui
  Scenario: CITY2-53 turning the setting off clears the list too
    Given the setting is on and a list is kept
    When the user turns the setting off
    Then the list of councils and editions is deleted from the browser
    And the panel is back to "Off." with "Nothing is kept while this is off."

  @ui
  Scenario: CITY2-54 records older than 12 months are dropped and nothing is ever sent to us
    Given the setting is on and a record is more than 12 months old
    When the user opens a council page
    Then that record is dropped, and no list, council or edition date has been sent to us, in a request, a log or analytics
    And the consent text says the list is on this device and anyone using it can see it

  @ui
  Scenario: CITY2-55 several skipped editions compare with the edition seen last time
    Given the setting is on and two newer editions have been published since the user's last visit
    When the user opens the council page
    Then the panel compares with the edition the user saw last time, not with the one before the newest
    And both figures it quotes come from the generated file

  @ui
  Scenario: CITY2-56 on desktop the panel sits at the top of the council page, under the council's name
    Given the user has opened the council page for council "E06999001" on desktop
    When the page has loaded
    Then "What changed since your last visit" sits under "Northbridge (sample)" and its population line, in each of its three states
    And "← Check another place" stays above the council's name

  # A council replaced during the pilot (CITY-97): its "what changed" records are dropped with a note (design spec). No board draws the note: proposed wording, finalised before build.
  @ui
  Scenario: CITY2-57 the records of a replaced council are dropped with a note
    Given the setting is on and a council the user viewed has been replaced by a new council
    When the user opens the new council's page
    Then the old council's records are dropped, and a note says so (wording to be drawn before build)
    And the note links to the new council, as CITY-97 does

  # The City Explorer About the data page (board CouncilAboutData; FE-33, DA-12). FE-45: DfT's status is shown only here.
  @ui
  Scenario: CITY2-58 About the data says where each fact comes from, its edition and its status as the publisher states it
    Given the user has opened "About the data" from the council page for council "E06999001"
    When the page has loaded
    Then the page heading is "About the data", with the link "← Back to the council page"
    And it reads "City Explorer’s sources: where each fact comes from, the date of the edition we hold and its status as the publisher states it. Sample data: every council, figure and neighbourhood on a City Explorer page is made up, shaped like the source named here."

  @ui
  Scenario: CITY2-59 the council tax row gives its edition, status and what Band D means
    Given the user has opened "About the data"
    When the user reads "Council tax by band"
    Then it reads "Edition 2026 to 2027, published 25 March 2026" and "Status: No designation recorded in our research."
    And it reads "Annual. Band D here is a two-adult equivalent: it is not what every household pays. Parish charges are inside the average, so it is not a particular home’s bill." with the source "MHCLG council tax levels"

  @ui
  Scenario: CITY2-60 the private rents row gives its edition, next release, status and how a missing month is shown
    Given the user has opened "About the data"
    When the user reads "Private rents"
    Then it reads "Edition of 21 October 2026; next release 18 November 2026" and "Status: Official statistics in development (the workbook’s own words)."
    And it reads "Monthly, UK-wide table with English councils. A month the source marks as not available is shown as missing, never as zero." with the source "ONS Price Index of Private Rents"

  @ui
  Scenario: CITY2-61 the house prices row says each release revises the previous 12 months and what a type with no figure shows
    Given the user has opened "About the data"
    When the user reads "House prices, all types and by property type"
    Then it reads "August 2026 data, published 21 October 2026" and "Status: No designation recorded in our research."
    And it reads "Monthly. Each release adds a new month and revises the previous 12, so the newest 12 months are marked provisional. The council file has detached, semi-detached, terraced and flat prices; a type with no figure for a council is shown as a gap, never as zero."
    And it carries the credit "Contains HM Land Registry data © Crown copyright and database right 2020. This data is licensed under the Open Government Licence v3.0." and the source "UK House Price Index"

  @ui
  Scenario: CITY2-62 the affordability row says the ratio is workplace-based
    Given the user has opened "About the data"
    When the user reads "Affordability ratio"
    Then it reads "Released 26 March 2026; next March 2027" and "Status: Accreditation not stated on the bulletin or dataset pages."
    And it reads "Yearly. It is the median house price to median earnings, workplace-based: it uses earnings where people work, not where they live." with the source "ONS housing affordability"

  @ui
  Scenario: CITY2-63 the tenure row says it is one day's count and that merged councils may not match
    Given the user has opened "About the data"
    When the user reads "Who rents, who owns"
    Then it reads "Census day, 21 March 2021 (we hold version 3; version 4 of 28 March 2023 exists)" and "Status: No designation recorded in our research."
    And it reads "A count of households on one day, so it is not a current figure. Councils merged after 2021 may not match the 2021 areas." with the source "Census 2021, TS054"

  @ui
  Scenario: CITY2-64 the population row gives its release and its accredited status
    Given the user has opened "About the data"
    When the user reads "Population"
    Then it reads "Mid-2025 estimate, released 29 July 2026" and "Status: Accredited official statistics (reviewed by the Office for Statistics Regulation, March 2017)."
    And it reads "The mid-year estimates stay the official series." with the source "ONS mid-year population estimates"

  @ui
  Scenario: CITY2-65 the transport connectivity row gives DfT's own status, scale and licence note
    Given the user has opened "About the data"
    When the user reads "Transport connectivity"
    Then it reads "Published 29 September 2025; Q4 2024 (October to December 2024), version V1.0.0" and "Status: Provisional. DfT publishes it as “Experimental Statistics”."
    And it quotes "DfT says: “All results presented in this publication are provisional results for 2021 LSOA boundaries and 2021 data sources.” Next update: to be decided."
    And it reads "Scores run from 0 to 100, where 100 is the most connected area on DfT’s scale, and DfT says scores should be interpreted relative to other areas." and "Licence: the DfT page says Open Government Licence v3.0; the data file’s own metadata says “TBA”." with the source "DfT transport connectivity metric"

  @ui
  Scenario: CITY2-66 the mortgage rates row says where the rates come from and that no rate is ever borrowed
    Given the user has opened "About the data"
    When the user reads "Mortgage rates"
    Then it reads "Latest month October 2026, published on the 5th working day of the following month" and "Status: No designation recorded in our research."
    And it reads "Monthly averages of quoted rates by loan-to-value band, not seasonally adjusted. The Bank says the advertised rates come from Moneyfacts, weighted by lenders’ business volumes. A deposit with no published rate band shows “No published rate”, never a borrowed rate." with the source "Bank of England quoted rates"

  @ui
  Scenario: CITY2-67 the neighbourhood boundaries and names rows give their editions, licences and the Library's caution
    Given the user has opened "About the data"
    When the user reads "Neighbourhood boundaries" and "Neighbourhood names"
    Then the boundaries read "ONS Open Geography Portal; May 2026 council layers, 2021 neighbourhood layers", "Status: No designation recorded in our research." and "Source: Office for National Statistics licensed under the Open Government Licence v.3.0. Contains OS data © Crown copyright and database right [year of the boundary edition]." with the source "ONS geography licences"
    And the names read "2021 MSOA names, version 2.3, published 13 February 2026", "Status: The Library says these are not official names." and "Published under the Open Parliament Licence; the source is acknowledged on the map." with the source "House of Commons Library MSOA names"

  @ui
  Scenario: CITY2-68 every row names its edition date and status, and a status the research did not record says so
    Given the user has opened "About the data"
    When the user reads the ten rows
    Then each row states "Status:" with the publisher's own designation, or "No designation recorded in our research." where none was recorded
    And no row names a status the sources research did not find, and no row's status is ranked or combined

  @ui
  Scenario: CITY2-69 the DfT status is shown on About the data only, not beside the connectivity figure
    Given the user has opened the council page for council "E06999001" and the neighbourhood page for neighbourhood "E01999011"
    When the user reads "Transport connectivity" on each
    Then no "provisional" or "Experimental Statistics" tag sits beside the figure (FE-45; CITY-82, HOOD-09)
    And "About the data" is where the status is shown (CITY2-65)

  @ui
  Scenario: CITY2-70 each row opens and closes with its own button
    Given the user has opened "About the data"
    When the user chooses the button of one row
    Then that row's date line, status, note and source open or close, and the others stay as they were
    And the button is reachable by keyboard and is at least 44 px tall

  @ui
  Scenario: CITY2-71 About the data is linked from How we got this on the council and neighbourhood pages
    Given the user has opened the council page for council "E06999001"
    When the user chooses the About the data link in "How we got this"
    Then this page opens, and the same link on the neighbourhood page (HOOD-33) opens the same page

  @ui
  Scenario: CITY2-72 About the data works by keyboard and has a dark twin
    Given the user has opened "About the data" on a phone and on desktop
    When the user works through the page by keyboard, and picks the dark theme in "Display"
    Then every control can be reached and used, and the dark twin shows the same rows and wording
    And nothing scrolls sideways
