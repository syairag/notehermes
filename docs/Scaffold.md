# NoteHermes 项目脚手架

## 项目结构

```
notehermes/
├── docs/                           # 项目文档（PRD、架构、设计稿等）
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   └── AGENT_ROLES.md
│
├── client/                         # 客户端代码
│   ├── harmony/                    # HarmonyOS NEXT 客户端
│   │   ├── entry/
│   │   │   └── src/main/ets/
│   │   │       ├── entryability/
│   │   │       │   └── EntryAbility.ets
│   │   │       ├── pages/
│   │   │       │   ├── InboxPage.ets          # 邮箱首页
│   │   │       │   ├── NotesPage.ets          # 笔记首页
│   │   │       │   ├── TasksPage.ets          # 任务首页
│   │   │       │   └── SearchPage.ets         # 全局搜索
│   │   │       ├── components/
│   │   │       │   ├── EmailCard.ets          # 邮件卡片组件
│   │   │       │   ├── NoteEditor.ets         # 笔记编辑器
│   │   │       │   ├── TaskBoard.ets          # 任务看板
│   │   │       │   └── AISummary.ets          # AI 摘要组件
│   │   │       ├── viewmodel/
│   │   │       │   ├── EmailViewModel.ets
│   │   │       │   ├── NoteViewModel.ets
│   │   │       │   └── TaskViewModel.ets
│   │   │       └── common/
│   │   │           ├── HttpClient.ets         # 网络请求封装
│   │   │           └── AIEngine.ets           # AI 接口封装
│   │   └── module.json5
│   │
│   ├── android/                    # Android 客户端
│   │   ├── app/src/main/java/com/notehermes/
│   │   │   ├── ui/
│   │   │   │   ├── inbox/
│   │   │   │   ├── notes/
│   │   │   │   └── tasks/
│   │   │   ├── data/
│   │   │   └── di/
│   │   └── build.gradle.kts
│   │
│   └── web/                        # Web / PWA 客户端
│       ├── src/
│       │   ├── app/                # Next.js App Router
│       │   │   ├── (dashboard)/
│       │   │   │   ├── inbox/page.tsx
│       │   │   │   ├── notes/page.tsx
│       │   │   │   └── tasks/page.tsx
│       │   │   └── layout.tsx
│       │   ├── components/
│       │   ├── lib/                # 共享工具库
│       │   └── hooks/
│       ├── package.json
│       └── tailwind.config.ts
│
├── server/                         # 后端服务
│   ├── api/                        # API Gateway + 业务服务
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── routers/
│   │   │   │   ├── emails.py
│   │   │   │   ├── notes.py
│   │   │   │   ├── tasks.py
│   │   │   │   ├── search.py
│   │   │   │   └── auth.py
│   │   │   ├── services/
│   │   │   │   ├── email_service.py       # IMAP/SMTP 操作
│   │   │   │   ├── note_service.py        # 笔记 CRUD
│   │   │   │   ├── task_service.py        # 任务状态机
│   │   │   │   └── connector_service.py   # 跨模块连接引擎
│   │   │   ├── models/
│   │   │   │   ├── email.py
│   │   │   │   ├── note.py
│   │   │   │   ├── task.py
│   │   │   │   └── entity_link.py
│   │   │   └── config.py
│   │   └── requirements.txt
│   │
│   ├── ai/                         # AI Agent 引擎
│   │   ├── src/
│   │   │   ├── llm_client.py           # 大模型调用封装
│   │   │   ├── embedder.py             # Embedding 服务
│   │   │   ├── prompts/
│   │   │   │   ├── email_summary.txt
│   │   │   │   ├── task_extraction.txt
│   │   │   │   ├── note_tagging.txt
│   │   │   │   └── search_rerank.txt
│   │   │   ├── agent.py                # Agent 编排逻辑
│   │   │   └── local_model.py          # 本地兜底模型
│   │   └── requirements.txt
│   │
│   └── sync/                       # 实时同步服务（WebSocket）
│       ├── src/
│       │   ├── server.py
│       │   └── handlers/
│       └── requirements.txt
│
├── infra/                          # 基础设施配置
│   ├── docker-compose.yml          # 本地开发环境一键启动
│   ├── Dockerfile.api
│   ├── Dockerfile.ai
│   ├── nginx.conf
│   └── scripts/
│       ├── init_db.sql             # 数据库初始化脚本
│       └── seed_data.py            # 测试数据生成
│
├── shared/                         # 跨端共享代码
│   ├── sdk/                        # 核心业务逻辑 SDK（TypeScript）
│   │   ├── src/
│   │   │   ├── types/              # 共享类型定义
│   │   │   ├── api/                # API 客户端
│   │   │   └── utils/              # 工具函数
│   │   └── package.json
│   └── prompts/                    # AI Prompt 模板（各端共享）
│
├── tests/                          # 测试
│   ├── api/
│   ├── ai/
│   └── e2e/
│
├── .github/workflows/              # CI/CD
│   ├── ci.yml
│   └── deploy.yml
│
└── README.md
```

---

## 2. 核心配置模板

### 2.1 docker-compose.yml（本地开发环境）

```yaml
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_USER: notehermes
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: notehermes
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  api:
    build: ./server/api
    ports: ["8000:8000"]
    depends_on: [postgres, redis]
    environment:
      DATABASE_URL: postgresql://notehermes:dev_password@postgres:5432/notehermes
      REDIS_URL: redis://redis:6379

  ai:
    build: ./server/ai
    ports: ["8001:8001"]
    environment:
      LLM_API_KEY: ${LLM_API_KEY}
      EMBEDDING_MODEL: text-embedding-3-small

volumes:
  pgdata:
```

### 2.2 环境变量模板（.env.example）

```bash
# 数据库
DATABASE_URL=postgresql://notehermes:dev_password@localhost:5432/notehermes
REDIS_URL=redis://localhost:6379

# AI 服务
LLM_API_KEY=sk-xxx
LLM_PROVIDER=openrouter  # openrouter | anthropic | qwen
EMBEDDING_MODEL=text-embedding-3-small

# 邮箱服务（可选，用于测试）
IMAP_HOST=imap.gmail.com
IMAP_PORT=993

# 对象存储（可选）
S3_ENDPOINT=
S3_BUCKET=notehermes-attachments
```

---

## 3. 开发启动命令

```bash
# 1. 启动基础设施
cd notehermes/infra && docker-compose up -d

# 2. 安装依赖
cd ../server/api && pip install -r requirements.txt
cd ../ai && pip install -r requirements.txt

# 3. 启动服务
cd ../api && uvicorn main:app --reload --port 8000
cd ../ai && python agent.py  # AI 服务

# 4. 启动 Web 客户端
cd ../../client/web && npm install && npm run dev

# 5. 运行测试
cd ../../tests && pytest
```

---

*文档结束。实际项目初始化时，按此结构创建目录和文件。*
