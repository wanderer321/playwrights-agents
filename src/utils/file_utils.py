"""File-system helpers for scanning and analysing project directories."""

import json
import os
from pathlib import Path
from typing import Any


def scan_project(root: str | Path) -> dict[str, Any]:
    """Scan a project directory and return its structure metadata."""
    root = Path(root)
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    info: dict[str, Any] = {
        "root": str(root.resolve()),
        "has_package_json": False,
        "has_playwright_config": False,
        "has_vite_config": False,
        "has_tsconfig": False,
        "frameworks": [],
        "test_dirs": [],
        "spec_files": [],
    }

    # Check for known config files
    for p in root.iterdir():
        name = p.name
        if name == "package.json":
            info["has_package_json"] = True
            try:
                pkg = json.loads(p.read_text(encoding="utf-8"))
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                if "react" in deps:
                    info["frameworks"].append("react")
                if "vue" in deps:
                    info["frameworks"].append("vue")
                if "@playwright/test" in deps:
                    info["has_playwright_config"] = True
            except Exception:
                pass
        elif name.startswith("playwright.config"):
            info["has_playwright_config"] = True
        elif name.startswith("vite.config"):
            info["has_vite_config"] = True
        elif name == "tsconfig.json":
            info["has_tsconfig"] = True

    # Find test directories and spec files
    for pattern in ("**/*.spec.ts", "**/*.spec.tsx", "**/*.test.ts", "**/__tests__/**"):
        for match in root.glob(pattern):
            if match.is_file():
                info["spec_files"].append(str(match.relative_to(root)))
                parent = match.parent
                rel = parent.relative_to(root)
                dir_str = str(rel)
                if dir_str not in info["test_dirs"]:
                    info["test_dirs"].append(dir_str)

    return info


def ensure_dir(path: str | Path) -> Path:
    """Create directory if it doesn't exist."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def scan_miniprogram(root: str | Path) -> dict[str, Any]:
    """Scan a WeChat Mini Program project directory."""
    root = Path(root)
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    # Some projects have the miniprogram code in a 'miniprogram' subdirectory
    miniprogram_dir = root / "miniprogram"
    has_miniprogram_subdir = miniprogram_dir.is_dir()

    info: dict[str, Any] = {
        "root": str(root.resolve()),
        "type": "miniprogram",
        "has_app_json": False,
        "has_project_config": False,
        "has_package_json": False,
        "pages": [],
        "components": [],
        "using_mpvue": False,
        "using_taro": False,
        "using_uni_app": False,
    }

    # Determine which directories to scan
    scan_targets = [root]
    if has_miniprogram_subdir:
        scan_targets.append(miniprogram_dir)

    for scan_root in scan_targets:
        for p in scan_root.iterdir():
            name = p.name
            if name == "app.json":
                info["has_app_json"] = True
                try:
                    app_config = json.loads(p.read_text(encoding="utf-8"))
                    pages = app_config.get("pages", [])
                    # Deduplicate pages
                    for page in pages:
                        if page not in info["pages"]:
                            info["pages"].append(page)
                    info["using_components"] = bool(app_config.get("usingComponents"))
                except Exception:
                    pass
            elif name in ("project.config.json", "project.config.json5"):
                info["has_project_config"] = True
                try:
                    proj = json.loads(p.read_text(encoding="utf-8"))
                    info["appid"] = proj.get("appid", "")
                except Exception:
                    pass
            elif name == "package.json":
                info["has_package_json"] = True
                try:
                    pkg = json.loads(p.read_text(encoding="utf-8"))
                    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                    if "taro" in str(deps):
                        info["using_taro"] = True
                        info["frameworks"] = [*info.get("frameworks", []), "taro"]
                    if "mpvue" in str(deps):
                        info["using_mpvue"] = True
                        info["frameworks"] = [*info.get("frameworks", []), "mpvue"]
                    if "@dcloudio/uni-app" in deps:
                        info["using_uni_app"] = True
                        info["frameworks"] = [*info.get("frameworks", []), "uni-app"]
                except Exception:
                    pass

    # Find page files (wxml) and component files
    for pattern in ("**/*.wxml", "**/*.json", "**/*.js", "**/*.wxss"):
        for match in root.glob(pattern):
            rel = str(match.relative_to(root))
            if "node_modules" not in rel and ".minium" not in rel:
                if match.suffix == ".wxml":
                    if "components" in rel.lower():
                        if rel not in info["components"]:
                            info["components"].append(rel)
                    else:
                        if rel not in info["pages"]:
                            info["pages"].append(rel)
                elif match.suffix == ".json" and "components" not in rel.lower():
                    if rel not in info["pages"]:
                        info["pages"].append(rel)

    return info
