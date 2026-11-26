# Deploy files

These files run the pilot API (#93), which replaced the placeholder app of the hosting foundation.

| File | What it is |
|---|---|
| `api.Dockerfile` | Builds the API image in two stages, with the base images pinned by digest. Build from the repository root with `--build-arg VESTAGRAPH_COMMIT=<sha>`. The image runs as user `10001`, listens on port 8080 and holds only the API, its workspace packages (`vestagraph-area`, `vestagraph-engine`) and the fixture data and schemas, not the tests or uv. |
| `compose.yml` | The Compose service `api` for the server. It has one placeholder: `<CADDY_NETWORK>` (the name of the existing reverse-proxy network). The API needs no secret. |

## The area check is closed

The image starts with `AREA_CHECK_OPEN` unset, so `POST /api/area-check` answers `503 Not available yet` and does not read the request body. Only the founder turns it on, together with the Privacy notice (decision 0014); it is an environment setting in the server's copy of `compose.yml`, not part of this template.

## One image

The server runs `vestagraph-api-live:production`. Only the approved release job writes that package: after the founder approves, it builds the image from the approved `main` commit and pushes `sha-<commit>` and `production` with a token held by the `production` environment. To roll back, run the Images workflow by hand with an earlier `main` commit; it rebuilds that commit. A merge to `main` starts a release only when it changes the API, area or engine package, the fixture data or schemas, `uv.lock`, `deploy/`, `.dockerignore`, `tools/release_check.py`, the launch guard (`tools/launch_guard.py`, `tools/launch_placeholders.json`) or the Images workflow itself (22 Nov 2026; the launch guard files since 26 Nov 2026; the API paths since #93); a documentation-only merge queues nothing.

After the approval and the build, and before the push, the **launch guard** (OP-06) starts the new image on the runner and reads its pages. If a page holds a draft string such as "To be written before launch (SE-02)", or a page cannot be read, the release stops and nothing is pushed; the log names each page and string. The fix is to write the missing text, or, for a rollback, to choose a commit without draft text. The guard uses `main`'s copy of its list, so a rollback to a commit with drafts stops too.

## Where the server copy lives

The real server copy of `compose.yml`, with the placeholder filled in, lives in the private infrastructure repository. This folder holds only the public template.
