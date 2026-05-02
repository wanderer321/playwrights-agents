"""Application entry point."""

import os
import sys
from pathlib import Path

# Ensure the project root is on sys.path so "from src import ..." works
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Add Python Scripts directory to PATH so minitest.exe and other CLI tools are found
_scripts_dir = Path(sys.executable).parent / "Scripts"
if _scripts_dir.is_dir():
    scripts_str = str(_scripts_dir)
    if scripts_str not in os.environ.get("PATH", ""):
        os.environ["PATH"] = scripts_str + os.pathsep + os.environ.get("PATH", "")

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
