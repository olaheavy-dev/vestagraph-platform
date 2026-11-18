@screen @buying @renting
Feature: Check an energy certificate (one home's certificate, looked up by its number)
  Question it answers: "I have a home in mind and its energy certificate number: what does that certificate say, how old is it, and what can't it tell me?"
  Modes: both (and anyone, with no account; the page behaves the same signed in or not and stores nothing)
  Added 18 Nov 2026 (stage 5b specification before the pilot gate, decision 0052; DA-09, "Certificate number (Recommended)"; status item 5b). The design is `docs/superpowers/specs/2026-11-18-energy-certificate-design.md` and its plan is `docs/superpowers/plans/2026-11-18-energy-certificate.md`.
  Fixtures: the synthetic sample certificates in `packages/fixtures/data/energy-certificates.json` and the generated `packages/fixtures/generated/energy-certificate-result.json`, cited by sample number (all start 0000-0000-0000-0000-, an obviously synthetic number): 0001 a current flat (rating band E), 0002 more than 10 years old, 0003 replaced by a newer certificate, 0004 cancelled, 0005 a non-domestic certificate, 0006 a certificate for Wales, 0007 an older schema with facts missing, 0008 registered on 29 February 2016, so valid until 28 February 2026. The topic registry `packages/fixtures/data/pilot-topics.json` holds the "Check this" row that opens the page (TOPIC-41).
  Figures: none typed here (AGENTS.md rule 2). Ratings, scores, the certificate's own running-cost estimates, indicative improvement costs and typical savings are inputs recorded with their source in the sample file and quoted by the page. "Valid until" and "more than 10 years old" are calculated outputs of `energy-certificate-result.json`: 10 years from the registration date (Energy Performance of Buildings (England and Wales) Regulations 2012, regulation 9(2)(a)), worked out for the fixtures' snapshot date (the file's `today`). A scenario never types a date, a rating or an amount.
  Rule 4: our own voice never calls a home, rating or improvement "good", "bad", "safe", "verified", "approved" or "recommended", and never turns the register's rating into a score of our own. Rule 6: a certificate for Wales shows "Wales is not yet covered." Rule 7: a fact an older certificate does not hold reads "Not on this certificate", never blank, zero or a favourable value.
  Wording status: this page is not on any board yet, and ALL of its wording is proposed, for the founder's copy review before the pilot gate (the list is in the task report and the pull request description). Nothing here is approved wording. Finalised before build.
  Address: the page is `/energy-certificate`. The certificate number is never in the path, the query string or the `#` fragment; it lives only in the page's state and in the request body (founder, 18 Nov 2026; decision 0014 treats a certificate number like a postcode). So a result can't be bookmarked or shared as a link; the printout is the way to keep it.
  No address or postcode, ever: the register's address and postcode fields are dropped on receipt (the data licence allows address use only for energy performance purposes), so the page never shows or implies an address, and never implies that the certificate belongs to a postcode searched before.
  Data scenarios (no tag) check the generated file with the energy certificate steps in docs/specs/README.md. Every other scenario is `@ui`, because the outcome is on the page. The register is faked in the browser tests (an adapter returning a sample, a missing number, an unavailable register and an over-limit answer); live-service tests stay out of the merge gate (decision 0029).

  Required states (design "States" list, the printout and the anti-goals; AGENTS.md rules 2, 4, 6 and 7):
    1. empty page, with the GOV.UK link and the one-line note about where the number is -> ENERGY-02, ENERGY-03
    2. number wrongly formatted, an inline error before any lookup (spaces and dashes ignored; 19 and 21 digits, and letters, rejected) -> ENERGY-04 to ENERGY-08
    3. checking, a skeleton and no spinner (FE-64) -> ENERGY-09
    4. found, current certificate -> ENERGY-10 to ENERGY-19
    5. found, more than 10 years old, with its date (and the 29 February boundary) -> ENERGY-20 to ENERGY-23
    6. found, replaced by a newer certificate, or cancelled, with a pointer to GOV.UK for a replaced one -> ENERGY-24 to ENERGY-27
    7. a non-domestic or display energy certificate -> ENERGY-28, ENERGY-29
    8. a certificate for Wales -> ENERGY-30, ENERGY-31
    9. not found -> ENERGY-32
    10. register unavailable or over its limit, "Not known right now" -> ENERGY-33, ENERGY-34
    11. a fact missing from an older certificate, "Not on this certificate" -> ENERGY-35, ENERGY-36
    the printout, ending with its sources page -> ENERGY-45 to ENERGY-47
    anti-goal: an address or postcode shown, implied or stored -> ENERGY-37, ENERGY-38, ENERGY-41
    anti-goal: the number in a URL, a log, an error report or analytics -> ENERGY-39, ENERGY-40
    anti-goal: a verdict word or a score of our own -> ENERGY-42
    anti-goal: a missing fact shown as zero, blank or favourable -> ENERGY-35, ENERGY-36
    anti-goal: the certificate's estimates presented as the household's bills -> ENERGY-14, ENERGY-15
    the way in from the area result and the landing page -> ENERGY-01 (the registry row), TOPIC-41, PRINT-21, LAND-21
    sources, display settings, dark mode, keyboard and screen reader, phone and desktop -> ENERGY-43, ENERGY-44, ENERGY-48 to ENERGY-52

  # ---- The way in ----

  # fixture: packages/fixtures/data/pilot-topics.json (the "Check this" row opens the page; the GOV.UK link moves onto the page)
  Scenario: ENERGY-01 the energy certificate row of the registry opens the page and is never counted
    Then topic "energy-certificate-home" is route-only and not counted
    And topic "energy-certificate-home" opens the Vestagraph page "/energy-certificate"

  # ---- State 1: the empty page ----

  @ui
  Scenario: ENERGY-02 the empty page asks for the number and shows no result
    Given the visitor opens "/energy-certificate"
    When the page has loaded
    Then the title reads "Check an energy certificate", a field is labelled "Certificate number" and a button reads "Search"
    And no rating, cost, address or postcode is shown, and the number is not asked for in the address bar

  @ui
  Scenario: ENERGY-03 the empty page says where the number is and links to GOV.UK
    Given the visitor opens "/energy-certificate"
    When the visitor reads under the field
    Then it says "The number is on the certificate. If you don't have it, you can find it on GOV.UK." with the link "Find an energy certificate (gov.uk) ↗" to https://www.gov.uk/find-energy-certificate
    And it doesn't say the certificate is for any postcode or address

  # ---- State 2: a wrongly formatted number ----

  @ui
  Scenario: ENERGY-04 spaces and dashes in the number are ignored
    Given the visitor opens "/energy-certificate"
    When the visitor types the sample number "0000-0000-0000-0000-0001" with spaces in place of the dashes and presses "Search"
    Then the certificate for that number is looked up and shown
    And no error about the format is shown

  @ui
  Scenario: ENERGY-05 a number with 19 digits is rejected before any lookup
    Given the visitor opens "/energy-certificate"
    When the visitor types 19 digits and presses "Search"
    Then an inline error under the field reads "A certificate number has 20 digits. Check the number and try again."
    And no request is made to the register

  @ui
  Scenario: ENERGY-06 a number with 21 digits is rejected before any lookup
    Given the visitor opens "/energy-certificate"
    When the visitor types 21 digits and presses "Search"
    Then the same inline error reads "A certificate number has 20 digits. Check the number and try again."
    And no request is made to the register

  @ui
  Scenario: ENERGY-07 a number with letters is rejected before any lookup
    Given the visitor opens "/energy-certificate"
    When the visitor types a number that contains a letter and presses "Search"
    Then the same inline error is shown and no request is made to the register

  @ui
  Scenario: ENERGY-08 the format error keeps what the visitor typed and is announced
    Given the visitor has pressed "Search" with a number of the wrong length
    When the error appears
    Then the field still holds what the visitor typed, the focus stays on the field, and a screen reader announces the error text
    And the error is not shown by colour alone

  # ---- State 3: checking ----

  @ui
  Scenario: ENERGY-09 while the register answers the page shows a skeleton and no spinner
    Given the visitor has pressed "Search" with a sample number and the register has not answered yet
    When the visitor looks at the page
    Then a skeleton in the shape of the result is shown, with no spinner (FE-64)
    And the button's label changes to "Checking" and it can't be pressed twice
    And with reduced motion the skeleton does not animate

  # ---- State 4: a current certificate (sample 0001) ----

  Scenario: ENERGY-10 the current sample is shown and is not more than 10 years old
    Then energy certificate "0000-0000-0000-0000-0001" has outcome "shown"
    And energy certificate "0000-0000-0000-0000-0001" is not more than 10 years old
    And energy certificate "0000-0000-0000-0000-0001" has status line "none"

  @ui
  Scenario: ENERGY-11 a current certificate shows its ratings now and potential, quoted
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0001"
    When the result is shown
    Then "Energy rating" shows the band and score of `currentRating` and, after an arrow, those of `potentialRating`, as in `energy-certificate-result.json`
    And a link "EPC register ↗" goes to the register's page for the certificate on GOV.UK
    And the rating is shown as the register's band and score, with no word of our own about it

  @ui
  Scenario: ENERGY-12 a current certificate shows its date, type and size from the certificate
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0001"
    When the visitor reads the line under the title
    Then it shows the property type, the total floor area and "valid until" with the certificate's `validUntil`, all quoted from the file
    And it shows no address, street, town or postcode

  @ui
  Scenario: ENERGY-13 the sample data chip says the numbers are made up
    Given the visitor has searched for a sample number while the register is not connected
    When the result is shown
    Then a chip reads "Sample data" and the page says that the certificate is a made-up example
    And no real certificate number or address is shown

  @ui
  Scenario: ENERGY-14 the running costs are labelled as the certificate's estimates, not bills
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0001"
    When the visitor reads "Running costs"
    Then the heading reads "Running costs (the certificate's estimates, not your bills)"
    And Heating, Hot water and Lighting each show their `currentPence` a year and, after an arrow, their `potentialPence`, written in pounds from the pence in the file

  @ui
  Scenario: ENERGY-15 the page adds the costs into no total and compares them with nothing
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0001"
    When the visitor reads the whole result
    Then there is no total yearly cost, no "you would save" figure of our own, and no comparison with an average home or the area
    And the cost lines are the certificate's own, each labelled with its heading

  @ui
  Scenario: ENERGY-16 each part of the home shows its description and star rating
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0001"
    When the visitor reads "The home, part by part"
    Then each `parts` entry shows its description and its stars out of five as text, for example "1 of 5 stars", as in the file
    And the stars are not the only way the rating is shown

  Scenario: ENERGY-17 the improvements keep the certificate's order and add no total
    Then energy certificate "0000-0000-0000-0000-0001" lists improvements in its own order with no total

  @ui
  Scenario: ENERGY-18 the suggested improvements are shown in the certificate's order
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0001"
    When the visitor reads "Suggested improvements (the certificate's, in its order)"
    Then the improvements are listed by their `sequence`, each with its description, its indicative cost and "typical saving" a year, as in the file
    And no improvement is marked "recommended", "best" or "worthwhile" and none is ranked by us

  @ui
  Scenario: ENERGY-19 the indicative cost and typical saving are labelled as the certificate's
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0001"
    When the visitor reads an improvement
    Then its cost reads as the certificate's "indicative cost" and its saving as the certificate's "typical saving", with the note "Estimates from the certificate, not quotes and not your bills."

  # ---- State 5: more than 10 years old (samples 0002 and 0008) ----

  Scenario: ENERGY-20 the older sample is more than 10 years old and still shown
    Then energy certificate "0000-0000-0000-0000-0002" has outcome "shown"
    And energy certificate "0000-0000-0000-0000-0002" is more than 10 years old

  # Worked boundary (regulation 9(2)(a); the engine's tested rule): a certificate registered on 29 Feb 2016 runs to 28 Feb 2026, before the file's snapshot date, so it is more than 10 years old.
  Scenario: ENERGY-21 the sample registered on 29 February is more than 10 years old
    Then energy certificate "0000-0000-0000-0000-0008" has outcome "shown"
    And energy certificate "0000-0000-0000-0000-0008" is more than 10 years old

  @ui
  Scenario: ENERGY-22 an older certificate is shown with a notice and its date
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0002"
    When the result is shown
    Then a notice above the rating reads "This certificate is more than 10 years old" with the certificate's `validUntil` date
    And the facts are still shown below it

  @ui
  Scenario: ENERGY-23 the notice for an older certificate gives no advice of our own
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0002"
    When the visitor reads the notice
    Then it states the date and nothing more, and doesn't say the facts are wrong, out of date or unreliable

  # ---- State 6: replaced or cancelled (samples 0003 and 0004) ----

  Scenario: ENERGY-24 the replaced sample carries the status "superseded"
    Then energy certificate "0000-0000-0000-0000-0003" has outcome "shown"
    And energy certificate "0000-0000-0000-0000-0003" has status line "superseded"

  @ui
  Scenario: ENERGY-25 a replaced certificate is shown with its status and a pointer to the newer one
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0003"
    When the result is shown
    Then a notice reads the certificate's `statusLine` text, "A newer certificate has replaced this one."
    And it adds "Look for the newer certificate on GOV.UK." with the link "Find an energy certificate (gov.uk) ↗"
    And the older certificate's facts are still shown below

  Scenario: ENERGY-26 the cancelled sample carries the status "cancelled"
    Then energy certificate "0000-0000-0000-0000-0004" has outcome "shown"
    And energy certificate "0000-0000-0000-0000-0004" has status line "cancelled"

  @ui
  Scenario: ENERGY-27 a cancelled certificate is shown with the register's status and no pointer
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0004"
    When the result is shown
    Then a notice reads the certificate's `statusLine` text, "The register has cancelled this certificate."
    And no pointer to a newer certificate is shown, because the register names none

  # ---- State 7: not a home certificate (sample 0005) ----

  Scenario: ENERGY-28 the non-domestic sample is not shown as a home certificate
    Then energy certificate "0000-0000-0000-0000-0005" has outcome "not-domestic"
    And energy certificate "0000-0000-0000-0000-0005" shows no ratings, costs, parts or improvements

  @ui
  Scenario: ENERGY-29 a non-domestic or display energy certificate number says the page covers homes only
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0005"
    When the result is shown
    Then the page reads "This page covers home energy certificates only." with the link "Find an energy certificate (gov.uk) ↗"
    And no rating, cost or fact of that certificate is shown

  # ---- State 8: Wales (sample 0006) ----

  Scenario: ENERGY-30 the Wales sample is not yet covered
    Then energy certificate "0000-0000-0000-0000-0006" has outcome "not-yet-covered"
    And energy certificate "0000-0000-0000-0000-0006" shows no ratings, costs, parts or improvements

  @ui
  Scenario: ENERGY-31 a certificate for Wales says Wales is not yet covered and shows nothing of it
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0006"
    When the result is shown
    Then the page reads "Wales is not yet covered." and shows no rating, cost or fact of that certificate (rule 6)

  # ---- State 9: not found ----

  @ui
  Scenario: ENERGY-32 a number the register doesn't hold says it was not found
    Given the register answers that no certificate has the number the visitor typed
    When the visitor presses "Search"
    Then the page reads "We couldn't find a certificate with that number. Check the number, or find it on GOV.UK." with the link "Find an energy certificate (gov.uk) ↗"
    And it doesn't say the home has no certificate, because the number may be wrong

  # ---- State 10: unavailable or over the limit ----

  @ui
  Scenario: ENERGY-33 an unavailable register reads "Not known right now"
    Given the register can't be reached (fake adapter)
    When the visitor presses "Search"
    Then the page reads "Not known right now" with "The energy certificate register isn't answering. Try again in a few minutes, or look on GOV.UK." and the link "Find an energy certificate (gov.uk) ↗"
    And no rating, cost or fact is shown, and nothing reads as zero or a clean result (rule 7)

  @ui
  Scenario: ENERGY-34 a register that says too many requests reads "Not known right now"
    Given the register answers HTTP 429, over its limit (fake adapter)
    When the visitor presses "Search"
    Then the page reads "Not known right now" with the same GOV.UK link, and does not blame the visitor or show the status code
    And pressing "Search" again after a pause tries once more

  # ---- State 11: facts missing from an older certificate (sample 0007) ----

  Scenario: ENERGY-35 the older-schema sample marks its missing facts
    Then energy certificate "0000-0000-0000-0000-0007" has outcome "shown"
    And energy certificate "0000-0000-0000-0000-0007" shows "propertyType" as missing
    And energy certificate "0000-0000-0000-0000-0007" shows "builtForm" as missing
    And energy certificate "0000-0000-0000-0000-0007" shows "parts" as missing
    And energy certificate "0000-0000-0000-0000-0007" shows "improvements" as missing

  @ui
  Scenario: ENERGY-36 a fact the certificate doesn't hold reads "Not on this certificate" in its row
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0007"
    When the result is shown
    Then the property type, built form, "The home, part by part" and "Suggested improvements" rows each read "Not on this certificate"
    And none of them is blank, zero, "none", a dash or a favourable value
    And a code that has no word in our tables also reads "Not on this certificate", never the raw code

  # ---- No address, no postcode ----

  @ui
  Scenario: ENERGY-37 the page shows no address or postcode for any sample
    Given the visitor has searched for each sample number in turn
    When the visitor reads every result
    Then no address line, town or postcode is shown, and nothing says "for" a postcode or address

  @ui
  Scenario: ENERGY-38 the page doesn't imply the certificate belongs to a postcode searched before
    Given the visitor has an area result open and follows its energy certificate row
    When the page "/energy-certificate" opens
    Then the page carries no postcode, no area name and no "for this postcode", and the field is empty
    And the area result is not told which certificate the visitor looked up

  # ---- The number is never in an address or a log (as WCHAT-96 and WCHAT-97) ----

  # 0014 and the design: the number is treated like a postcode.
  @ui
  Scenario: ENERGY-39 the certificate number is in no address the page makes
    Given the visitor has searched for a sample number and has the result open
    When the visitor searches, opens the notices' links, prints and comes back
    Then no request the page makes carries the number in its URL path, query string, `#` fragment or Referer header
    And the address bar still reads "/energy-certificate"

  @ui
  Scenario: ENERGY-40 the certificate number is in no log, error report or analytics event
    Given the visitor has searched for a sample number, then for one the register can't answer, then for one with a wrong format
    When the visitor has finished
    Then no server, application, hosting, error-report or analytics log entry contains the number
    And the number is sent only in the request body

  @ui
  Scenario: ENERGY-41 the page stores nothing about the certificate
    Given the visitor has searched for a sample number, signed in or not
    When the visitor closes the tab and opens "/energy-certificate" again
    Then the field is empty and no certificate is shown
    And nothing about the certificate is in the browser's storage or in the visitor's account, and no "save" button is offered

  # ---- Voice ----

  @ui
  Scenario: ENERGY-42 no state calls a home, a rating or an improvement good, bad, safe, verified, approved or recommended
    Given the visitor has seen every state of the page
    When the visitor reads all its text
    Then none of "good", "bad", "safe", "verified", "approved" or "recommended" is said in our voice about a home, a rating or an improvement
    And the register's rating bands and scores are quoted, and no score, band or verdict of our own is added (rule 4)

  # ---- Sources ----

  @ui
  Scenario: ENERGY-43 How we got this names the register, the date and what the certificate can't tell
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0001"
    When the visitor opens "How we got this"
    Then it names the energy certificate register, its open government licence, the certificate's valid-until date and that the figures are estimates from the certificate
    And it says what a certificate can't tell the visitor, and that we don't show or keep the address

  @ui
  Scenario: ENERGY-44 About the data has one entry for the register
    Given the visitor opens "About the data"
    When the visitor reads it
    Then there is one entry for the energy certificate register with its link, its licence and its limits, and it is the only new entry

  # ---- The printout ----

  @ui
  Scenario: ENERGY-45 the page offers "Print or save as PDF" for a shown certificate
    Given the visitor has searched for the sample number "0000-0000-0000-0000-0001"
    When the visitor reads the result
    Then a "Print or save as PDF" button is offered, and it is not offered for a state that shows no certificate

  @ui
  Scenario: ENERGY-46 the printout shows what the page shows, quoted, in the area printout's style
    Given the visitor has chosen "Print or save as PDF" for the sample number "0000-0000-0000-0000-0001"
    When the visitor reads the printout
    Then it shows the ratings, the running costs labelled as the certificate's estimates, the parts and the improvements in the certificate's order, with no total and no address or postcode
    And every line is at least 12 pt and it is readable in greyscale (PRINT-16, PRINT-17)

  @ui
  Scenario: ENERGY-47 the printout ends with its sources page and the privacy line
    Given the visitor has chosen "Print or save as PDF" for the sample number "0000-0000-0000-0000-0001"
    When the visitor reads the last page
    Then it is the sources page, with dates only (FE-33), and it says "Privacy: this summary was made in your browser. Vestagraph didn't store your search."
    And the suggested file name of the PDF doesn't contain the certificate number

  # ---- Display, accessibility and layouts ----

  @ui
  Scenario: ENERGY-48 display settings apply as on the other pilot pages
    Given the visitor has set the text size and the theme in display settings
    When the visitor opens "/energy-certificate"
    Then the page uses those settings as the area result does (DISP-01 to DISP-06)

  @ui
  Scenario: ENERGY-49 dark mode shows every state with the same content
    Given the visitor has chosen the dark theme
    When the visitor sees each state of the page
    Then each state reads exactly as in the light theme, and its text and controls keep their contrast

  @ui
  Scenario: ENERGY-50 the page works by keyboard and with a screen reader
    Given the visitor uses only the keyboard
    When the visitor tabs through the page, searches and reads a result
    Then the field has a label, the notices are announced when they appear, every link and button can be reached in a sensible order and the focus is always visible

  @ui
  Scenario: ENERGY-51 on a phone the result is one column and nothing needs sideways scrolling
    Given the visitor is on a phone, 390 px wide
    When the visitor reads a result
    Then every section is stacked in one column, and the estimates and star ratings stay readable without scrolling sideways

  @ui
  Scenario: ENERGY-52 on a desktop the page is the same content, laid out wider
    Given the visitor is on a desktop, 1440 px wide
    When the visitor reads a result
    Then the same sections are shown in the same order, with no fact that appears only on one size
