@screen @buying @renting
Feature: Display settings (theme and text size on the area check)
  Question it answers: "Can I read this comfortably, in my own light and size?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: none; this is behaviour of the page, not data.
  What it is: a "Display" button on the area check that opens a small panel with two choices, theme
    (Device, Light, Dark) and text size (Standard, Large, Larger) (FE-23, B16). The site also works at 200%
    browser zoom (FE-23).
  Storage: until the PECR check on remembering a choice in the browser (decision 0014 part 1; FE-23), the
    choices are not remembered between visits and nothing is stored.
  Required states (design docs/superpowers/specs/2026-11-14-first-design-batch-design.md, "Theme and text size";
    AGENTS.md rule 7):
    the Display button, its two choices and their options -> DISP-01, DISP-06
    the largest text size, one column and no sideways scroll -> DISP-02, DISP-04
    nothing remembered between visits until the PECR check -> DISP-03, DISP-05

  @ui
  Scenario: DISP-01 the Display button opens theme and text size
    Given the user is on Check an area
    When the user chooses "Display"
    Then a panel opens with Theme (Device, Light, Dark) and Text size (Standard, Large, Larger)

  @ui
  Scenario: DISP-06 the Display panel is reachable and operable by keyboard
    Given the user is on Check an area
    When the user uses only the keyboard
    Then the Display button and every choice in its panel can be reached and operated

  @ui
  Scenario: DISP-02 at Larger the result reflows to one column
    Given the user has checked a complete postcode
    When the user chooses the text size "Larger"
    Then the result reflows to one column

  @ui
  Scenario: DISP-03 the choices are not remembered between visits
    Given the user has chosen a theme and a text size
    When the user leaves the page and returns on a later visit
    Then the page opens with Device theme and Standard text size

  @ui
  Scenario: DISP-04 at Larger the page has no sideways scroll
    Given the user has checked a complete postcode
    When the user chooses the text size "Larger"
    Then the page has no sideways scroll

  @ui
  Scenario: DISP-05 the display choices are stored nowhere
    Given the user has chosen a theme and a text size
    When the user leaves the page and returns on a later visit
    Then nothing about the choices has been stored in the browser (no cookie, local storage or session storage)
