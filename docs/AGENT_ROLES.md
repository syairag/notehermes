# 首批 Agent 岗位描述（技能配置）

## NoteHermes 项目首批招聘

---

## Agent #1 — 全栈后端工程师（Python/FastAPI + AI）

### 基本信息
- **代号：** `backend-ai-eng`
- **优先级：** 🔴 最高（MVP 核心）
- **招聘时间：** Week 1（与项目同步启动）
- **专属 AI 模型：** `qwen3-coder-next`（最新代码模型，擅长 SQL/API 生成）
- **专属 AI 模型：** `qwen3-coder-next`（最新代码模型，擅长 SQL/API 生成）

### 核心职责
1. FastAPI 后端服务开发（邮箱、笔记、任务三大模块 API）
2. AI 集成：邮件摘要 Prompt 工程、任务提取 Pipeline、Embedding 服务
3. pgvector 向量检索实现与优化
4. IMAP/SMTP 协议对接（Gmail/Outlook/企业邮箱）
5. PostgreSQL 数据模型设计与优化

### 技能要求
```yaml
必需技能:
  - Python 3.11+（FastAPI / Pydantic / SQLAlchemy）
  - LLM API 集成（DashScope / 通义灵码 Coding 通道）
  - 配置专属模型：qwen3-coder-next
  - 向量数据库（pgvector / Milvus / Weaviate）
  - IMAP/SMTP 协议
  - PostgreSQL 15+（JSONB / 事务 / 索引优化）
  - Docker / Docker Compose

加分项:
  - LangChain / LlamaIndex 经验
  - RAG（检索增强生成）实战经验
  - 邮件系统集成经验
  - 本地 LLM 部署经验（llama.cpp / Ollama）
```

### 首月交付物
- [ ] 邮箱接入 API（IMAP 同步 + 邮件 CRUD）
- [ ] AI 邮件摘要 + 待办提取 Pipeline
- [ ] 笔记服务 API（CRUD + 标签系统）
- [ ] 任务服务 API + 状态机
- [ ] pgvector 语义搜索接口

---

## Agent #2 — 前端/客户端工程师（HarmonyOS + Web）

### 基本信息
- **代号：** `frontend-client-eng`
- **优先级：** 🔴 最高（与后端并行）
- **招聘时间：** Week 1
- **专属 AI 模型：** `qwen3.6-plus`（视觉理解 + 深度思考，擅长 UI 还原）
- **专属 AI 模型：** `qwen3.6-plus`（视觉理解 + 深度思考，擅长 UI 还原）

### 核心职责
1. HarmonyOS NEXT 客户端开发（ArkTS/ArkUI）
   - 邮箱列表 + 邮件详情 + AI 摘要展示
   - 笔记编辑器 + 搜索界面
   - 任务看板（To Do / Doing / Done）
2. Web/PWA 客户端开发（Next.js 14 + TailwindCSS）
   - 与鸿蒙端共享核心逻辑（SDK 封装）
   - 响应式布局适配桌面/移动端
3. 实时同步集成（WebSocket 连接）
4. 离线缓存策略（本地数据库 + 同步队列）

### 技能要求
```yaml
必需技能:
  - ArkTS + ArkUI（HarmonyOS NEXT 开发）
  - Next.js 14+（App Router + Server Components）
  - TypeScript / React
  - TailwindCSS
  - 状态管理（zustand / Redux / ArkUI 状态）
  - 网络请求封装 + 离线缓存

加分项:
  - PWA 开发经验
  - 富文本编辑器开发（Markdown / ProseMirror / TipTap）
  - 跨端共享 SDK 设计经验
  - WebSocket 实时通信
```

### 首月交付物
- [ ] HarmonyOS 三模块基础 UI（邮箱/笔记/任务）
- [ ] Web 端 Dashboard 页面
- [ ] 邮件卡片 + AI 摘要组件
- [ ] Markdown 笔记编辑器
- [ ] 任务看板交互
- [ ] 跨端共享 SDK v0.1

---

## Agent #3 — AI/NLP 工程师（Prompt 工程 + RAG）

### 基本信息
- **代号：** `ai-engineer`
- **优先级：** 🟡 次优先级（但需提前介入）
- **招聘时间：** Week 2（后端 API 框架搭建后立即介入）
- **专属 AI 模型：** `glm-5`（深度思考，擅长 Prompt 调优与逻辑推理）
- **专属 AI 模型：** `glm-5`（深度思考，擅长 Prompt 调优与逻辑推理）

### 核心职责
1. Prompt 工程：邮件摘要、任务提取、笔记标签、搜索重排
2. RAG Pipeline 搭建：笔记向量化存储 + 语义检索 + 上下文增强
3. 多模型适配：云端大模型 vs 本地小模型的自动切换策略
4. 输出质量控制：AI 提取结果的置信度评分、错误修正机制
5. 隐私脱敏：邮件/笔记内容发送给 AI 前的自动脱敏处理

### 技能要求
```yaml
必需技能:
  - Prompt Engineering（结构化输出、Few-shot、CoT）
  - Embedding 模型（text-embedding / bge-m3）
  - 向量检索优化（Top-K 策略、混合检索）
  - Python（LangChain / LlamaIndex / 自研 Pipeline）
  - JSON Schema 约束输出

加分项:
  - 信息抽取（NER、关系抽取）经验
  - 邮件 NLP 处理经验
  - 本地模型量化部署（GGUF / AWQ）
  - AI 可观测性（LangSmith / Arize Phoenix）
```

### 首月交付物
- [ ] 邮件摘要 + 待办提取 Prompt 模板库
- [ ] 笔记自动标签分类 Pipeline
- [ ] 语义搜索 RAG Pipeline（v1）
- [ ] AI 输出置信度评分机制
- [ ] 隐私脱敏中间件

---

## Agent #4 — QA 测试工程师

### 基本信息
- **代号：** `qa-engineer`
- **优先级：** 🟡 次优先级
- **招聘时间：** Week 3（开发中期介入，编写用例 + 早期测试）
- **专属 AI 模型：** `MiniMax-M2.5`（极速深度思考，适合批量生成用例）

### 核心职责
1. 功能测试（邮箱接入、笔记编辑、任务流转全流程）
2. AI 输出质量测试（摘要准确性、任务提取召回率/准确率）
3. 跨端兼容性测试（HarmonyOS / Android / Web）
4. 性能测试（首屏加载、AI 响应延迟、搜索响应时间）
5. 隐私安全测试（数据脱敏验证、本地模式测试）

### 技能要求
```yaml
必需技能:
  - 自动化测试框架（pytest / Playwright）
  - API 测试（Postman / httpx）
  - AI 输出评估方法（人工标注对比、自动化评分）
  - 跨端测试策略

加分项:
  - LLM 输出质量评估经验
  - 性能测试工具（k6 / Locust）
  - 安全测试基础
```

### 首月交付物
- [ ] 功能测试用例集（覆盖 P0 功能）
- [ ] AI 输出质量评估框架
- [ ] 自动化测试 CI 集成
- [ ] 性能基准报告

---

## 📅 招聘时间线

```
Week 1 必须到位：
├── Agent #1 全栈后端工程师 ← 搭 API + 接 AI
└── Agent #2 前端客户端工程师 ← 搭 UI + 接 SDK

Week 2 到位：
└── Agent #3 AI/NLP 工程师 ← 优化 Prompt + RAG Pipeline

Week 3 到位（提前介入）：
└── Agent #4 QA 测试工程师 ← 写用例 + 早期功能测试

老板预算参考（4人 + 我 = 5人团队）：
├── MVP 阶段（6周）人力成本可控
├── AI 工程师提前介入，确保 Phase 1 的 AI 体验达标
├── QA 提前介入，降低返工风险
└── 后续按产品表现决定是否扩充 Phase 2 团队
```

---

*文档结束。待 PRD 审批后开始招聘/配置 Agent。*
