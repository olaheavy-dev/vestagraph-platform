@screen @buying @renting
Feature: Landing
  Question it answers: "What can this help me do?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: the postcode-level sample area data for the hero, `packages/fixtures/data/postcode-area.json`
    (postcode NB1 4XY); inputs: its recorded distances; figures: none.
  Route: / (the landing is the area check: the one search box, for a postcode or a town, is the main action; decision 0046, FE-37 amended 15 Nov 2026).
  Updated 17 Nov 2026 (PR C of the City Explorer plan, Task 14c; decisions 0055 and 0056; register lines FE-37 amended and FE-49): the postcode box became one box for a postcode, town or city (LAND-01, LAND-02, LAND-11, LAND-14 to LAND-16); the four wording edits and the FAQ answer "Do you keep my search?" are LAND-17 to LAND-19; the City Explorer council link and the how-to section are in the section list below (LAND-20; the section's own scenarios are HOWTO-32 to HOWTO-34). Boards: Landing, LandingDark, LandingPhone and LandingPhoneDark, and LandingAssistantSection and LandingAssistantSectionPhone with their Dark twins, on the canvas page "Pilot · public area check" (design canvas version 407). Quoted strings are the canvas's, word for word.
  The link "No postcode yet? Explore a council area" under the box (the site plan's item 1, which left "kept or dropped" to this task) is dropped: the one box now takes a town, the boards draw no such link, and a second way in under it would compete with the box (agent's call, approved by the founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)")). The council link stays in the footer (LAND-20).
  Sections, in order, from the information architecture's "Landing": the promise with the search
    box; the hero map; Data from (the source wall); How it works; How to read a result (a showcase card, FE-36); Use in ChatGPT or Claude (a short section with a "How to connect" link, decision 0056; its scenarios are HOWTO-32 to HOWTO-34 in `use-in-chatgpt-or-claude.feature`); Coming next, with a free account; Questions; the footer, with the City Explorer council link "Explore council areas" (decision 0055) and "Use in ChatGPT or Claude" (LAND-20)
    ("Honest by design" removed 14 Nov 2026, FE-35).
  Required states (doc 03 §5):
    basic/paid boundaries -> LAND-05
    narrow and mobile layouts with a list alternative to the map -> LAND-11
    text the one box cannot search as a postcode -> LAND-14 (LAND-12, the postcode-only message, is withdrawn)
    a town, city or council name; a place outside England -> LAND-15, LAND-16
    the hero's wording, How it works and the FAQ answer for the one box -> LAND-17 to LAND-19
    the link to Check an energy certificate -> LAND-21
    Recent postcodes under the search box, off by default, on with its list, storage unavailable -> LAND-22 to LAND-24 (the behaviour is `pilot/area-share.feature`, RECENT-01 to RECENT-14)
    the footer links to How it works, Privacy notice and Accessibility, and the How it works section's link -> LAND-25, LAND-26 (the pages are `pilot/public-pages.feature`)
    the "How to read a result" showcase and where "How we got this" is -> LAND-13
    A complete postcode hands over to Check an area (14-check-an-area.feature), which holds the
    loading, not found, source failed and outside England states.
  Free and paid: the area check is free and needs no account. Account features (cost estimate,
    compare, questions) are described only as "Coming next … not available yet" (LAND-05; decision 0046).

  @ui
  # Changed 14 Nov 2026 (FE-37): placeholder "Enter a postcode", no example hint; the label stays.
  # Changed 17 Nov 2026 (FE-37 amended 15 Nov 2026): one box for a postcode, town or city: label "Postcode, town or city", placeholder "Enter a postcode or town", button "Search".
  Scenario: LAND-01 the search box is the main action
    Given the user is not signed in
    When the user opens the landing page
    Then the first action is a field with a persistent "Postcode, town or city" label, the placeholder "Enter a postcode or town" meeting 4.5:1 contrast, no example hint under it, and a "Search" button

  @ui
  # Changed 17 Nov 2026: under the search box; the desktop board adds a second sentence, the phone board has the first only.
  Scenario: LAND-02 the landing says it covers England only
    Given the user is not signed in
    When the user opens the landing page
    Then "England only for now" is shown under the search box, and on desktop it continues "Wales, Scotland and Northern Ireland aren’t covered yet."

  @ui
  Scenario: LAND-03 checking a postcode opens Check an area with the postcode in the fragment
    Given the user is on the landing page
    When the user checks a complete postcode
    Then Check an area opens with the postcode after "#postcode=", and the query string holds no postcode

  @ui
  # Changed 14 Nov 2026 (FE-37): the link reads "Try a sample".
  Scenario: LAND-04 the sample link opens the sample area
    Given the user is on the landing page
    When the user chooses "Try a sample"
    Then Check an area opens on the sample postcode, labelled "Sample data"

  @ui
  Scenario: LAND-05 account features are described, never offered
    Given the user is not signed in
    When the user opens the landing page
    Then the cost estimate, compare, and tracking questions and answers per home appear only in a "Coming next" panel labelled "not available yet", with no active control

  # fixture: packages/fixtures/data/postcode-area.json (NB1 4XY, the hero's nearest places)
  @ui
  Scenario: LAND-06 the hero's places come from the sample data
    Given the user is not signed in
    When the user opens the landing page
    Then the hero summary card's four nearest places, their distances and the "+N more nearby" count come from the postcode-level sample data, the pin is labelled "Postcode centre", and the hero map and card carry a visible "Sample area" label (M5: the town is invented and the page sits beside real data)

  @ui
  Scenario: LAND-07 the hero map is a static image
    Given the user is not signed in
    When the user opens the landing page
    Then the hero map is a static image, and the live map library is not loaded

  @ui
  # Changed 14 Nov 2026 (FE-34): the "can't tell you" line is gone from the cards; each source's limits live on the general About the data page (FE-34 amended 14 Nov 2026).
  Scenario: LAND-08 the source wall names each source and links About the data
    Given the user is not signed in
    When the user opens the landing page
    Then each "Data from" card shows a source's name and what it covers, with no logo and no "can't tell you" line, and links to About the data, where the source's limits are

  @ui
  Scenario: LAND-09 the example result is labelled as a sample
    Given the user is not signed in
    When the user opens the landing page
    Then the Schools card in "How to read a result" is labelled "Sample"

  @ui
  Scenario: LAND-10 the landing never calls an area or home safe
    Given the user is not signed in
    When the user opens the landing page
    Then no text calls an area or a home "safe", "verified" or "approved" (AGENTS.md rule 4)

  @ui
  # Changed 17 Nov 2026 (FE-37 amended): the search box.
  Scenario: LAND-11 on a phone the search box comes first and the hero's places are text
    Given the user is not signed in
    And the screen is 390 pixels wide
    When the user opens the landing page
    Then the search box is the first control, and the hero's places and distances are readable as text, not only in the image

  # Withdrawn 17 Nov 2026 (FE-37 amended 15 Nov 2026): the box is no longer postcode-only, so text that is not a complete postcode is searched as a place, not refused with the postcode format. Replaced by LAND-14; kept unedited for its ID.
  @ui @withdrawn
  Scenario: LAND-12 an incomplete postcode on the landing is not searched
    Given the user is on the landing page
    When the user checks an incomplete postcode
    Then an inline message under the "Postcode" field explains the format, and the page does not move to Check an area

  # Added 14 Nov 2026 (FE-34, FE-36): the showcase's fourth callout points to the page-level section.
  # Changed 14 Nov 2026 (FE-34, FE-24 amended; founder: "General page + short note (Recommended)"): the callout points to the short note at the bottom of every result, with the full method and limits on About the data.
  # Approved 14 Nov 2026: the founder kept the callout 4 wording (prompt window: "Keep it (Recommended)").
  @ui
  Scenario: LAND-13 the "How to read a result" showcase explains where "How we got this" is
    Given the user is not signed in
    When the user views "How to read a result"
    Then the sample card carries no "How we got this" row, and callout 4 reads "How we got this" with "At the bottom of every result: a short note on how this search was worked out. The full method and what each source can't tell you are on About the data."

  # Added 17 Nov 2026 (Task 14c). FE-37 amended 15 Nov 2026: a postcode opens the area check; a place name opens its council page or "choose a council"; a place in Wales, Scotland or Northern Ireland says "not yet covered". The behaviour after the box is City Explorer's (CITY-22, CITY-08 to CITY-21); these scenarios check what the landing box sends where.
  # Replaces LAND-12. The design does not say how a postcode-shaped but incomplete entry is told from a place name: this scenario takes the plain reading (it is searched as a place, and nothing matching it gives CITY-21's "couldn’t find" page). Proposed behaviour (agent's), approved by the founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)"); no postcode format message is shown.
  @ui
  Scenario: LAND-14 text that is not a complete postcode is searched as a place
    Given the user is on the landing page
    When the user types an incomplete postcode in the search box and chooses "Search"
    Then the entry is searched as a place name, the page does not move to Check an area, and a match of nothing gives the "We couldn’t find" page of CITY-21

  @ui
  Scenario: LAND-15 a town or council name opens its council page, or asks the visitor to choose
    Given the user is on the landing page
    When the user types "Northbridge (sample)" and chooses "Search"
    Then the page for council "E06999001" opens (CITY-08), and a name that matches several councils asks the visitor to choose and picks none (CITY-10, CITY-12)

  @ui
  Scenario: LAND-16 a place in Wales, Scotland or Northern Ireland says not yet covered
    Given the user is on the landing page
    When the user types "Afonbryn (sample)" and chooses "Search"
    Then the page says "Not yet covered", as CITY-20 specifies, and no council page opens (rule 6)

  # FE-49 (founder, 15 Nov 2026: "Approve all four (Recommended)"). The boards: Landing (desktop) and LandingPhone; the phone's subline ends after "Free, no account." because the phone board has less room.
  @ui
  Scenario: LAND-17 the hero's subline adds each council's published figures
    Given the user is not signed in
    When the user opens the landing page
    Then on desktop the line under the headline reads "Schools, transport, shops, parks, health, places of worship, flood risk and recorded crime for any postcode in England, and each council’s published figures. Free, no account, and every fact shows where it came from."
    And on a phone it reads "Schools, transport, shops, parks, health, places of worship, flood risk and recorded crime for any postcode in England, and each council’s published figures. Free, no account."

  @ui
  Scenario: LAND-18 How it works says to type a postcode or town and separates the postcode from the town result
    Given the user is not signed in
    When the user reads "How it works"
    Then step 1 is titled "Type a postcode or town" with "Any postcode, town or city in England. No account, nothing to install."
    And step 2, "See what’s around", reads "For a postcode: transport, shops, parks, health, schools, places of worship, flood risk and recorded crime. For a town or city: its council’s published figures. Each with its source."

  # Founder's wording, 17 Nov 2026 (prompt window, FE-49 amended): the clause "unless you sign in and save an area" was added because signed-in users can save areas (0058). The landing FAQ boards still show the old answer and are to be redrawn (#318).
  @ui
  Scenario: LAND-19 the FAQ answers "Do you keep my search?" for a postcode or a place name
    Given the user is not signed in
    When the user opens "Do you keep my search?" in Questions
    Then it reads "No. What you type, a postcode or a place name, is only used to show your result. We don’t keep it or link it to you, unless you sign in and save an area."

  # The boards draw a footer of How it works, About the data, Privacy and Accessibility. The site plan's footer also lists "Explore council areas" (0055) and "Use in ChatGPT or Claude" (0056); neither is drawn on the landing boards, so this scenario is proposed wording, approved by the founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)"), finalised in the build.
  @ui
  Scenario: LAND-20 the footer links the council pages and the how-to page
    Given the user is not signed in
    When the user reaches the footer of the landing page
    Then it links "Explore council areas", which opens the landing page's one search box, the council search (CITY-07 to CITY-22; no board draws a separate search page, agent's call, 17 Nov 2026; approved by the founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)")), and "Use in ChatGPT or Claude", which opens that page (HOWTO-31)

  # Added 18 Nov 2026 (energy certificate design: "the landing gets a link under the search box or in the footer (the boards decide)"). Drawn on the four landing boards (19 Nov 2026, canvas version 413; "Current" labels from version 414), under the search box (DA-32, founder-approved 19 Nov 2026: "Keep all (Recommended)"); the wording was approved by the founder on 19 Nov 2026 (copy review, "Approve as written (Recommended)"), finalised in the build.
  @ui
  Scenario: LAND-21 the landing links to the energy certificate page
    Given the user is not signed in
    When the user reads the landing page
    Then it links "Check an energy certificate" to "/energy-certificate", described as "Have a certificate number? See what that home's energy certificate says."
    And the link carries no postcode, no search text and no certificate number

  # Added 19 Nov 2026 (pilot design batch, PR 1; design `docs/superpowers/specs/2026-11-19-pilot-design-batch-design.md`, section "3. Recent postcodes"; plan Task 2). The behaviour is RECENT-01 to RECENT-14 in `pilot/area-share.feature`; these three scenarios place it on the landing. Drawn on the `RecentPostcodes` board (canvas version 1795107206-3e0d), so the wording is proposed, for the founder's copy review before build.
  @ui
  Scenario: LAND-22 under the search box Recent postcodes is off by default and names its consent
    Given the user is not signed in and has never turned Recent postcodes on
    When the user reads under the search box
    Then "Remember postcodes on this device" is shown with the action "Turn on" and "Nothing is kept while this is off." (RECENT-02), under the "England only for now" line
    And nothing is written to the browser, and the search box stays the first control (LAND-01, LAND-11)

  @ui
  Scenario: LAND-23 with Recent postcodes on, the landing lists up to 5 postcodes, newest first
    Given the user has turned on "Remember postcodes on this device" and has checked postcodes
    When the user opens the landing page
    Then up to 5 postcodes are listed under the search box, newest first, each a link that opens its result with the postcode after "#postcode=" (LAND-03; RECENT-05, RECENT-06)
    And "Clear" and "Turn off" are available, the list is never sent to us (RECENT-11), and no analytics event, error report or page title holds a postcode from the link (SHARE-05)

  @ui
  Scenario: LAND-24 if browser storage is unavailable the landing says Recent postcodes can't be turned on here and the search still works
    Given a private window or a browser that blocks storage
    When the user reads under the search box
    Then the setting says it can't be turned on here (RECENT-10) and no list is shown
    And the postcode search works exactly as before

  # Added 19 Nov 2026 (pilot design batch, PR 2; `pilot/public-pages.feature`). LAND-22 to LAND-24 are the area features pull request's (#350). The boards draw the footer of How it works, About the data, Privacy and Accessibility (LAND-20's comment); this scenario only says where its three links go. Proposed wording, for the founder's copy review.
  @ui
  Scenario: LAND-25 the footer links How it works, Privacy notice and Accessibility to their pages
    Given the user is on the landing page
    When the user reaches the footer
    Then "How it works" opens "/how-it-works" (HOW-01), "Privacy notice" opens "/privacy" (PRIV-01) and "Accessibility" opens "/accessibility" (A11Y-01)
    And the links carry no postcode, no search text and no certificate number

  @ui
  Scenario: LAND-26 the landing's How it works section links to the How it works page
    Given the user is on the landing page
    When the user reads "How it works" (LAND-18)
    Then it offers a link "More on how it works" (proposed wording) that opens "/how-it-works" (HOW-01)
    And the link carries no postcode or search text
