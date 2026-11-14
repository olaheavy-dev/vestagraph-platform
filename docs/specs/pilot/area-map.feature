@screen @buying @renting
Feature: Area maps (the quiet 3D map on every area map)
  Question it answers: "Where are the places from our data, and how far are they from the postcode?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: the postcode-level sample area data, `packages/fixtures/data/postcode-area.json`
    (NB1 4XY normal, NB7 1RR sparse); distances come from `packages/fixtures/generated/area-result.json`
    (the tested `vestagraph_area` package, FE-38); figures: none typed here.
  What it is: the style every area map uses (register line FE-42; it sets the look for the real map too, FE-03):
    our places in full-colour 3D, other houses and trees faded, a label on hover or keyboard focus, a
    map zoomed to fit the places found, and three dashed rings. Crime is never drawn on a map (FE-25, B5);
    flood has its own map (FE-25). Every map has a list, and the desktop map has a legend and place list beside it
    (design docs/superpowers/specs/2026-11-14-first-design-batch-design.md, Constraints and the planning notes).
  Rule 2: no distance, ring label or count is typed in a scenario; a place's distance is quoted from
    `area-result.json` and every ring label comes from the tested distance rule
    (`vestagraph_area.distance.display_distance`, FE-27); the outer ring's distance is the search limit
    `SEARCH_LIMIT_METRES` in `packages/vestagraph-area/src/vestagraph_area/priorities.py`.
  Required states (register line FE-42; AGENTS.md rules 2 and 7):
    our places stand out, other houses and trees fade -> MAP-01
    a place's label on hover and keyboard focus, and a phone tap -> MAP-02, MAP-03, MAP-04
    zoom to fit, and zoom out to the whole search -> MAP-05, MAP-09
    the three rings and their labels -> MAP-06, MAP-07, MAP-08
    every map has a list, and the desktop legend and place list -> MAP-10, MAP-11
    the maps that are not drawn: crime, flood -> MAP-12, MAP-13

  @ui
  Scenario: MAP-01 our places are full-colour 3D and other houses and trees fade
    Given an area map is open
    When the map is shown
    Then the places from our data are full-colour 3D buildings
    And other houses and trees fade into the ground (FE-42)

  @ui
  Scenario: MAP-02 hovering a place pin shows its name, type and distance
    Given an area map is open
    When the visitor hovers a place pin
    Then a label shows the place's name, type and distance
    And the distance is quoted from `area-result.json` in the display unit (FE-27)

  @ui
  Scenario: MAP-03 keyboard focus shows the same label as hover
    Given an area map is open
    When a place pin receives keyboard focus
    Then it shows the same label as hover (FE-42)

  @ui
  Scenario: MAP-04 a phone tap opens the place panel
    Given an area map is open on a phone
    When the visitor taps a place pin
    Then the place panel opens (FE-42)

  @ui
  Scenario: MAP-05 the map opens zoomed to fit the places found
    Given the result for "NB7 1RR" is open
    When the map is shown
    Then it is zoomed to fit the places found

  @ui
  Scenario: MAP-06 the map draws three dashed rings
    Given an area map is open
    When the map is shown
    Then dashed rings are drawn at 500 m, at 1 mile and at the search limit (the three ring distances FE-42 fixes; their labels come from `display_distance`)
    And the rings are drawn at the map's own scale

  @ui
  Scenario: MAP-07 a ring is labelled as straight-line distance, not a walking route
    Given an area map is open
    When the visitor reads a ring's label
    Then the label says the ring is straight-line distance, not a walking route (FE-42)

  @ui
  Scenario: MAP-08 every ring label follows the country's display units
    Given an area map is open
    When the visitor reads the ring labels
    Then each ring label comes from the tested distance rule (FE-27)
    And the outer ring at the search limit is labelled in miles from `display_distance`, not "5 km search"
    And no ring label is typed by hand (rule 2)

  @ui
  Scenario: MAP-09 the visitor can zoom out to the whole search
    Given an area map is open
    When the visitor zooms out
    Then the whole search, out to the outer ring, can be seen (FE-42, FE-19)

  @ui
  Scenario: MAP-10 every map has a list
    Given an area map is open
    When the visitor looks for the places on it
    Then the same places are also given as a list (design spec, Constraints)

  @ui
  Scenario: MAP-11 on desktop a legend and place list sit beside the map
    Given an area map is open on desktop
    When the map is shown
    Then a legend and a place list are beside the map (design spec, planning notes)

  @ui
  Scenario: MAP-12 Recorded crime is never drawn on a map
    Given the result for "NB1 4XY" is open
    When the visitor looks at the maps
    Then no crime is drawn on any map (FE-25, B5)

  @ui
  Scenario: MAP-13 flood has its own map, not part of the places map
    Given the result for "NB1 4XY" is open
    When the visitor looks at the places map
    Then no flood is drawn on it, because flood has its own map once flood outlines are recorded (FE-25, B5)
