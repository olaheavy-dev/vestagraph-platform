@screen @buying @renting
Feature: Nearby
  Question it answers: "Would daily life work?"
  Modes: both
  Fixtures: homes B1, R1, WALES-1; inputs: area records "R1-AREA-CRIME-2", "B1-AREA-FLOOD-1",
    "B1-AREA-SCHOOL-INSPECTION-1", "B1-AREA-AMENITY-6", "B1-AREA-COMMUTE-1", "WALES-1-AREA-FLOOD-1",
    household criterion "COMMUTE" (packages/fixtures/data/household.json); figures: none
    (Nearby shows recorded facts with distances from the fixtures, never calculated figures).
  Route: /homes/[slug]/nearby. Each topic's detail opens as a bottom sheet on a phone and a side panel on
    desktop, never a separate page, and the open topic is linkable through the "#" part (register line FE-20;
    corrected 14 Nov 2026, C1 of the pilot design review; .design/prototype/INFORMATION_ARCHITECTURE.md, "Nearby").
    One thing at a time on the right column or the phone screen: see "Layering" there (FE-26).
  Required states (doc 03 §5 and AGENTS.md rule 7):
    a source request that failed, not shown as a clean result -> NEAR-01, NEAR-07
    a source that does not cover the location -> NEAR-04, NEAR-10
    an address in Wales, Scotland or Northern Ireland, "not yet covered" -> NEAR-04, NEAR-10
    stale information: the row shows no label or source date, About the data shows each source's date and no status word (FE-33 amended 14 Nov 2026); a fact's own date, such as an inspection date, stays -> NEAR-03, NEAR-09
    missing never shown as zero or a favourable value -> NEAR-02, NEAR-05, NEAR-08
    narrow and mobile layouts with a list alternative to the map -> NEAR-11
    the limits on the general About the data page, never on a row, at the top of a sheet or under each topic; the result ends with a short "How we got this" note that links there -> NEAR-13
    basic/paid boundaries -> NEAR-16
    the "Ask about this area" entry on Nearby and Nearby > Schools, opening the chat (0063) -> NEAR-17
  Free and paid (doc 02 §8): the Nearby map and list with straight-line distances are free; routed
    travel times to the household's own destinations are paid (routing is a metered third-party
    cost), so the prototype shows them only as a labelled, simulated boundary (NEAR-16). Walking times
    from the postcode centre to nearby places (a self-hosted batch, pilot, DA-08) are free.

  Scenario: NEAR-01 a failed crime lookup is not shown as no crime
    Then area record "R1-AREA-CRIME-2" has status "source-failed"
    And area record "R1-AREA-CRIME-2" shows no value

  Scenario: NEAR-02 no flood record in the source is a gap, not a clean result
    Then area record "B1-AREA-FLOOD-1" has status "no-record-in-source"
    And area record "B1-AREA-FLOOD-1" shows no value

  Scenario: NEAR-03 a stale school inspection keeps its record
    Then area record "B1-AREA-SCHOOL-INSPECTION-1" has status "stale"

  Scenario: NEAR-04 a home in Wales is not yet covered
    Then home "WALES-1" has coverage "not-yet-covered"
    And area record "WALES-1-AREA-FLOOD-1" has status "not-covered"
    And area record "WALES-1-AREA-FLOOD-1" shows no value

  Scenario: NEAR-05 a missing childcare place is a gap
    Then area record "B1-AREA-AMENITY-6" has status "no-record-in-source"
    And area record "B1-AREA-AMENITY-6" shows no value

  @ui
  Scenario: NEAR-06 the page opens as one summary row per topic
    Given home "B1" is at story step 1
    When the user opens Nearby
    Then one row per topic shows its headline fact, and opening a row opens its sheet or panel, not a new page, in the order of the information architecture: your commute, getting around, everyday places, places of worship, schools, flood, recorded crime, sold nearby, planning nearby and broadband

  @ui
  # Changed 14 Nov 2026 (FE-33, DA-12): the row says "Not known right now" in its own text; About the data shows no status word.
  Scenario: NEAR-07 the failed crime topic says it is not known right now
    Given home "R1" is at story step 1
    When the user opens Nearby
    Then the recorded crime topic shows "Not known right now", "Couldn't fetch this time · Try again" and "This doesn't mean there's nothing to report" for "R1-AREA-CRIME-2"

  @ui
  # Changed 14 Nov 2026 (FE-34): the "doesn't tell you" note is no longer a visible line; it sits on the general About the data page (FE-34 amended 14 Nov 2026).
  Scenario: NEAR-08 the flood gap is never a reassuring label
    Given home "B1" is at story step 1
    When the user opens Nearby
    Then the flood topic shows the label of "B1-AREA-FLOOD-1" as recorded, with its long-term flood risk link, and no "no risk", "low risk" or "clear" label, and the recorded limit note is on the general About the data page, not under the flood topic

  @ui
  # Changed 14 Nov 2026 (FE-33, DA-12): the "Old" label is gone and the source date is on About the data (dates only); the inspection date is the fact itself and stays.
  Scenario: NEAR-09 the stale inspection shows its inspection date and no label
    Given home "B1" is at story step 1
    When the user opens the schools topic
    Then "B1-AREA-SCHOOL-INSPECTION-1" shows "Inspected <Month Year>" with its framework only on the general About the data page (FE-36), and its source stamp shows only the source's icon, name and link, with no "Old" label, no "Older inspection" badge (FE-35) and no source date

  @ui
  Scenario: NEAR-10 Wales shows one not yet covered card
    Given the user has opened the home "WALES-1"
    When the user opens Nearby
    Then one "Not yet covered" card is shown, and no topic is shown as empty

  @ui
  Scenario: NEAR-11 on a phone every topic has a list, and the map is optional
    Given home "B1" is at story step 1
    And the screen is 390 pixels wide
    When the user opens a topic
    Then the topic opens as a bottom sheet with a visible Close, it shows a list, and the map is a view the user can choose

  @ui
  Scenario: NEAR-12 crime is shown as counts and never on the map
    Given home "B1" is at story step 1
    When the user opens the recorded crime topic
    Then crime shows as counts by month and category, and the map shows no crime marker

  @ui
  # Changed 14 Nov 2026 (FE-34, replacing FE-28): the founder removed every visible limit line. The limits
  # live inside the page's one "How we got this" section (FE-24), closed by default, and on About the data.
  # Changed again 14 Nov 2026 (FE-34, one per page): topics no longer carry their own "How we got this".
  # Changed 14 Nov 2026 (FE-34, FE-24 amended; founder: "General page + short note (Recommended)"): the limits live on the general About the data page; the result keeps a short "How we got this" note with a link there.
  # Earlier change (M3, FE-28): the full note on every row made the list long again.
  Scenario: NEAR-13 what a topic doesn't tell you sits on the general About the data page
    Given home "B1" is at story step 1
    And the screen is 390 pixels wide
    When the user opens Nearby and then a topic
    Then no row and no sheet or panel top shows a limit line or a "What this doesn't tell you" note, no topic carries its own "How we got this", the result ends with a short "How we got this" note (one line per topic, with its icon, name and source links) and the link "How each source works and what it can't tell you: About the data →", and on About the data each topic row, opened by keyboard, shows its method, limits and coverage

  @ui
  Scenario: NEAR-14 the commute row gives no verdict
    Given home "B1" is at story step 1
    When the user opens Nearby
    Then the commute row shows "B1-AREA-COMMUTE-1" next to the household's criterion "COMMUTE", with no verdict

  # FE-25 (13 Nov 2026): on the pilot area check, the flood topic's own flat map (FE-20) may draw the
  # official outlines if an open dataset is licensed; on Nearby the main map still shows no flood marker.
  @ui
  Scenario: NEAR-15 flood is shown in the list and never on the map
    Given home "B1" is at story step 1
    When the user opens the flood topic
    Then flood shows in the list only, and the map shows no flood marker

  @ui
  Scenario: NEAR-16 distances are straight-line and routed times to the household's own destinations are a labelled boundary
    Given home "B1" is at story step 1
    When the user opens getting around
    Then every distance is labelled straight-line, and routed travel time to the household's own destinations appears only as a labelled, simulated paid feature, never as a working control; walking times from the postcode centre to nearby places (pilot) are a separate free feature

  # 21 Nov 2026 (0063 point 8, FE-85): the same entry as Check an area (AREA-51 to AREA-53), on the Nearby result and its Schools topic.
  @ui
  Scenario: NEAR-17 Nearby and Nearby > Schools show "Ask about this area" on a covered result, and it opens the chat with that area
    Given the user has the Nearby result for a covered sample area open, and then its Schools topic
    When the user chooses "Ask about this area" on each
    Then the chat page opens each time with that area in the panel and no postcode in any address (WCHAT-150), and the entry is not shown on a not-yet-covered or not-found result (WCHAT-151)
