"""FastAPI application setup."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.ai_gateway.gateway import AIGateway
from src.backend.project_manager import ProjectManager
from src.backend.test_runner import TestRunner
from src.utils.config import load_settings

container: dict = {}

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def create_app() -> FastAPI:
    settings = load_settings()
    app = FastAPI(title="Playwright Agents", version="1.0.0")

    ai = AIGateway(settings)
    pm = ProjectManager(data_path=DATA_DIR)
    runner = TestRunner(ai, DATA_DIR)

    container["config"] = settings
    container["ai"] = ai
    container["project_mgr"] = pm
    container["test_runner"] = runner

    from src.backend.routes_api import router as api
    from src.backend.routes_ws import router as ws
    app.include_router(api)
    app.include_router(ws)

    if FRONTEND_DIR.exists():
        app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

    return app
