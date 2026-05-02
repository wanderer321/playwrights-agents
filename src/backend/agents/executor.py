"""Executor — runs Playwright or Minium tests and parses results."""

from src.playwright_core.executor import PlaywrightExecutor
from src.backend.miniprogram.executor import MiniumExecutor


class Executor:
    """Run tests in a given project directory (H5 or MiniProgram)."""

    def __init__(self, project_dir: str, project_type: str = "h5", minium_config: dict | None = None):
        self.project_dir = project_dir
        self.project_type = project_type
        self.minium_config = minium_config or {}

    async def run(
        self,
        test_path: str | None = None,
        project: str = "chromium",
        log=None,
    ):
        if self.project_type == "miniprogram":
            engine = MiniumExecutor(self.project_dir, self.minium_config)
            return await engine.run_tests(
                test_path=test_path,
                log_callback=log,
            )
        else:
            engine = PlaywrightExecutor(self.project_dir)
            return await engine.run_tests(
                test_path=test_path,
                project=project,
                log_callback=log,
            )
