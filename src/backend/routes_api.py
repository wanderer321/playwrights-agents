"""HTTP REST API routes."""

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.backend.project_manager import ProjectManager
from src.backend.test_runner import TestRunner
from src.playwright_core.installer import PlaywrightInstaller

router = APIRouter(prefix="/api")
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def deps():
    from src.backend.app import container
    return container


class AddProjectRequest(BaseModel):
    name: str
    project_type: str = "h5"
    frontend_dirs: list[str] = []
    backend_dirs: list[str] = []
    single_dirs: list[str] = []
    miniprogram_config: dict = {}


class UpdateProjectRequest(BaseModel):
    name: str | None = None
    project_type: str | None = None
    frontend_dirs: list[str] | None = None
    backend_dirs: list[str] | None = None
    single_dirs: list[str] | None = None
    miniprogram_config: dict | None = None


class StartTestRequest(BaseModel):
    project_id: str
    force_regenerate_plan: bool = False


class StopTestRequest(BaseModel):
    task_id: str


class PlaywrightUpdateRequest(BaseModel):
    version: str | None = None
    work_dir: str = "."


class ValidatePathRequest(BaseModel):
    path: str


@router.post("/validate-path")
async def validate_path(req: ValidatePathRequest):
    """Verify a directory path exists and is accessible."""
    p = Path(req.path)
    if p.exists() and p.is_dir():
        return {"valid": True, "path": str(p), "message": "目录存在且可访问"}
    elif p.exists() and not p.is_dir():
        return {"valid": False, "path": req.path, "message": "路径存在但不是目录"}
    else:
        return {"valid": False, "path": req.path, "message": "目录不存在，请检查路径是否正确"}


@router.get("/projects")
async def list_projects():
    return deps()["project_mgr"].list_projects()


@router.post("/projects")
async def add_project(req: AddProjectRequest):
    p = deps()["project_mgr"].add_project(
        name=req.name,
        project_type=req.project_type,
        frontend_dirs=req.frontend_dirs,
        backend_dirs=req.backend_dirs,
        single_dirs=req.single_dirs,
        miniprogram_config=req.miniprogram_config,
    )
    return p


@router.put("/projects/{pid}")
async def update_project(pid: str, req: UpdateProjectRequest):
    updates = {k: v for k, v in req.dict(exclude_none=True).items()}
    p = deps()["project_mgr"].update_project(pid, updates)
    if not p:
        raise HTTPException(404, "项目不存在")
    return p


@router.delete("/projects/{pid}")
async def delete_project(pid: str):
    if not deps()["project_mgr"].delete_project(pid):
        raise HTTPException(404, "项目不存在")
    return {"ok": True}


@router.post("/test/start")
async def start_test(req: StartTestRequest):
    runner: TestRunner = deps()["test_runner"]
    project = deps()["project_mgr"].get_project(req.project_id)
    if not project:
        raise HTTPException(404, "项目不存在")

    task = runner.create_task(project)
    task.force_regenerate_plan = req.force_regenerate_plan
    import asyncio
    loop = asyncio.get_event_loop()
    async_task = loop.create_task(runner.run_full_pipeline(task.id))
    runner._asyncio_tasks[task.id] = async_task
    return {"task_id": task.id, "status": task.status}


@router.post("/test/start-expanded")
async def start_expanded_test(req: StartTestRequest):
    runner: TestRunner = deps()["test_runner"]
    project = deps()["project_mgr"].get_project(req.project_id)
    if not project:
        raise HTTPException(404, "项目不存在")

    task = runner.create_task(project)
    task.force_regenerate_plan = req.force_regenerate_plan
    import asyncio
    loop = asyncio.get_event_loop()
    async_task = loop.create_task(runner.run_expanded_pipeline(task.id))
    runner._asyncio_tasks[task.id] = async_task
    return {"task_id": task.id, "status": task.status}


@router.post("/test/stop")
async def stop_test(req: StopTestRequest):
    runner: TestRunner = deps()["test_runner"]
    task = runner.tasks.get(req.task_id)
    if not task:
        raise HTTPException(404, "任务不存在")
    if task.status != "running":
        return {"task_id": task.id, "status": task.status, "message": f"测试状态为 {task.status}，无法停止"}
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(runner.stop_task(req.task_id))
    return {"task_id": task.id, "status": "stopping"}


@router.get("/test/status/{tid}")
async def test_status(tid: str):
    task = deps()["test_runner"].tasks.get(tid)
    if not task:
        raise HTTPException(404, "任务不存在")
    return {
        "task_id": task.id,
        "status": task.status,
        "progress": task.progress,
        "created_at": task.created_at,
        "completed_at": task.completed_at,
    }


@router.get("/test/report/{tid}")
async def test_report(tid: str):
    task = deps()["test_runner"].tasks.get(tid)
    if not task:
        raise HTTPException(404, "任务不存在")
    return {"task_id": task.id, "status": task.status, "result": task.result, "logs": task.logs}


@router.get("/test/logs/{tid}")
async def test_logs(tid: str):
    task = deps()["test_runner"].tasks.get(tid)
    if not task:
        raise HTTPException(404, "任务不存在")
    return {"logs": task.logs}


@router.get("/ai/status")
async def ai_status():
    cfg = deps()["config"].get("ai", {})
    return {
        "provider": cfg.get("provider", "aliyun"),
        "model": cfg.get("model", "glm-5"),
    }


@router.post("/playwright/update")
async def update_playwright(req: PlaywrightUpdateRequest):
    inst = PlaywrightInstaller(work_dir=req.work_dir)
    ver = await inst.install(version=req.version)
    return {"version": ver}


@router.get("/playwright/version")
async def playwright_version():
    inst = PlaywrightInstaller()
    return {"version": await inst.get_current_version()}


@router.get("/tasks")
async def list_tasks():
    return [
        {"task_id": t.id, "project_name": t.project.get("name", ""),
         "project_type": t.project.get("project_type", "h5"),
         "status": t.status, "progress": t.progress, "created_at": t.created_at}
        for t in deps()["test_runner"].tasks.values()
    ]


@router.get("/reports")
async def list_reports():
    """List all historical test reports from the data directory."""
    reports = []
    for f in sorted(DATA_DIR.glob("report_*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            tid = f.stem.replace("report_", "")
            reports.append({
                "task_id": tid,
                "project_name": data.get("project_name", data.get("name", "")),
                "project_type": data.get("project_type", "h5"),
                "status": data.get("status", "completed"),
                "summary": data.get("summary", {}),
                "created_at": data.get("completed_at", data.get("created_at", "")),
                "file": f.name,
                "time": f.stat().st_mtime,
            })
        except Exception:
            pass
    return reports


@router.get("/reports/{tid}")
async def get_report(tid: str):
    """Get a specific historical test report."""
    report_file = DATA_DIR / f"report_{tid}.json"
    plan_file = DATA_DIR / f"plan_{tid}.md"
    if not report_file.exists():
        raise HTTPException(404, "报告不存在")
    try:
        data = json.loads(report_file.read_text(encoding="utf-8"))
        plan = plan_file.read_text(encoding="utf-8") if plan_file.exists() else ""
        return {**data, "plan": plan}
    except json.JSONDecodeError:
        raise HTTPException(500, "报告文件损坏")
