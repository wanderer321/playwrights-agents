"""Minium test execution wrapper for WeChat Mini Programs."""

import asyncio
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


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


class MiniumExecutor:
    """Run Minium tests for WeChat Mini Programs and capture results."""

    def __init__(self, project_dir: str | Path, minium_config: dict | None = None):
        self.project_dir = Path(project_dir)
        self.minium_config = minium_config or {}
        self._test_dir = self.project_dir / "minium_tests"
        self._output_dir = self._test_dir / "outputs"

    async def run_tests(
        self,
        test_path: str | None = None,
        log_callback=None,
    ) -> TestReport:
        """Run Minium tests and return a structured report.

        Args:
            test_path: relative path to test file or directory (None = all tests)
            log_callback: async callable receiving log lines
        """
        report = TestReport(
            task_id=f"minium_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            summary={"total": 0, "passed": 0, "failed": 0, "skipped": 0, "duration_ms": 0},
            suites=[],
        )

        # Check if minium is available
        try:
            import minium  # noqa: F401
        except ImportError:
            if log_callback:
                await log_callback("[minium] Minium 未安装，请执行: pip install minium\n")
            report.summary["error"] = "Minium not installed"
            return report

        # Check for devtools config
        dev_tool_path = self.minium_config.get("dev_tool_path", "")
        if dev_tool_path and not os.path.isfile(dev_tool_path):
            if log_callback:
                await log_callback(f"[minium] 开发者工具路径无效: {dev_tool_path}\n")
            report.summary["error"] = f"DevTools not found: {dev_tool_path}"
            return report

        # Prepare config
        config = self._build_config()
        config_file = self._test_dir / "config.json"
        self._test_dir.mkdir(parents=True, exist_ok=True)
        self._output_dir.mkdir(parents=True, exist_ok=True)
        config_file.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

        if log_callback:
            await log_callback(f"[minium] 配置已保存: {config_file}\n")

        # Run tests via minitest CLI
        suite_file = self._test_dir / "suite.json"
        suite_data = self._build_suite(test_path)
        suite_file.write_text(json.dumps(suite_data, ensure_ascii=False, indent=2), encoding="utf-8")

        # Use minitest CLI (installed as minitest.exe via pip)
        cmd = [
            "minitest",
            "-c", str(config_file),
            "-s", str(suite_file),
        ]

        if log_callback:
            await log_callback(f"[minium] 执行测试: {' '.join(cmd)}\n")

        try:
            process = await asyncio.create_subprocess_shell(
                "minitest -c " + str(config_file) + " -s " + str(suite_file),
                cwd=str(self._test_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout_chunks: list[str] = []
            stderr_chunks: list[str] = []

            async def _read_stream(stream, store):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    decoded = line.decode("utf-8", errors="replace")
                    store.append(decoded)
                    if log_callback:
                        await log_callback(decoded)

            await asyncio.gather(
                _read_stream(process.stdout, stdout_chunks),
                _read_stream(process.stderr, stderr_chunks),
            )

            await process.wait()
            stdout_text = "".join(stdout_chunks)
            stderr_text = "".join(stderr_chunks)

            # Parse output
            self._parse_output(report, stdout_text, stderr_text)

            # Try to parse JSON report if generated
            report_file = self._output_dir / "summary.json"
            if report_file.exists():
                try:
                    data = json.loads(report_file.read_text(encoding="utf-8"))
                    self._parse_summary_json(report, data)
                except Exception:
                    pass

        except FileNotFoundError as e:
            if log_callback:
                await log_callback(f"[minium] 执行失败: {e}\n")
            report.summary["error"] = f"Minium execution failed: {e}"
        except Exception as e:
            if log_callback:
                await log_callback(f"[minium] 错误: {e}\n")
            report.summary["error"] = str(e)

        report.raw_output = report.raw_output or stdout_text if 'stdout_text' in dir() else ""
        return report

    def _build_config(self) -> dict:
        """Build Minium config.json."""
        import sys
        return {
            "project_path": str(self.project_dir),
            "dev_tool_path": self.minium_config.get("dev_tool_path", ""),
            "platform": self.minium_config.get("platform", "ide"),
            "debug_mode": self.minium_config.get("debug_mode", "info"),
            "auto_relaunch": self.minium_config.get("auto_relaunch", True),
            "assert_capture": self.minium_config.get("assert_capture", True),
            "test_result_path": str(self._output_dir),
            "python_path": sys.executable,
        }

    def _build_suite(self, test_path: str | None) -> dict:
        """Build Minium suite.json."""
        pkg_list = []

        if test_path and Path(test_path).is_dir():
            # Directory: add each Python file as a package
            for f in sorted(Path(test_path).glob("*.py")):
                pkg_list.append({"pkg": f.stem, "case_list": ["test_*"]})
        elif test_path and str(test_path).endswith(".py"):
            # Single file
            pkg_list.append({"pkg": Path(test_path).stem, "case_list": ["test_*"]})
        else:
            # Default: wildcard
            pkg_list.append({"pkg": "*.py", "case_list": ["test_*"]})

        return {"pkg_list": pkg_list}

    def _parse_output(self, report: TestReport, stdout: str, stderr: str):
        """Parse console output for test results."""
        raw = stdout + stderr
        report.raw_output = raw

        # Count test outcomes by line patterns
        lines = raw.splitlines()
        total = passed = failed = skipped = 0
        current_suite: SuiteResult | None = None
        suites_map: dict[str, SuiteResult] = {}

        for line in lines:
            line_lower = line.lower()
            # Detect suite/test class
            if "test_" in line and ("class " in line_lower or "suite" in line_lower):
                suite_name = line.strip().split()[-1].replace("(", "").replace(")", "")
                current_suite = SuiteResult(title=suite_name, file="")
                suites_map[suite_name] = current_suite

            # Detect test method
            if "test_" in line_lower and ("..." in line or "→" in line or "ok" in line_lower or "fail" in line_lower):
                title = line.strip()
                if not current_suite:
                    current_suite = SuiteResult(title="default", file="")
                    suites_map["default"] = current_suite

                if "ok" in line_lower or "passed" in line_lower or "✓" in line:
                    current_suite.tests.append(SingleTestResult(title=title, file="", status="passed"))
                    passed += 1
                elif "fail" in line_lower or "✗" in line or "error" in line_lower:
                    current_suite.tests.append(SingleTestResult(title=title, file="", status="failed"))
                    failed += 1
                else:
                    current_suite.tests.append(SingleTestResult(title=title, file="", status="skipped"))
                    skipped += 1
                total += 1

        report.summary = {
            "total": total or raw.count("test_"),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration_ms": 0,
        }
        report.suites = list(suites_map.values())

    def _parse_summary_json(self, report: TestReport, data: dict):
        """Parse Minium summary.json report.

        Format from Minium's summary.json:
          test_num: total test count
          errors: list of {module, error_type, case_name, exception}
          failures: list of {module, error_type, case_name, exception}
        """
        total = data.get("test_num", 0)

        # Collect errors and failures, deduplicate by case_name
        seen: set[str] = set()
        failed_cases: list[dict] = []

        for entry in data.get("errors", []) + data.get("failures", []):
            cn = entry.get("case_name", "")
            if cn and cn not in seen:
                seen.add(cn)
                failed_cases.append(entry)

        passed = total - len(failed_cases)

        suite_map: dict[str, SuiteResult] = {}
        for entry in failed_cases:
            module = entry.get("module", "Unknown")
            if module not in suite_map:
                suite_map[module] = SuiteResult(title=module, file="")
            suite_map[module].tests.append(SingleTestResult(
                title=entry.get("case_name", ""),
                file="",
                status="failed",
                error=entry.get("exception", None),
            ))

        report.suites = list(suite_map.values())
        report.summary = {
            "total": total or report.summary["total"],
            "passed": passed or report.summary["passed"],
            "failed": len(failed_cases) or report.summary["failed"],
            "skipped": 0,
            "duration_ms": report.summary["duration_ms"],
        }
