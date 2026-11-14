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
