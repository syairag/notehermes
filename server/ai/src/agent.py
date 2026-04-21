import json
import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from src.config import AIConfig

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
    """Extract tasks from email text using DashScope API (glm-5)."""
    system_prompt = (
        "Extract tasks from this email. Return JSON list with title, "
        "due_date (YYYY-MM-DD), priority. Current year is 2026."
    )

    headers = {
        "Authorization": f"Bearer {AIConfig.API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": AIConfig.get_model("ai_nlp"),  # glm-5
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.text},
        ],
    }

    async with httpx.AsyncClient(base_url=AIConfig.BASE_URL) as client:
        response = await client.post(
            "/chat/completions",
            headers=headers,
            json=payload,
            timeout=60.0,
        )
        response.raise_for_status()
        data = response.json()

    content = data["choices"][0]["message"]["content"].strip()

    # Strip markdown code fences if present
    if content.startswith("```"):
        lines = content.splitlines()
        lines = [l for l in lines if not l.startswith("```")]
        content = "\n".join(lines).strip()

    tasks = json.loads(content)
    return {"tasks": tasks}

@app.post("/embed")
async def embed(req: EmbeddingRequest):
    # TODO: Call Embedding model
    return {"embedding": [0.0] * 1536}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
