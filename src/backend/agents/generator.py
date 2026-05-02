"""Generator — turns test descriptions into Playwright or Minium test code."""

from src.ai_gateway.gateway import AIGateway
from src.ai_gateway.prompts import build_generator_prompt


class Generator:
    """Generate test code from a test case description."""

    def __init__(self, ai: AIGateway):
        self.ai = ai

    async def run(self, description: str, snapshot: str | None = None, project_type: str = "h5", log=None) -> str:
        if log:
            platform = "Minium" if project_type == "miniprogram" else "Playwright"
            await log(f"[generator] 生成 {platform} 测试代码...\n")

        code = await self.ai.chat_str(build_generator_prompt(description, snapshot, project_type), max_tokens=8192)

        if log:
            await log(f"[generator] 代码已生成 ({len(code)} 字符)\n")
        return code
