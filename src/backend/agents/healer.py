"""Healer — diagnoses failing tests and suggests fixes (H5 or MiniProgram)."""

import json

from src.ai_gateway.gateway import AIGateway
from src.ai_gateway.prompts import build_healer_prompt
from src.backend import diagnostic


class Healer:
    """Analyse test failures, suggest fixes, and classify root-cause category."""

    def __init__(self, ai: AIGateway):
        self.ai = ai

    async def diagnose(self, error: str, snapshot: str | None = None, code: str | None = None, project_type: str = "h5", log=None) -> dict:
        if log:
            await log("[healer] 分析失败原因...\n")

        # 1. Rule-based diagnosis (fast, offline)
        rule_diag = diagnostic.analyze(error, code=code, snapshot=snapshot)

        # 2. AI-powered diagnosis (detailed root cause + fix)
        result = await self.ai.chat_str(build_healer_prompt(error, snapshot, code, project_type))
        if log:
            await log(f"[healer] AI 诊断完成 ({len(result)} 字符)\n")

        ai_diag = {}
        try:
            start = result.index("{")
            end = result.rindex("}") + 1
            ai_diag = json.loads(result[start:end])
        except (ValueError, json.JSONDecodeError):
            ai_diag = {"root_cause": result[:300], "fix_suggestion": "", "confidence": "low"}

        # 3. Merge: prefer rule-based for category, AI for details
        merged = {
            "category": rule_diag["category"],
            "category_label": rule_diag["category_label"],
            "explanation": rule_diag["explanation"],
            "root_cause": ai_diag.get("root_cause", ""),
            "fix_suggestion": ai_diag.get("fix_suggestion", ""),
            "confidence": rule_diag["confidence"]
            if rule_diag["confidence"] == "high"
            else ai_diag.get("confidence", "low"),
        }
        return merged
