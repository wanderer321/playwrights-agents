"""WebSocket routes for real-time log streaming."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws/logs/{task_id}")
async def ws_logs(ws: WebSocket, task_id: str):
    await ws.accept()
    from src.backend.app import container
    runner = container["test_runner"]
    task = runner.tasks.get(task_id)

    if not task:
        await ws.send_json({"type": "error", "message": "任务不存在"})
        await ws.close()
        return

    for log in task.logs:
        await ws.send_json({"type": "log", "message": log})

    async def send(m: str):
        try:
            await ws.send_json({"type": "log", "message": m})
        except Exception:
            pass

    runner.on_log(task_id, send)

    try:
        import asyncio
        while True:
            await asyncio.sleep(1)
            await ws.send_json({"type": "progress", "status": task.status, "progress": task.progress})
            if task.status in ("completed", "failed"):
                await ws.send_json({"type": "complete", "status": task.status, "result": task.result})
                break
    except WebSocketDisconnect:
        pass
