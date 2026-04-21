from fastapi import FastAPI
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
