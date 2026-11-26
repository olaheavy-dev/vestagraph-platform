# Deploy files

These files run the placeholder app, which proves the hosting set-up before the real app exists.

| File | What it is |
|---|---|
| `placeholder.Dockerfile` | Builds the placeholder image. Build from the repository root with `--build-arg VESTAGRAPH_COMMIT=<sha>`. The image runs as user `10001` and listens on port 8080. |
| `compose.yml` | The Compose service for the server. It has two placeholders: `<CADDY_NETWORK>` (the name of the existing reverse-proxy network) and `<SECRETS_DIR>` (the server folder that holds the secret files). |
| `secrets.example` | The names of the secret files, one per line. Secrets travel as files, never as environment variables. |

## Secrets

Create one file for each name in `secrets.example`, inside `<SECRETS_DIR>`. Each file must be owned by user `10001` and have mode `0400`. Never commit a secret file.

Compose mounts each secret at `/run/secrets/<name>`, so the app reads `/run/secrets/secret_check`.

## One image

The server runs `vestagraph-placeholder-live:production`. Only the approved release job writes that package: after the founder approves, it builds the image from the approved `main` commit and pushes `sha-<commit>` and `production` with a token held by the `production` environment. To roll back, run the Images workflow by hand with an earlier `main` commit; it rebuilds that commit. A merge to `main` starts a release only when it changes the placeholder package, `deploy/`, `.dockerignore`, `tools/release_check.py`, the launch guard (`tools/launch_guard.py`, `tools/launch_placeholders.json`) or the Images workflow itself (22 Nov 2026; the launch guard files since 26 Nov 2026); a documentation-only merge queues nothing.

After the approval and the build, and before the push, the **launch guard** (OP-06) starts the new image on the runner and reads its pages. If a page holds a draft string such as "To be written before launch (SE-02)", or a page cannot be read, the release stops and nothing is pushed; the log names each page and string. The fix is to write the missing text, or, for a rollback, to choose a commit without draft text. The guard uses `main`'s copy of its list, so a rollback to a commit with drafts stops too.

## Where the server copy lives

The real server copy of `compose.yml`, with the placeholders filled in, lives in the private infrastructure repository. This folder holds only the public template.
