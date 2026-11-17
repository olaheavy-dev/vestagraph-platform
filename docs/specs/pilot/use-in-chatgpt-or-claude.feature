@screen @buying @renting
Feature: Use in ChatGPT or Claude (the pilot's how-to page and its landing section)
  Question it answers: "How do I use Vestagraph's area and council facts in my own ChatGPT or Claude, and what does that share?"
  Modes: both (and anyone, with no account; decisions 0046, 0056 and 0058)
  Added 17 Nov 2026 (PR C of the City Explorer plan, Task 14c; decisions 0056 point 2, 0057, 0051 and 0058; register lines FE-46, FE-49 and PD-18). The page is the "how-to page, linked" that 0056 chose over leaving the public MCP server unexplained, with the "short section on landing" the founder added (0056, 15 Nov 2026). The server and its tools are `area-tools.feature` (TOOLS); this file specifies the page and the landing section only, and checks what they say, not what any host's app does.
  Fixtures: none. The page quotes no figure; where it names a council figure it names the field (`packages/fixtures/data/council-area.json`) and never a number (AGENTS.md rule 2).
  Boards, on the canvas page "Pilot · public area check" (design canvas version 407): UseInAssistant (desktop, 1280 wide) and UseInAssistantPhone (390 wide); LandingAssistantSection and LandingAssistantSectionPhone (the landing's short section); AreaCardWidgetFullPhone (the widget on a phone, `area-card.feature`). Each has its Dark twin in the "Pilot 6 · dark" row. Quoted strings below are the canvas's, word for word (apostrophes as drawn).
  Route: chosen at build (no route is drawn; the City Explorer routes are in `.design/prototype/INFORMATION_ARCHITECTURE.md`).
  Wording status: the boards still hold placeholders for facts only testing, the build or the privacy notice can answer: the public server address (set when the server is built), the example question for each app (written at build), whether the area card shows in ChatGPT for a server you add yourself, whether it shows in Claude for a connector added by address, whether developer mode still exists for an account and what switching it on changes, whether ChatGPT Free, Plus and Pro can add a server, and whether "No authentication" is offered on every plan. The page never states an unconfirmed fact (rule 1): each stays a visible "not known" line, or is left out, until it is tested (HOWTO-06, HOWTO-19, HOWTO-22, HOWTO-24 and HOWTO-28). Not drawn on any board, so proposed wording that is finalised in the build: the page's "what the tools do not do" line (HOWTO-08), the link from each area result (HOWTO-29) and the footer link on pages other than the how-to page (HOWTO-31). The ChatGPT steps are the corrected ones in `area-tools.feature` (checked 15 Nov 2026 against OpenAI's documentation, `docs/reviews/2026-11-15-use-in-assistant-research.md`); they are not derived again here. The admin-permission facts for ChatGPT Business and Enterprise come from a search summary of a help page that returned 403, so they are "to confirm in the real app" (area-tools.feature, 0056's 15 Nov 2026 note).
  What the page says about what is sent and kept follows decision 0057 (the "What the Use in ChatGPT or Claude page says" section); the wording follows OpenAI's "may send" and the founder's ruling on 0057 (anonymous daily totals, "fewer than 10" below 10, complementary suppression). 0057 is proposed wording until the privacy notice (SE-02) is final.
  Rule 4 and 0054: the page never calls an area, a council or a home "verified", "safe" or "approved" and gives no verdict, score or ranking of its own.

  Board-to-scenario map (each board has a Dark twin showing the same wording; HOWTO-35):
    UseInAssistant and UseInAssistantPhone: header and title -> HOWTO-01, HOWTO-02, HOWTO-36; What this is -> HOWTO-03; What Vestagraph gives your assistant -> HOWTO-04 to HOWTO-09; What your assistant app sees -> HOWTO-10, HOWTO-11; What Vestagraph keeps -> HOWTO-12 to HOWTO-15; the privacy link -> HOWTO-16, HOWTO-17; Setting to know about, ChatGPT -> HOWTO-18 to HOWTO-20; Connect in ChatGPT -> HOWTO-21 to HOWTO-24; Connect in Claude -> HOWTO-25 to HOWTO-27; the example question -> HOWTO-28; footer -> HOWTO-31
    LandingAssistantSection and LandingAssistantSectionPhone: HOWTO-32 to HOWTO-34
    AreaCardWidgetFullPhone (the widget the example question draws) -> HOWTO-39
    Where the page is linked from: the landing -> HOWTO-34; each area result -> HOWTO-29; each City Explorer page -> HOWTO-30 (CITY-93, HOOD-34); the footer -> HOWTO-31
    Phone and desktop layouts -> HOWTO-37; keyboard, targets and reading order -> HOWTO-38; dark twin -> HOWTO-35; no forbidden words -> HOWTO-40

  Required states (doc 03 §5; AGENTS.md rules 1, 4 and 7):
    loading, empty, ambiguous match, not covered, not found, stale: not applicable (a static page that holds no search and no stored data)
    partial answer: a fact testing has not confirmed is said to be not known, never guessed -> HOWTO-06, HOWTO-14, HOWTO-19, HOWTO-24
    source failed, offline: not applicable (no source is read; the page is part of the site)
    privacy: what the app sends, what is kept, the link to the privacy notice -> HOWTO-10 to HOWTO-17
    accessibility: HOWTO-35 to HOWTO-38

  # The page's top.
  @ui
  Scenario: HOWTO-01 the page opens with its title and what it is for
    Given the user is on the landing page
    When the user opens "Use in ChatGPT or Claude"
    Then the page heading is "Use in ChatGPT or Claude" and the line under it reads "Connect your own ChatGPT or Claude to Vestagraph’s public area and council facts."

  @ui
  Scenario: HOWTO-02 the link above the title goes back to Vestagraph
    Given the user has opened "Use in ChatGPT or Claude"
    When the user chooses "← Back to Vestagraph"
    Then the landing page opens

  # What this is.
  @ui
  Scenario: HOWTO-03 "What this is" explains MCP in plain words and says it is optional
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What this is"
    Then it says that MCP, the Model Context Protocol, is the standard way an AI app connects to an outside service, and that connecting lets the user’s own ChatGPT or Claude look up public area and council facts, with their sources, while they chat
    And it says "Your own ChatGPT or Claude does the AI work, under its own terms; Vestagraph’s server only returns sourced facts. You don’t need this to check an area or a council on Vestagraph."

  # What Vestagraph gives your assistant (TOOLS-16, TOOLS-17: read only, no key).
  @ui
  Scenario: HOWTO-04 the page says the connection is public area data only, read only, with no account and no keys
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What Vestagraph gives your assistant"
    Then the first line reads "Public area data only, read only. No account and no keys."

  # The council figures are the fields of council-area.json; the list names the fields, never a value (rule 2).
  @ui
  Scenario: HOWTO-05 the council line names the published figures and says each has its source, edition and level
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What Vestagraph gives your assistant"
    Then the council line reads "For a council: its published figures (population, council tax by band, average rent and price, the affordability ratio, who rents and who owns, connectivity), each with its source, edition and level."
    And the fields it names are the fields the council tools return (TOOLS-52 and TOOLS-53)

  @ui
  Scenario: HOWTO-06 the area card is described as an optional widget and text answers work in every app
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What Vestagraph gives your assistant"
    Then it says the area card, a map of the nearest places, is an optional widget, and that "Text answers work in every app, because the tools return a readable result without the widget."
    And for whether the card shows in ChatGPT for a server you add yourself, and in Claude for a connector added by address, it shows a "not known" line and states nothing (rule 1)

  # Each fact links its official page, read 15 Nov 2026 (design note on the board).
  @ui
  Scenario: HOWTO-07 each statement about an app's own behaviour links the app maker's page
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads the lines about the area card in ChatGPT and about connectors in Claude
    Then the ChatGPT line links "OpenAI: ChatGPT UI", and the Claude lines link "Anthropic: interactive tools in Claude" and "Anthropic: fuller in-chat apps"

  # Proposed wording (not drawn on a board): the board's closing line there says only what the tools return and that the assistant's wording is outside Vestagraph's control. The tools' limits are TOOLS-58 (no cost figure), TOOLS-38 (no listing) and TOOLS-59 (no ranking).
  @ui
  Scenario: HOWTO-08 the page says what the tools do not do
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What Vestagraph gives your assistant"
    Then it says the tools return no cost estimate, no listing and no ranking or verdict of a place, and "Your assistant’s own wording is outside Vestagraph’s control."

  @ui
  Scenario: HOWTO-09 the page says the tools return only published figures with their source, edition and level
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads the end of "What Vestagraph gives your assistant"
    Then it reads "Vestagraph’s tools return only published figures, each with its source, edition and level. Your assistant’s own wording is outside Vestagraph’s control."

  # What your assistant app sees (decision 0057).
  @ui
  Scenario: HOWTO-10 the page lists what ChatGPT may send with a tool call and links OpenAI's reference
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What your assistant app sees"
    Then "ChatGPT may send, with a tool call" is followed by an anonymised user ID, an anonymised conversation ID, an anonymised organisation ID "when there is one", a coarse location hint (city, region, country, time zone, longitude, latitude) "which may be missing", an optional device and app hint "which may be missing" and the requested language
    And the list links "OpenAI plugins reference"

  @ui
  Scenario: HOWTO-11 the page says Vestagraph logs nothing the user types and works the same without the hints
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What your assistant app sees"
    Then it says "Vestagraph does not put your postcode, place name or anything else you type in its logs." and "Location and the device hint are hints only and may be missing; Vestagraph works the same without them."

  # What Vestagraph keeps (0057: complementary suppression; the generated check before any totals are shown is a build task of 0057).
  @ui
  Scenario: HOWTO-12 the page says Vestagraph keeps only anonymous daily totals and names what they are counted by
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What Vestagraph keeps"
    Then it says the details are read only to add to anonymous daily totals by tool, host, outcome, city, region, country and language (location and language come from ChatGPT only), then dropped
    And it says "Nothing that identifies you is stored: no user, conversation or organisation ID, no coordinates, no device hint."

  @ui
  Scenario: HOWTO-13 the page says a count below 10 shows as "fewer than 10"
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What Vestagraph keeps"
    Then it says "A count below 10 shows as “fewer than 10”." and that when a hidden count could be worked out from a total or another count, that one is hidden too, checked automatically before any totals are shown

  @ui
  Scenario: HOWTO-14 the page does not say what Claude sends, because Anthropic does not document it
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads the "Claude" part of "What Vestagraph keeps"
    Then it says Anthropic’s documentation does not say what Claude sends with a tool call beyond the request itself, that connections come from Anthropic’s cloud, and "Anything Claude sends is dropped, not counted."
    And the line links "Claude help: custom connectors"

  @ui
  Scenario: HOWTO-15 the totals are counts only and name no person, home or search
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What Vestagraph keeps"
    Then no sentence says Vestagraph keeps a postcode, a place name, a question or an ID (decision 0057, 0014)

  @ui
  Scenario: HOWTO-16 the page links the privacy notice
    Given the user has opened "Use in ChatGPT or Claude"
    When the user chooses "Read the privacy notice"
    Then the privacy notice opens

  @ui
  Scenario: HOWTO-17 the privacy link sits with "What Vestagraph keeps" and is reachable by keyboard
    Given the user has opened "Use in ChatGPT or Claude"
    When the user tabs to "Read the privacy notice"
    Then the link takes focus with a visible outline, and activating it with Enter opens the privacy notice

  # Setting to know about, ChatGPT (0056 point 2: the page must say plainly what a risky setting means and what it trades off).
  @ui
  Scenario: HOWTO-18 the page states what OpenAI's documentation says about developer mode, and no more
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "Setting to know about · ChatGPT"
    Then it says "OpenAI’s current documentation describes adding a server as a plugin" and that its text no longer mentions developer mode, with links "OpenAI: Add custom MCP server" and "OpenAI developer mode page"

  @ui
  Scenario: HOWTO-19 what developer mode means for an account is not stated until it has been tested
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What it means" under developer mode
    Then the page shows a "not known" line instead of a claim about whether developer mode exists for an account or what switching it on changes (rule 1)

  @ui
  Scenario: HOWTO-20 "What you trade off" quotes OpenAI and says Vestagraph's tools only read
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "What you trade off"
    Then it quotes OpenAI: "Only connect to MCP servers you trust.", says write actions need confirmation by default and that remembering an approval for a conversation means later write actions in it may run without asking, and ends "Vestagraph’s tools only read."

  # Connect in ChatGPT (the corrected steps, area-tools.feature and 0056's 15 Nov 2026 note).
  @ui
  Scenario: HOWTO-21 the ChatGPT steps are the six numbered steps in order
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "Connect in ChatGPT"
    Then the six steps are numbered 1 to 6: go to ChatGPT Plugins (chatgpt.com/plugins); select the plus button, then "Add custom MCP server"; enter a name and, under Connection, the server address; under authentication choose "No authentication"; review the risk warning and select "I understand and want to continue", then "Create as a plugin"; install it, then start a new conversation with the plugin enabled

  @ui
  Scenario: HOWTO-22 the server address is the public address of the built server
    Given the user has opened "Connect in ChatGPT" or "Connect in Claude"
    When the user reads the server address in step 3 of ChatGPT and step 2 of Claude
    Then it is the server's one public HTTPS address, the same in both, and the page shows no address until the server is built

  @ui
  Scenario: HOWTO-23 "No authentication" is described as one option OpenAI lists with OAuth
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads step 4 of "Connect in ChatGPT"
    Then it reads "Under authentication, choose “No authentication”. OpenAI lists it with OAuth as an authentication option."

  # The admin permission facts come from a search summary; they stay marked "read as a search summary" until confirmed in the real app.
  @ui
  Scenario: HOWTO-24 the ChatGPT note says who can add a server by plan, and what is not known
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads the note under "Connect in ChatGPT"
    Then it says that on Business only admins and owners can create and publish, that on Enterprise and Edu an admin can give selected members creation rights with the permission "Create plugins with MCPs", off by default in Enterprise workspaces, and that this is "read as a search summary"
    And for Free, Plus and Pro, and for whether "No authentication" is offered on every plan, it shows a "not known" line and states nothing (rule 1)

  # Connect in Claude (area-tools.feature: Claude custom connector, "No sign in", one custom connector on the free plan).
  @ui
  Scenario: HOWTO-25 the Claude steps for Free, Pro, Max and Ultra are numbered in order
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads "Connect in Claude"
    Then step 1 reads "On Free, Pro, Max or Ultra: open Customize, then Connectors, then Add, then “Add custom connector”.", step 2 says to enter a name and the server address and select Continue, and step 3 says to choose the authentication option "No sign-in", then Add, then Connect if shown

  @ui
  Scenario: HOWTO-26 the Claude step for Team and Enterprise names who can add a connector
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads step 4 of "Connect in Claude"
    Then it says that on Team and Enterprise an Owner (on Enterprise, also a member with a custom role that can manage libraries) adds it in Organization settings, then Connectors, then Add, Custom, Web, and that members then select Connect under Customize, then Connectors

  @ui
  Scenario: HOWTO-27 the Claude note says the free plan allows one connector and the address must be public HTTPS
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads the note under "Connect in Claude"
    Then it says the free plan allows one custom connector, that Claude connects from Anthropic’s cloud so the address must be public HTTPS on port 443, and that Anthropic warns Claude can access and perform actions within the services you connect
    And it links "Claude: custom connectors" and "Claude help: custom connectors"

  # The example question is written at build and checked against the tools (AI-03); it uses the sample postcode, so its result is labelled sample (HOWTO-39).
  @ui
  Scenario: HOWTO-28 each app's steps end with an example question the tools can answer
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads the end of "Connect in ChatGPT" and of "Connect in Claude"
    Then each shows "Try a question:" followed by one example question, and no question appears until it has been run against the tools

  # Where the page is linked from (decision 0056 point 2): each area result, each City Explorer page and the footer. The landing section is below.
  # Not drawn on the area result boards: proposed wording, "Use in ChatGPT or Claude →", as the council boards draw it.
  @ui
  Scenario: HOWTO-29 each area result links to the page
    Given the user has checked a postcode in England and the result is shown
    When the user chooses "Use in ChatGPT or Claude →" at the foot of the result
    Then "Use in ChatGPT or Claude" opens

  # CITY-93 and HOOD-34 specify the same link on the council page and the neighbourhood page; the council and neighbourhood boards draw it above "Design note".
  @ui
  Scenario: HOWTO-30 each City Explorer page links to the page
    Given the user has opened the council page for council "E06999001", or one of its neighbourhood pages
    When the user chooses "Use in ChatGPT or Claude →"
    Then "Use in ChatGPT or Claude" opens (CITY-93, HOOD-34)

  # The how-to page's own footer lists the link as the last item; the other pages' footer is proposed wording (decision 0056, IA "Landing" item 9).
  @ui
  Scenario: HOWTO-31 the footer links the page
    Given the user is on any page of the site with the footer
    When the user chooses "Use in ChatGPT or Claude" in the footer
    Then "Use in ChatGPT or Claude" opens
    And on the how-to page the footer reads "How it works", "About the data", "Privacy notice", "Accessibility" and "Use in ChatGPT or Claude"

  # The landing section (boards LandingAssistantSection and LandingAssistantSectionPhone; 0056, founder: "Short section on landing").
  @ui
  Scenario: HOWTO-32 the landing section is a short card after "How to read a result" and before "Coming next"
    Given the user is on the landing page
    When the user scrolls from "How to read a result" to "Coming next, with a free account"
    Then the section between them is a card labelled "Use Vestagraph in ChatGPT or Claude", and the search box is still the first control on the page (LAND-11)

  @ui
  Scenario: HOWTO-33 the landing section says what it is in one line, with what Vestagraph keeps in small print
    Given the user is on the landing page
    When the user reads the "Use Vestagraph in ChatGPT or Claude" section
    Then the label reads "IN YOUR OWN ASSISTANT", the heading "Use Vestagraph in ChatGPT or Claude", and the line "Use Vestagraph’s area and council facts in your own ChatGPT or Claude."
    And the small print reads "Your assistant app sees what it sends us. We keep only anonymous daily totals, shown as “fewer than 10” below 10."

  @ui
  Scenario: HOWTO-34 "How to connect" on the landing opens the page
    Given the user is on the landing page
    When the user chooses "How to connect"
    Then "Use in ChatGPT or Claude" opens, and the illustration beside the button has the text alternative "Your assistant app on the left, connected to Vestagraph’s public facts on the right"

  # Display, layout and access.
  @ui
  Scenario: HOWTO-35 the dark twin of the page and the landing section show the same wording
    Given the user is on "Use in ChatGPT or Claude" or on the landing page
    When the user picks the dark theme in "Display"
    Then the same headings, steps and quoted wording are shown, and the contrast of every line is at least 4.5:1

  @ui
  Scenario: HOWTO-36 the desktop header links Check an area and City Explorer, and the phone header does not
    Given the user opens "Use in ChatGPT or Claude" on desktop and then on a phone 390 pixels wide
    When the page has loaded
    Then on desktop the header shows "Check an area", "City Explorer" and "Display", and on the phone it shows the logo link "Vestagraph home" and "Display"

  @ui
  Scenario: HOWTO-37 on a phone the page is one column and nothing scrolls sideways
    Given the user opens "Use in ChatGPT or Claude" on a phone 390 pixels wide
    When the user reads the page from top to bottom
    Then every section and every numbered step is in one column in the same order as on desktop, and nothing scrolls sideways

  @ui
  Scenario: HOWTO-38 the page works by keyboard, with 44 px targets and every link named
    Given the user is on "Use in ChatGPT or Claude"
    When the user works through the page by keyboard
    Then every link and button can be reached in reading order with a visible focus outline, each is at least 44 by 44 pixels, and each link names where it goes

  # Sample label (register FE-46): every widget board carries "Sample data: a made-up town". The example question (HOWTO-28) uses the sample postcode.
  @mcp
  Scenario: HOWTO-39 the area card for the sample postcode carries "Sample data: a made-up town"
    Given an assistant is connected to the area tools and the user has asked the example question for the sample postcode "NB1 4XY"
    When the assistant draws the area card
    Then the card carries the label "Sample data: a made-up town" (FE-46)

  @ui
  Scenario: HOWTO-40 the page never calls an area, a council or a home safe, verified or approved
    Given the user has opened "Use in ChatGPT or Claude"
    When the user reads the whole page
    Then no text calls an area, a council or a home "safe", "verified" or "approved", and none gives a score, rating or verdict of Vestagraph’s own (AGENTS.md rule 4, decision 0054)
