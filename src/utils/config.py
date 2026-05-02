"""Configuration loader — merges settings.yaml with environment variables."""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
SETTINGS_PATH = CONFIG_DIR / "settings.yaml"
ENV_PATH = CONFIG_DIR / ".env"


def load_settings(path: Path | None = None) -> dict[str, Any]:
    """Load settings.yaml, then overlay environment variables."""
    load_dotenv(ENV_PATH)

    path = path or SETTINGS_PATH
    if path.exists():
        with open(path, encoding="utf-8") as f:
            cfg: dict = yaml.safe_load(f) or {}
    else:
        cfg = {}

    # --- overlay env vars ---
    env_map = {
        "ai.provider": "AI_PROVIDER",
        "ai.model": "AI_MODEL",
        "ai.api_key": "AI_API_KEY",
        "ai.base_url": "AI_BASE_URL",
        "ai.temperature": "AI_TEMPERATURE",
        "ai.max_tokens": "AI_MAX_TOKENS",
        "server.host": "SERVER_HOST",
        "server.port": "SERVER_PORT",
        "server.log_level": "LOG_LEVEL",
        "playwright.version": "PLAYWRIGHT_VERSION",
        "playwright.default_project": "PLAYWRIGHT_PROJECT",
        "playwright.timeout": "PLAYWRIGHT_TIMEOUT",
    }

    def _set_nested(d: dict, key: str, value: Any) -> None:
        parts = key.split(".")
        for p in parts[:-1]:
            d = d.setdefault(p, {})
        d[parts[-1]] = value

    for cfg_key, env_key in env_map.items():
        val = os.environ.get(env_key)
        if val is not None:
            # Type coercion for known numeric keys
            if cfg_key in ("ai.temperature",):
                val = float(val)
            elif cfg_key in ("ai.max_tokens", "server.port", "playwright.timeout"):
                val = int(val)
            _set_nested(cfg, cfg_key, val)

    return cfg


def get_api_key(name: str = "ALIYUN_BAILIAN_API_KEY") -> str | None:
    """Read an API key from environment (already loaded via dotenv)."""
    return os.environ.get(name)
