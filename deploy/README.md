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

## Two images

The build workflow publishes `sha-<commit>` tags to `vestagraph-placeholder`. The server runs `vestagraph-placeholder-live:production`. Only the approved release job writes that live package, with a token held by the `production` environment.

## Where the server copy lives

The real server copy of `compose.yml`, with the placeholders filled in, lives in the private infrastructure repository. This folder holds only the public template.
