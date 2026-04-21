from fastapi import FastAPI
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
