"""Playwright installation and version management."""

import asyncio
import subprocess
import sys
from pathlib import Path


class PlaywrightInstaller:
    """Manage Playwright and browser installations."""

    def __init__(self, work_dir: str | Path | None = None):
        self.work_dir = Path(work_dir) if work_dir else Path.cwd()

    async def get_current_version(self) -> str:
        """Get installed Playwright version."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "npx", "playwright", "--version",
                cwd=str(self.work_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            return stdout.decode().strip()
        except Exception:
            return "not installed"

    async def install(self, version: str | None = None) -> str:
        """Install or update Playwright.

        Args:
            version: specific version (e.g. "1.59.1"), or None for latest
        Returns:
            Installed version string
        """
        # Step 1: Install/update npm package
        package = f"@playwright/test@{version}" if version else "@playwright/test@latest"

        proc = await asyncio.create_subprocess_exec(
            "npm", "install", "--save-dev", package,
            cwd=str(self.work_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()

        # Step 2: Install browsers
        proc2 = await asyncio.create_subprocess_exec(
            "npx", "playwright", "install", "chromium",
            cwd=str(self.work_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc2.communicate()

        return await self.get_current_version()

    async def list_browsers(self) -> list[dict]:
        """List installed browsers."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "npx", "playwright", "install", "--dry-run",
                cwd=str(self.work_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            # Parse the output to determine what's available
            lines = stdout.decode().splitlines()
            return [{"name": l.strip(), "installed": True} for l in lines if l.strip()]
        except Exception:
            return []
