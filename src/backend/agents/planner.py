"""Planner — analyses a project and produces a test plan (H5 or MiniProgram)."""

from src.ai_gateway.gateway import AIGateway
from src.ai_gateway.prompts import build_planner_prompt
from src.utils.file_utils import scan_project, scan_miniprogram


class Planner:
    """Analyse project structure and generate a test plan."""

    def __init__(self, ai: AIGateway):
        self.ai = ai

    async def run(self, project_root: str, project_type: str = "h5", expanded: bool = False, log=None) -> str:
        if log:
            mode = "扩充" if expanded else "标准"
            await log(f"[planner] 扫描项目结构 ({project_type}, {mode}模式)...\n")

        info = scan_miniprogram(project_root) if project_type == "miniprogram" else scan_project(project_root)

        if project_type == "miniprogram":
            summary = (
                f"项目路径: {info['root']}\n"
                f"类型: 微信小程序\n"
                f"有 app.json: {info['has_app_json']}\n"
                f"有 project.config: {info['has_project_config']}\n"
                f"框架: {info.get('frameworks', []) or '原生'}\n"
                f"页面数: {len(info.get('pages', []))}\n"
                f"组件数: {len(info.get('components', []))}\n"
                f"使用 Taro: {info.get('using_taro', False)}\n"
                f"使用 Uni-app: {info.get('using_uni_app', False)}\n"
            )
        else:
            summary = (
                f"项目路径: {info['root']}\n"
                f"框架: {', '.join(info['frameworks']) or '未知'}\n"
                f"有 package.json: {info['has_package_json']}\n"
                f"有 Playwright 配置: {info['has_playwright_config']}\n"
                f"测试目录: {', '.join(info['test_dirs']) or '无'}\n"
                f"已有测试文件: {len(info['spec_files'])}\n"
            )

        if log:
            await log(f"[planner] {summary}\n")
            await log("[planner] AI 生成测试计划中...\n")

        plan = await self.ai.chat_str(build_planner_prompt(summary, project_type, expanded=expanded))
        if log:
            await log(f"[planner] 测试计划已生成 ({len(plan)} 字符)\n")
        return plan
