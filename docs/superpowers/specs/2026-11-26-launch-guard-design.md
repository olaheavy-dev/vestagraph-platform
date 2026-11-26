# Launch guard (OP-06): design

Date: 26 Nov 2026. Size: a small change. Register line: OP-06 (`docs/decisions/README.md`). Status: approved (founder, 26 Nov 2026, prompt window: "Approve (Recommended)", with the agent's calls in "Left to the builder").

## Intent and why

The pilot's pages show unfinished text on purpose (SE-07): the Privacy notice's legal parts read "To be written before launch (SE-02)", and other pages hold similar draft lines. OP-06 (founder, 19 Nov 2026: "Yes, at stage 5b (Recommended)") makes the release fail while any of those strings is in what visitors see, because nothing else stops a draft reaching the public (benchmark B7).

## Founder's choices (26 Nov 2026, prompt windows)

- **Where it bites:** "Release only (Recommended)". The guard runs in the release job, after the founder's approval and before the image is pushed. Pull requests and CI are not blocked by draft strings, because the drafts are meant to exist while we build.
- **When to build:** "Now, wired into the release (Recommended)". It is built before the real pages exist (#86), so it protects their first release. Today it finds nothing: the placeholder serves only `/healthz`.
- **How it checks:** "A. Run image, read pages (Recommended)". It starts the newly built image on the runner and reads the pages it serves, so it checks what visitors get.

## Goals, non-goals, anti-goals

- Goal: a release whose pages contain any listed draft string fails before the push, and the log names the string and the page.
- Goal: the list of draft strings cannot fall behind the specifications.
- Non-goal: checking that required pages exist (for example that `/privacy` is there). A missing page is not OP-06's job.
- Non-goal: blocking pull requests or `make check` on draft strings.
- Anti-goal: a guard that passes when it could not read the pages. If the app does not start, or a page answers with a server error or cannot be fetched, the release fails (rule 7 in spirit: "could not check" is never shown as a clean result).

## Approaches considered

- **A. Run the built image and read its pages (chosen).** Checks exactly what visitors get, including text the build assembles. Adds about a minute to a release. Text drawn only by JavaScript in the browser would be missed; #86 settles how its pages are rendered and, if needed, extends the guard.
- B. Search the files inside the built image: fast, but misses text assembled at run time and fires on text visitors never see.
- C. Search the source code at the released commit: simplest, but furthest from what visitors see.

## Design

1. **The list:** `tools/launch_placeholders.json`, a JSON array of the exact draft strings. It starts with the four in the specifications today: "To be written before launch (SE-02)", "Contact details to be added before launch", "To be completed after testing, before launch", "Draft wording, to be confirmed before launch (0057)." Strings are only removed by a pull request that also removes them from the specifications.
2. **The sync test:** a pytest test reads every `docs/specs/**/*.feature` file and finds each quoted string containing "before launch". It fails if one is missing from the list, naming the file and line.
3. **The tool:** `tools/launch_guard.py`, standard library only (like `tools/release_check.py`), with unit tests. Given a base URL, the list file and a fixed list of paths (`/`, `/how-it-works`, `/privacy`, `/accessibility`), it:
   - waits for `/healthz` to answer (with a timeout);
   - fetches each fixed path, then follows same-site links (`href` on the same host) found in HTML pages, up to a page limit;
   - for each response body, decodes HTML entities (`&amp;`, `&#39;` and so on) and collapses whitespace, then looks for each listed string;
   - treats a 404 as "no page here" (its body is still checked); treats a server error, a timeout or a failed fetch as a failure of the guard;
   - exits 1 if any string is found or any page could not be read, printing each page and string; otherwise exits 0, printing how many pages it read.
4. **The release step** in `.github/workflows/images.yml`, after "Build the image from the approved commit" and before "Log in to GHCR": write a throwaway secret file, start the image with `docker run` (read-only, with that file at `/run/secrets/secret_check`, port 8080 published on the runner's localhost only), run main's copy of the guard against it (copied before the checkout, as the release check is), then stop and remove the container. `tools/launch_guard.py` and `tools/launch_placeholders.json` join the workflow's paths. Using main's copy means a rollback to an older commit whose pages still hold drafts is also stopped.
5. **Records:** OP-06's register line gains the "where, when and how" above; `deploy/README.md` and the deployment notes say a release can fail at the guard and what to do; the status file is updated.

## Review fixes (26 Nov 2026)

The pre-push reviews found that markup can split a draft string (React's server rendering puts `<!-- -->` between joined text parts; `<em>` does the same), so the guard also searches each page's text with tags and comments taken out, and ignores soft hyphens and zero-width characters. Redirects are no longer followed automatically: one is followed only when it stays on the site, so the guard never reads the live site instead of the new image. A page over 5 MB, or a link that is not a valid URL, is reported, not a crash. Pages are decoded with the charset they declare. The step now cleans up with a `trap`, uses `deploy/compose.yml`'s memory and process limits, and stops the image's own output from sending workflow commands. Codex's review then found that `<br>` and block elements joined words ("writtenbefore") and that a redirect loop passed with no page read: a line break or block element now counts as a space, and each redirect chain is followed to its page, with a loop or more than 10 hops reported as an unread page. Note for #86: `<link href>` targets (stylesheets, preloads, icons) are read too, and count towards the 200-page limit.

## Left to the builder

- The page limit (proposed 200) and the timeouts (proposed: 60 s for the app to start, 10 s per page).
- The exact `docker run` options, matching `deploy/compose.yml`'s security settings where they apply on the runner.

## Merge

`images.yml` is on the founder-only list, so the founder merges this pull request.
