"""Diagnostic analyzer — categorises test failures into root-cause buckets.

Category          | Meaning
------------------|--------------------------------------------------
app_bug           | 被测对象存在缺陷 (bug in the tested application)
tool_issue        | 测试工具或基础设施问题 (tool/infrastructure issue)
test_issue        | 测试用例本身存在问题 (bug in the test case itself)
unknown           | 无法确定 (could not be classified)
"""

import re
from typing import Any

# ── Category labels (shown in reports) ──

CATEGORY_LABEL: dict[str, str] = {
    "app_bug": "被测对象存在缺陷",
    "tool_issue": "测试工具或基础设施问题",
    "test_issue": "测试用例本身存在问题",
    "unknown": "无法确定",
}

# ── Error pattern definitions ──
# (category, compiled_regex, explanation)

_PATTERNS: list[tuple[str, re.Pattern, str]] = [
    # ── Tool / infrastructure issues ──
    (
        "tool_issue",
        re.compile(r"Connection(?:Refused|Error| refused| failed)", re.I),
        "无法连接到 DevTools / 小程序IDE，请检查工具是否已登录并畅通",
    ),
    (
        "tool_issue",
        re.compile(r"(?:Socket|WebSocket).*(?:closed|disconnect)", re.I),
        "WebSocket 连接断开，IDE 可能意外关闭或网络中断",
    ),
    (
        "tool_issue",
        re.compile(r"(?:ReadTimeout|MiniTimeoutError|TimeoutError)", re.I),
        "操作超时，可能是环境负载过高或网络延迟",
    ),
    (
        "tool_issue",
        re.compile(r"PageNotFoundError|page not found", re.I),
        "页面路径不存在或未在 app.json 中注册",
    ),
    (
        "tool_issue",
        re.compile(r"MiniumError", re.I),
        "Minium 框架内部错误，可能是 IDE 版本不兼容",
    ),
    # Navigation failures due to page stack limits
    (
        "tool_issue",
        re.compile(r"navigateTo.*fail|navigate_to.*fail|webview.*limit", re.I),
        "页面栈溢出，连续 navigate_to 超过小程序 webview 数量限制",
    ),
    (
        "tool_issue",
        re.compile(r"app\.(?:switch_tab|navigate_to).*Error", re.I),
        "页面导航失败，请确认页面路径和导航方式（tabBar vs 非 tabBar）",
    ),
    # ── Test-case issues ──
    (
        "test_issue",
        re.compile(r"SyntaxError|IndentationError|TabError", re.I),
        "测试代码存在语法错误（缩进、括号不匹配等）",
    ),
    (
        "test_issue",
        re.compile(r"NameError", re.I),
        "测试代码使用了未定义的变量或函数",
    ),
    (
        "test_issue",
        re.compile(r"AttributeError.*(?:object has no attribute|module.*no attr)", re.I),
        "测试代码调用了 Minium 不存在的 API",
    ),
    (
        "test_issue",
        re.compile(r"ImportError|ModuleNotFoundError", re.I),
        "测试代码导入模块失败，缺少依赖",
    ),
    (
        "test_issue",
        re.compile(r"TypeError.*(?:unexpected keyword|positional argument)", re.I),
        "测试代码调用了错误的函数签名",
    ),
    (
        "test_issue",
        re.compile(r"py_compile|PyCompileError", re.I),
        "生成的测试文件存在 Python 编译错误",
    ),
    # MiniElementNotFoundError alone is ambiguous — subclass check below
    # ── Application bugs ──
    (
        "app_bug",
        re.compile(r"AssertionError|assertEqual|assertIn|assertTrue.*failed", re.I),
        "断言失败，被测对象行为与预期不符（文案、状态、数据等）",
    ),
    (
        "app_bug",
        re.compile(r"expected.*but found|expected.*actual", re.I),
        "页面实际内容与预期不符，可能是被测对象缺陷",
    ),
]


def _has_vague_selector(code: str | None) -> bool:
    """Check if code uses generic selectors unlikely to match real WXML."""
    if not code:
        return False
    vague = re.findall(
        r"""(?:get_element|get_elements)\s*\(\s*["']\.[a-z]+(?:-[a-z]+)*["']""",
        code,
    )
    # If most selectors are single-class without component prefixes, flag it
    return len(vague) > 5


def _match_mini_element_not_found(error: str, code: str | None) -> str | None:
    """Sub-rule for MiniElementNotFoundError — needs code context."""
    if "MiniElementNotFoundError" not in error:
        return None
    # If we have no code to inspect, classify as test_issue (likely wrong selector)
    if not code:
        return "test_issue"
    # If code uses vague selectors, it's a test issue
    if _has_vague_selector(code):
        return "test_issue"
    # Selector looks plausible but element not found — likely app bug
    return "app_bug"


def analyze(error: str, code: str | None = None, snapshot: str | None = None) -> dict[str, Any]:
    """Analyse a test failure and return a structured diagnosis.

    Returns
    -------
    dict with keys:
        category       — str: one of the four category codes
        category_label — str: Chinese label
        explanation    — str: human-readable explanation
        confidence     — str: "high" | "medium" | "low"
    """
    if not error or not error.strip():
        return _result("unknown", "无错误信息", "low")

    # ── 1. Check MiniElementNotFoundError with code context ──
    cat = _match_mini_element_not_found(error, code)
    if cat:
        if cat == "test_issue":
            return _result(
                cat,
                "元素选择器与页面实际结构不匹配，使用了猜测的类名而非 WXML 中的真实类名",
                "medium",
            )
        return _result(
            cat,
            "元素未找到但选择器与页面结构匹配，可能是被测对象缺少该元素或其状态不正确",
            "medium",
        )

    # ── 2. Check known patterns ──
    for category, pattern, explanation in _PATTERNS:
        if pattern.search(error):
            return _result(category, explanation, "high")

    # ── 3. Fallback: generic classification by error type ──
    if re.search(r"(?:assert|expect|should)", error, re.I):
        return _result("app_bug", "断言失败，建议结合被测对象确认行为是否符合预期", "medium")

    if re.search(r"(?:loading|load|render|display)", error, re.I):
        return _result("tool_issue", "页面加载或渲染超时，建议检查环境状态", "medium")

    return _result("unknown", f"未能自动识别错误类型: {error[:200]}", "low")


def _result(category: str, explanation: str, confidence: str) -> dict[str, Any]:
    return {
        "category": category,
        "category_label": CATEGORY_LABEL.get(category, "无法确定"),
        "explanation": explanation,
        "confidence": confidence,
    }
