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
    flood outlines are a 2D-map layer only (MAP-13, MAP-19). Every map has a list, and the desktop map has a legend and place list beside it
    (design docs/superpowers/specs/2026-11-14-first-design-batch-design.md, Constraints and the planning notes).
  Changed 16 Nov 2026 (the benchmark design pass, canvas version 405, plan
    docs/superpowers/plans/2026-11-16-benchmark-design-pass.md Task 5; FE-68, DA-22, DA-24, DA-25, DA-27, DA-31, FE-69):
    every map keeps this 3D style by default, the full Map screen (phone and desktop) adds a "2D" switch to a flat
    OpenStreetMap-style street map with a layers control (flood outlines, listed buildings and conservation areas,
    road and rail noise) drawn from `packages/fixtures/data/map-layers.json` (FE-68). The outlines never say whether
    a home or the postcode centre is inside them. Scenarios MAP-14 to MAP-26.
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
    the maps that are not drawn in 3D: crime, flood -> MAP-12, MAP-13
    design pass (FE-68, FE-42 dated note, DA-22 to DA-27, DA-31):
      3D by default, rings in view, pins at their recorded distances, badges beside pins -> MAP-14, MAP-15, MAP-16
      the 3D and 2D switch, the 2D street map and its attribution -> MAP-17, MAP-18
      the layers control, its captions and the noise bands -> MAP-19, MAP-20, MAP-26
      layer statuses and gap layers worded from status -> MAP-21, MAP-22, MAP-23
      the list as the accessible equivalent of the 2D map -> MAP-24
      no screen says whether a home or the postcode centre is inside an outline -> MAP-25

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

  # Changed 16 Nov 2026 (FE-68, DA-22): flood outlines are now recorded (as a layer in `map-layers.json`), but they are drawn only on the 2D street map (MAP-19), never on the 3D map. The 3D board says "Crime and flood are not on the 3D map; flood outlines are on the 2D map".
  @ui
  Scenario: MAP-13 flood outlines are not part of the 3D places map
    Given the result for "NB1 4XY" is open
    When the visitor looks at the 3D places map
    Then no flood outline or flood warning is drawn on it (FE-25, FE-68, B5)
    And the Map screen's 3D board says "Crime and flood are not on the 3D map; flood outlines are on the 2D map" with links to Recorded crime and Flood, and the desktop result's header map says "Crime and flood stay off the map."

  # ---- Design pass, 16 Nov 2026 (canvas version 405) ----

  # FE-42 dated note, 16 Nov 2026: the desktop result's header map and the printout cover follow the same rules. Every ring label comes from `display_distance` (MAP-08), so none is typed here.
  @ui
  Scenario: MAP-14 every map opens zoomed to fit with the 500 m and 1 mile rings in view and the outer ring when zoomed out
    Given an area map is open in the 3D style on a phone, on desktop, in the desktop result's header or on the printout cover
    When the map is shown
    Then it is zoomed to fit the places found, with the dashed rings at 500 m and 1 mile in view
    And the outer ring at the search limit comes into view when the visitor zooms out (MAP-09)
    And the map says in its own words that the rings are straight-line distance, not a walking route, and names the search limit in miles, quoted from `display_distance` (MAP-08): the Map screen "Dashed rings are straight-line distance, not a walking route. Search limit: <search limit in miles from display_distance>, zoom out to see the outer ring.", the desktop result "Rings show straight-line distance from the postcode centre, not a walking route. Search limit: <search limit in miles from display_distance>, zoom out to see the outer ring.", and the printout "Rings show straight-line distance from the postcode centre: 500 m and 1 mile. Search limit: <search limit in miles from display_distance>." (the printout also says "Crime and flood are not mapped.")

  # The data has no coordinates, only a distance from the postcode centre (design pass data plan, section 1.1), so a pin's distance is its recorded distance; its direction is drawn for legibility and is not a fact (the approved states board says the same of its sample map).
  @ui
  Scenario: MAP-15 every place pin sits at its recorded distance from the postcode centre
    Given the result for "NB1 4XY" is open
    When the visitor looks at the map
    Then each place pin is drawn at its recorded distance from the postcode centre at the map's own scale, as quoted from `area-result.json`
    And a place that is not on the map is named under it, for example "Not on the map: " followed by the place's name
    And no pin's direction is described as a fact

  # Founder's screenshot feedback, 16 Nov 2026 (Task 4 "As drawn"): numbered badges never hide the icon they number.
  @ui
  Scenario: MAP-16 numbered badges sit beside the pins and never cover an icon
    Given a map with numbered places is shown (the desktop map, the printout cover)
    When the visitor looks at a pin
    Then its number sits beside the pin, and no badge covers any pin's icon
    And the numbers match the numbers in the place list and on the topic pages

  # FE-68 (founder, 16 Nov 2026, "3D, plus a flat map option"): every map stays 3D by default; only the full Map screen has the switch.
  @ui
  Scenario: MAP-17 the Map screen has a 2D and 3D switch and opens in 3D
    Given the Map screen is open on a phone or on desktop
    When the screen has loaded
    Then a "2D" and "3D" switch is shown and "3D" is selected
    And choosing "2D" shows the flat street map and choosing "3D" returns to the 3D map with the same places and the same filters
    And the switch can be reached and operated by keyboard, and its target is at least 44 px

  # DA-25: OpenStreetMap data, our own hosted tiles, never the public tile servers; ODbL attribution required.
  @ui
  Scenario: MAP-18 the 2D street map is OpenStreetMap-style and carries its attribution
    Given the Map screen is open in the 2D style
    When the map is shown
    Then a flat street map is drawn with the same place pins, the rings (MAP-14) and the postcode centre pin
    And "© OpenStreetMap contributors" is shown on the map
    And the tiles come from our own hosting, never from the OpenStreetMap public tile servers (DA-25)

  # Layers exist on the 2D map only (FE-68). Names are the approved labels.
  @ui
  Scenario: MAP-19 the 2D map has a layers control with three switches
    Given the Map screen is open in the 2D style
    When the visitor opens "Layers"
    Then three switches are listed: "Flood outlines", "Listed buildings and conservation areas" and "Road and rail noise"
    And each is a real switch that can be reached and operated by keyboard
    And a layer whose switch is off leaves the map and its legend entries leave with it

  # Wording quoted from `map-layers.json` (label, caption, period, source): FE-69 "Approve as written (Recommended)" for the layer labels, limits and band names. Features and bands are quoted from the layer, never typed.
  @ui
  Scenario: MAP-20 each layer shows its label, caption, period and source
    Given the Map screen is open in the 2D style for the postcode "NB1 4XY" and the layers are on
    When the visitor reads a layer's entry
    Then it shows the layer's label, its feature names or bands as recorded (for example "Zone 3", "Grade II", "Lden 55.0-59.9"), its caption, its period and its source label with the date of the data, all quoted from the record named by ID in `map-layers.json`
    And the flood outline layers carry "Describes an area, not one property; ignores flood defences" and "Describes an area, not one property"
    And the listed buildings layer carries "No result does not mean no constraint; a listing point, not the protected extent" and the conservation areas layer "No result does not mean no constraint"
    And the noise layers carry "Modelled for 2021, not measured"
    And the sample source labels read "Synthetic sample, shaped like <the real source>" while the data is a sample (DA-31)

  # fixture: packages/fixtures/data/map-layers.json
  Scenario: MAP-21 the normal sample postcode has every layer recorded except rail noise
    Then map layer "NB1-4XY-LAYER-FLOOD-ZONES-1" has status "recorded"
    And map layer "NB1-4XY-LAYER-SURFACE-WATER-1" has status "recorded"
    And map layer "NB1-4XY-LAYER-LISTED-BUILDINGS-1" has status "recorded"
    And map layer "NB1-4XY-LAYER-CONSERVATION-AREAS-1" has status "recorded"
    And map layer "NB1-4XY-LAYER-ROAD-NOISE-1" has status "recorded"
    And map layer "NB1-4XY-LAYER-RAIL-NOISE-1" has status "no-record-in-source"

  # fixture: packages/fixtures/data/map-layers.json (NB7 1RR: one layer of each gap status)
  Scenario: MAP-22 the sparse postcode's layers are gaps with their own statuses
    Then map layer "NB7-1RR-LAYER-FLOOD-ZONES-1" has status "no-record-in-source"
    And map layer "NB7-1RR-LAYER-SURFACE-WATER-1" has status "source-failed"
    And map layer "NB7-1RR-LAYER-LISTED-BUILDINGS-1" has status "no-record-in-source"
    And map layer "NB7-1RR-LAYER-CONSERVATION-AREAS-1" has status "not-covered"
    And map layer "NB7-1RR-LAYER-ROAD-NOISE-1" has status "source-failed"
    And map layer "NB7-1RR-LAYER-RAIL-NOISE-1" has status "no-record-in-source"

  # Gap wording from status (rule 7). Drawn and approved: the "no record in the source" entry for rail noise, "The source has no record of rail noise for this postcode. That does not mean there is no rail noise." (FE-69 agent correction). The wording for a failed lookup and for a layer that does not cover the area is not drawn yet and is proposed: it follows the topics' "Not known right now" and "Not covered for this area" (TOPIC-25, the states board).
  @ui
  Scenario: MAP-23 a gap layer says what the status says and never reads as no risk
    Given the Map screen is open in the 2D style
    When a layer has no features because of its status
    Then a layer with the status "no-record-in-source" reads "No record in the source", for rail noise followed by "The source has no record of rail noise for this postcode. That does not mean there is no rail noise."
    And a layer with the status "source-failed" reads as not known right now, and one with "not-covered" as not covered for this area (proposed wording)
    And no gap layer reads as "no flood risk", "no noise" or "no constraint", and none is drawn as an empty outline (rule 7)

  @ui
  Scenario: MAP-24 the list is the accessible equivalent of the 2D map
    Given the Map screen is open in the 2D style
    When the visitor chooses "List" on a phone, or looks beside the map on desktop
    Then the same places are listed nearest first with their distances quoted from `area-result.json` (MAP-10, MAP-11)
    And each layer's label, caption and features are available as text, so the layers need no sight of the map
    And hiding a kind of place with a filter says so in the list, for example "Police hidden by your filter"

  # DA-31 note, 16 Nov 2026 (founder, "Move the sample shapes"): the sample NB1 4XY outlines stay clear of the postcode centre. The check is `test_map_layers_sample_outlines_do_not_cover_the_postcode_centre` in the fixture validator package; this scenario is the screen's rule. The real map may place a postcode inside an outline, and no text ever says so.
  @ui
  Scenario: MAP-25 no screen says whether a home or the postcode centre is inside an outline
    Given the Map screen is open in the 2D style with the flood, planning and noise layers on
    When the visitor reads the map, its layers and the list
    Then no text says that the postcode centre or a home is inside, outside, in or near a flood zone, a conservation area or a noise band
    And "Outlines describe an area, not one property. A blank area does not mean no risk or constraint." is shown on the map
    And a place or postcode pin is never coloured or marked by a layer

  @ui
  Scenario: MAP-26 the noise layer shows modelled bands, never one figure for a home
    Given the Map screen is open in the 2D style for the postcode "NB1 4XY"
    When the visitor reads the Road and rail noise entry
    Then road noise shows its Lden bands as recorded and the caption "Modelled for 2021, not measured"
    And no decibel figure or noise level is given for the postcode or a home (DA-27)
