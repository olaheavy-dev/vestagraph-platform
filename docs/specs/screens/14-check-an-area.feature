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
    current copy" instead of a date (AREA-25); the stored data, the area tools (and the later workspace chat's grounding) keep
    the Cached, Old and Unavailable labels (area-tools.feature).
  Changed 14 Nov 2026 (FE-34, FE-24): each source's method, limits and coverage live on one general About
    the data page, the same for every postcode (AREA-25); each result ends with a short "How we got this"
    note with one line per topic and a link to that page (AREA-27).
  Changed 16 Nov 2026 (the benchmark design pass, canvas version 405, plan
    docs/superpowers/plans/2026-11-16-benchmark-design-pass.md, Tasks 3 to 7; FE-26 dated note, FE-68, FE-69, DA-22 to
    DA-31): the desktop result has a place header with the map, At a glance as a row of facts, a jump row and a right
    column (AREA-37 to AREA-43); the new topics, their rows and the Check this rows are in `area-topics.feature`
    (TOPIC-26 to TOPIC-40); every map keeps FE-42's 3D style and the Map screen adds a flat 2D map with layers
    (`area-map.feature`, MAP-14 to MAP-26); the printout is `area-printout.feature` (PRINT-01 to PRINT-20); About the
    data and the NB7 1RR states are AREA-44 to AREA-47. FE-69's short list of proposed wording was approved on 18 Nov 2026
    (founder, "Approve as written (Recommended)"), so no wording here is still proposed.
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
    the "Ask about this area" entry with its AI badge and an active Save for the area, leading signed-out visitors to sign-in (0058) -> AUTH-15, AUTH-16, AUTH-17, AUTH-26 (sign-in.feature)
    the desktop result: place header with the map, At a glance as a row of facts, the counts line, the jump row, the right column, and an opened topic in place of the right column (FE-26, 16 Nov 2026) -> AREA-37 to AREA-43
    the place header's "About <council>" link to City Explorer -> AREA-48; About the data and City Explorer's own sources -> AREA-49
    About the data's entry for the energy certificate register -> AREA-50
    About the data with the design pass's new sources, dates only -> AREA-44, AREA-45
    the sparse area's gaps and not-known rows for radon, broadband coverage and council rent -> AREA-46, AREA-47 (radon: TOPIC-29; questions: GLANCE-04)
    (each of these states gives its cause, a line of reassurance and one action, B22)
  Free and paid: the area check is free and needs no account. Saving a home needs an account that
    doesn't exist yet, so it appears only as "Coming next · not available yet" (AREA-11; decision 0046).
    16 Nov 2026 (0058): saving an area is live: Save on the result and "Ask about this area" lead signed-out
    visitors to sign-in and back (AUTH-15 to AUTH-17, AUTH-26); saving a home still waits.

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
  # Changed 16 Nov 2026 (design pass, FE-21): the printout is now a cover, At a glance, every topic and a Sources and credits page; its full specification is `area-printout.feature` (PRINT-01 to PRINT-20). This scenario keeps the example postcode's "Sample data" header and the "Not known right now" rule.
  Scenario: AREA-12 the printout of the example postcode keeps every topic, including gaps, and says "Sample data"
    Given the user has checked the example sample postcode and one topic has no current copy
    When the user chooses "Print or save as PDF"
    Then the print page lists every topic with its source's name, the topic with no copy prints as "Not known right now", the "How we got this" pages give each topic's method and limits, the closing "Sources and credits" page gives each source's data date, with no status word, and the header says "Sample data"

  # Split 14 Nov 2026 (C5): real postcodes are real data, so "Sample data" belongs only to the example.
  @ui
  # Changed 14 Nov 2026 (FE-33): the closing page gives each source's date and no status word.
  # Changed 16 Nov 2026 (design pass, FE-21): see PRINT-01 to PRINT-20; the cover's made-at time is PRINT-01.
  Scenario: AREA-20 the printout of any other postcode shows when it was made, not "Sample data"
    Given the user has checked a postcode that is not the example and one topic has no current copy
    When the user chooses "Print or save as PDF"
    Then the print page header shows the time the report was made, each topic shows its source's name, the topic with no copy prints as "Not known right now", the "How we got this" pages give each topic's method and limits, the closing "Sources and credits" page gives each source's data date, with no status word, and nothing says "Sample data"

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
  # Changed 16 Nov 2026 (FE-69, founder: "Approve, printout flood wording (Recommended)"): the sentence now reads "The warning check is not a flood risk check", so it is clear it is the warning check, not flood risk, that is meant.
  Scenario: AREA-21 the flood row's official warnings link is its source stamp, with the check time but no label
    Given the user is on Check an area and our flood copy was refreshed within the last hour
    When the user views the flood row
    Then it shows the warnings in force "when we last checked, at <time>", its official warnings link is the Environment Agency source stamp (DA-12: no separate GOV.UK warnings link), no status word, and the word "live" and any "clear" or "safe" label are not shown
    And when our copy holds no warning for the area, the row says "No flood warnings right now (when we last checked, at <time>)" followed in the same fact by the link "Long-term flood risk ↗" (FE-25; founder, 14 Nov 2026: "Say it in the fact (Recommended)", so the fact cannot read as an all-clear), and "The warning check is not a flood risk check" sits in the short "How we got this" note at the bottom of the result, with no "How we got this" under the flood topic itself (FE-34)

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
    # Changed 16 Nov 2026 (design pass): the rows now include the new sources, AREA-44.

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
    # Examples (FE-11; audit P3, 19 Nov 2026): "Open in Google Maps ↗" and "Satellite view ↗" each carry the postcode and each says "Google will see this postcode"
    And "Open in Google Maps ↗" and "Satellite view ↗" are two such links, each with "Google will see this postcode" beside it

  # Added 14 Nov 2026 (FE-34, one per page).
  # Changed 14 Nov 2026 (FE-34, FE-24 amended; founder: "General page + short note (Recommended)" and "I pick B but add the icons"): the section is a short note, not every topic's method and limits.
  # Changed 16 Nov 2026 (design pass): the note names the 1 km square for radon and says what the Check this rows are; the founder approved "The warning check is not a flood risk check" (FE-69), and the other added sentences were approved too on 18 Nov 2026 (FE-69, founder, "Approve as written (Recommended)"). The Check this rows are listed in the note with their official links.
  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY)
  @ui
  Scenario: AREA-27 the postcode result ends with a short "How we got this" and a link to About the data
    Given the user has checked a sample postcode in England
    When the results are shown
    Then no topic carries its own "How we got this", each topic ends with its source links only
    And a short "How we got this" sits at the bottom of the result, reachable by keyboard, with a short paragraph on what is specific to this search (distances are straight-line from the centre of this postcode, when flood warnings were last checked and that the warning check is not a flood risk check, the wider areas some figures are published for (the neighbourhood and the council area, and the 1 km square around the postcode for radon), that rows marked "Check this" link to an official service and this address has not been looked up there, that counts and priority results come from tested rules and never AI, and a sample-data note where relevant)
    And it then shows one line per topic with its icon, name and source links (route-only and "Check this" topics show their official link), and the link "How each source works and what it can't tell you: About the data →"

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

  # Added 16 Nov 2026 (design pass, Task 3 "As drawn", FE-26 dated note; board AreaResultDesktop).
  @ui
  Scenario: AREA-37 the desktop result opens with a place header holding the map
    Given the user has checked the sample postcode "NB1 4XY" on desktop
    When the results are shown
    Then the top of the page is a place header with the postcode, the area name and its level, the sample note "Sample data: a made-up town" and the places map
    And the postcode and area name are quoted from `postcode-area.json`, never typed
    And the map follows the area map rules in `area-map.feature` (MAP-01 to MAP-13) and stays in the header
    And no score, band or verdict appears in the header

  # Added 16 Nov 2026 (Task 3). Plan's acceptance: every big figure is quoted from `area-result.json` with its stamp (rule 2). The four figures are the nearest bus stop, the railway station, the nearest GP surgery and the primary school (the same records the priorities use, PRIO-01 and PRIO-02).
  # fixture: packages/fixtures/generated/area-result.json (NB1 4XY)
  Scenario: AREA-38 each big figure of At a glance has a recorded distance to quote
    Then area result "NB1 4XY" has a display distance for record "NB1-4XY-AREA-TRANSPORT-STOP-1"
    And area result "NB1 4XY" has a display distance for record "NB1-4XY-AREA-TRANSPORT-STOP-2"
    And area result "NB1 4XY" has a display distance for record "NB1-4XY-AREA-AMENITY-10"
    And area result "NB1 4XY" has a display distance for record "NB1-4XY-AREA-SCHOOL-1"

  @ui
  Scenario: AREA-39 on desktop At a glance is a row of facts, each with its level and source stamp
    Given the user has checked the sample postcode "NB1 4XY" on desktop
    When At a glance is shown
    Then it shows a row of facts, each a big figure with the place's name, its level ("From the postcode centre", DA-14) and its source stamp (the source's icon, name and ↗, FE-33)
    And each figure is the display distance quoted from `area-result.json` for the records named in AREA-38, in metres under 1 mile and in miles from 1 mile (FE-27)
    And no figure is a score, a band, a verdict or a total, and none is typed by hand

  # The counts line replaces the 3+1 grid on desktop (Task 3). Counts are quoted from `area-result.json` (`glance.found`, `glance.notKnown`, `glance.coverageFound`, `glance.coverageTotal` and the length of `glance.questions`); none is typed here (rule 2; GLANCE-06 is the phone layout).
  @ui
  Scenario: AREA-40 the desktop counts line shows found, not known and questions to ask
    Given the user has checked a sample postcode on desktop
    When At a glance is shown
    Then a compact line shows the found count, "Not known: <count> topics" and "Questions to ask: <count>", each quoted from `area-result.json`
    And a count of zero reads "None to list" and has no link (GLANCE-10)
    And a count above zero opens the list of its items (GLANCE-07)
    And the coverage line "<found> of <total> topics returned facts. Topics we don't cover yet are listed at the end, with official links." is quoted from `area-result.json`
    And "Things to check in person" shows no count (FE-41)

  @ui
  Scenario: AREA-41 the jump row links to every topic and to Questions to ask and Check in person
    Given the user has checked a sample postcode on desktop
    When the visitor looks at the "Jump to" row
    Then it lists "Questions to ask" and "Check in person" first, then every topic shown on the result in registry order of `pilot-topics.json` (the counted topics and the Family view), then "Not yet covered here"
    And choosing an item moves to that part of the page and moves focus to its heading
    And it can be reached and operated by keyboard

  # FE-26 dated note, 16 Nov 2026: "agent's call"; approved by the founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)").
  @ui
  Scenario: AREA-42 the right column under the map holds Check in person and the places
    Given the user has checked a sample postcode on desktop and no topic is open
    When the result is shown
    Then the right column holds "Check in person" (the fixed reviewed lists from `pilot-topics.json`, FE-39) and "Places on the map, nearest first" with each place's distance quoted from `area-result.json`
    And "Questions to ask" with its gap questions and "Ask about this area" and "What matters to you · Set priorities" sit in the left column
    And a filter that hides a kind of place says so in the list, for example "Police hidden by your filter"

  # Agent's call, approved by the founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)"; FE-26 dated note, Task 3 "As drawn"). If the founder later prefers the panel to open beside the list instead, this scenario is the one to change.
  @ui
  Scenario: AREA-43 on desktop an opened topic replaces the right column and the map stays in the header
    Given the user has checked a sample postcode on desktop and no topic is open
    When the visitor opens a topic
    Then the topic's panel takes the place of the right column (Check in person and the places)
    And the map stays in the place header
    And only one topic is open at a time (FE-26)
    And when the topic closes the right column returns with its previous state
    And focus moves to the panel's heading when it opens, and Escape closes it and returns focus to the row (TOPIC-03, TOPIC-15)

  # Added 16 Nov 2026 (Task 6b "As drawn", FE-33 dates only). Dates come from `postcode-area.json` and `map-layers.json`.
  # About the data's source label pattern and the short source name "BGS and UKHSA" were proposed wording, approved by the founder on 18 Nov 2026 (FE-69, "Approve as written (Recommended)").
  @ui
  Scenario: AREA-44 About the data lists the design pass's new sources with dates only
    Given the user is on Check an area and has opened About the data
    When the visitor looks at the new topic rows
    Then Radon lists its source (BGS and UKHSA radon atlas) with the data date of its edition, Broadband lists "Ofcom Connected Nations: postcode coverage" with its snapshot month, Housing affordability lists the ONS Price Index of Private Rents, Flood lists the EA Flood Map for Planning and the EA surface water map, Planning nearby lists "Planning Data Platform: planning applications, listed buildings, conservation areas", and Noise lists "Defra strategic noise maps, round 4" with the year it was modelled
    And every date is quoted from the records and layers named by ID in `postcode-area.json` and `map-layers.json`, and no status word is shown (FE-33)
    And the topics we link to only (council tax band of a home, mobile by network, ground and mining) read "We don't hold this yet" with their official link

  @ui
  # Changed 17 Nov 2026 (Codex review): About the data is the same for every postcode (FE-34, AREA-25), so it states the noise source's general coverage, not one postcode's result; the postcode-specific wording lives in TOPIC-38 and MAP-23. Wording proposed by the agent, approved by the founder on 18 Nov 2026 (FE-69, "Approve as written (Recommended)").
  Scenario: AREA-45 About the data describes the noise source in general and never says a gap means no noise
    Given the user is on Check an area and has opened About the data
    When the visitor opens "Noise"
    Then it reads "Road and rail noise are modelled map layers (2021, not measured). The source may have no record for a postcode; that does not mean there is no noise."
    And it names no postcode and no single result
    And it does not read "rail noise isn't in this source"

  # fixture: packages/fixtures/data/postcode-area.json (NB7 1RR); the counts are quoted from `area-result.json` (`glance`) and worked in `test-cases/area-glance.json` (DA-31 "As built"), never typed in a scenario. Radon's record and outcome are checked in TOPIC-29 and the gap questions in GLANCE-04.
  Scenario: AREA-46 the sparse postcode's broadband coverage and council rent have no record in the source
    Then postcode record "NB7-1RR-AREA-BROADBAND-COVERAGE-1" has status "no-record-in-source"
    And postcode record "NB7-1RR-AREA-COUNCIL-RENT-1" has status "no-record-in-source"
    And area result "NB7 1RR" has topic "broadband" with outcome "found"
    And area result "NB7 1RR" has topic "housing-affordability" with outcome "found"

  # The wording of the gap rows was approved by the founder on 18 Nov 2026 (FE-69, "the wording for the NB7 gaps"); the rows follow the approved states board's pattern.
  @ui
  Scenario: AREA-47 the sparse area's gaps page lists radon, broadband coverage and council rent without reading as a clean result
    Given the user has checked the sample postcode "NB7 1RR"
    When the visitor reads "Gaps on this page"
    Then Radon reads "Not known right now" with "We don't hold a current copy of this source."
    And Broadband reads "No broadband coverage figure for this postcode in this source"
    And Housing affordability has two gap rows: "No affordability ratio for this area in this source" and "No average private rent for this area in this source"
    And none of them reads as zero, none or a clean result (rule 7)

  # Added 17 Nov 2026 (City Explorer plan Task 14c; design `docs/superpowers/specs/2026-11-15-city-explorer-design.md`, "The way back": the area result links to its council's page, "About <council>"; decision 0055). The council comes from the postcode (`council-result.json` search: NB1 4XY leads to E06999001, checked in TOOLS-50). Not drawn on the desktop place header board (AreaResultDesktop shows the postcode and "Northbridge, England" with no link; the result's topic row has "See Northbridge in City Explorer →", TOPIC-33 in `area-topics.feature`, DA-29): the link is the design's, with wording "About" and the council's name, proposed by the agent and approved by the founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)").
  @ui
  Scenario: AREA-48 the desktop place header links to the council's City Explorer page
    Given the user has checked the sample postcode "NB1 4XY" on desktop
    When the user chooses the "About Northbridge (sample)" link in the place header
    Then the City Explorer page for council "E06999001" opens, and the council's name in the link is quoted from `council-area.json`, never typed
    And the postcode is not carried in the address (decision 0014)

  # City Explorer's own About the data (CouncilAboutData: its sources, editions and statuses) is fully specified in `city-explorer-part-2.feature`, CITY2-58 to CITY2-72, and is linked from "How we got this" on the council and neighbourhood pages (CITY2-71). This page's About the data stays the one general page of the area result (FE-34, AREA-25), so nothing is duplicated; the AboutData board lists no source that only City Explorer uses.
  @ui
  Scenario: AREA-49 City Explorer's sources are on City Explorer's About the data, not repeated here
    Given the user is on Check an area and has opened About the data
    When the visitor looks for the sources City Explorer shows for a council
    Then the page lists only the area result's topics with their sources and data dates, and a source that only City Explorer uses (CITY2-58 to CITY2-68) is described on City Explorer's own About the data, not on this page

  # The energy certificate register is a live lookup that keeps nothing (DA-09), so this entry carries no "Data from" date: there is no copy of the data to date. The board shows the line "We look this up when you ask and keep no copy" in its place (canvas version 413; unchanged at 414). The wording was approved by the founder on 19 Nov 2026 (copy review, "Approve as written (Recommended)"), copied from the AboutData board.
  @ui
  Scenario: AREA-50 About the data lists the energy certificate register, its licence and what it can't tell you
    Given the user is on Check an area and has opened About the data
    When the visitor reads the entry "Energy certificate register"
    Then it names the register and links to it with the source stamp "EPC register ↗" (the register's search page on GOV.UK, which carries no certificate number)
    And it gives the licence "Open Government Licence v3.0" and says the register's address and postcode are dropped when a certificate arrives and nothing is kept
    And under "What it can't tell you" it says a certificate can't tell you what your own bills will be, or what has changed in the home since it was made, and that its cost lines, improvements and savings are estimates, not bills and not quotes
    And the entry shows no "Data from" date, because Vestagraph holds no copy of this register's data, and says instead, in its approved line, "We look this up when you ask and keep no copy"
