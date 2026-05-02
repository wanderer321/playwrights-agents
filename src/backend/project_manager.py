"""Project configuration management for H5 and MiniProgram projects."""

import json
from pathlib import Path
from typing import Any

from src.utils.file_utils import scan_project, scan_miniprogram


def _resolve_dir(d: str, project_type: str = "h5") -> str:
    """Resolve a possibly-relative directory path to absolute.

    Tries in order:
    1. As-is if already absolute and exists
    2. Relative to CWD
    3. Relative to common workspace roots
    Falls back to the original string if nothing matches.
    For miniprogram projects, also probes one level deeper if the resolved
    path doesn't contain project.config.json (the actual miniprogram root).
    """
    def _looks_like_mp_root(p: Path) -> bool:
        return (p / "project.config.json").exists() or (p / "miniprogram" / "app.json").exists()

    def _resolve(p: Path) -> str:
        resolved = p.resolve()
        if project_type == "miniprogram" and resolved.is_dir():
            # If this doesn't look like a miniprogram root, check one level deeper
            if not _looks_like_mp_root(resolved):
                children = list(resolved.iterdir())
                if len(children) == 1 and children[0].is_dir():
                    deeper = children[0]
                    if _looks_like_mp_root(deeper):
                        return str(deeper.resolve())
        return str(resolved)

    p = Path(d)

    # Already absolute
    if p.is_absolute():
        return _resolve(p)

    # Relative to CWD
    try:
        return _resolve(p.resolve(strict=True))
    except (OSError, RuntimeError):
        pass

    # Relative to common workspace directories
    for base in [Path("D:\\githome"), Path("D:\\githome\\PPT"), Path.home()]:
        candidate = base / d
        if candidate.is_dir():
            return _resolve(candidate)

    return d  # store as-is if unresolvable


class ProjectManager:
    """Manage project configurations (CRUD) for H5 and MiniProgram projects."""

    def __init__(self, data_path: str | Path):
        self.data_file = Path(data_path) / "projects.json"
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self._projects: dict[str, dict] = {}
        self._load()

    def _load(self):
        if self.data_file.exists():
            try:
                self._projects = json.loads(self.data_file.read_text(encoding="utf-8"))
            except Exception:
                self._projects = {}
        else:
            self._projects = {}

    def _save(self):
        self.data_file.write_text(
            json.dumps(self._projects, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add_project(
        self,
        name: str,
        project_type: str = "h5",
        frontend_dirs: list[str] | None = None,
        backend_dirs: list[str] | None = None,
        single_dirs: list[str] | None = None,
        miniprogram_config: dict | None = None,
    ) -> dict:
        pid = str(len(self._projects) + 1)
        dirs = single_dirs or frontend_dirs or []

        # Resolve relative paths to absolute
        frontend_dirs = [_resolve_dir(d) for d in (frontend_dirs or [])]
        backend_dirs = [_resolve_dir(d) for d in (backend_dirs or [])]
        single_dirs = [_resolve_dir(d, project_type) for d in (single_dirs or [])]
        dirs = single_dirs or frontend_dirs or []

        self._projects[pid] = {
            "id": pid,
            "name": name,
            "project_type": project_type,
            "frontend_dirs": frontend_dirs,
            "backend_dirs": backend_dirs,
            "single_dirs": single_dirs,
            "miniprogram_config": miniprogram_config or {},
            "scanned": {},
        }

        # Auto-scan directories based on type
        scan_fn = scan_miniprogram if project_type == "miniprogram" else scan_project
        for d in dirs + backend_dirs:
            try:
                self._projects[pid]["scanned"][d] = scan_fn(d)
            except Exception as e:
                self._projects[pid]["scanned"][d] = {"error": str(e)}

        self._save()
        return self._projects[pid]

    def list_projects(self) -> list[dict]:
        return list(self._projects.values())

    def delete_project(self, pid: str) -> bool:
        if pid in self._projects:
            del self._projects[pid]
            self._save()
            return True
        return False

    def get_project(self, pid: str) -> dict | None:
        return self._projects.get(pid)

    def update_project(self, pid: str, updates: dict) -> dict | None:
        if pid not in self._projects:
            return None
        self._projects[pid].update(updates)
        self._save()
        return self._projects[pid]
