# Playwright Agents — 单机版

将 Playwright（H5）和 Minium（微信小程序）的自动化测试流程（计划 → 生成 → 执行 → 修复）封装为独立的单机 Web 应用。

## 功能

- **双平台支持**：H5 页面使用 Playwright，微信小程序使用 Minium，统一管理界面
- **Web 管理界面**：项目管理、测试控制台、实时日志（WebSocket）、结果展示
- **AI 驱动**：集成多个 AI 提供商（阿里云百炼、Anthropic 代理、OpenAI 兼容），负责自动生成测试计划和测试代码
- **Playwright 集成**：自动化测试执行、JSON 报告解析、版本管理
- **Minium 集成**：微信小程序自动化测试，自动生成 config.json/suite.json，解析 minitest 结果
- **失败诊断**：AI 自动分析失败用例，给出修复建议（Healer Agent）
- **项目扫描**：自动检测 H5 项目中的 spec 文件和 MiniProgram 项目中的页面结构

## 系统架构

```
┌──────────────────────────────────────────────┐
│              Web 前端 (HTML/CSS/JS)           │
├──────────────────────────────────────────────┤
│          FastAPI 后端 (HTTP + WebSocket)      │
├──────────┬──────────┬──────────┬─────────────┤
│ AI       │ Planner  │ Generator│ Executor    │
│ Gateway  │ Agent    │ Agent    │ (Playwright │
│(多Provider)│(测试计划)│(生成代码) │ / Minium)   │
└──────────┴──────────┴──────────┴─────────────┘
```

## 环境要求

- Python 3.10+
- Node.js 18+
- Chrome/Edge 浏览器（H5 测试）
- 微信开发者工具 + 小程序项目（小程序测试）

## 快速开始

### 1. 安装依赖

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Playwright 已在项目目录安装：

```bash
npx playwright install chromium
```

Minium（如需测试小程序）：

```bash
pip install minium
```

### 2. 配置 AI API

编辑 `config\.env`:

```env
# provider: anthropic（默认）→ 使用 AI_API_KEY + AI_BASE_URL (Anthropic 协议)
# provider: openai_compat → 使用 AI_API_KEY + AI_BASE_URL (OpenAI 协议)
# provider: aliyun → 使用 AI_API_KEY (DashScope OpenAI 兼容模式)
AI_API_KEY=sk-your-api-key
AI_BASE_URL=https://your-proxy-url/anthropic

# 服务器配置
SERVER_HOST=127.0.0.1
SERVER_PORT=8765
```

或在 `config/settings.yaml` 中配置：

```yaml
ai:
  provider: anthropic       # aliyun | anthropic | openai_compat
  model: glm-5
  api_key: ""
  base_url: ""
  temperature: 0.3
  max_tokens: 4096
```

> **环境变量优先级高于 settings.yaml**，已定义的 env var 会覆盖 yaml 中的值。

### 3. 启动

```bash
python src\main.py
```

浏览器打开 `http://127.0.0.1:8765`

## 使用流程

### H5 项目

1. **添加项目** → 选择"H5"类型，填写项目名称，选择代码目录
2. **开始测试** → 选择项目，点击"开始测试"
3. **AI 规划** → Planner Agent 自动分析项目结构，生成测试计划
4. **代码生成** → Generator Agent 根据计划生成 Playwright 测试代码
5. **自动执行** → Playwright 运行测试，实时显示日志
6. **结果报告** → 展示通过/失败统计，失败用例自动触发 Healer 诊断

### 微信小程序项目

1. **添加项目** → 选择"小程序"类型，填写项目名称、代码目录、微信开发者工具 CLI 路径
2. **选择基础平台** → 根据小程序框架选择 `ide`（原生）或 `ide_python`（Taro/uni-app 等）
3. **后续流程** → 与 H5 相同，AI 生成 Minium 测试代码并执行

## AI 提供商

系统通过 AI Gateway 统一管理多个 LLM 提供商：

| 提供商 | provider 值 | API 协议 | 适用场景 |
|--------|-----------|---------|---------|
| 阿里云百炼 | `aliyun` | DashScope OpenAI 兼容 | 国内直连 |
| Anthropic 代理 | `anthropic` | Anthropic Messages API | DashScope Anthropic 代理 |
| OpenAI 兼容 | `openai_compat` | OpenAI Chat API | 通用 OpenAI 格式 |

Gateway 会自动转换消息格式，对上层 Agent 透明。

## 四种 AI Agent

| Agent | 功能 | 平台感知 |
|-------|------|---------|
| **Planner** | 分析项目结构，生成测试计划（功能点分解 + 测试策略） | 根据 project_type 选择 H5/小程序 的提示词 |
| **Generator** | 根据计划生成可执行的测试代码 | 生成 Playwright `spec.ts` 或 Minium Python 测试 |
| **Executor** | 运行测试并解析结果 | 创建 PlaywrightExecutor 或 MiniumExecutor |
| **Healer** | 分析失败用例，给出修复建议 | 根据平台类型适配错误分析策略 |

## 关键技术实现

### Playwright JSON 报告解析

Playwright 的 `--reporter json` 输出层级化的 suites 结构（describe 块嵌套）。解析器需要递归处理：

```python
def _process_suites(suites_data, parent_file=""):
    for suite_data in suites_data:
        # 处理当前层级的 specs
        for spec in suite_data.get("specs", []):
            ...
        # 递归处理嵌套 suites
        if suite_data.get("suites"):
            nested = _process_suites(suite_data["suites"], file)
            suites.extend(nested)
```

同时处理两种状态约定：
- `result.status` 可能是 `"passed"` 或 `"expected"`
- 失败状态包括 `"failed"`、`"unexpected"`、`"timedOut"`

### 目录选择器

Chrome 89+ 支持 `showDirectoryPicker()` API，可获取完整目录路径。fallback 使用 `<input webkitdirectory>` + 手动输入路径。

### Windows 兼容

- 使用 `asyncio.create_subprocess_shell` 代替 `create_subprocess_exec`，以正确解析 `.cmd` 文件（npx.cmd）
- 使用 `shlex.join()` 构造命令行字符串

### 小程序测试集成

- **Minium 1.6.0**：微信官方 Python 测试框架
- 自动生成 `config.json`（devtools 路径、平台选项）和 `suite.json`（测试用例列表）
- 通过 `minitest` CLI 执行，解析 JSON 输出文件
- 支持 `ide`（原生小程序）和 `ide_python`（Taro/uni-app/mpvue）两种平台

## 项目结构

```
D:\githome\playwright-agents\
├── config\                        # 配置文件
│   ├── settings.yaml              # 主配置（AI 提供商、模型、服务器等）
│   └── .env                       # API 密钥和环境变量
├── src\
│   ├── main.py                    # 应用入口（uvicorn 启动）
│   ├── backend\                   # FastAPI 后端
│   │   ├── api.py                 # REST API + WebSocket 端点
│   │   ├── project_manager.py     # 项目管理（CRUD、文件扫描）
│   │   ├── test_runner.py         # 测试执行调度（平台感知）
│   │   ├── prompts.py             # AI 提示词模板（H5 + 小程序）
│   │   └── miniprogram\           # 微信小程序支持
│   │       └── executor.py        # MiniumExecutor（config/suite 生成、结果解析）
│   ├── frontend\                  # Web 前端
│   │   ├── index.html             # 主页面（项目列表 + 控制台 + 结果）
│   │   ├── css\style.css          # 样式（双平台主题色、响应式布局）
│   │   └── js\
│   │       ├── app.js             # 主逻辑（平台切换、目录选择、表单处理）
│   │       └── api.js             # API 调用封装
│   ├── ai_gateway\                # AI 模型网关
│   │   ├── gateway.py             # 统一入口，按 provider 分发
│   │   └── providers\
│   │       ├── base.py            # LLMProvider 抽象基类
│   │       ├── aliyun.py          # 阿里云百炼（DashScope）
│   │       ├── anthropic.py       # Anthropic 协议（DashScope 代理）
│   │       └── openai_compat.py   # OpenAI 兼容格式
│   ├── mcp_server\                # MCP Server（Agent 执行引擎）
│   │   ├── server.py              # MCP 协议实现
│   │   └── agents.py              # 4 种 Agent 实现
│   ├── playwright_core\           # Playwright 集成
│   │   └── executor.py            # PlaywrightExecutor（运行 + 报告解析）
│   └── utils\
│       ├── config.py              # 配置加载（yaml + env 合并）
│       └── file_utils.py          # 文件工具（目录扫描、小程序结构分析）
├── data\                          # 运行时数据（项目配置、报告）
├── requirements.txt               # Python 依赖
└── README.md                      # 本文件
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects` | 获取项目列表 |
| POST | `/api/projects` | 添加项目（支持 H5/小程序） |
| DELETE | `/api/projects/{id}` | 删除项目 |
| POST | `/api/test/start` | 开始测试 |
| GET | `/api/projects/{id}/files` | 扫描项目文件 |
| WS | `/ws/test/{task_id}` | 测试日志实时推送 |
| GET | `/api/test/report/{task_id}` | 获取测试报告 |
| GET | `/api/config` | 获取系统配置 |
| PUT | `/api/config` | 更新系统配置 |

启动后访问 `http://127.0.0.1:8765/docs` 查看完整 OpenAPI 文档。

## 环境变量参考

| 变量 | 对应配置路径 | 说明 |
|------|-------------|------|
| `AI_API_KEY` | ai.api_key | API 密钥 |
| `AI_BASE_URL` | ai.base_url | API 地址 |
| `AI_PROVIDER` | ai.provider | 提供商（aliyun/anthropic/openai_compat） |
| `AI_MODEL` | ai.model | 模型名称 |
| `AI_TEMPERATURE` | ai.temperature | 温度参数 |
| `AI_MAX_TOKENS` | ai.max_tokens | 最大 Token 数 |
| `SERVER_HOST` | server.host | 监听地址 |
| `SERVER_PORT` | server.port | 监听端口 |
| `PLAYWRIGHT_PROJECT` | playwright.default_project | 默认浏览器项目 |
| `PLAYWRIGHT_TIMEOUT` | playwright.timeout | 测试超时(ms) |

## 常见问题

### JSON 报告只解析了 1 条测试

Playwright `--reporter json` 的输出中，`describe` 嵌套块对应 `suites[].suites[]`。旧版解析器只处理了顶层 `specs`，新版已改为递归遍历所有层级。

### npx 命令找不到

Windows 上 `npx` 实际是 `npx.cmd`，`create_subprocess_exec` 无法解析。改用 `create_subprocess_shell` + `shlex.join()`。

### API 返回 404

确认 `.env` 中的 `AI_BASE_URL` 对应的 provider 协议与实际 API 匹配：
- `anthropic` provider → 需要支持 `/v1/messages` 的 Anthropic 协议端点
- `openai_compat` provider → 需要支持 `/v1/chat/completions` 的 OpenAI 协议端点
- `aliyun` provider → DashScope 兼容模式

### 目录选择器无法获取路径

Chrome 89+ 使用 `showDirectoryPicker()` 自动获取路径。老旧浏览器或不安全上下文（HTTP）会 fallback 到手动输入。

## 许可证

MIT
#   p l a y w r i g h t s - a g e n t s  
 