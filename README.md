# NoteHermes 🤖 — AI-Driven Smart Workspace

**NoteHermes** 是一款 AI 驱动的智能工作台，深度整合**邮箱、笔记、任务**三大核心模块。
> "邮件自动变任务，笔记自动变知识，任务自动被跟进。"

## ✨ 核心特性

- 📧 **智能邮箱接入**：支持 IMAP/SMTP，**原生支持国内世纪互联版 (21Vianet) Microsoft 365**。
- 🤖 **AI 任务自动提取**：Agent 自动阅读邮件，智能识别待办事项、截止日期和优先级，一键生成任务。
- 🔍 **活的知识库**：基于 `pgvector` 的笔记语义搜索，笔记不再只是死文本，而是可检索的知识资产。
- 📱 **多端适配**：提供 Web (Next.js) 和 鸿蒙 (HarmonyOS) 客户端支持。
- 🧠 **多模型智能路由**：后端任务自动使用 `qwen3-coder-next`，AI 逻辑自动使用 `glm-5`，按需分配，降本增效。

---

## 🚀 快速开始 (Quick Start)

### 1. 环境要求
- Docker & Docker Compose
- Python 3.11+ (仅开发模式需要)
- Node.js 18+ (仅前端开发需要)

### 2. 启动基础设施 (数据库 & Redis)

```bash
cd infra
docker-compose up -d
```

### 3. 配置环境变量

复制 `.env.example` 到 `.env` 并填写关键配置：

```bash
cp .env.example .env
# 编辑 .env 文件...
```

**必须配置的项：**
- `DASHSCOPE_API_KEY`: 您的阿里云 DashScope API Key (用于 AI 引擎)。
- `DATABASE_URL`: PostgreSQL 连接地址 (默认已配好)。

### 4. 启动服务

**方式 A：一键启动所有服务 (推荐)**
```bash
# 在项目根目录
docker-compose -f infra/docker-compose.yml up --build
```

**方式 B：开发模式启动**

*启动后端 API:*
```bash
cd server/api
pip install -r requirements.txt
uvicorn src.main:app --reload
```

*启动 AI 引擎:*
```bash
cd server/ai
pip install -r requirements.txt
python src/agent.py
```

*启动 Web 客户端:*
```bash
cd client/web
npm install
npm run dev
```

---

## 📚 API 文档 (核心接口)

启动后，访问 `http://localhost:8000/docs` 查看 Swagger UI。

### 📧 邮箱模块
- `POST /api/v1/emails/sync`: 同步并处理新邮件。

### ✅ 任务模块 (核心)
- `GET /api/v1/tasks/`: 获取任务列表 (支持 `?status=todo` 过滤)。
- `POST /api/v1/tasks/`: 手动创建任务。
- **`POST /api/v1/tasks/extract-from-email`**: **🌟 AI 自动提取任务**。
  - **Body**: `{ "email_content": "..." }`
  - **Action**: AI 分析内容并自动在数据库创建任务。

### 📝 笔记模块
- `GET /api/v1/notes/`: 获取笔记列表。
- `POST /api/v1/notes/`: 创建笔记 (支持标签)。

---

## 🛠️ 项目结构

```text
notehermes/
├── docs/               # 📝 PRD, 架构设计, Agent 岗位描述
├── server/
│   ├── api/            # 🐍 FastAPI 后端服务 (业务逻辑/数据库)
│   └── ai/             # 🧠 Python AI 引擎 (模型调用/Prompt)
├── client/
│   ├── web/            # 🌐 Next.js Web 客户端 (看板 UI)
│   └── harmony/        # 📱 HarmonyOS 客户端 (ArkTS)
├── shared/             # 🔗 跨端共享 SDK
└── infra/              # 🐳 Docker 配置与数据库脚本
```

---

## 👥 研发团队配置

项目内置了基于角色的 **AI 模型路由** (`server/ai/src/config.py`)，各角色使用专属模型：

| 角色 | 专属模型 | 职责 |
| :--- | :--- | :--- |
| **Agent #1 (后端)** | `qwen3-coder-next` | 代码生成，数据库操作，API 逻辑 |
| **Agent #2 (前端)** | `qwen3.6-plus` | UI 构建，视觉理解，复杂组件开发 |
| **Agent #3 (AI 逻辑)** | `glm-5` | 意图识别，推理分析，Prompt 调优 |
| **Agent #4 (QA)** | `MiniMax-M2.5` | 测试用例生成，代码审查 |

---

## 📄 License

Private - All rights reserved by Toby & NoteHermes Team.
