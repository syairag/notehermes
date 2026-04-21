# NoteHermes 🤖

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
