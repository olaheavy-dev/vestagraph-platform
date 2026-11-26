"""Settings from the environment (and .env locally), read once per process.

Names are the upper-case field names with no prefix (APP_ENV, LOG_LEVEL, VESTAGRAPH_COMMIT, ...).
From the founder's house-template-fastapi v0.11.1, without the database, storage and model settings.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ENV_FILE="" turns the file off: the tests set it before any app code loads, so a
    # developer's backend/.env (real keys included) never reaches them.
    # hide_input_in_errors: a validation error must never echo the raw input, which may hold a key.
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE", ".env") or None,
        extra="ignore",
        frozen=True,
        hide_input_in_errors=True,
    )

    app_env: Literal["local", "test", "production"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    # JSON logs in production; readable console logs everywhere else.
    log_json: bool = False
    # Largest request body the API reads, in bytes; larger ones get a 413 (16 KiB).
    max_request_bytes: int = Field(default=16_384, gt=0)
    # The commit the image was built from, shown by /healthz; set by the release build.
    vestagraph_commit: str = "unknown"
    # Where the fixture data lives; the default is the repository's packages/fixtures.
    fixtures_dir: Path = Path(__file__).resolve().parents[3] / "fixtures"
    # The area check stays off until the launch guard allows it (it answers 503 while off).
    area_check_open: bool = False
    # Interactive API docs at /docs. Unset means on everywhere except production. The schema at
    # /openapi.json stays on in every environment.
    docs_enabled: bool | None = None

    # Browser origins allowed to call the API (CORS), e.g. ["https://app.example.com"]. Empty
    # means none: same-origin and server-to-server calls only.
    cors_origins: list[str] = []
    # Host headers the API answers to, e.g. ["api.example.com"]; ["*"] accepts any.
    allowed_hosts: list[str] = ["*"]

    @property
    def docs_on(self) -> bool:
        return self.app_env != "production" if self.docs_enabled is None else self.docs_enabled


@lru_cache
def get_settings() -> Settings:
    return Settings()
