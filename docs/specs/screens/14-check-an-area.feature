@screen @buying @renting
Feature: Check an area
  Question it answers: "What is around this postcode?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: home WALES-1 (outside England); inputs: area record "WALES-1-AREA-SCHOOL-1";
    the postcode-level sample area data, `packages/fixtures/data/postcode-area.json`
    (NB1 4XY normal, NB7 1RR sparse and failed flood, NB9 9ZZ unknown); figures: none.
  Route: /area#postcode=… (the postcode lives in the URL fragment, never the query string, so it
    never reaches a server, application or hosting log of ours; decisions 0014 and 0046). The one
    exception is an outbound link the visitor clicks, which may carry the postcode to that site and
    says so (register line FE-11).
  Reuses the Nearby topic summary and topic details (04-nearby.feature), without the commute row.
  A topic's detail opens as a bottom sheet on a phone and a side panel on desktop, never a separate
    page (register line FE-20), and the open topic is linkable through the same "#" part as the postcode.
  Layering (register line FE-26): one thing at a time on the right column or the phone screen; the rule
    is written once in the site plan (.design/prototype/INFORMATION_ARCHITECTURE.md, "Layering").
  Words for gaps and states: the site plan's vocabulary table (P1, 14 Nov 2026): "Unavailable" (we hold
    no current copy of a source), "Couldn't load this" (the visitor's request to us failed), "No record
    in this source", "No <place> found within <radius>", "Old", "Not yet covered".
  Changed 14 Nov 2026 (FE-33, DA-12): on the page, a fact shows only its source's icon, name and link, with
    no status word and no date; a fact whose source is unavailable says "Not known right now" in its own
    text. About the data shows each source's link and the date of the data we hold, with no status word
    (founder, 14 Nov 2026: "Dates only, no notes"); a source we hold no current copy of says "We hold no
    current copy" instead of a date (AREA-25); the stored data, the area tools and our chat's grounding keep
    the Cached, Old and Unavailable labels (area-tools.feature).
  Changed 14 Nov 2026 (FE-34, FE-24): each source's method, limits and coverage live on one general About
    the data page, the same for every postcode (AREA-25); each result ends with a short "How we got this"
    note with one line per topic and a link to that page (AREA-27).
  Required states (doc 03 §5, the information architecture's "Check an area" and AGENTS.md rule 7):
    the postcode never reaches a log (decisions 0014, 0046) -> AREA-03, AREA-15
    an outbound link says where it goes and whether it carries the postcode (FE-11) -> AREA-18
    loading -> AREA-06
    invalid format -> AREA-04
    postcode not found, never shown as empty topics -> AREA-05
    our stored copy of a source is missing or failed, not shown as a clean result -> AREA-07, AREA-14
    the visitor's own request to us failed, a different state with Try again -> AREA-19
    flood warnings: the Environment Agency stamp as the official warnings link, the check time on the row but no label; About the data always shows the time we last checked (after 1 hour the copy is labelled Old in the data only, not on the page), and after 1 day the row says "Not known right now" -> AREA-21, AREA-22, AREA-23, AREA-25
    a fact's stamp is its source's icon, name and link, with no status word and no date -> AREA-26
    the printout: the sample postcode says "Sample data", any other postcode its made-at time -> AREA-12, AREA-20
    distances in England: metres under 1 mile, miles from 1 mile, stored in metres -> AREA-24
    an address in Wales, Scotland or Northern Ireland, "not yet covered" -> AREA-01, AREA-02, AREA-08
    narrow and mobile layouts with a list alternative to the map -> covered by NEAR-11 (same topic details; a sheet on a phone, FE-20)
    a short "How we got this" at the bottom of the result, with one line per topic and a link to About the data, where each topic's method and limits are -> AREA-27
    the postcode service down, never "not found" -> AREA-28
    the area check's request limit reached -> AREA-29
    offline -> AREA-30
    every source unavailable, the rows stay, one line to About the data -> AREA-31, AREA-34
    a search that crosses the border, places across it may be missing (B9) -> AREA-32, AREA-35
    a sparse area, the map opens on its places, the outer ring labelled with the search distance (FE-42) -> AREA-33, AREA-36
    (each of these states gives its cause, a line of reassurance and one action, B22)
  Free and paid: the area check is free and needs no account. Saving a home needs an account that
    doesn't exist yet, so it appears only as "Coming next · not available yet" (AREA-11; decision 0046).

  # Home "WALES-1" still stands in for a postcode outside England: postcode-area.json is England only (rule 6).
  Scenario: AREA-01 a postcode outside England is not yet covered
    Then home "WALES-1" has coverage "not-yet-covered"

  Scenario: AREA-02 a not covered topic has nothing to show
    Then area record "WALES-1-AREA-SCHOOL-1" has status "not-covered"
    And area record "WALES-1-AREA-SCHOOL-1" shows no value

  @ui
  Scenario: AREA-03 the postcode stays out of the query string
    Given the user is on Check an area
    When the user checks a complete postcode
    Then the address bar shows the postcode after "#postcode=", and the query string holds no postcode

  @ui
  Scenario: AREA-04 an incomplete postcode is not searched
    Given the user is on Check an area
    When the user checks an incomplete postcode
    Then an inline message under the "Postcode" field explains the format, and no search is made

  # fixture: packages/fixtures/data/postcode-area.json (NB9 9ZZ, the unknown postcode)
  @ui
  Scenario: AREA-05 an unknown postcode shows only that it wasn't found
    Given the user is on Check an area
    When the user checks a well-formed postcode that the sample data doesn't know
    Then "We couldn't find that postcode" is shown, and no topic is shown

  @ui
  Scenario: AREA-06 topics load as skeletons, never as empty rows
    Given the user is on Check an area
    When the user checks a complete postcode and the results are still loading
    Then each topic shows a loading skeleton, and no topic shows as empty

  @ui
  # Changed 14 Nov 2026 (FE-33, DA-12): the row says "Not known right now" in its own text; About the data shows no status word, only "We hold no current copy" in place of a date.
  Scenario: AREA-07 a source we hold no current copy of says it is not known right now and the rest still shows
    Given the user is on Check an area
    When the user checks a complete postcode and our stored copy of one topic's source is missing or failed to load
    Then that topic shows "Not known right now" with "We don't hold a current copy of this source", its official link where one exists and no "Try again", and the other topics still show

  # Corrected 14 Nov 2026 (C3 of the pilot design review): the pilot reads only our stored copies, never
  # a source live, so asking again cannot change the result until our next refresh.
  @ui
  Scenario: AREA-19 a request to our own service that fails offers Try again
    Given the user is on Check an area
    When the user checks a complete postcode and the request to our service fails (network or our API down)
    Then the page shows "Couldn't load this · Try again", never "We couldn't find that postcode" and never an empty or clean result

  @ui
  Scenario: AREA-08 outside England shows a not yet covered card
    Given the user is on Check an area
    When the user checks the postcode of home "WALES-1"
    Then a "Not yet covered" card is shown on Check an area with the postcode still only after "#postcode=", and no topic is shown as empty

  @ui
  Scenario: AREA-09 the map's centre pin is the postcode centre
    Given the user has checked a complete postcode
    When the user opens the map view
    Then the centre pin is labelled "Postcode centre", and no address pin is shown

  @ui
  Scenario: AREA-10 there is no commute row
    Given the user is on Check an area
    When the user checks a complete postcode
    Then the topic summary has no commute row

  @ui
  Scenario: AREA-11 saving a home is only described, never offered
    Given the user has checked a complete postcode
    When the results are shown
    Then saving a home, and tracking questions and answers per home, appear only in a "Coming next · not available yet" panel, with no active button

  @ui
  # Changed 14 Nov 2026 (FE-33): the closing page gives each source's date and no status word.
  Scenario: AREA-12 the printout of the example postcode keeps every topic, including gaps, and says "Sample data"
    Given the user has checked the example sample postcode and one topic has no current copy
    When the user chooses "Print or save as PDF"
    Then the print page lists every topic with its source's name, the topic with no copy prints as "Not known right now", the closing "How we got this" page gives each source's data date, with no status word, and the header says "Sample data"

  # Split 14 Nov 2026 (C5): real postcodes are real data, so "Sample data" belongs only to the example.
  @ui
  # Changed 14 Nov 2026 (FE-33): the closing page gives each source's date and no status word.
  Scenario: AREA-20 the printout of any other postcode shows when it was made, not "Sample data"
    Given the user has checked a postcode that is not the example and one topic has no current copy
    When the user chooses "Print or save as PDF"
    Then the print page header shows the time the report was made, each topic shows its source's name, the topic with no copy prints as "Not known right now", the closing "How we got this" page gives each source's data date, with no status word, and nothing says "Sample data"

  @ui
  Scenario: AREA-16 a not covered postcode prints as not covered
    Given the user has checked the postcode of home "WALES-1"
    When the user chooses "Print or save as PDF"
    Then the print page shows "Not yet covered" and leaves nothing out

  @ui
  Scenario: AREA-17 the printout is made in the browser
    Given the user has checked a complete postcode
    When the user chooses "Print or save as PDF"
    Then the print page is made in the browser, and no request is sent that carries the postcode

  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY, distanceMethod from the postcode centre)
  @ui
  Scenario: AREA-13 distances are measured from the postcode centre
    Given the user has checked a sample postcode
    When the results are shown
    Then every distance comes from the postcode-level sample data, measured from the postcode centre, not from a home

  # Units follow the country (register line FE-27, 14 Nov 2026): stored values stay in metres; the display
  # unit comes from the country entry in the data contract. Crime stays police.uk's own "within 1 mile".
  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY under 1 mile; NB7 1RR from 1 mile)
  @ui
  Scenario: AREA-24 in England distances show in metres under 1 mile and in miles from 1 mile
    Given the user has checked a sample postcode in England
    When the results are shown
    Then a distance that rounds to under 1,610 m reads in metres rounded to the nearest 10 m, like "120 m" or "1,450 m"
    And a distance of 1,605 to 1,609 m reads "1.0 miles", because the unit is chosen from the rounded value (FE-27 amended)
    And a distance of 1 mile or more reads in miles to one decimal, like "1.3 miles"
    And crime reads "within 1 mile", the stored values are in metres, and no distance is shown in kilometres

  # fixture: packages/fixtures/data/postcode-area.json (NB7 1RR NB7-1RR-AREA-FLOOD-1, source-failed)
  @ui
  Scenario: AREA-14 a missing flood copy is not the same as no warning
    Given the user is on Check an area
    When the user checks a complete postcode and we hold no current copy of the flood warnings
    Then the flood topic shows "Not known right now", "We don't hold a current copy of this source", the link "Check GOV.UK flood warnings ↗" (DA-12's one exception, since there is no source stamp to tap) and "This is not the same as no warning", with no "Try again" and no status word or date on the row

  # Flood warnings (register line DA-12, 14 Nov 2026). The Environment Agency says its flood data is updated
  # every 15 minutes, gives no service-level guarantee and is not for safety-critical use
  # (https://environment.data.gov.uk/flood-monitoring/doc/reference, read 14 Nov 2026). The 1 hour and
  # 1 day limits below are the founder's accepted default, not an Environment Agency rule.
  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY NB1-4XY-AREA-FLOOD-1; the test sets the clock against checkedAt (AREA-22, AREA-23))
  @ui
  # Changed 14 Nov 2026 (FE-33, DA-12): no status label on the flood row (founder: "No exceptions"); About the data shows it (AREA-25).
  # Changed again 14 Nov 2026 (DA-12): the flood row keeps its check time (founder: "keep time for the flood"); its limit sits in the page's one "How we got this" (FE-34).
  # Changed 14 Nov 2026 (FE-34, one per page): "This is not a flood risk check" is in the page's "How we got this" section, not under the flood topic.
  Scenario: AREA-21 the flood row's official warnings link is its source stamp, with the check time but no label
    Given the user is on Check an area and our flood copy was refreshed within the last hour
    When the user views the flood row
    Then it shows the warnings in force "when we last checked, at <time>", its official warnings link is the Environment Agency source stamp (DA-12: no separate GOV.UK warnings link), no status word, and the word "live" and any "clear" or "safe" label are not shown
    And when our copy holds no warning for the area, the row says "No flood warnings right now (when we last checked, at <time>)" followed in the same fact by the link "Long-term flood risk ↗" (FE-25; founder, 14 Nov 2026: "Say it in the fact (Recommended)", so the fact cannot read as an all-clear), and "This is not a flood risk check" sits in the short "How we got this" note at the bottom of the result, with no "How we got this" under the flood topic itself (FE-34)

  @ui
  # Changed 14 Nov 2026 (FE-33, DA-12): the check time is on About the data, with no "Old" word (founder: "Dates only, no notes").
  Scenario: AREA-22 a flood copy over 1 hour old shows its last-checked time on About the data
    Given our flood copy is more than 1 hour old and less than 1 day old
    When the user views the flood row and then About the data
    Then the flood row still shows the source's icon, name and link and "when we last checked, at <time>", but no label, and About the data shows the flood source with the time we last checked and no status word

  @ui
  # Changed 14 Nov 2026 (FE-33, DA-12): the row says "Not known right now" in its own text; About the data shows the time we last checked, with no "Unavailable" word.
  Scenario: AREA-23 a flood copy over 1 day old makes the row say "Not known right now"
    Given our flood copy is more than 1 day old
    When the user views the flood row and then About the data
    Then the row shows "Not known right now" and "This is not the same as no warning", no warning status from the old copy is shown, and About the data shows the flood source with the time we last checked and no status word

  # Added 14 Nov 2026 (FE-33, DA-12): where the source date now lives.
  # Changed 14 Nov 2026 (FE-33, FE-34 amended): dates only, no status words; one general page the same for every postcode, as topic rows that open to each topic's method, limits and coverage.
  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY and NB7 1RR, sources with dates and statuses)
  @ui
  Scenario: AREA-25 About the data lists every source with its link and date, and no status words
    Given the user is on Check an area and has checked a postcode
    When the user opens About the data
    Then About the data is one general page, the same for every postcode, listing every source the area check uses as a topic row with its icon, name, official link and the date of the data we hold, and no status word (Cached, Fallback, Old or Unavailable)
    And a source we hold no current copy of says "We hold no current copy" instead of a date, and the flood source shows when we last checked
    And each row opens to that topic's method, what it can't tell you and its coverage, and "How At a glance is counted" and "How priorities are checked" are rows at the top

  # Added 14 Nov 2026 (FE-33): the stamp on a fact.
  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY)
  @ui
  Scenario: AREA-26 a fact's source stamp is the source's icon, name and link only
    Given the user is on Check an area and has checked a postcode
    When the user looks at the source on any fact
    Then it shows the source's icon, its name and a "↗" mark and is a link to the official page, with no status word (Cached, Old, Unavailable or Fallback) and no date

  @ui
  Scenario: AREA-15 no request carries the postcode in its address
    Given the user is on Check an area
    When the user checks a complete postcode
    Then no request the page makes by itself carries the postcode in its URL path or query string

  @ui
  Scenario: AREA-18 an outbound link says where it goes and that it carries the postcode
    Given the user is on Check an area
    When the user checks a complete postcode
    Then each outbound link that carries the postcode names its site and says that site will see the postcode
    And no outbound link sends a referrer, and nothing is sent until the user clicks it

  # Added 14 Nov 2026 (FE-34, one per page).
  # Changed 14 Nov 2026 (FE-34, FE-24 amended; founder: "General page + short note (Recommended)" and "I pick B but add the icons"): the section is a short note, not every topic's method and limits.
  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY)
  @ui
  Scenario: AREA-27 the postcode result ends with a short "How we got this" and a link to About the data
    Given the user has checked a sample postcode in England
    When the results are shown
    Then no topic carries its own "How we got this", each topic ends with its source links only
    And a short "How we got this" sits at the bottom of the result, reachable by keyboard, with a short paragraph on what is specific to this search (distances are straight-line from the centre of this postcode, when flood warnings were last checked and that this is not a flood risk check, the wider areas some figures are published for, that counts and priority results come from tested rules and never AI, and a sample-data note where relevant)
    And it then shows one line per topic with its icon, name and source links (route-only topics show their official link), and the link "How each source works and what it can't tell you: About the data →"

  # Added 14 Nov 2026 (first design batch, B22): each state below gives its cause, a line of reassurance and one action.
  @ui
  Scenario: AREA-28 when the postcode service is down the page says so and offers Try again
    Given the user is on Check an area
    When the user checks a complete postcode and the postcode lookup service is not responding
    Then the page says the postcode lookup service isn't responding and that nothing is wrong with the postcode, offers "Try again", and does not say "We couldn't find that postcode"

  @ui
  Scenario: AREA-29 when the area check's request limit is reached the page says to try again in a minute
    Given the user is on Check an area
    When the user checks a postcode after the area check's request limit for them has been reached
    Then the page says too many checks have been made, that results already shown stay on screen and checks open again shortly, and offers one action, "Try again in a minute", as on the approved states board, with no topic shown as empty

  @ui
  Scenario: AREA-30 offline shows that the connection is down and keeps what is already on the page
    Given the user has checked a complete postcode and the results are shown
    When the device goes offline
    Then the page says the connection is down and offers "Try again" for when it is back, and the results already shown stay on the page unchanged

  # fixture: packages/fixtures/data/postcode-area.json (the test makes every source unavailable)
  @ui
  Scenario: AREA-31 when every source is unavailable the rows stay and each says it is not known right now
    Given the user is on Check an area
    When the user checks a complete postcode and we hold no current copy of any source
    Then every topic row stays, each says "Not known right now", and no row reads as empty, zero or a clean result

  @ui
  Scenario: AREA-34 when every source is unavailable one line points to About the data
    Given the user is on Check an area
    When the user checks a complete postcode and we hold no current copy of any source
    Then one line above the rows points to About the data, as the single action, and no "Try again" is offered, because asking again cannot change our stored copies

  # fixture still to add: no postcode in `postcode-area.json` crosses a border yet, and there is no data step for it; until a border fixture exists the scenario is @ui only (B9, `docs/reviews/2026-11-14-pilot-design-review.md`).
  # B9 fixes that places beyond the border may be missing; the wording and the one action are from the approved states board (canvas version 178).
  @ui
  Scenario: AREA-32 a search that crosses the border says places across it may be missing
    Given the user is on Check an area
    When the user checks a postcode whose search area crosses into another nation
    Then a notice says the search reaches into another nation, that places beyond the border may be missing from this search (B9), that the places found in England are still shown, and offers one action, the link "What England-only means", as on the approved states board

  @ui
  Scenario: AREA-35 a search that crosses the border leaves no topic reading as a clean result
    Given the user is on Check an area
    When the user checks a postcode whose search area crosses into another nation
    Then no topic reads as a clean result because of the border, and a topic with nothing found does not read as none exist

  # fixture: packages/fixtures/generated/area-result.json (NB7 1RR)
  @ui
  Scenario: AREA-33 a sparse area opens the map zoomed to its places
    Given the user has checked the sample postcode "NB7 1RR"
    When the user opens the map view
    Then the map opens zoomed to the places the data holds for that postcode

  # The distance is not in `area-result.json`: it is the search limit `SEARCH_LIMIT_METRES` in `packages/vestagraph-area/src/vestagraph_area/priorities.py`, shown in the display unit, miles, by `vestagraph_area.distance.display_distance` (FE-42).
  @ui
  Scenario: AREA-36 the outer ring is labelled with the search distance
    Given the user has checked the sample postcode "NB7 1RR"
    When the user opens the map view
    Then the outer ring is labelled with the search distance, quoted from the source named above and never typed here
