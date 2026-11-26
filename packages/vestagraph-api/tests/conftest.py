"""Test setup: turn the .env file off before any vestagraph_api code loads, so a developer's real
.env (keys included) never reaches the tests. settings.py reads ENV_FILE once, at import."""

import os

os.environ["ENV_FILE"] = ""
