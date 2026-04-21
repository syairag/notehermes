from fastapi import APIRouter, HTTPException
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
