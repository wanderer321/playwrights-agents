"""PageScanner — captures WXML structure of all mini program pages."""

import asyncio
import json
import os
import sys
from pathlib import Path


class PageScanner:
    """Scan all pages of a WeChat Mini Program and capture their WXML structure.

    Uses a temporary Minium test script executed via minitest CLI to navigate
    through every page and capture page.wxml, then returns the results as a
    {page_path: wxml_string} dictionary for use by the Generator.
    """

    def __init__(self, project_dir: str | Path, minium_config: dict | None = None, log=None):
        self.project_dir = Path(project_dir)
        self.minium_config = minium_config or {}
        self.log = log
        self._test_dir = self.project_dir / "minium_tests"
        self._output_dir = self._test_dir / "outputs"

    async def _log(self, msg: str):
        if self.log:
            await self.log(msg)

    def _read_app_config(self) -> tuple[list[str], list[str]]:
        """Read app.json to get all page paths and tabBar page paths."""
        app_json_path = self.project_dir / "miniprogram" / "app.json"
        if not app_json_path.exists():
            app_json_path = self.project_dir / "app.json"
        if not app_json_path.exists():
            raise FileNotFoundError(f"Cannot find app.json in {self.project_dir}")

        data = json.loads(app_json_path.read_text(encoding="utf-8"))
        all_pages = data.get("pages", [])
        tabbar_pages = []
        tabbar_config = data.get("tabBar", {})
        for item in tabbar_config.get("list", []):
            tabbar_pages.append(item.get("pagePath", ""))
        return all_pages, tabbar_pages

    def _generate_scan_script(self, tabbar_pages: list[str], output_path: str) -> str:
        """Generate a temporary Minium test script that scans all pages."""
        tabbar_json = json.dumps(tabbar_pages, ensure_ascii=False)
        return f'''"""Auto-generated page scanner — captures WXML for all pages."""
import json
import os
import time
import minium


class ScanPages(minium.MiniTest):
    def test_scan_all_pages(self):
        result = {{}}
        tabbar = {tabbar_json}
        all_pages = self.app.get_all_pages_path()
        wait_sec = int(os.environ.get("SCAN_WAIT_MS", "1500")) / 1000.0

        for page in all_pages:
            try:
                if page in tabbar:
                    self.app.switch_tab("/" + page)
                else:
                    self.app.navigate_to("/" + page)
                time.sleep(wait_sec)
                result[page] = self.page.wxml
            except Exception as e:
                result[page] = f"<!-- scan error: {{e}} -->"

        out = "{output_path}"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
'''

    async def scan(self) -> dict[str, str]:
        """Scan all pages and return {page_path: wxml_string}.

        The returned dict includes a '_meta' key with metadata like tabBar pages:
            {"_meta": {"tabbar_pages": [...]}, "pages/index/index": "<wxml>", ...}

        Returns an empty dict if scanning fails entirely.
        """
        await self._log("[scanner] 读取 app.json 页面配置...\n")
        all_pages, tabbar_pages = self._read_app_config()
        await self._log(f"[scanner] 共 {len(all_pages)} 个页面, {len(tabbar_pages)} 个 tabBar 页\n")

        self._test_dir.mkdir(parents=True, exist_ok=True)
        self._output_dir.mkdir(parents=True, exist_ok=True)

        scan_output = self._output_dir / "scanned_pages.json"
        scan_output_str = str(scan_output).replace("\\", "/")

        # Write temporary scan script
        script_name = "_scan_pages.py"
        script_path = self._test_dir / script_name
        script_path.write_text(
            self._generate_scan_script(tabbar_pages, scan_output_str),
            encoding="utf-8",
        )

        # Write minium config
        config = {
            "project_path": str(self.project_dir),
            "dev_tool_path": self.minium_config.get("dev_tool_path", ""),
            "platform": self.minium_config.get("platform", "ide"),
            "debug_mode": self.minium_config.get("debug_mode", "info"),
            "auto_relaunch": self.minium_config.get("auto_relaunch", True),
            "assert_capture": self.minium_config.get("assert_capture", True),
            "test_result_path": str(self._output_dir),
            "python_path": sys.executable,
        }
        config_file = self._test_dir / "config.json"
        config_file.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

        # Write suite file (only runs the scan script)
        suite = {
            "pkg_list": [
                {"pkg": script_name.replace(".py", ""), "case_list": ["test_scan_*"]},
            ]
        }
        suite_file = self._test_dir / "_scan_suite.json"
        suite_file.write_text(json.dumps(suite, ensure_ascii=False, indent=2), encoding="utf-8")

        # Run minitest
        cmd = f"minitest -c {config_file} -s {suite_file}"
        await self._log(f"[scanner] 执行页面扫描: {cmd}\n")

        env = os.environ.copy()
        env["SCAN_OUTPUT"] = scan_output_str
        env["SCAN_WAIT_MS"] = self.minium_config.get("scan_wait_ms", "1500")

        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                cwd=str(self._test_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
            stdout, stderr = await process.communicate()

            for line in (stdout.decode("utf-8", errors="replace") + stderr.decode("utf-8", errors="replace")).splitlines():
                await self._log(f"  {line}\n")
        except Exception as e:
            await self._log(f"[scanner] 执行失败: {e}\n")
            return {}

        # Read results
        if scan_output.exists():
            try:
                data = json.loads(scan_output.read_text(encoding="utf-8"))
                await self._log(f"[scanner] 成功扫描 {len(data)}/{len(all_pages)} 个页面\n")
                for page in all_pages:
                    if page not in data:
                        data[page] = "<!-- page not scanned -->"
                # Add metadata including tabBar pages for AI context
                data["_meta"] = {
                    "tabbar_pages": tabbar_pages,
                    "total_pages": len(all_pages),
                }
                return data
            except json.JSONDecodeError as e:
                await self._log(f"[scanner] 结果解析失败: {e}\n")
                return {}
        else:
            await self._log(f"[scanner] 未生成结果文件: {scan_output}\n")
            return {}
