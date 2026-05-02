"""Background test orchestrator — runs the full pipeline for H5 or MiniProgram."""

import asyncio
import datetime
import json
import re
import uuid
from pathlib import Path
from typing import Any, Callable

from src.backend.agents.planner import Planner
from src.backend.agents.generator import Generator
from src.backend.agents.executor import Executor
from src.backend.agents.healer import Healer
from src.backend.project_manager import _resolve_dir
from src.ai_gateway.gateway import AIGateway


class TestTask:
    def __init__(self, task_id: str, project: dict):
        self.id = task_id
        self.project = project
        self.status = "pending"
        self.progress = 0.0
        self.logs: list[str] = []
        self.result: dict | None = None
        self.created_at = datetime.datetime.now().isoformat()
        self.completed_at: str | None = None


class TestRunner:
    """Orchestrate the full pipeline: plan → generate → execute → heal."""

    def __init__(self, ai: AIGateway, data_dir: str | Path):
        self.ai = ai
        self.data_dir = Path(data_dir)
        self.tasks: dict[str, TestTask] = {}
        self._callbacks: dict[str, list[Callable]] = {}
        self.planner = Planner(ai)
        self.generator = Generator(ai)
        self.healer = Healer(ai)

    def create_task(self, project: dict) -> TestTask:
        tid = str(uuid.uuid4())[:8]
        task = TestTask(tid, project)
        self.tasks[tid] = task
        self._callbacks[tid] = []
        return task

    def on_log(self, task_id: str, cb: Callable):
        if task_id in self._callbacks:
            self._callbacks[task_id].append(cb)

    async def _log(self, task_id: str, msg: str):
        task = self.tasks.get(task_id)
        if task:
            task.logs.append(msg)
        for cb in self._callbacks.get(task_id, []):
            try:
                await cb(msg)
            except Exception:
                pass

    async def run_full_pipeline(self, task_id: str):
        await self._run_pipeline(task_id, expanded=False)

    async def run_expanded_pipeline(self, task_id: str):
        await self._run_pipeline(task_id, expanded=True)

    async def _run_pipeline(self, task_id: str, expanded: bool = False):
        task = self.tasks.get(task_id)
        if not task:
            return
        task.status = "running"

        async def log(msg):
            await self._log(task_id, msg)

        try:
            project_type = task.project.get("project_type", "h5")
            minium_config = task.project.get("miniprogram_config", {})

            # Determine project root and resolve to absolute path
            single = task.project.get("single_dirs", [])
            dirs = single or (task.project.get("frontend_dirs", []) + task.project.get("backend_dirs", []))
            if not dirs:
                raise ValueError("没有配置项目目录")
            root = _resolve_dir(dirs[0], project_type=project_type)
            if not Path(root).is_dir():
                raise NotADirectoryError(
                    f"目录不存在: {root}\n"
                    f"请确认项目路径正确，然后在项目设置中修改目录。"
                )

            mode_label = "扩充测试" if expanded else "标准测试"
            platform_label = "微信小程序" if project_type == "miniprogram" else "H5 网页"
            await log(f"=== 项目类型: {platform_label} | 模式: {mode_label} ===\n")

            # Step 1: Plan
            step_count = "4"
            if expanded:
                await log("=== 步骤 1/4: 生成扩充测试计划 ===\n")
            else:
                await log("=== 步骤 1/4: 生成测试计划 ===\n")
            task.progress = 0.1
            plan = await self.planner.run(root, project_type=project_type, expanded=expanded, log=log)
            plan_file = self.data_dir / f"plan_{task.id}.md"
            plan_file.write_text(plan, encoding="utf-8")
            await log(f"计划已保存: {plan_file}\n")

            # Step 2: Page discovery + Generate test code
            task.progress = 0.3

            if project_type == "miniprogram":
                page_snapshots: dict[str, str] = {}
                await log(f"=== 步骤 2/{step_count}: 扫描页面结构 + 生成测试代码 ===\n")

                # Page discovery: capture real WXML for all pages
                from src.backend.miniprogram.page_scanner import PageScanner
                scanner = PageScanner(root, minium_config, log=log)
                page_snapshots = await scanner.scan()
                await log(f"[scanner] 已扫描 {len(page_snapshots)} 个页面\n")

                gen_dir = self.data_dir / f"gen_{task.id}"
                gen_dir.mkdir(parents=True, exist_ok=True)

                code = await self.generator.run(
                    plan,
                    snapshot=json.dumps(page_snapshots, ensure_ascii=False) if page_snapshots else None,
                    project_type=project_type,
                    log=log,
                )

                # Extract Python code blocks and save as test files
                blocks = re.findall(r'```python\n(.*?)```', code, re.DOTALL)
                saved = []
                for i, block in enumerate(blocks):
                    fname = f"test_gen_{i}.py"
                    (gen_dir / fname).write_text(block.strip(), encoding="utf-8")
                    saved.append(fname)

                if not blocks:
                    fname = "test_gen.py"
                    (gen_dir / fname).write_text(code, encoding="utf-8")
                    saved.append(fname)

                await log(f"[generator] 已生成 {len(saved)} 个测试文件\n")

                # Copy generated files to minium_tests dir so minitest can find them
                minium_test_dir = Path(root) / "minium_tests"
                minium_test_dir.mkdir(parents=True, exist_ok=True)
                for fname in saved:
                    src = gen_dir / fname
                    dst = minium_test_dir / fname
                    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                await log(f"[generator] 测试文件已复制到: {minium_test_dir}\n")

                # Validate generated Python files for syntax errors
                import py_compile, tempfile
                valid_files = []
                for fname in saved:
                    src = minium_test_dir / fname
                    try:
                        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as tf:
                            tf.write(src.read_text(encoding="utf-8"))
                            tf.flush()
                        py_compile.compile(tf.name, doraise=True)
                        valid_files.append(fname)
                    except py_compile.PyCompileError as e:
                        await log(f"[generator] 语法错误 {fname}: {e}\n")
                    finally:
                        Path(tf.name).unlink(missing_ok=True)

                if not valid_files:
                    raise SyntaxError("所有生成的测试文件都存在语法错误，无法执行")

                # Remove invalid test files
                for fname in saved:
                    if fname not in valid_files:
                        (minium_test_dir / fname).unlink(missing_ok=True)
                await log(f"[generator] 语法检查通过: {len(valid_files)}/{len(saved)} 个文件\n")
                test_path = str(minium_test_dir)
            else:
                # H5: generate Playwright test code from the plan
                await log(f"=== 步骤 2/{step_count}: 生成测试代码 ===\n")

                code = await self.generator.run(
                    plan,
                    snapshot=None,
                    project_type="h5",
                    log=log,
                )

                gen_dir = self.data_dir / f"gen_{task.id}"
                gen_dir.mkdir(parents=True, exist_ok=True)

                # Extract TypeScript/JavaScript code blocks
                blocks = re.findall(r'```(?:typescript|ts|javascript|js)\n(.*?)```', code, re.DOTALL)
                if not blocks:
                    blocks = re.findall(r'```\n(.*?)```', code, re.DOTALL)

                saved = []
                for i, block in enumerate(blocks):
                    fname = f"expanded_gen_{i}.spec.ts"
                    (gen_dir / fname).write_text(block.strip(), encoding="utf-8")
                    saved.append(fname)

                if not blocks:
                    fname = "expanded_gen.spec.ts"
                    # Strip any markdown fences from raw output
                    cleaned = re.sub(r'^```(?:typescript|ts|javascript|js)?\s*\n?', '', code)
                    cleaned = re.sub(r'\n```\s*$', '', cleaned)
                    (gen_dir / fname).write_text(cleaned.strip(), encoding="utf-8")
                    saved.append(fname)

                await log(f"[generator] 已生成 {len(saved)} 个测试文件\n")

                # Copy generated files to the project's tests/generated directory
                h5_test_dir = Path(root) / "tests" / "generated"
                h5_test_dir.mkdir(parents=True, exist_ok=True)
                for fname in saved:
                    src = gen_dir / fname
                    dst = h5_test_dir / fname
                    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                await log(f"[generator] 测试文件已复制到: {h5_test_dir}\n")

                test_path = "tests/generated"

            # Step 3: Execute
            step_label = f"3/{step_count}"
            await log(f"\n=== 步骤 {step_label}: 执行测试 ===\n")
            task.progress = 0.4
            executor = Executor(root, project_type=project_type, minium_config=minium_config)
            report = await executor.run(test_path=test_path, log=log)

            s = report.summary
            await log(f"\n结果: {s.get('passed', 0)}/{s.get('total', 0)} 通过\n")

            # Step 4: Heal
            task.progress = 0.8
            failures = []
            for suite in report.suites:
                for t in suite.tests:
                    if t.status == "unexpected" or t.status == "failed":
                        failures.append(t)

            if failures:
                await log(f"\n=== 步骤 4/{step_count}: 诊断 {len(failures)} 个失败用例 ===\n")
                for f in failures:
                    diag = await self.healer.diagnose(f.error or "", code=getattr(f, "code", None), project_type=project_type, log=log)
                    f.diagnosis = diag  # type: ignore

            # Build diagnostic category summary (failures only)
            cat_counts: dict[str, int] = {}
            cat_labels: dict[str, str] = {}
            for f in failures:
                d = getattr(f, "diagnosis", None) or {}
                cat = d.get("category", "unknown")
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
                if cat not in cat_labels:
                    cat_labels[cat] = d.get("category_label", "无法确定")

            if failures and cat_counts:
                await log("\n诊断汇总:\n")
                for cat, count in sorted(cat_counts.items()):
                    label = cat_labels.get(cat, cat)
                    await log(f"  {label}: {count} 个\n")

            task.progress = 1.0
            task.status = "completed"
            task.completed_at = datetime.datetime.now().isoformat()
            task.result = {
                "test_mode": "expanded" if expanded else "standard",
                "project_name": task.project.get("name", ""),
                "project_type": project_type,
                "created_at": task.created_at,
                "completed_at": task.completed_at,
                "summary": report.summary,
                "diagnostic_summary": {
                    "total_failures": len(failures),
                    "categories": {cat_labels.get(c, c): n for c, n in sorted(cat_counts.items())},
                },
                "suites": [
                    {"title": s.title, "file": s.file, "tests": [
                        {"title": t.title, "status": t.status,
                         "error": t.error, "diagnosis": getattr(t, "diagnosis", None)}
                        for t in s.tests
                    ]}
                    for s in report.suites
                ],
            }

            report_file = self.data_dir / f"report_{task.id}.json"
            report_file.write_text(json.dumps(task.result, ensure_ascii=False, indent=2), encoding="utf-8")

        except Exception as e:
            task.status = "failed"
            await log(f"\n[错误] {e}\n")
            import traceback
            await log(traceback.format_exc())
