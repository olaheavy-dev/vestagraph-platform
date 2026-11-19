@screen @buying
Feature: Every data step wording runs against the real data (proof for issue #193)
  The wording is the contract in docs/specs/README.md; the real specifications use only some of it.

  Scenario: WORD-01 all seven steps accept the documented wording
    Given home "B1" is at story step 2
    Then figure "B1.from-step-1.monthly.buildings-insurance" exists
    And figure "B1.from-step-1.monthly.buildings-insurance" has status "missing"
    And figure "B1.from-step-1.monthly.buildings-insurance" shows no amount
    And figure "B1.from-step-1.monthly.service-charge" cites evidence "B1-SC-LISTING"
    And the total "B1.from-step-1.monthly.total" is partial with reason "buildings-insurance"
    And evidence "B1-STAMP-DUTY" exists

  Scenario: WORD-02 the area and coverage steps accept the documented wording
    Then area record "R1-AREA-CRIME-2" has status "source-failed"
    And area record "R1-AREA-CRIME-2" shows no value
    And home "WALES-1" has coverage "not-yet-covered"

  Scenario: WORD-03 the area result steps accept the documented wording
    Then area result "NB1 4XY" has topic "schools" with outcome "found"
    And area result "NB1 4XY" leaves topic "noise" out of the coverage total
    And area result "NB1 4XY" asks the gap question for record "NB1-4XY-AREA-AMENITY-6"
    And area result "NB1 4XY" has priority "SAMPLE-PRIORITY-CHILDCARE" with outcome "not-known"
    And area result "NB1 4XY" has priority "SAMPLE-PRIORITY-GP" with nearest record "NB1-4XY-AREA-AMENITY-10"
    And area result "NB1 4XY" has a display distance for record "NB1-4XY-AREA-SCHOOL-1"
    And area result "NB1 4XY" counts buses for stop "NB1-4XY-AREA-TRANSPORT-STOP-1" on route "12" at hour 8
    And postcode record "NB1-4XY-AREA-SCHOOL-INSPECTION-1" has status "stale"

  Scenario: WORD-04 the map layer steps accept the documented wording
    Then map layer "NB1-4XY-LAYER-FLOOD-ZONES-1" has status "recorded"
    And topic "flood" draws map layer "flood-zones"

  Scenario: WORD-05 the council steps accept the documented wording
    Then council "E07999001" has field "rentSeries" with status "no-record-in-source"
    And council "E07999001" series "affordabilitySeries" marks a method break
    And council "E07999002" at band "D" has problem "council-tax-missing"
    And council "E07999001" at band "D" has no rent side
    And council "E06999001" at band "D" for product "5-year-fixed" has problem "rate-band-unavailable"
    And council "E06999001" at band "D" for product "2-year-fixed" has comparison "more"
    And council "E07999001" at band "D" for product "2-year-fixed" has no comparison
    And council "E06999001" caption "rent" has pattern "trend-rose"
    And council "E06999001" caption "price:terraced" has pattern "trend-fell"
    And council "E07999001" caption "price:flat" has reason "no-record-in-source"
    And council search "Capital (synthetic)" has kind "choose"
    And council search "Capital (synthetic)" lists council "E06999001"
    And council search "East Westshire Borough (synthetic)" lists council "E07999001" with note "former-name"

  Scenario: WORD-06 the neighbourhood steps accept the documented wording
    Then council "E07999001" neighbourhood "E01999031" has fact "deprivation" with status "no-record-in-source"
    And council "E06999001" neighbourhood "E01999011" has fact "connectivity" at level "neighbourhood"
    And council "E06999001" lists neighbourhood "E01999011" with label "Northbridge Centre (synthetic) (011A)"
    And council "E06999001" neighbourhood "E01999011" has tenure shares
    And council "E07999002" lists no neighbourhoods

  Scenario: WORD-07 the energy certificate steps accept the documented wording
    Then topic "energy-certificate-home" is route-only and not counted
    And topic "energy-certificate-home" opens the Vestagraph page "/energy-certificate"
    And energy certificate "0000-0000-0000-0000-0001" has outcome "shown"
    And energy certificate "0000-0000-0000-0000-0001" is not more than 10 years old
    And energy certificate "0000-0000-0000-0000-0002" is more than 10 years old
    And energy certificate "0000-0000-0000-0000-0003" has status line "superseded"
    And energy certificate "0000-0000-0000-0000-0001" has status line "none"
    And energy certificate "0000-0000-0000-0000-0007" shows "parts" as missing
    And energy certificate "0000-0000-0000-0000-0005" shows no ratings, costs, parts or improvements
    And energy certificate "0000-0000-0000-0000-0001" lists improvements in its own order with no total
    And energy certificate "0000-0000-0000-0000-0001" has an inspection date

  Scenario: WORD-08 the problem report count steps accept the documented wording
    Then the problem report counts are kept for 90 days
    And the problem report counts hold a fact count for topic "flood" with record "NB1-4XY-AREA-FLOOD-1" and reason "out-of-date"
    And the problem report counts hold an area count for topic "sold-nearby" with reason "wrong" and no record ID
    And the problem report counts hold a figure count for "council-tax-band-d" at level "council" for area "E06999001"
    And no problem report count has a "postcode" field
    And every problem report count date is a day with no time
    And every problem report count has one of the three fixed reasons
