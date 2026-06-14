"""Application configuration and logging setup."""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dependency is declared in requirements.
    load_dotenv = None

if load_dotenv:
    load_dotenv()


def _setting(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is not None:
        return value
    try:
        import streamlit as st

        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        return default
    return default


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


class AppSettings(BaseModel):
    """Environment-driven settings for local and cloud deployments."""

    app_name: str = "AI Business Automation Agent"
    app_tagline: str = "Enterprise AI workflows for operations, strategy, and executive productivity."
    environment: str = Field(default_factory=lambda: _setting("APP_ENV", "development") or "development")
    openai_api_key: str | None = Field(default_factory=lambda: _setting("OPENAI_API_KEY"))
    openai_model: str = Field(default_factory=lambda: _setting("OPENAI_MODEL", "gpt-4.1-mini") or "gpt-4.1-mini")
    temperature: float = Field(default_factory=lambda: float(_setting("OPENAI_TEMPERATURE", "0.35") or "0.35"))
    max_tokens: int = Field(default_factory=lambda: int(_setting("OPENAI_MAX_TOKENS", "2200") or "2200"))
    demo_mode: bool = Field(default_factory=lambda: _as_bool(_setting("DEMO_MODE"), False))
    log_level: str = Field(default_factory=lambda: _setting("LOG_LEVEL", "INFO") or "INFO")
    output_dir: Path = Field(default_factory=lambda: Path(_setting("OUTPUT_DIR", "outputs") or "outputs"))

    @property
    def has_openai_key(self) -> bool:
        return bool(self.openai_api_key and self.openai_api_key.strip())

    @property
    def effective_demo_mode(self) -> bool:
        return self.demo_mode or not self.has_openai_key


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()


def configure_logging() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
