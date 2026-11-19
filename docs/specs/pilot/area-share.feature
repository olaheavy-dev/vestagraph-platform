@screen @buying @renting
Feature: Share a link and Recent postcodes (on an area result, compare and the landing)
  Question it answers: "Can I send this result to someone, and can this device remember the postcodes I looked at, only if I choose?"
  Modes: both (and anyone, with no account; decisions 0014 and 0046)
  Added 19 Nov 2026 (pilot design batch, PR 1; design `docs/superpowers/specs/2026-11-19-pilot-design-batch-design.md`, sections "2. Share a link" and "3. Recent postcodes"; plan Task 2; decisions 0014, 0053; register lines FE-05, FE-22, FE-73, PD-21; pilot design `2026-11-13-pilot-area-ai-design.md` goal 7). The council versions are `city-explorer-part-2.feature` (Share, CITY2-30 to CITY2-32; "Remember councils on this device", CITY2-46 onward); this feature mirrors their patterns with their own, separate setting. Compare's own Share this comparison is COMPARE-29 to COMPARE-31 in `area-compare.feature`. The landing's Recent postcodes is LAND-22 onwards in `screens/01-landing.feature`.
  Fixtures: none needed. Every scenario is a behaviour of the page or the browser, so every scenario is `@ui`; the postcodes quoted are the sample postcodes NB1 4XY and NB7 1RR (`packages/fixtures/data/postcode-area.json`). No figure is typed or shown (AGENTS.md rule 2).
  Rule 1 and 5 (PECR, 0014): nothing is stored on the visitor's device until they turn Recent postcodes on. The setting is its own consent, because each purpose is its own PECR consent; it is not shared with "Remember councils on this device".
  Boards: drawn in plan Task 3 (canvas section 'Pilot 8 · Compare, share, report'): the area result's header with Share (phone share sheet note, desktop "Link copied", the copy-failed state) and the Recent postcodes panel in its states on the landing and the area result.
  Wording status: nothing here is drawn on a board yet, so all wording below that the design does not quote is proposed, for the founder's copy review before build. Quoted from the design (approved 19 Nov 2026): "Share", "Link copied", "Couldn't copy. Here's the link to copy yourself", "Remember postcodes on this device", "Turn on", "Clear" and "Turn off". Proposed: the consent text (RECENT-02), the "On" and "Off" lines (RECENT-02, RECENT-05), the "Cleared" lines (RECENT-08) and the unavailable-storage line (RECENT-10).
  No sample record is needed for any state here, so no `noticed` issue is open for this feature.

  Required states (design "States to cover"; AGENTS.md rules 1 and 5; PECR):
    Share: share sheet on a phone -> SHARE-01; copied on desktop -> SHARE-02; copy failed with the link shown and selected -> SHARE-03; only the postcode in the link -> SHARE-04, SHARE-05; opening a shared link -> SHARE-06, SHARE-07
    Recent postcodes: off by default -> RECENT-01, RECENT-02; on and empty -> RECENT-04; on with entries (up to 5, newest first) -> RECENT-05, RECENT-06; postcodes added from a check, compare and a shared link -> RECENT-07; cleared -> RECENT-08; older than 12 months dropped -> RECENT-14; turned off -> RECENT-09; storage unavailable -> RECENT-10; never sent to us -> RECENT-11; separate from councils -> RECENT-12; keyboard, size, dark twin -> RECENT-13

  # ---- Share a link (design section 2) ----

  @ui
  Scenario: SHARE-01 on a phone Share opens the device's share sheet
    Given the result for "NB1 4XY" is open on a phone that offers a share sheet
    When the visitor chooses "Share" in the result's header
    Then the device's share sheet opens with the link to the result
    And no account is needed, and nothing is stored or logged to make the link

  @ui
  Scenario: SHARE-02 on desktop Share copies the link and says "Link copied"
    Given the result for "NB1 4XY" is open on a desktop with no share sheet
    When the visitor chooses "Share" in the result's header
    Then the link is copied and the control says "Link copied", announced to a screen reader
    And the message goes away on its own, and no other control moves

  @ui
  Scenario: SHARE-03 if copying fails, the link is shown and selected for the visitor to copy
    Given the result for "NB1 4XY" is open and the browser refuses the copy
    When the visitor chooses "Share"
    Then the page says "Couldn't copy. Here's the link to copy yourself" with the link shown in a field and selected
    And "Link copied" is not shown

  @ui
  Scenario: SHARE-04 the shared link carries the postcode after the # and nothing else
    Given the visitor has set limits, opened a topic and picked display settings on the result for "NB1 4XY"
    When the visitor shares the result
    Then the link holds the postcode after the "#" only (goal 7 of the pilot design), as AREA-03 sets
    And it holds no limit (PRIO-16), no display setting and no open topic

  @ui
  Scenario: SHARE-05 the shared link never has a query string
    Given the visitor shares the result for "NB1 4XY"
    When the visitor reads the link
    Then the query string is empty, so the postcode never reaches a server log or analytics (0014, 0053)

  @ui
  Scenario: SHARE-06 opening a shared link runs the search as if the postcode had been typed
    Given the visitor opens a shared link holding "NB1 4XY"
    When the page has loaded
    Then the result for "NB1 4XY" is shown as if typed, with the same loading, not found and not covered states as a typed search (AREA-05, AREA-06, AREA-08)
    And nothing about the visit is stored or logged, except the Recent postcodes list when the visitor has turned it on (RECENT-07)

  @ui
  Scenario: SHARE-07 a shared link with spaces, lower case or an incomplete postcode is handled as typed
    Given the visitor opens a shared link holding "nb1 4xy"
    When the page has loaded
    Then the result for "NB1 4XY" is shown, as if the postcode had been typed with that case and spacing
    And a link holding an incomplete postcode shows the message of AREA-04 and makes no search

  # ---- Recent postcodes (design section 3) ----

  @ui
  Scenario: RECENT-01 nothing is stored while Recent postcodes is off, and it is off by default
    Given a visitor who has never turned Recent postcodes on
    When the visitor checks "NB1 4XY" and "NB7 1RR"
    Then no postcode is written to the browser, and the list is not shown
    And no record of the check is sent to us for this purpose

  @ui
  Scenario: RECENT-02 under the search box the setting is named and can be turned on
    Given the landing or the result for "NB1 4XY" is open and the setting is off
    When the visitor reads under the search box
    Then it says "Remember postcodes on this device" with the action "Turn on" and "Nothing is kept while this is off." (proposed wording)
    And the consent text reads "This keeps a short list of the postcodes you check, so you can open them again. It is a short browsing history. It stays in this browser and is never sent to us. Anyone using this device can see it. It is kept until you clear it, at most 12 months. Turning this off clears it." (proposed wording, mirroring City Explorer's consent text, CITY2-46; the 12 months are the founder's decision, 19 Nov 2026, SE-08)

  @ui
  Scenario: RECENT-03 turning it on asks nothing else and starts the list empty
    Given the setting is off
    When the visitor chooses "Turn on"
    Then the setting is on, with nothing in the list yet, and no postcode already checked is added
    And the search still works exactly as before

  @ui
  Scenario: RECENT-04 on with nothing kept says so
    Given the setting is on and no postcode has been checked since
    When the visitor reads the setting
    Then it says "On. Postcodes are kept until you clear them, at most 12 months, and only on this device." and that nothing is kept yet, and "Postcodes you check from now on are listed here." (proposed wording, as CITY2-50), with "Turn off" available
    And no empty list or "0" is shown as a result

  @ui
  Scenario: RECENT-05 on, the list shows up to 5 postcodes, newest first, each a link
    Given the setting is on and the visitor has checked 6 different postcodes, the sixth last
    When the visitor reads the list
    Then it shows the 5 most recent, newest first, and the oldest is dropped, each postcode a link that opens its result
    And a postcode checked again moves to the top and is not listed twice

  @ui
  Scenario: RECENT-06 a postcode on the list opens its result as if typed and sends nothing extra
    Given the setting is on and "NB7 1RR" is on the list
    When the visitor chooses "NB7 1RR"
    Then the result for "NB7 1RR" opens as a typed search would (SHARE-06), with the postcode after the "#" only
    And the list is read from the browser, not asked of a server

  @ui
  Scenario: RECENT-07 postcodes checked, entered on compare or opened from a shared link are added while it is on
    Given the setting is on
    When the visitor checks "NB1 4XY", compares "NB1 4XY" with "NB7 1RR" and opens a shared link holding another postcode
    Then each postcode is added once, newest first, and a postcode that is not found or outside England is not added (agent's call, open to the founder: a postcode with no result is not worth opening again)
    And with the setting off none of these is kept (RECENT-01)

  @ui
  Scenario: RECENT-08 Clear deletes the list at once and the setting stays on
    Given the setting is on and a list is kept
    When the visitor chooses "Clear"
    Then the list is deleted from the browser and the page says "Cleared. The list of postcodes is deleted from this device." and "Still on, with nothing kept." (proposed wording)
    And "Turn off" is still available

  @ui
  Scenario: RECENT-09 turning it off deletes the list and the setting
    Given the setting is on and a list is kept
    When the visitor chooses "Turn off"
    Then the list and the setting are both deleted from the browser, and the page is back to "Nothing is kept while this is off."
    And nothing is left to be read later, including the fact that the setting was ever on

  @ui
  Scenario: RECENT-10 if browser storage is unavailable the setting says it can't be turned on here, and the search still works
    Given a private window or a browser that blocks storage
    When the visitor chooses "Turn on", or reads the setting
    Then it says "This can’t be turned on here: your browser isn’t allowing Vestagraph to keep anything on this device." (proposed wording) and no list is shown
    And the postcode search, Share and compare all still work, and no error report is raised

  @ui
  Scenario: RECENT-11 the list is only in the browser and never sent to us
    Given the setting is on and a list is kept
    When the visitor checks another postcode
    Then the list is not in any request, header, cookie, log, error report or analytics event, and the postcode being checked travels in the request body only (0014, 0053)
    And the privacy page names Recent postcodes and says where the list is kept (SE-07; written in the public pages batch)

  @ui
  Scenario: RECENT-12 Recent postcodes is its own setting, separate from Remember councils on this device
    Given the visitor has turned on "Remember councils on this device" (CITY2-46 onward)
    When the visitor reads the Recent postcodes setting
    Then Recent postcodes is still off, and turning one on or off does not turn the other on, off or clear its list
    And each setting has its own consent text, because each purpose is its own PECR consent

  @ui
  Scenario: RECENT-13 Recent postcodes works by keyboard, with 44 px targets, and has a dark twin
    Given the visitor has opened the landing and the result on a phone and on desktop
    When the visitor works through the setting and the list by keyboard
    Then every control (Turn on, a listed postcode, Clear, Turn off) can be reached and used, each at least 44 px tall, with the focus visible, and nothing scrolls sideways at 390 px
    And the dark twin shows the same states in WCAG 2.2 AA contrast

  # Founder's decision, 19 Nov 2026 (prompt window, "12 months, like councils (Recommended)", register line SE-08): the list has the same limit as City Explorer's (CITY2-54).
  @ui
  Scenario: RECENT-14 entries older than 12 months are dropped, and nothing is ever sent to us
    Given the setting is on and a postcode was added more than 12 months ago
    When the visitor opens the landing or a result
    Then that postcode is dropped from the list and from the browser, and no list or postcode has been sent to us, in a request, a log or analytics
    And the consent text says the list is on this device, anyone using it can see it, and it is kept until cleared, at most 12 months (RECENT-02)
