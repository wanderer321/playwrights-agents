"""Playwright test execution wrapper."""

import asyncio
import json
import os
import shlex
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.utils.file_utils import ensure_dir


@dataclass
class SingleTestResult:
    title: str
    file: str
    status: str  # passed | failed | skipped
    duration_ms: float = 0
    error: str | None = None


@dataclass
class SuiteResult:
    title: str
    file: str
    tests: list[SingleTestResult] = field(default_factory=list)


@dataclass
class TestReport:
    task_id: str
    timestamp: str
    summary: dict
    suites: list[SuiteResult]
    raw_output: str = ""


class PlaywrightExecutor:
    """Run Playwright tests and capture results."""

    def __init__(self, project_dir: str | Path, config: dict | None = None):
        self.project_dir = Path(project_dir)
        self.config = config or {}
        self._report_dir = ensure_dir(self.project_dir / "test-results" / "reports")

    async def run_tests(
        self,
        test_path: str | None = None,
        project: str = "chromium",
        extra_args: list[str] | None = None,
        log_callback=None,
    ) -> TestReport:
        """Run Playwright tests and return a structured report.

        Args:
            test_path: relative path to test file or directory (None = all tests)
            project: browser project name (chromium, firefox, webkit)
            extra_args: additional CLI flags
            log_callback: async callable receiving log lines
        """
        cmd = ["npx", "playwright", "test", "--project", project, "--reporter", "json"]

        if test_path:
            cmd.append(str(test_path))

        if extra_args:
            cmd.extend(extra_args)

        if log_callback:
            await log_callback(f"[exec] cd {self.project_dir} && {' '.join(cmd)}\n")

        # Run the process (use shell on Windows for .cmd resolution)
        process = await asyncio.create_subprocess_shell(
            shlex.join(cmd),
            cwd=str(self.project_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout_chunks: list[str] = []
        stderr_chunks: list[str] = []

        async def _read_stream(stream, store, label):
            while True:
                line = await stream.readline()
                if not line:
                    break
                decoded = line.decode("utf-8", errors="replace")
                store.append(decoded)
                if log_callback:
                    await log_callback(decoded)

        await asyncio.gather(
            _read_stream(process.stdout, stdout_chunks, "stdout"),
            _read_stream(process.stderr, stderr_chunks, "stderr"),
        )

        await process.wait()

        stdout_text = "".join(stdout_chunks)
        stderr_text = "".join(stderr_chunks)
        raw_output = stdout_text + stderr_text

        # Parse JSON reporter output
        return self._parse_report(stdout_text, stderr_text, raw_output)

    def _parse_report(self, stdout: str, stderr: str, raw: str) -> TestReport:
        """Parse JSON output from playwright --reporter json."""
        import datetime

        report = TestReport(
            task_id=f"task_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.datetime.now().isoformat(),
            summary={
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "duration_ms": 0,
            },
            suites=[],
            raw_output=raw,
        )

        # Try to parse the JSON reporter output (last JSON block in stdout)
        try:
            # Find the first JSON object in stdout
            json_start = stdout.find("{")
            json_end = stdout.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                data = json.loads(stdout[json_start:json_end])
                self._populate_from_json(data, report)
            else:
                # Fall back to line-count heuristic
                report.summary["total"] = raw.count("passed") + raw.count("failed")
        except (json.JSONDecodeError, KeyError) as e:
            report.summary["error"] = f"Failed to parse results: {e}"

        return report

    def _populate_from_json(self, data: dict, report: TestReport) -> None:
        total = 0
        passed = 0
        failed = 0
        skipped = 0
        max_duration = 0.0

        def _process_suites(suites_data: list[dict], parent_file: str = "") -> list[SuiteResult]:
            suites: list[SuiteResult] = []
            nonlocal total, passed, failed, skipped, max_duration

            for suite_data in suites_data:
                file = suite_data.get("file", parent_file)
                suite = SuiteResult(
                    title=suite_data.get("title", ""),
                    file=file,
                )

                # Process specs at this level
                for spec in suite_data.get("specs", []):
                    for test_data in spec.get("tests", []):
                        results = test_data.get("results", [{}])
                        result = results[0] if results else {}
                        status = result.get("status", "unknown")
                        duration = result.get("duration", 0) / 1000  # ms
                        error = None
                        if result.get("errors"):
                            error = result["errors"][0].get("message", str(result["errors"][0]))

                        # Determine pass/fail: compare result.status to expectedStatus
                        expected = test_data.get("expectedStatus", "passed")
                        is_pass = status == expected or status in ("passed", "expected")
                        is_fail = status in ("failed", "unexpected", "timedOut")

                        t = SingleTestResult(
                            title=spec.get("title", test_data.get("title", "")),
                            file=file,
                            status=status,
                            duration_ms=duration,
                            error=error,
                        )
                        suite.tests.append(t)
                        total += 1
                        if is_pass:
                            passed += 1
                        elif is_fail:
                            failed += 1
                        else:
                            skipped += 1
                        max_duration = max(max_duration, duration)

                # Recurse into nested suites
                if suite_data.get("suites"):
                    nested = _process_suites(suite_data["suites"], file)
                    suites.extend(nested)

                # Only add if it has specs (leaf suite)
                if suite.tests:
                    suites.append(suite)

            return suites

        report.suites = _process_suites(data.get("suites", []))

        report.summary = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration_ms": max_duration,
        }
