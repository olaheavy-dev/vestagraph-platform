@screen @buying @renting
Feature: Sign in to chat and save areas (the pilot's sign-in)
  Added 16 Nov 2026 (decision 0058, register lines SE-06, FE-56, FE-60). Anonymous visitors still use the public pages with no account (decisions 0046 and 0051); signing in is needed only to chat and to save areas.
  Question it answers: "How do I sign in, and what happens to where I was and what I was doing?"
  Modes: both
  Fixtures: the postcode in the return scenarios is a sample postcode from `packages/fixtures/data/postcode-area.json` (NB1 4XY); figures: none.
    The accounts, the sign-in email and the users in these scenarios are made up for the test run (rule 5): no real address, no real provider account.
  Where: the sign-in page (a full page on a phone and on desktop, FE-63), reached from "Ask about this area" (or "Ask more about this", FE-58) and Save when signed out, and from the chat's own entry. The email link, its states and the GitHub no-email state are drawn on the canvas page "Pilot · Signed-in chat" (SignedInSignIn, SignedInEmailStates, SignedInGitHubNoEmail, SignedInPublicEntry and their phone, desktop and Dark versions).
  Methods: Google, GitHub and "Email me a link" (decision 0058). The email link works once and lasts 5 minutes (SE-06).
  The server checks in these scenarios (logs, headers, tokens, sessions) are tagged @ui, as in area-chat.feature: they run in the same playwright-bdd suite against the running stack (SP-03).
  Copy: quoted messages are proposed wording, finalised at board review and in the build. The fixed texts are "Check your email" (the same words for every address), "Send a new link" (the one action on the expired or used page) and the chat texts in workspace-chat.feature.
  AI: no scenario here calls a model, so none is an AI-03 case.
  Required states (plan docs/superpowers/plans/2026-11-16-signed-in-chat.md, Tasks 3 and 6; Review Focus 2 and 3; AGENTS.md rules 4, 5 and 7):
    the three sign-in methods -> AUTH-01
    what signing in keeps, shown before the first message -> AUTH-02
    the bot check on sign-up and on each email-link request, never on a chat message -> AUTH-03, AUTH-04, AUTH-05
    "Check your email", the same for a known and an unknown address -> AUTH-06
    link expired -> AUTH-07; link already used -> AUTH-08; opened on another device -> AUTH-09
    email service unavailable -> AUTH-10
    GitHub with no verified email -> AUTH-11
    one account per verified email, never linked on an unverified one, never because a provider is trusted -> AUTH-12, AUTH-13, AUTH-14
    signed out on a public page: the entry and Save lead to sign-in -> AUTH-15 (an area result), AUTH-28 (a council page)
    the public "Ask about this area" entry carries the AI badge (FE-13) -> AUTH-26
    back where they were, and the action finished -> AUTH-16, AUTH-17
    the session expires while typing -> AUTH-18
    no postcode in any sign-in request -> AUTH-19, AUTH-20
    the magic-link token is in no log -> AUTH-21
    sign out -> AUTH-22, AUTH-23; Sign out everywhere -> AUTH-24
    a revoked session's unexpired token refused on every request: a write -> AUTH-25, a read -> AUTH-27

  @ui
  Scenario: AUTH-01 the sign-in page offers Google, GitHub and an email link
    Given the user is signed out and opens the sign-in page
    When the page has loaded
    Then it offers three ways in: "Continue with Google", "Continue with GitHub" and "Email me a link", each a button at least 44 px high

  @ui
  Scenario: AUTH-02 the sign-in page says what signing in keeps, before the first message
    Given the user is signed out and opens the sign-in page
    When the page has loaded and no message has been sent
    Then one line says what signing in keeps (the account, saved areas and chats, kept 12 months after last use and deletable) and links the privacy notice

  @ui
  Scenario: AUTH-03 signing up for the first time runs the bot check
    Given a person with no account chooses a sign-in method
    When the sign-up request is made
    Then the bot check runs before the account is created, and a failed check creates no account

  @ui
  Scenario: AUTH-04 each email-link request runs the bot check
    Given the user is on the sign-in page
    When the user asks for an email link, and then asks for another
    Then the bot check runs on each request, and a failed check sends no email

  @ui
  Scenario: AUTH-05 a chat message does not run the bot check
    Given the user is signed in and has opened the chat
    When the user sends a message
    Then no bot check runs for that message (the account, the daily cap and the rate limits protect it, decision 0058)

  # Review Focus 3: asking for a link says the same whether or not an account exists.
  @ui
  Scenario: AUTH-06 "Check your email" reads the same for a known and an unknown address
    Given one address has an account and another has none
    When the user asks for an email link with each address
    Then both times the page shows the same "Check your email" screen with the same words, the two responses are identical to the page, and they take the same time within the test's tolerance, so timing does not reveal whether an account exists

  @ui
  Scenario: AUTH-07 an expired email link says so and offers one action
    Given the user was sent an email link more than 5 minutes ago (SE-06)
    When the user opens the link
    Then the page says the link has expired or been used, signs nobody in, and offers one action, "Send a new link"

  @ui
  Scenario: AUTH-08 an email link that was already used says so and offers one action
    Given the user opened an email link once and was signed in
    When the same link is opened a second time
    Then the page says the link has expired or been used, signs nobody in, and offers one action, "Send a new link"

  # Review Focus 3: the postcode is never in the link, so another device cannot carry it.
  @ui
  Scenario: AUTH-09 a link opened on another device signs the user in to a new chat with a short note
    Given the user asked for an email link on one device
    When the user opens the link, within 5 minutes, on a different device
    Then the user is signed in on that device to a new chat with a short note that the earlier page and any postcode were not carried over, and the link contains no postcode

  @ui
  Scenario: AUTH-10 when the email service is down the page says so and offers another way in
    Given the email service is unavailable
    When the user asks for an email link
    Then the page says the link could not be sent, with no error detail and no address repeated, and offers one action: try again (Google and GitHub stay on the page)

  # B22: cause, reassurance, one action.
  @ui
  Scenario: AUTH-11 GitHub with no verified email says why and offers another way in
    Given a GitHub account whose email is neither verified nor shared
    When the user continues with GitHub
    Then no account is created, and the page says GitHub shared no verified email, that nothing was saved, and offers one action: use Google (an email link is on the sign-in page)

  @ui
  Scenario: AUTH-12 two methods with the same verified email reach the same account
    Given an account made with Google for a verified email address
    When the user signs in with an email link to the same verified address
    Then the user reaches the same account, with the same saved areas and chats

  @ui
  Scenario: AUTH-13 an unverified email is never linked to an existing account
    Given an account exists for an email address
    When a provider reports that same address as unverified
    Then no link is made, the existing account is untouched, and the user is told that provider shared no verified email (AUTH-11)

  # Better Auth's trusted-providers setting would link without a verified email; the build leaves it empty.
  @ui
  Scenario: AUTH-14 no provider is trusted into linking accounts without a verified email
    Given the server's account-linking settings
    When they are read
    Then they list no trusted provider, so linking depends only on a verified email

  @ui
  Scenario: AUTH-15 on a public page, the chat entry and Save lead to sign-in when signed out
    Given the user is signed out and has checked a complete postcode (fixture NB1 4XY)
    When the user chooses "Ask about this area" or Save
    Then the sign-in page opens, and the area result is still there to return to

  # FE-56: the return target is held in the tab, never stored.
  @ui
  Scenario: AUTH-16 after signing in, the user returns to the page they came from
    Given a signed-out user chose Save on the result for a sample postcode (NB1 4XY)
    When the user signs in
    Then the page they came from opens again with the same area result

  @ui
  Scenario: AUTH-17 after returning, the action they chose finishes
    Given a signed-out user chose Save on the result for a sample postcode (NB1 4XY) and signed in
    When the page has opened again
    Then the area is saved, a confirmation says "Saved", and the user did not have to choose Save again

  @ui
  Scenario: AUTH-18 when the session expires while typing, the draft is kept in the tab and sign-in follows
    Given the user is signed in and has typed a message but not sent it
    When the session has expired and the user sends it
    Then nothing is sent to the model, the draft stays in the tab's session storage, the sign-in page opens, and after sign-in the draft is back in the message box, unsent

  # Rules: postcodes never in a URL, a sign-in request or a log (0014, 0046); the return target lives in sessionStorage.
  @ui
  Scenario: AUTH-19 no sign-in request carries a postcode in its URL, body or Referer
    Given the user is signed out on the result for a sample postcode (NB1 4XY)
    When the user signs in by any of the three methods
    Then no request to the sign-in service carries the postcode in its URL path, query string, body or Referer header

  @ui
  Scenario: AUTH-20 the sign-in callbackURL is a path only
    Given the user is signed out on the result for a sample postcode (NB1 4XY)
    When the user asks for an email link or continues with a provider
    Then the callbackURL sent is a path with no query string and no postcode, and the return target is held in the tab's session storage only

  @ui
  Scenario: AUTH-21 the magic-link token is in no log
    Given the user asks for an email link and opens it
    When the server, hosting, tracing and error-report logs are searched
    Then no entry contains "token=" or the token's value

  @ui
  Scenario: AUTH-22 signing out ends the session and signed-in pages are never cached
    Given the user is signed in
    When the user signs out and then presses Back
    Then every signed-in page and the sign-out response carry "Cache-Control: no-store", and after sign-out the back button does not show the signed-in page

  @ui
  Scenario: AUTH-23 signing out clears the chat sidebar from the page
    Given the user is signed in and the sidebar lists saved areas and past chats
    When the user signs out
    Then the page shows the signed-out state and the saved areas, chat titles and account link are not in the page

  @ui
  Scenario: AUTH-24 Sign out everywhere ends every session of the account
    Given the user is signed in on two devices
    When the user chooses "Sign out everywhere" on one
    Then both devices are signed out, and the next request from the other device, a read or a write, is refused as signed out (AUTH-25, AUTH-27)

  # Review Focus 2: the 15-minute token may not have expired yet.
  @ui
  Scenario: AUTH-25 a revoked session's unexpired token is refused on a write
    Given a user signed out, or signed out everywhere, and the 15-minute token they held has not yet expired
    When a request with that token sends a message or saves an area
    Then the server refuses it because the session no longer exists, no model call is made and nothing is stored

  # FE-13 (founder: "AI badge on the entry"), kept for the pilot by 0058. Replaces CHAT-03 (with WCHAT-08).
  @ui
  Scenario: AUTH-26 the "Ask about this area" entry on Check an area carries the AI badge
    Given the user, signed in or signed out, is on Check an area
    When the user checks a complete postcode (fixture NB1 4XY)
    Then the "Ask about this area" entry shows the "AI" badge (FE-13)

  # Review Focus 2, final review (16 Nov 2026): the API checks that the session still exists on every request, reads too, not only the token (0058, 16 Nov board-review note; agent's call, open to the founder).
  @ui
  Scenario: AUTH-27 a revoked session's unexpired token is refused on a read
    Given a user signed out, or signed out everywhere, and the 15-minute token they held has not yet expired
    When a request with that token lists the chats, opens a past chat or lists the saved areas
    Then the server refuses it because the session no longer exists, and the response holds no chat, message or saved area

  # Plan Task 3 and the site plan: the council page's entry and Save lead to sign-in like the area result's (AUTH-15).
  @ui
  Scenario: AUTH-28 on a council page, the chat entry and Save lead to sign-in when signed out
    Given the user is signed out and has opened the council page for council "E06999001"
    When the user chooses "Ask about this area" or Save
    Then the sign-in page opens, and the council page is still there to return to
