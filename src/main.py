"""Application entry point."""

import sys
from pathlib import Path

# Ensure the project root is on sys.path so "from src import ..." works
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import uvicorn

from src.backend.app import create_app
from src.utils.config import load_settings

if __name__ == "__main__":
    settings = load_settings()
    server_cfg = settings.get("server", {})
    app = create_app()

    uvicorn.run(
        app,
        host=server_cfg.get("host", "127.0.0.1"),
        port=int(server_cfg.get("port", 8765)),
        log_level=server_cfg.get("log_level", "info"),
    )
