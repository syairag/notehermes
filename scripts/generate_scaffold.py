#!/usr/bin/env python3
"""
NoteHermes Project Scaffold Generator
Creates the full project structure as defined in docs/Scaffold.md
"""

import os
import json

BASE_DIR = "/opt/data/projects/notehermes"

def create_file(path, content=""):
    """Create a file with given content."""
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"✅ Created {path}")

def create_readme(path):
    create_file(path, f"# {os.path.basename(path).replace('.md', '')}\n\nDirectory for {os.path.basename(path).replace('.md', '')} module.\n")

# ================= INFRASTRUCTURE =================

create_file("infra/.gitkeep")

create_file("infra/docker-compose.yml", """version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg15
    container_name: notehermes-postgres
    environment:
      POSTGRES_USER: notehermes
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: notehermes
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U notehermes"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: notehermes-redis
    ports: ["6379:6379"]
    volumes: ["redisdata:/data"]

  api:
    build:
      context: ../server/api
      dockerfile: ../../infra/Dockerfile.api
    container_name: notehermes-api
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: postgresql://notehermes:dev_password@postgres:5432/notehermes
      REDIS_URL: redis://redis:6379
      LLM_API_KEY: ${LLM_API_KEY}
      LLM_PROVIDER: ${LLM_PROVIDER:-openrouter}
      AI_SERVICE_URL: http://ai:8001
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
      ai:
        condition: service_started

  ai:
    build:
      context: ../server/ai
      dockerfile: ../../infra/Dockerfile.ai
    container_name: notehermes-ai
    ports: ["8001:8001"]
    environment:
      LLM_API_KEY: ${LLM_API_KEY}
      EMBEDDING_MODEL: text-embedding-3-small

volumes:
  pgdata:
  redisdata:
""")

create_file("infra/Dockerfile.api", """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
""")

create_file("infra/Dockerfile.ai", """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "src/agent.py"]
""")

create_file("infra/scripts/init_db.sql", """-- NoteHermes Database Initialization

CREATE EXTENSION IF NOT EXISTS vector;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Emails Table
CREATE TABLE IF NOT EXISTS emails (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    message_id VARCHAR(255) UNIQUE,
    subject VARCHAR(500),
    from_address VARCHAR(255),
    to_address VARCHAR(255),
    body TEXT,
    summary TEXT,
    received_at TIMESTAMPTZ,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Notes Table
CREATE TABLE IF NOT EXISTS notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(500),
    content TEXT,
    tags VARCHAR(50)[],
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tasks Table
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'todo', -- todo, doing, done
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high, urgent
    due_date TIMESTAMPTZ,
    source_type VARCHAR(20), -- manual, email, note
    source_id UUID,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Entity Links (Cross-module connections)
CREATE TABLE IF NOT EXISTS entity_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type VARCHAR(20) NOT NULL, -- email, note, task
    source_id UUID NOT NULL,
    target_type VARCHAR(20) NOT NULL,
    target_id UUID NOT NULL,
    link_type VARCHAR(20), -- extracted_from, related_to, attachment
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_emails_user_id ON emails(user_id);
CREATE INDEX IF NOT EXISTS idx_emails_received_at ON emails(received_at DESC);
CREATE INDEX IF NOT EXISTS idx_notes_user_id ON notes(user_id);
CREATE INDEX IF NOT EXISTS idx_notes_embedding ON notes USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_entity_links_source ON entity_links(source_type, source_id);
""")

create_file("infra/scripts/.gitkeep")

# ================= SERVER: API =================

create_file("server/api/.gitkeep")
create_file("server/api/requirements.txt", """fastapi==0.110.0
uvicorn[standard]==0.27.1
pydantic==2.6.3
pydantic-settings==2.2.1
sqlalchemy==2.0.28
asyncpg==0.29.0
alembic==1.13.1
redis==5.0.3
httpx==0.27.0
python-dotenv==1.0.1
pyjwt==2.8.0
passlib[bcrypt]==1.7.4
""")

create_file("server/api/src/__init__.py")

create_file("server/api/src/main.py", """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import emails, notes, tasks, search, auth
from src.config import settings

app = FastAPI(
    title="NoteHermes API",
    description="AI-Driven Smart Workspace Backend",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(emails.router, prefix="/api/v1/emails", tags=["emails"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "notehermes-api"}
""")

create_file("server/api/src/config.py", """from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://notehermes:dev_password@localhost:5432/notehermes"
    REDIS_URL: str = "redis://localhost:6379"
    LLM_API_KEY: str = ""
    LLM_PROVIDER: str = "openrouter"
    AI_SERVICE_URL: str = "http://localhost:8001"
    JWT_SECRET: str = "dev-secret-change-in-prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"

settings = Settings()
""")

create_file("server/api/src/models/__init__.py")
create_file("server/api/src/models/email.py", """from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class EmailBase(BaseModel):
    subject: Optional[str] = None
    from_address: str
    to_address: str
    body: str

class EmailCreate(EmailBase):
    pass

class EmailResponse(EmailBase):
    id: uuid.UUID
    message_id: Optional[str] = None
    summary: Optional[str] = None
    received_at: Optional[datetime] = None

    class Config:
        from_attributes = True
""")

create_file("server/api/src/models/note.py", """from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class NoteBase(BaseModel):
    title: Optional[str] = None
    content: str

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: uuid.UUID
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
""")

create_file("server/api/src/models/task.py", """from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: uuid.UUID
    due_date: Optional[datetime] = None
    source_type: Optional[str] = None
    source_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
""")

create_file("server/api/src/models/entity_link.py", """from pydantic import BaseModel
from typing import Optional
import uuid

class EntityLinkCreate(BaseModel):
    source_type: str
    source_id: uuid.UUID
    target_type: str
    target_id: uuid.UUID
    link_type: Optional[str] = "related_to"

class EntityLinkResponse(EntityLinkCreate):
    id: uuid.UUID

    class Config:
        from_attributes = True
""")

create_file("server/api/src/routers/__init__.py")

create_file("server/api/src/routers/auth.py", """from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(req: LoginRequest):
    # TODO: Implement actual auth
    return {"access_token": "dev-token", "token_type": "bearer"}

@router.get("/me")
async def get_me():
    return {"id": "dev-user", "email": "dev@notehermes.com", "name": "Developer"}
""")

create_file("server/api/src/routers/emails.py", """from fastapi import APIRouter, HTTPException
from typing import List
from src.models.email import EmailResponse, EmailCreate

router = APIRouter()

@router.get("/", response_model=List[EmailResponse])
async def list_emails(skip: int = 0, limit: int = 20):
    # TODO: Fetch from DB
    return []

@router.get("/{email_id}", response_model=EmailResponse)
async def get_email(email_id: str):
    # TODO: Fetch from DB
    raise HTTPException(status_code=404, detail="Email not found")

@router.post("/summarize/{email_id}")
async def summarize_email(email_id: str):
    # TODO: Call AI service
    return {"summary": "AI summary will appear here"}

@router.post("/extract-tasks/{email_id}")
async def extract_tasks(email_id: str):
    # TODO: Call AI service to extract tasks
    return {"tasks_extracted": []}
""")

create_file("server/api/src/routers/notes.py", """from fastapi import APIRouter, HTTPException
from typing import List
from src.models.note import NoteResponse, NoteCreate

router = APIRouter()

@router.get("/", response_model=List[NoteResponse])
async def list_notes(skip: int = 0, limit: int = 20):
    # TODO: Fetch from DB
    return []

@router.post("/", response_model=NoteResponse)
async def create_note(note: NoteCreate):
    # TODO: Save to DB
    return note

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str):
    raise HTTPException(status_code=404, detail="Note not found")

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, note: NoteCreate):
    raise HTTPException(status_code=404, detail="Note not found")

@router.delete("/{note_id}")
async def delete_note(note_id: str):
    return {"status": "deleted"}
""")

create_file("server/api/src/routers/tasks.py", """from fastapi import APIRouter, HTTPException
from typing import List
from src.models.task import TaskResponse, TaskCreate

router = APIRouter()

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(status: str = None, skip: int = 0, limit: int = 20):
    return []

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    return task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/{task_id}/status")
async def update_task_status(task_id: str, status: str):
    return {"id": task_id, "status": status}
""")

create_file("server/api/src/routers/search.py", """from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    scope: str = "all"  # all, notes, emails, tasks

@router.post("/")
async def search(req: SearchRequest):
    # TODO: Implement semantic search via AI service
    return {
        "query": req.query,
        "results": [],
        "took_ms": 0
    }
""")

create_file("server/api/src/services/__init__.py")
create_readme("server/api/src/services/.gitkeep.md")

create_file("server/api/src/services/email_service.py", """# Email Service
# Handles IMAP/SMTP operations and email parsing
""")

create_file("server/api/src/services/note_service.py", """# Note Service
# Handles note CRUD and tagging
""")

create_file("server/api/src/services/task_service.py", """# Task Service
# Handles task state machine and automation
""")

create_file("server/api/src/services/connector_service.py", """# Connector Service
# Handles cross-module data flows (email->task, note->task, etc.)
""")

# ================= SERVER: AI =================

create_file("server/ai/.gitkeep")

create_file("server/ai/requirements.txt", """openai==1.14.0
httpx==0.27.0
pydantic==2.6.3
python-dotenv==1.0.1
numpy==1.26.4
tiktoken==0.6.0
""")

create_file("server/ai/src/__init__.py")

create_file("server/ai/src/agent.py", """from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NoteHermes AI Service")

class SummaryRequest(BaseModel):
    text: str

class TaskExtractionRequest(BaseModel):
    text: str

class EmbeddingRequest(BaseModel):
    text: str

@app.get("/health")
async def health():
    return {"status": "ok", "service": "notehermes-ai"}

@app.post("/summarize")
async def summarize(req: SummaryRequest):
    # TODO: Call LLM for summarization
    return {"summary": f"[AI Summary] Placeholder for {len(req.text)} chars"}

@app.post("/extract-tasks")
async def extract_tasks(req: TaskExtractionRequest):
    # TODO: Call LLM for task extraction
    return {"tasks": []}

@app.post("/embed")
async def embed(req: EmbeddingRequest):
    # TODO: Call Embedding model
    return {"embedding": [0.0] * 1536}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
""")

create_file("server/ai/src/llm_client.py", """# LLM Client Wrapper
# Supports OpenAI, Anthropic, OpenRouter, Qwen
""")

create_file("server/ai/src/embedder.py", """# Embedding Service
# Handles text vectorization for semantic search
""")

create_file("server/ai/src/prompts/.gitkeep")
create_file("server/ai/src/prompts/email_summary.txt", "You are an AI assistant. Summarize the following email in 3 bullet points.\n\nEmail:\n{text}")
create_file("server/ai/src/prompts/task_extraction.txt", "Extract actionable tasks from the following text. Return as JSON list with title, due_date, priority.\n\nText:\n{text}")
create_file("server/ai/src/prompts/note_tagging.txt", "Suggest 3-5 relevant tags for the following note content.\n\nNote:\n{text}")
create_file("server/ai/src/prompts/search_rerank.txt", "Given the query and the retrieved documents, rank them by relevance.\n\nQuery: {query}\n\nDocuments:\n{docs}")

create_file("server/ai/src/local_model.py", """# Local Model Fallback
# Handles offline inference using llama.cpp or similar
""")

# ================= SERVER: SYNC =================

create_file("server/sync/.gitkeep")
create_file("server/sync/requirements.txt", """fastapi==0.110.0
uvicorn[standard]==0.27.1
websockets==12.0
redis==5.0.3
""")

create_file("server/sync/src/__init__.py")

create_file("server/sync/src/server.py", """from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NoteHermes Sync Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/sync")
async def websocket_sync(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # TODO: Handle sync events
            await websocket.send_text(f"Echo: {data}")
    except Exception:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
""")

# ================= CLIENT: WEB =================

create_file("client/web/.gitkeep")

create_file("client/web/package.json", """{
  "name": "notehermes-web",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "^18",
    "react-dom": "^18",
    "zustand": "^4.5.0",
    "tailwindcss": "^3.4.1",
    "postcss": "^8",
    "autoprefixer": "^10.0.1",
    "@heroicons/react": "^2.1.1",
    "axios": "^1.6.7"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "eslint": "^8",
    "eslint-config-next": "14.1.0"
  }
}
""")

create_file("client/web/tsconfig.json", """{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
""")

create_file("client/web/tailwind.config.ts", """import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
export default config;
""")

create_file("client/web/next.config.js", """/** @type {import('next').NextConfig} */
const nextConfig = {};

module.exports = nextConfig;
""")

create_file("client/web/postcss.config.js", "module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };")

create_file("client/web/src/app/layout.tsx", """import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NoteHermes",
  description: "AI-Driven Smart Workspace",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
""")

create_file("client/web/src/app/globals.css", """@tailwind base;
@tailwind components;
@tailwind utilities;
""")

create_file("client/web/src/app/(dashboard)/layout.tsx", """export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return <div className="flex h-screen bg-gray-50">{children}</div>;
}
""")

create_file("client/web/src/app/(dashboard)/inbox/page.tsx", 'export default function InboxPage() { return <div className="p-6"><h1 className="text-2xl font-bold">📧 Inbox</h1><p>AI summaries and emails will appear here.</p></div>; }')
create_file("client/web/src/app/(dashboard)/notes/page.tsx", 'export default function NotesPage() { return <div className="p-6"><h1 className="text-2xl font-bold">📝 Notes</h1><p>Your smart notebook with AI search.</p></div>; }')
create_file("client/web/src/app/(dashboard)/tasks/page.tsx", 'export default function TasksPage() { return <div className="p-6"><h1 className="text-2xl font-bold">✅ Tasks</h1><p>Task board and smart scheduling.</p></div>; }')
create_file("client/web/src/app/page.tsx", "export default function Home() { return <main className='flex items-center justify-center h-screen'><h1 className='text-4xl font-bold'>NoteHermes</h1></main>; }")

# ================= CLIENT: HARMONYOS =================

create_file("client/harmony/.gitkeep")
create_readme("client/harmony/README.md")
create_file("client/harmony/entry/src/main/ets/.gitkeep")
create_file("client/harmony/entry/src/main/module.json5", """{
  "module": {
    "name": "entry",
    "type": "entry",
    "description": "NoteHermes HarmonyOS Client",
    "mainElement": "EntryAbility",
    "deviceTypes": ["phone", "tablet"],
    "deliveryWithInstall": true,
    "installationFree": false,
    "pages": "$profile:main_pages",
    "abilities": [
      {
        "name": "EntryAbility",
        "srcEntry": "./ets/entryability/EntryAbility.ets",
        "description": "Main Entry",
        "icon": "$media:icon",
        "label": "NoteHermes",
        "startWindowIcon": "$media:icon",
        "startWindowBackground": "$color:start_window_background",
        "exported": true,
        "skills": [
          {
            "entities": ["entity.system.home"],
            "actions": ["action.system.home"]
          }
        ]
      }
    ]
  }
}
""")

create_file("client/harmony/entry/src/main/ets/entryability/EntryAbility.ets", """// EntryAbility.ets
import { AbilityConstant, UIAbility, Want } from '@kit.AbilityKit';
import { window } from '@kit.ArkUI';

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    console.info('NoteHermes EntryAbility onCreate');
  }

  onDestroy(): void {
    console.info('NoteHermes EntryAbility onDestroy');
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        console.error('Failed to load content');
        return;
      }
      console.info('Succeeded in loading content');
    });
  }
}
""")

create_file("client/harmony/entry/src/main/ets/pages/Index.ets", """// Index.ets - Main Home Page
@Entry
@Component
struct Index {
  @State message: string = 'NoteHermes';

  build() {
    Row() {
      Column() {
        Text(this.message)
          .fontSize(32)
          .fontWeight(FontWeight.Bold)
      }
      .width('100%')
    }
    .height('100%')
  }
}
""")

create_file("client/harmony/entry/src/main/ets/pages/InboxPage.ets", "// InboxPage.ets")
create_file("client/harmony/entry/src/main/ets/pages/NotesPage.ets", "// NotesPage.ets")
create_file("client/harmony/entry/src/main/ets/pages/TasksPage.ets", "// TasksPage.ets")
create_file("client/harmony/entry/src/main/ets/pages/SearchPage.ets", "// SearchPage.ets")

# ================= SHARED SDK =================

create_file("shared/sdk/.gitkeep")

create_file("shared/sdk/package.json", """{
  "name": "@notehermes/sdk",
  "version": "0.1.0",
  "private": true,
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "dependencies": {
    "axios": "^1.6.7"
  },
  "devDependencies": {
    "typescript": "^5"
  }
}
""")

create_file("shared/sdk/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
""")

create_file("shared/sdk/src/index.ts", "export * from './types';\nexport * from './api';\n")
create_file("shared/sdk/src/types/index.ts", """export interface User {
  id: string;
  email: string;
  name: string;
}

export interface Email {
  id: string;
  subject: string;
  from: string;
  body: string;
  summary?: string;
}

export interface Note {
  id: string;
  title: string;
  content: string;
  tags: string[];
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'todo' | 'doing' | 'done';
  priority: 'low' | 'medium' | 'high' | 'urgent';
}
""")

create_file("shared/sdk/src/api/index.ts", """import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NOTEHERMES_API_URL || 'http://localhost:8000/api/v1',
});

export const emailApi = {
  list: () => api.get('/emails/'),
  get: (id: string) => api.get(`/emails/${id}`),
  summarize: (id: string) => api.post(`/emails/summarize/${id}`),
};

export const noteApi = {
  list: () => api.get('/notes/'),
  create: (data: any) => api.post('/notes/', data),
};

export const taskApi = {
  list: () => api.get('/tasks/'),
  create: (data: any) => api.post('/tasks/', data),
};

export default api;
""")

# ================= TESTS =================

create_file("tests/.gitkeep")
create_file("tests/api/test_emails.py", """def test_list_emails(client):
    response = client.get("/api/v1/emails/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
""")

create_file("tests/api/.gitkeep")
create_file("tests/ai/.gitkeep")
create_file("tests/e2e/.gitkeep")

# ================= .GITIGNORE =================

create_file(".gitignore", """# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# Build
dist/
.next/
build/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
""")

# ================= README =================

create_file("README.md", """# NoteHermes 🤖

**AI-Driven Smart Workspace** — Email, Notes, Tasks unified by AI.

> "Emails become tasks, notes become knowledge, tasks get done."

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/syairag/notehermes.git
cd notehermes

# 2. Start Infrastructure
cd infra && docker-compose up -d

# 3. Start API
cd ../server/api && pip install -r requirements.txt
uvicorn src.main:app --reload

# 4. Start Web Client
cd ../../client/web && npm install && npm run dev
```

## 📚 Documentation
- [PRD](docs/PRD.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Scaffold](docs/Scaffold.md)
- [Agent Roles](docs/AGENT_ROLES.md)

## 📦 Project Structure
- `server/api/` — FastAPI Backend
- `server/ai/` — AI Agent Engine
- `client/web/` — Next.js Web Client
- `client/harmony/` — HarmonyOS NEXT Client
- `shared/sdk/` — Cross-platform SDK
- `infra/` — Docker & Infrastructure

## 👥 Team
- **Toby** (syairag) — Owner
- **Tony** — R&D Director / Lead Architect

## 📄 License
Private — All rights reserved
""")

print("🎉 NoteHermes Project Scaffold Generated Successfully!")
