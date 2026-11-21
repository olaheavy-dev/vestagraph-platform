@screen @buying @renting
Feature: Your account (the pilot's account pages: saved areas, chats, sign-in methods and deleting)
  Kept for when sign-in opens (0063 point 2); not part of the pilot. Written 16 Nov 2026 for decision 0058; accounts, saved areas and chat history left the pilot on 20 Nov 2026 (0063). The scenarios the chat page shared with these pages (renaming, the sidebar's list, saving, deleting a chat) are in chat-signed-in-later.feature. These scenarios stay as they are until sign-in opens and a decision brings them back.
  Added 16 Nov 2026 (decision 0058 choices 1 and 6, its Builder notes and its 16 Nov board-review note; register lines FE-53, FE-65, FE-66 and SE-06).
  Question it answers: "What does Vestagraph keep about me, and how do I change or delete it?"
  Modes: both. Signed in only: anyone not signed in goes through sign-in first (sign-in.feature, FE-56).
  Fixtures: saved areas are sample postcodes from `packages/fixtures/data/postcode-area.json` (NB1 4XY, NB7 1RR); figures: none.
    The accounts, emails, chats and saved areas in these scenarios are made up for the test run (rule 5): no real address, no real provider account.
    Fixtures to add (issue #302): an account with 20 saved areas (ACCT-02) and one with more than 20 chats spread over today, this week, this month and earlier (ACCT-04, ACCT-05; #302 extended 19 Nov 2026 to cover these); the test setup builds them.
  Where: `/account` is an overview: the newest 3 saved areas and the newest 3 chats, each with "See all", the sign-in methods, Sign out, Sign out everywhere, how long things are kept, and Delete account. `/account/areas` lists every saved area and `/account/chats` lists the chats (FE-66). Boards: SignedInAccount, SignedInAccountPhone, SignedInAccountAreas, SignedInAccountAreasPhone, SignedInAccountChats and SignedInAccountChatsPhone, each with its Dark twin, on the canvas page "Pilot · Signed-in chat"; the Undo toast and the confirm dialog are FeedbackKit's, on "Brand and style".
  Deleting one item (0058, board-review ruling): deleting one chat or removing one saved area hides it at once and shows the kit's Undo toast; the server commits the delete itself 10 seconds after the request, so it happens even if the browser closes or crashes; Undo is a request to the server before then; the toast does not pause on hover or focus. "Delete all chats" asks first instead.
  Sign-in methods (0058, board-review note): the Email link row has no Remove. The rule that the last sign-in method can't be removed counts only Google and GitHub.
  "Use" (0058 choice 6): a chat is used when it is opened or a message is sent in it, and is deleted 12 months after the later of the two. An account is used by any request with a valid sign-in, and is deleted 24 months after the last one, with no warning email. Traces are kept 30 days (0058 choice 9; WCHAT-63).
  The server checks in these scenarios (database rows, deletion jobs, refusals, logs) are tagged @ui, as in chat.feature: they run in the same playwright-bdd suite against the running stack (SP-03). Time-based scenarios set the server's clock in the test; they never wait.
  Copy: the fixed texts are the chat texts in chat.feature. Every quoted message here, including "Undo available for 10 seconds" and "An email link always reaches your account at this verified address. To stop it, delete your account.", was proposed wording from the boards (drawn at the board review); these two texts were approved by the founder on 18 Nov 2026 (prompt window, "Approve as written (Recommended)"). Other messages here are finalised in the build.
  AI: no scenario here calls a model, so none is an AI-03 case.
  Elsewhere: (these WCHAT scenarios are in chat-signed-in-later.feature) renaming a chat from the sidebar is WCHAT-44, the sidebar's own chat list is WCHAT-46, WCHAT-98, WCHAT-103 and WCHAT-104, saving an area and the 20 limit are WCHAT-47 to WCHAT-50, a deleted saved area's past chats are WCHAT-53, a chat deleted while it streams is WCHAT-57, WCHAT-100 and WCHAT-101, its traces are WCHAT-64; Sign out and Sign out everywhere are AUTH-22 to AUTH-25 and AUTH-27.
  Required states (plan docs/superpowers/plans/2026-11-16-signed-in-chat.md Task 3 and Task 7 step 1; Review Focus 2; FE-53, FE-65, FE-66; AGENTS.md rules 5 and 7):
    the /account overview with its own pages -> ACCT-01
    saved areas: the list of up to 20 and its limit line, remove with Undo -> ACCT-02, ACCT-22, ACCT-03
    chats: newest 20 then "Show more", grouped by day, title search, the number found, nothing found, search words in no address or log -> ACCT-04, ACCT-05, ACCT-06, ACCT-37, ACCT-38, ACCT-39
    rename a chat -> ACCT-07; delete one chat with Undo: hidden at once, the toast and its announcement, focus on Undo, no pause -> ACCT-08, ACCT-40, ACCT-41, ACCT-42
    another account's chat or saved area, by its ID: refused as not found -> ACCT-35, ACCT-36 (and WCHAT-93, WCHAT-94)
    Undo is a request to the server; the server hides the item at once and commits after 10 seconds, even if the browser closes -> ACCT-09, ACCT-26, ACCT-32, ACCT-33, ACCT-10
    the saved-area Remove and Undo requests keep the postcode out of every address and log -> ACCT-27, ACCT-34
    "Delete all chats" asks first, and what it deletes -> ACCT-11, ACCT-12
    the Email link row has no Remove -> ACCT-13; the last of Google and GitHub can't be removed, on the page and at the server, and with both either can go, and what stays -> ACCT-14, ACCT-23, ACCT-24, ACCT-29, ACCT-30
    deleting the account needs a fresh sign-in -> ACCT-15, ACCT-25, ACCT-31
    deleting removes chats, saved areas, the daily count, traces, the sign-in tables and the email service's copy -> ACCT-16
    nothing is written after the delete, even with an unexpired token (Review Focus 2) -> ACCT-17; a pending email link stops working -> ACCT-28
    retention shown on the page; chats after 12 months, idle accounts after 24 months, traces after 30 days -> ACCT-18, ACCT-19, ACCT-20 (traces: WCHAT-63)
    empty: no saved areas, no chats -> ACCT-21

  # FE-66.
  @ui
  Scenario: ACCT-01 the account overview shows the newest 3 of each with "See all", and links to their own pages
    Given a signed-in user has 10 saved areas and more than 3 chats
    When the user opens /account
    Then the page shows the newest 3 saved areas with the count "10 of 20" and "See all" to /account/areas, the newest 3 chats with "See all" to /account/chats, the sign-in methods, Sign out, Sign out everywhere, how long things are kept and Delete account

  # FE-53, FE-65: at most 20, so no paging.
  @ui
  Scenario: ACCT-02 the saved areas page lists every saved area, with no paging
    Given a signed-in user has 20 saved areas (fixture to add, #302)
    When the user opens /account/areas
    Then all 20 are listed on one page with no "Show more" and no pages, each with Remove

  @ui
  Scenario: ACCT-22 the saved areas page states the limit of 20
    Given a signed-in user has saved areas
    When the user opens /account/areas
    Then a line says an account can keep up to 20 saved areas (FE-53) and that, at 20, one must be removed before saving another

  @ui
  Scenario: ACCT-03 removing a saved area hides it at once with Undo, and past chats stay
    Given a signed-in user has saved "NB7 1RR" and has a past chat about it
    When the user chooses Remove on "NB7 1RR" on /account/areas
    Then "NB7 1RR" is hidden at once from every list, the Undo toast says the area is no longer saved and that past chats about it stay as they are, with "Undo available for 10 seconds", and nothing asks to confirm first

  # FE-65: the account page shows the newest 20, then "Show more" loads the next 20 in place.
  @ui
  Scenario: ACCT-04 the chats page shows the newest 20, then "Show more" adds the next 20
    Given a signed-in user has more than 20 chats (fixture to add, #302)
    When the user opens /account/chats and chooses "Show more"
    Then the newest 20 are listed first, the next 20 are added in place below them, focus moves to the first new chat, and a status line says how many are shown out of the total

  # FE-65: Europe/London calendar days; the week starts on Monday.
  @ui
  Scenario: ACCT-05 chats are grouped Today, This week, This month and Older by Europe/London days
    Given a signed-in user has chats last used today, earlier this week, earlier this month and before this month (fixture to add, #302)
    When the user opens /account/chats
    Then they are listed under Today, This week, This month and Older, using Europe/London calendar days and weeks that start on Monday, newest first within each group

  # FE-65: the founder chose title search; search words never travel in an address or reach a log.
  @ui
  Scenario: ACCT-06 the chats page searches by title
    Given a signed-in user is on /account/chats
    When the user searches a word from one chat's title
    Then only the chats whose title contains the word are listed

  # FE-54. Renaming from the sidebar is WCHAT-44.
  @ui
  Scenario: ACCT-07 the user can rename a chat on the chats page
    Given a signed-in user is on /account/chats
    When the user chooses Rename on a chat, types a new title and chooses "Save name"
    Then the chat shows the new title on /account/chats, in the sidebar and on /account, and it stays after a reload

  # 0058, board-review ruling: one delete happens at once with Undo, not a confirm.
  @ui
  Scenario: ACCT-08 deleting one chat hides it at once, with no confirm first
    Given a signed-in user is on /account/chats
    When the user chooses Delete on a chat
    Then the chat is hidden at once from every list, and nothing asks to confirm first

  @ui
  Scenario: ACCT-09 Undo asks the server to keep the item, before the 10 seconds end
    Given a signed-in user has just deleted a chat, or removed a saved area, and 10 seconds have not passed since the request
    When the user chooses Undo with a tap or with Enter
    Then the page sends the server an undo request, the item is back in every list, focus returns to the restored row, and after the 10 seconds nothing of it has been deleted

  # The server commits; the browser's toast is only the way to send Undo.
  @ui
  Scenario: ACCT-10 the server commits a delete 10 seconds after the request, even if the browser closes
    Given a signed-in user deleted a chat, or removed a saved area, and closed the browser straight after
    When 10 seconds have passed since the delete request (the test sets the server's clock)
    Then the server has deleted it on its own, with no further request from the browser, and a chat's traces are deleted with it (WCHAT-64)

  @ui
  Scenario: ACCT-11 "Delete all chats" asks first, and Cancel deletes nothing
    Given a signed-in user has 3 chats and is on /account/chats
    When the user chooses "Delete all chats…" and then Cancel
    Then a dialog first asks "Delete all chats?", says it deletes all 3 chats, their cards and the records kept to fix faults, that saved areas stay and that it can't be undone, and after Cancel all 3 chats are still there

  @ui
  Scenario: ACCT-12 confirming "Delete all chats" deletes every chat and its traces, and saved areas stay
    Given a signed-in user has chats with traces and has saved areas
    When the user chooses "Delete all chats…" and confirms
    Then every chat of that account and every trace of those chats is deleted, the chat lists show the kit's empty state, and every saved area is still there

  # 0058, board-review note: an email link always reaches the account at its verified address.
  @ui
  Scenario: ACCT-13 the Email link sign-in method has no Remove
    Given a signed-in user's account has Google and the email link as sign-in methods
    When the user opens /account
    Then the Email link row has no Remove button and says "An email link always reaches your account at this verified address. To stop it, delete your account."

  # The last-method rule counts only Google and GitHub (0058, board-review note); the email link is not counted, and it still works.
  @ui
  Scenario: ACCT-14 the last of Google and GitHub can't be removed
    Given a signed-in user's account has Google as its only Google or GitHub method, alongside the email link
    When the user opens /account
    Then Google's Remove is turned off, and the row says it is the last of Google and GitHub on this account so it can't be removed, and that to remove it the user can link GitHub first or delete the account

  @ui
  Scenario: ACCT-23 the server refuses to remove the last of Google and GitHub
    Given a signed-in user's account has GitHub as its only Google or GitHub method, alongside the email link
    When a request to remove GitHub is sent straight to the server
    Then the server refuses it and GitHub stays linked

  @ui
  Scenario: ACCT-24 with both Google and GitHub linked, either one can be removed
    Given a signed-in user's account has Google, GitHub and the email link
    When the user chooses Remove on Google
    Then Google is removed

  @ui
  Scenario: ACCT-29 after Google is removed, GitHub and the email link stay linked
    Given a signed-in user's account has Google, GitHub and the email link, and the user has removed Google
    When the user opens /account
    Then GitHub and the email link are still listed as linked

  @ui
  Scenario: ACCT-30 after Google is removed, GitHub's Remove is turned off as the last of Google and GitHub
    Given a signed-in user's account has Google, GitHub and the email link, and the user has removed Google
    When the user opens /account
    Then GitHub's Remove is turned off, and the row says it is the last of Google and GitHub on this account (the email link is not counted)

  # Delete account, step 1 and 2: a fresh sign-in confirms it is the user.
  @ui
  Scenario: ACCT-15 deleting the account needs a fresh sign-in, and nothing is deleted before it
    Given a signed-in user chooses Delete account
    When the page lists what will be deleted and asks the user to sign in again, and the user cancels at that step
    Then nothing has been deleted and the account is unchanged

  @ui
  Scenario: ACCT-25 an existing session alone can't delete the account
    Given a signed-in user has not signed in again since choosing Delete account
    When a delete-account request is sent with only the existing session, from the page or straight to the server
    Then the server refuses it and nothing is deleted

  @ui
  Scenario: ACCT-31 the account is deleted only after a fresh sign-in with one of its methods succeeds
    Given a signed-in user has chosen Delete account and been asked to sign in again
    When the fresh sign-in with one of the account's methods succeeds
    Then the account is deleted, and not before that sign-in

  # 0058 choice 6 and Builder notes: one database holds Better Auth's tables and ours, so deleting is one operation.
  @ui
  Scenario: ACCT-16 deleting the account removes everything kept about the user
    Given a signed-in user with chats, traces, saved areas and a daily message count has confirmed Delete account with a fresh sign-in
    When the delete has finished
    Then the database holds no row for that user in the chats, saved areas and daily count tables or Better Auth's user, session, account and verification tables, the trace store holds none of their traces, the email-sending service has been asked to delete its copy of the address, and the page says what was deleted, that the user is signed out and that Check an area and City Explorer stay open with no account

  # Review Focus 2: the 15-minute token may not have expired yet.
  @ui
  Scenario: ACCT-17 nothing is written for a deleted account, even with a token that has not expired
    Given a user deleted their account while another tab held a 15-minute token that has not yet expired and an answer was streaming there
    When that tab sends a message, saves an area or the streamed answer ends
    Then the server refuses each write because the account no longer exists, no model call is made, and no row, count or trace for that user is written after the delete

  # 0058 choice 6: the rules are on the account page and in the privacy notice.
  @ui
  Scenario: ACCT-18 the account page says how long each thing is kept
    Given a signed-in user is on /account
    When the page has loaded
    Then it says chats are deleted 12 months after their last use, the records of chats kept to fix faults are kept 30 days and only the person who runs Vestagraph can see them, and an account not used for 24 months is deleted with everything in it and no reminder, with a link to the privacy notice

  @ui
  Scenario: ACCT-19 a chat is deleted 12 months after it was last opened or last had a message sent, whichever is later
    Given a chat last had a message sent 13 months ago and was last opened 11 months ago (the test sets the server's clock)
    When the deletion job runs now, and again 1 month and 1 day later
    Then the chat is kept on the first run, because its last use was opening it 11 months ago, and deleted with its traces on the second

  @ui
  Scenario: ACCT-20 an account is deleted 24 months after its last use, with no warning email
    Given an account whose last request with a valid sign-in was 24 months and 1 day ago (the test sets the server's clock)
    When the deletion job runs
    Then the account is deleted with everything ACCT-16 lists, no email is sent to the user, and an account whose session made a valid request 23 months ago is kept

  @ui
  Scenario: ACCT-21 with no saved areas or no chats the pages show how to start
    Given a signed-in user has no saved areas and no chats
    When the user opens /account, /account/areas and /account/chats
    Then each list shows the kit's empty state with a small illustration, plain words and one action back to the chat

  # 0058, board-review ruling: the server hides the item at once, not only the page.
  @ui
  Scenario: ACCT-26 within the 10 seconds a deleted item is hidden everywhere, not only on the page
    Given a signed-in user has just deleted a chat, or removed a saved area, and 10 seconds have not passed since the request
    When the page is reloaded
    Then the reloaded page does not show the item

  @ui
  Scenario: ACCT-32 within the 10 seconds a deleted item is hidden in another tab
    Given a signed-in user has just deleted a chat, or removed a saved area, and 10 seconds have not passed since the request
    When the account is opened in another tab
    Then the other tab does not show the item

  @ui
  Scenario: ACCT-33 within the 10 seconds the server's lists do not return a deleted item
    Given a signed-in user has just deleted a chat, or removed a saved area, and 10 seconds have not passed since the request
    When the chat list and the saved-areas list are requested straight from the server
    Then neither response contains the item

  # Postcodes never in a URL or a log (0014, 0046).
  @ui
  Scenario: ACCT-27 removing a saved area and undoing it keep the postcode out of every address and log
    Given a signed-in user has saved "NB7 1RR"
    When the user removes it on /account/areas and then chooses Undo
    Then both requests name the saved area by its ID, with the postcode in no URL path, query string or Referer header

  @ui
  Scenario: ACCT-34 removing a saved area and undoing it leave no postcode in any log
    Given a signed-in user has saved "NB7 1RR"
    When the user removes it on /account/areas and then chooses Undo
    Then no server, hosting or error-report log entry contains the postcode

  # Review Focus 2 and 3: the verification rows go with the account (ACCT-16).
  @ui
  Scenario: ACCT-28 an email link sent before the account was deleted no longer signs in
    Given a user asked for an email link and then, within its 5 minutes (SE-06), deleted their account
    When the email link is opened
    Then the page says the link has expired or been used, nobody is signed in, and no new account is created

  # Added 16 Nov 2026 (final review of the specifications). OWASP's broken access control (0058 "Secure"): the server checks that every ID belongs to the signed-in account, and answers "not found" so it does not reveal that the ID exists.
  @ui
  Scenario: ACCT-35 a request about another account's chat is refused as not found
    Given user B has a chat, and user A is signed in
    When user A sends requests to open, rename, delete and undo the delete of that chat by its ID, straight to the server
    Then the server refuses each as not found, and user B's chat is unchanged

  @ui
  Scenario: ACCT-36 a request about another account's saved area is refused as not found
    Given user B has saved "NB7 1RR", and user A is signed in
    When user A sends requests to open, remove and undo the removal of that saved area by its ID, straight to the server
    Then the server refuses each as not found, and user B's saved area is unchanged

  # Split from ACCT-06.
  @ui
  Scenario: ACCT-37 the chats page announces the number of chats found once
    Given a signed-in user is on /account/chats
    When the user searches a word from one chat's title
    Then the status region announces the number found once

  @ui
  Scenario: ACCT-38 a chat search with no match shows "nothing found"
    Given a signed-in user is on /account/chats
    When the user searches a word in no chat's title
    Then the kit's "nothing found" empty state is shown

  @ui
  Scenario: ACCT-39 the chats page's search words are in no address and no log
    Given a signed-in user is on /account/chats
    When the user searches a word
    Then the word is sent in the request body, in no URL path, query string or Referer header, and no log entry contains it (FE-65)

  # Split from ACCT-08 (0058, board-review ruling).
  @ui
  Scenario: ACCT-40 the Undo toast says what was deleted, and its time is announced once
    Given a signed-in user is on /account/chats
    When the user chooses Delete on a chat
    Then the Undo toast says the chat is deleted with its cards and the records kept to fix faults, and the status region says once "Undo available for 10 seconds"

  @ui
  Scenario: ACCT-41 after deleting one chat, focus moves to Undo
    Given a signed-in user is on /account/chats
    When the user chooses Delete on a chat
    Then focus moves to the toast's "Undo" button, which is at least 44 px high

  @ui
  Scenario: ACCT-42 the Undo toast does not pause on hover or focus
    Given a signed-in user has just deleted a chat and the pointer and focus are on the Undo toast
    When 10 seconds have passed since the delete request (the test sets the server's clock)
    Then Undo is no longer available and the server has committed the delete (ACCT-10)
