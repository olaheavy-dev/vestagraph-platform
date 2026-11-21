@screen @buying @renting
Feature: The chat, for when sign-in opens (the signed-in chat's scenarios that need an account, saved areas, past chats or history)
  Kept for when sign-in opens (0063 point 2); not part of the pilot.
  These scenarios moved unchanged, with their WCHAT numbers, from the workspace chat's specification (now chat.feature, the pilot's anonymous chat) on 21 Nov 2026. They describe 0058's signed-in chat: an account, saved areas, past chats, the sidebar, the 12-month history and the count per account. They are all `@ui`, so `make test` parses them and does not run them. When sign-in opens, a decision brings the ones it needs back into chat.feature and records the change; until then, change nothing here. `make test` parses these scenarios and skips them because they are `@ui`; the playwright-bdd UI suite (SP-03) must exclude this file until a `later` tag exists (issue #374).
  Fixtures to add (issue #302): a source with a newer edition than a stored widget (WCHAT-40), a source that is Unavailable when a stored widget is updated (WCHAT-110) and a list of 20 saved areas (WCHAT-48, WCHAT-49), plus the chat lists WCHAT-46, WCHAT-98 and WCHAT-103 need (chats in several date groups, more than 15 chats, chats to search; #302 extended 19 Nov 2026); the test setup builds them, and the build adds any data they need.
  Elsewhere: sign-in is in sign-in.feature and the account pages are in account.feature, both kept for later (0063); the chat the pilot runs is in chat.feature.

  # Replaces CHAT-25 (a new postcode cleared the chat; chats are now kept), with WCHAT-40.
  @ui
  Scenario: WCHAT-07 a returning user opens a new chat with the last chat first in the sidebar
    Given a signed-in user has past chats and saved areas
    When the workspace page loads
    Then a new empty chat is open, the sidebar lists the last chat first, and no earlier message is shown in the chat

  # Past chats. Review Focus 4.
  @ui
  Scenario: WCHAT-40 a past chat shows its stored widget with its source date and an Update button
    Given a past chat holds a widget for a sample postcode (NB1 4XY), and the source has a newer edition (fixture to add, #302)
    When the user reopens the chat
    Then the widget shows the stored figures with their original source date and an Update button, and nothing on it looks current

  @ui
  Scenario: WCHAT-41 Update fetches fresh data with no model call and does not count toward the 15
    Given a past chat's widget is open
    When the user chooses Update
    Then the widget shows the newer edition with its date, the fake AI provider received no request, and the user's count for the day is unchanged (FE-62)

  @ui @ai03
  Scenario: WCHAT-42 after Update the earlier words stay and are marked as written about the earlier data
    Given a past chat's widget has been updated
    When the chat is shown
    Then the earlier words stay, each marked "Written about the data from <date>" with the old date, and the new figures are not described by them

  # FE-54.
  @ui
  Scenario: WCHAT-43 a chat is titled with the first words of its first message
    Given a signed-in user sends a first message in a new chat
    When the message is sent
    Then the chat appears in the sidebar titled with the first words of that message

  @ui
  Scenario: WCHAT-44 the user can rename a chat
    Given a chat is titled from its first words
    When the user renames it and saves
    Then the sidebar and the account page show the new title, and it stays after a reload

  @ui
  Scenario: WCHAT-45 a chat open in two tabs shows a notice in the second
    Given the same chat is open in one tab
    When it is opened in a second tab
    Then the second tab says "This chat is open in another tab" with the one action Reload, and sends nothing

  @ui
  Scenario: WCHAT-46 a returning user's past chats are grouped by Europe/London days in the sidebar
    Given a signed-in user has chats from today, this week, this month and earlier
    When the user opens the sidebar's chat list
    Then the chats are grouped Today, This week, This month and Older by Europe/London days, with weeks starting on Monday (FE-65)

  # Saved areas.
  @ui
  Scenario: WCHAT-47 a user can save an area from a widget
    Given a signed-in user has a widget for a sample postcode (NB1 4XY)
    When the user chooses Save
    Then the area appears under saved areas in the sidebar, and a confirmation says "Saved"

  @ui
  Scenario: WCHAT-48 an account can keep up to 20 saved areas
    Given a signed-in user has 19 saved areas (fixture to add, #302)
    When the user saves one more
    Then it is saved, and the account has 20 (FE-53)

  @ui
  Scenario: WCHAT-49 saving a 21st area is refused with the one action of removing one first
    Given a signed-in user has 20 saved areas (fixture to add, #302)
    When the user tries to save another
    Then nothing is saved, and the message says the limit is reached and offers one action: remove one first

  @ui
  Scenario: WCHAT-50 saving an area already saved, written differently, is shown as already saved
    Given a signed-in user has saved "NB1 4XY"
    When the user saves the same postcode written "nb14xy"
    Then no second copy is made, and the confirmation says "Already saved"

  # Builder notes: saved areas reach the model through a tool.
  @ui @ai03
  Scenario: WCHAT-51 the list_saved_areas tool returns typed data, never prompt text
    Given a signed-in user has saved areas
    When the model calls the saved-areas tool (fake AI provider)
    Then the tool result is typed data with the area's postcode and name fields, and the server did not paste the saved areas into the instructions or the user's message as text

  @ui @ai03
  Scenario: WCHAT-52 "Compare my two saved areas" compares them from the tools
    Given a signed-in user has exactly two saved areas, NB1 4XY and NB7 1RR
    When the user asks "Compare my two saved areas"
    Then a compare table is drawn from the tool results for both, each side with its own levels, source stamps and "Not known" where a record is missing, with no verdict words

  @ui
  Scenario: WCHAT-53 deleting a saved area leaves past chats readable with their stored widgets
    Given a past chat holds a widget for a saved area
    When the user removes that saved area and reopens the chat
    Then the chat and its stored widget are still readable, and the widget no longer shows as saved

  # The hide at once, the server's commit 10 seconds after the request and Undo are ACCT-26, ACCT-10 and ACCT-09, as for any deleted chat.
  @ui
  Scenario: WCHAT-57 deleting a chat while it streams stops the answer
    Given an answer is streaming in a chat
    When the user deletes that chat
    Then the stream stops and no more sentences appear

  @ui
  Scenario: WCHAT-64 deleting a chat deletes its traces when the delete commits
    Given a chat has traces and the user deletes it
    When the server commits the delete, 10 seconds after the request
    Then the chat's traces are deleted with it

  # Added 16 Nov 2026 (final review of the specifications): access control, splits of scenarios with several outcomes, and gaps.
  # OWASP's broken access control (0058 "Secure"): the server checks that every ID belongs to the signed-in account.
  @ui @ai03
  Scenario: WCHAT-93 the saved-areas tool returns only the signed-in user's saved areas
    Given two signed-in users each have saved areas, user A "NB1 4XY" and user B "NB7 1RR"
    When the model calls the saved-areas tool in user A's chat (fake AI provider)
    Then the tool result holds user A's saved areas only, and none of user B's

  @ui
  Scenario: WCHAT-94 a message or an Update sent to another account's chat is refused as not found
    Given user B has a chat with a widget, and user A is signed in
    When user A sends a message to that chat, or chooses Update on its widget, by the chat's ID, straight to the server
    Then the server refuses each as not found, no model call is made, and user B's chat is unchanged

  # FE-65 (agent's call, approved by the founder on 18 Nov 2026 (prompt window, "Keep all (Recommended)")).
  @ui
  Scenario: WCHAT-98 the sidebar shows 5 chats, and "Show more" adds 10 at a time
    Given a signed-in user has more than 15 chats
    When the user opens the sidebar and chooses "Show more"
    Then the sidebar first lists the newest 5 chats, and "Show more" adds the next 10 below them

  @ui
  Scenario: WCHAT-100 a chat deleted while it streams stores nothing more of the answer
    Given an answer is streaming in a chat
    When the user deletes that chat
    Then the server stores nothing more of that answer after the delete request

  @ui
  Scenario: WCHAT-101 Undo on a chat deleted while it streamed brings it back as it stood
    Given a user deleted a chat while its answer streamed, and 10 seconds have not passed since the request
    When the user chooses Undo
    Then the chat is back in the sidebar with the part of the answer stored before the delete, and no new answer is started

  # FE-65: the sidebar's title search (the account page's is ACCT-06).
  @ui
  Scenario: WCHAT-103 the sidebar's search lists only chats whose title matches
    Given a signed-in user has chats with different titles
    When the user searches the sidebar for a word from one title
    Then only the chats whose title contains that word are listed

  @ui
  Scenario: WCHAT-104 the sidebar's search word is in no address and no log
    Given a signed-in user has chats with different titles
    When the user searches the sidebar for a word
    Then the word is sent in the request body, in no URL path, query string or Referer header, and no log entry contains it (FE-65)

  # Rule 7: Unavailable is said, the stored figures stay dated, and nothing looks current.
  @ui @ai03
  Scenario: WCHAT-110 Update when the source is now Unavailable keeps the stored figures, dated
    Given a past chat's widget is open and its source is now Unavailable (fixture to add, #302)
    When the user chooses Update
    Then the widget says the source is Unavailable now and keeps the stored figures with their original source date, never shown as current
