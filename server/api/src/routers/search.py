from fastapi import APIRouter
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
