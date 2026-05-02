# Playwright Agents 单机版 — 设计文档

> 版本: 1.0  
> 日期: 2026-04-28  
> 状态: 设计定稿

---

## 目录

- [第一部分：研究分析与设计原理](#第一部分研究分析与设计原理)
- [第二部分：实现方案](#第二部分实现方案)
- [第三部分：功能说明](#第三部分功能说明)
- [第四部分：对比分析框架](#第四部分对比分析框架)
- [第五部分：部署与使用指南](#第五部分部署与使用指南)

---

# 第一部分：研究分析与设计原理

## 1. 可行性分析

### 1.1 CLI 模式 → 单机程序的切换

| 维度 | CLI 模式 | 单机程序模式 | 可行性 |
|------|----------|-------------|--------|
| 运行时依赖 | 依赖 Claude Code 运行环境 | 独立 Python 进程运行 | **可行** — Playwright 本身就是 Python/Node 独立工具 |
| AI 能力 | Claude 内置理解代码 | 需外接大模型 API | **可行** — 通过阿里云百炼等 API 获得代码理解能力 |
| 上下文感知 | Claude 自动读取工作目录 | 需手动指定项目目录 | **可行** — 文件系统扫描 + 配置化 |
| 测试执行 | Playwright CLI 直接运行 | Playwright CLI 直接运行 | **相同** — 本质都是调用 `npx playwright test` |
| 失败分析 | Claude 分析错误日志 | AI 模型分析错误日志 | **可行** — 将日志 + 截图喂给 AI 分析 |

**结论：完全可行。** 核心能力（Playwright 执行、测试结果分析）不依赖 Claude 特有功能。

### 1.2 IDE 打开代码 → 单机设置目录

单机程序通过配置文件管理项目目录，扫描文件系统获取代码结构，分析项目类型（React/Vue/框架等），定位测试文件。这和 IDE 手动感知代码的差异可以通过以下方式弥补：

- 用户指定代码目录
- 自动扫描 `package.json` / `playwright.config.ts` 等标志性文件
- 通过 AI 分析目录结构理解项目类型

### 1.3 MCP 能力调用 → 单机程序内部能力

远程 MCP Server 本质上是将 Playwright 测试流程封装为 HTTP 可调用的服务。本地实现可以将相同逻辑直接嵌入到程序中，无需 HTTP 调用层。

| 远程 MCP 能力 | 本地等价实现 | 差异 |
|---------------|-------------|------|
| 项目探索 (Planner) | 代码扫描 + AI 分析 | 本地可读取完整代码（无传输限制） |
| 测试生成 (Generator) | AI 生成测试代码 + 写入文件 | 基本一致 |
| 测试执行 | `npx playwright test` | 完全一致 |
| 失败修复 (Healer) | AI 分析日志 + 自动编辑代码 | 本地能直接读写文件，更高效 |

---

## 2. 远程 MCP Server 逻辑推测

### 2.1 总体架构推测

基于对 Playwright Agents MCP 使用体验的逆向推理：

```
┌─────────────────────────────────────────────────┐
│                 MCP Server                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ Planner  │  │Generator │  │   Healer     │   │
│  │  Agent   │  │  Agent   │  │    Agent     │   │
│  └────┬─────┘  └────┬─────┘  └──────┬───────┘   │
│       │              │               │           │
│  ┌────▼──────────────▼───────────────▼───────┐   │
│  │         LLM Service (Claude API)          │   │
│  └───────────────────────────────────────────┘   │
│  ┌───────────────────────────────────────────┐   │
│  │      Browser Automation (Playwright)      │   │
│  └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### 2.2 核心模块推测

#### Planner Agent
- **输入**：项目 URL 或代码
- **处理流**：
  1. 启动浏览器导航到项目页面
  2. 抓取页面快照（Accessibility Snapshot）
  3. 遍历所有页面/路由
  4. 将页面结构和交互点发给 LLM
  5. LLM 输出结构化的测试计划（Markdown）
- **推测依据**：实际观察到 Planner 会打开浏览器访问页面，然后产出一份 markdown，包含测试套件和用例

#### Generator Agent
- **输入**：测试计划（Markdown）
- **处理流**：
  1. 解析测试计划中的套件和用例
  2. 对每个用例，结合页面快照中的元素引用
  3. LLM 生成 Playwright 测试代码
  4. 将代码写入 `.spec.ts` 文件
- **推测依据**：实际观察到 Generator 会抓取页面元素参考然后生成测试代码，产出的代码包含了 selector 引用

#### Healer Agent
- **输入**：失败测试的日志
- **处理流**：
  1. 执行测试，捕获失败
  2. 用 `test_debug` 让测试停在失败位置
  3. 用 `browser_snapshot` 抓取当前页面状态
  4. 将错误信息 + 页面快照发给 LLM
  5. LLM 判断根因（选择器过期/逻辑变化/时序问题）
  6. 自动编辑测试文件修复
  7. 重新执行验证
- **推测依据**：实际观察到 Healer 会 debug 测试、抓 snapshot、分析、然后编辑文件

### 2.3 Key Insight

MCP Server 的核心价值不是"远程执行"，而是**将 Playwright 的浏览器自动化能力 + AI 的代码理解能力组合成一个可编排的工作流**。三个 Agent 本质上都是 Prompt Engineering + 工具调用的组合：

```
[用户请求] → [LLM 理解意图] → [调用浏览器工具获取信息] → [LLM 分析] → [生成代码/报告]
```

---

## 3. 本地 MCP Server 设计方案

### 3.1 设计原理

直接复用 MCP 协议，在本地启动一个 MCP Server 进程，提供与远程版本相同的工具接口。不同的是：

- 本地 Server 直接访问文件系统（无需 GitHub API）
- 本地 Server 使用配置的大模型（如阿里云百炼）代替 Claude
- 本地 Server 的 Playwright 直接操作本地浏览器

### 3.2 核心模块

```
┌──────────────────────────────────────────────────────────┐
│                 Local MCP Server                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────────┐  │
│  │ Planner │ │Generator│ │ Executor│ │   Healer     │  │
│  │ Agent   │ │ Agent   │ │ Agent   │ │    Agent     │  │
│  └────┬────┘ └────┬────┘ └────┬────┘ └──────┬───────┘  │
│       │           │           │              │          │
│  ┌────▼───────────▼───────────▼──────────────▼──────┐  │
│  │          LLM Service (AI Gateway)                │  │
│  │   [当前: 阿里云百炼 | 可切换: OpenAI/其他]        │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │          Playwright Engine                       │  │
│  │   [test execution, browser management, etc.]     │  │
│  └──────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 3.3 与远程版本的能力对比

| 能力 | 远程 MCP Server | 本地 MCP Server | 差距分析 |
|------|----------------|-----------------|---------|
| 代码理解 | Claude（顶尖） | glm-5/其他模型 | AI 能力有差距，但可通过 prompt 工程弥补 |
| 浏览器操作 | Playwright MCP | Playwright MCP | **一致** |
| 文件读写 | 受限（MCP 协议） | 直接文件系统 | **本地更强** |
| 测试执行 | 远程服务器 | 本地机器 | **本地更强**（无网络延迟） |
| 计划生成 | Claude 分析 | AI 分析 | 质量取决于底层 AI 模型 |
| 失败修复 | Claude 分析 + 编辑 | AI 分析 + 编辑 | 质量取决于底层 AI 模型 |
| 实时反馈 | 有网络延迟 | 无网络延迟 | **本地更快** |

---

## 4. 整体架构设计

```
┌─────────────────────────────────────────────────────────────────────┐
│                     单机 Web 应用程序                                 │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐      │
│  │                  浏览器前端 (HTML/CSS/JS)                   │      │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐   │      │
│  │  │项目配置面板│ │测试控制台 │ │结果展示   │ │MCP切换开关 │   │      │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────────┘   │      │
│  └──────────────────────────┬────────────────────────────────┘      │
│                             │ HTTP REST + WebSocket                 │
│  ┌──────────────────────────▼────────────────────────────────┐      │
│  │                  FastAPI 后端                                │      │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐   │      │
│  │  │Project   │ │ Test     │ │ Log      │ │ MCP        │   │      │
│  │  │Manager   │ │ Runner   │ │ Streamer │ │ Proxy      │   │      │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────────┘   │      │
│  └──────────────────────────────────────────────────────────┘      │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │  ┌────────────┐  ┌────────────────┐  ┌──────────────┐   │      │
│  │  │ AI Gateway │  │ Playwright     │  │ Local MCP    │   │      │
│  │  │ (LLM API)  │  │ Integration    │  │ Server       │   │      │
│  │  └────────────┘  └────────────────┘  └──────────────┘   │      │
│  └──────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.1 数据流

```
用户配置项目路径 → 扫描项目结构 → AI分析项目 → 生成测试计划
    → 用户确认计划 → AI生成测试代码 → 写入文件 → 执行测试
    → 收集结果 → AI分析失败 → 自动修复 → 重新执行 → 输出报告
```

---

## 5. 技术选型及理由

| 组件 | 选型 | 理由 |
|------|------|------|
| 后端框架 | FastAPI | Python 异步支持好、WebSocket 原生支持、自动 API 文档 |
| 前端 | 原生 HTML/CSS/JS | 轻量级、无依赖、打包简单 |
| AI 网关 | Python httpx + SSE | 支持流式、非阻塞 |
| MCP 协议实现 | 自定义 HTTP Server | 轻量级、无额外依赖 |
| Playwright 调用 | subprocess + JSON reporter | 稳定、可解析 |
| 配置管理 | YAML + 环境变量 | 清晰、易修改 |
| 进程管理 | asyncio.subprocess | Python 原生异步支持 |

---

# 第二部分：实现方案

## 1. 项目目录结构

```
D:\githome\playwright-agents\
├── docs\
│   └── design-document.md          # 本设计文档
├── config\
│   ├── settings.yaml               # 主配置文件
│   └── .env.example                # 环境变量模板
├── src\
│   ├── main.py                     # 应用入口
│   ├── backend\
│   │   ├── __init__.py
│   │   ├── app.py                  # FastAPI 应用
│   │   ├── routes_api.py           # HTTP API 路由
│   │   ├── routes_ws.py            # WebSocket 路由
│   │   ├── project_manager.py      # 项目管理器
│   │   ├── test_runner.py          # 测试执行器
│   │   └── log_streamer.py         # 日志流
│   ├── frontend\
│   │   ├── index.html              # 主页面
│   │   ├── css\
│   │   │   └── style.css           # 样式
│   │   └── js\
│   │       ├── app.js              # 主逻辑
│   │       ├── api.js              # API 客户端
│   │       └── websocket.js        # WebSocket 客户端
│   ├── ai_gateway\
│   │   ├── __init__.py
│   │   ├── gateway.py              # AI 网关主模块
│   │   ├── providers\
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # 基类
│   │   │   ├── aliyun.py           # 阿里云百炼
│   │   │   └── openai_compat.py    # OpenAI 兼容
│   │   └── prompts.py              # Prompt 模板
│   ├── playwright_core\
│   │   ├── __init__.py
│   │   ├── executor.py             # 测试执行器
│   │   ├── installer.py            # Playwright 安装/更新
│   │   ├── analyzer.py             # 结果分析器
│   │   └── reporter.py             # 报告生成器
│   ├── mcp_server\
│   │   ├── __init__.py
│   │   ├── server.py               # MCP Server 主模块
│   │   ├── agents\
│   │   │   ├── __init__.py
│   │   │   ├── planner.py          # Planner Agent
│   │   │   ├── generator.py        # Generator Agent
│   │   │   ├── executor.py         # Executor Agent
│   │   │   └── healer.py           # Healer Agent
│   │   └── tools.py                # MCP 工具定义
│   └── utils\
│       ├── __init__.py
│       ├── config.py               # 配置加载
│       └── file_utils.py           # 文件操作
├── requirements.txt                # Python 依赖
└── README.md                       # 使用说明
```

---

## 2. 核心模块职责

### 2.1 AI Gateway (`ai_gateway/`)

**职责**：统一所有 AI 模型调用的出入口

- 封装不同模型的 API 差异
- 提供 OpenAI 兼容接口
- 支持流式/非流式响应
- Prompt 模板管理

**接口**：

```python
class AIGateway:
    async def chat(self, messages, stream=False, model=None, **kwargs) -> str | AsyncIterator[str]:
        """统一聊天接口"""
    
    async def analyze_code(self, code_context: str, task: str) -> str:
        """分析代码"""
    
    async def generate_test(self, plan: dict, page_snapshot: str) -> str:
        """生成测试代码"""
    
    async def diagnose_failure(self, error_log: str, page_snapshot: str) -> dict:
        """诊断测试失败"""
```

### 2.2 Playwright Integration (`playwright_core/`)

**职责**：封装 Playwright 的安装、执行、结果分析

- 执行测试并捕获 stdout/stderr
- 解析 JSON 格式的测试结果
- 管理 Playwright 和浏览器版本

**接口**：

```python
class PlaywrightExecutor:
    async def run_tests(self, test_dir: str, project: str = "chromium") -> TestResult:
        """运行测试"""
    
    async def install(self, version: str = None):
        """安装/更新 Playwright"""
    
    def parse_results(self, raw_json: str) -> TestReport:
        """解析测试结果"""
```

### 2.3 Local MCP Server (`mcp_server/`)

**职责**：提供与远程 MCP Server 兼容的接口

- 实现 Planner/Generator/Executor/Healer 四个 Agent
- 每个 Agent 封装为可独立调用的工具
- 通过 HTTP 提供 MCP 兼容接口

### 2.4 Web 后端 (`backend/`)

**职责**：提供 HTTP API 和 WebSocket

- 项目管理（CRUD 项目配置）
- 测试任务调度
- 实时日志推送
- MCP 切换代理

---

## 3. 关键接口设计

### 3.1 HTTP API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/projects` | 添加项目 |
| GET | `/api/projects` | 列出项目 |
| DELETE | `/api/projects/{id}` | 删除项目 |
| POST | `/api/test/start` | 开始测试 |
| GET | `/api/test/status/{task_id}` | 查询测试状态 |
| GET | `/api/test/report/{task_id}` | 获取测试报告 |
| POST | `/api/mcp/switch` | 切换 MCP 模式 |
| GET | `/api/mcp/status` | 查询 MCP 状态 |
| POST | `/api/playwright/update` | 更新 Playwright |

### 3.2 WebSocket

| 事件 | 方向 | 说明 |
|------|------|------|
| `log` | Server → Client | 实时日志 |
| `progress` | Server → Client | 进度更新 |
| `test_complete` | Server → Client | 测试完成通知 |
| `error` | Server → Client | 错误通知 |

---

## 4. 配置管理方案

### `config/settings.yaml`

```yaml
ai:
  provider: aliyun           # 当前 AI 提供商
  model: glm-5               # 模型名称
  temperature: 0.3           # 生成温度
  max_tokens: 4096           # 最大 token 数

playwright:
  version: latest            # Playwright 版本
  default_project: chromium  # 默认浏览器
  timeout: 30000             # 测试超时 (ms)

mcp:
  mode: local                # local | remote
  remote_url: ""             # 远程 MCP Server URL
  remote_token: ""           # 远程 MCP Token

server:
  host: 127.0.0.1
  port: 8765
  log_level: info
```

### `.env` 文件

```bash
# AI 模型 API 密钥
ALIYUN_BAILIAN_API_KEY=your_key_here

# 远程 MCP Server（可选）
REMOTE_MCP_URL=https://...
REMOTE_MCP_TOKEN=...
```

---

## 5. AI 网关设计细节

### 5.1 架构

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────┐
│  业务代码     │────▶│  AI Gateway      │────▶│  Provider   │
│  (Agent/App)  │     │  (统一接口)      │     │  (适配器)   │
└──────────────┘     └──────────────────┘     └─────────────┘
                                                    │
                          ┌─────────────────────────┼─────────┐
                          ▼                         ▼         │
                    ┌────────────┐           ┌────────────┐   │
                    │ 阿里云百炼  │           │ OpenAI 兼容 │   │
                    │ (DashScope)│           │ (OpenRouter│   │
                    └────────────┘           │  等)       │   │
                                             └────────────┘   │
                          ┌────────────────────────────────────┘
                          ▼
                    ┌────────────┐
                    │ 未来扩展... │
                    └────────────┘
```

### 5.2 Prompt 模板

系统设计了多套 Prompt 模板，分别对应 Planner/Generator/Healer 的不同场景。模板放在 `ai_gateway/prompts.py` 中，方便调整优化。

---

## 6. Playwright 集成方案

### 6.1 执行流程

```
1. 定位测试文件 → 2. 构建 npx 命令 → 3. 启动子进程
    → 4. 捕获 stdout/stderr → 5. 解析 JSON 结果
    → 6. 收集截图/日志 → 7. 返回结构化报告
```

### 6.2 版本管理

提供独立的更新脚本 `update_playwright.py`：
- 更新 npm 包版本
- 更新浏览器驱动
- 验证安装

---

# 第三部分：功能说明

## 1. Web 界面功能

### 项目配置面板
- 添加前端代码目录（支持多个）
- 添加后端代码目录（支持多个）
- 查看已配置项目列表
- 删除项目配置

### 测试控制台
- "开始测试" 按钮
- 实时日志显示区（滚动）
- 进度指示器

### 结果展示
- 测试总数 / 通过 / 失败统计
- 每个测试用例的详细结果
- 失败用例的错误信息 + AI 诊断
- 测试报告下载

### MCP 切换开关
- 选择 "本地 MCP" 或 "远程 MCP"
- 配置远程地址（远程模式下）

---

## 2. 使用流程

```
1. 启动应用
2. 在浏览器中打开 Web 界面
3. 在项目配置面板添加代码目录
4. 选择 MCP 模式（本地/远程）
5. 点击 "开始测试"
6. 在控制台观察实时日志
7. 查看测试结果报告
8. （可选）查看 AI 对失败用例的诊断
```

---

## 3. 配置示例

见 `config/settings.yaml` 和 `.env` 文件。

---

## 4. 测试报告格式

```json
{
  "task_id": "task_20260428_001",
  "timestamp": "2026-04-28T10:00:00Z",
  "summary": {
    "total": 34,
    "passed": 31,
    "failed": 3,
    "skipped": 0,
    "duration_ms": 27000
  },
  "suites": [
    {
      "title": "Home / Workbench",
      "file": "tests/home/home-module-cards.spec.ts",
      "tests": [
        {
          "title": "TC-HOME-001: Verify landing page loads",
          "status": "passed",
          "duration_ms": 742
        }
      ]
    }
  ],
  "failures": [
    {
      "test": "TC-ORDER-003: Create orders",
      "error": "Error: ...",
      "diagnosis": "AI 诊断结果...",
      "suggested_fix": "建议修改..."
    }
  ]
}
```

---

# 第四部分：对比分析框架

## 1. 远程 vs 本地 MCP 对比维度

| 维度 | 远程 MCP Server | 本地 MCP Server | 评价方法 |
|------|----------------|-----------------|---------|
| 代码理解准确度 | Claude 顶级 | 取决于配置的模型 | 同一份代码产出的测试计划质量对比 |
| 测试生成质量 | Claude 生成 | AI 模型生成 | 生成代码的语法正确率、覆盖率 |
| 修复成功率 | Claude 分析 | AI 模型分析 | 同一份失败日志的根因判断准确率 |
| 执行速度 | 有网络延迟 | 本地直接执行 | 端到端耗时对比 |
| 功能完整性 | 完整 | 逐步完善 | 边界用例覆盖度 |

## 2. 对比测试方法

1. 用相同项目分别在远程和本地模式下运行
2. 收集两套结果（测试计划、生成代码、执行结果、修复方案）
3. 逐项对比差异

## 3. 预期差异

| 场景 | 远程 MCP | 本地 MCP (glm-5) | 影响 |
|------|---------|-------------------|------|
| 复杂代码理解 | 优秀 | 良好 | 测试计划的深度 |
| 选择器推断 | 准确 | 较准确 | 测试稳定性 |
| 失败根因分析 | 深入 | 较浅 | 修复效率 |
| 边缘情况处理 | 全面 | 有限 | 测试覆盖率 |

---

# 第五部分：部署与使用指南

## 1. 环境要求

- Python 3.10+
- Node.js 18+（Playwright 需要）
- Chrome/Edge 浏览器（Playwright 测试用）

## 2. 安装步骤

```bash
# 1. 克隆/进入项目目录
cd D:\githome\playwright-agents

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 3. 安装 Python 依赖
pip install -r requirements.txt

# 4. 配置环境变量
copy config\.env.example config\.env
# 编辑 .env 填入 API Key

# 5. 启动应用
python src/main.py
```

## 3. 启动命令

```bash
# 开发模式
uvicorn src.backend.app:app --reload --port 8765

# 生产模式
python src/main.py
```

## 4. Playwright 版本更新

```bash
# 方式1：通过 Web 界面点击 "更新 Playwright"
# 方式2：命令行
python src/playwright_core/installer.py --update
```

## 5. AI 模型配置

编辑 `config/settings.yaml`：

```yaml
ai:
  provider: aliyun        # 可选: aliyun, openai_compat
  model: glm-5            # 模型名
```

或通过环境变量覆盖：

```bash
export AI_PROVIDER=openai_compat
export AI_MODEL=gpt-4o
export OPENAI_API_KEY=sk-...
```
