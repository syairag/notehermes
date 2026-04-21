from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.task import TaskResponse, TaskCreate
from src.services import task_service
import uuid
from pydantic import BaseModel
import httpx

router = APIRouter()

DEV_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


class TaskStatusUpdate(BaseModel):
    status: str


class EmailExtractionRequest(BaseModel):
    email_content: str


AI_SERVICE_URL = "http://localhost:8001/extract-tasks"


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(status: Optional[str] = None, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return task_service.get_tasks(db, user_id=DEV_USER_ID, status=status, skip=skip, limit=limit)


@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, user_id=DEV_USER_ID, task=task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    task = task_service.get_task(db, user_id=DEV_USER_ID, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: uuid.UUID, task: TaskCreate, db: Session = Depends(get_db)):
    updated = task_service.update_task(db, user_id=DEV_USER_ID, task_id=task_id, task_data=task.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.put("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(task_id: uuid.UUID, status_update: TaskStatusUpdate, db: Session = Depends(get_db)):
    updated = task_service.update_task(db, user_id=DEV_USER_ID, task_id=task_id, task_data={"status": status_update.status})
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}")
async def delete_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    if not task_service.delete_task(db, user_id=DEV_USER_ID, task_id=task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "deleted"}


@router.post("/extract-from-email", response_model=List[TaskResponse])
async def extract_from_email(request: EmailExtractionRequest, db: Session = Depends(get_db)):
    """Extract tasks from email content using the AI service."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            AI_SERVICE_URL,
            json={"email_content": request.email_content},
            timeout=30.0,
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"AI service returned error: {response.text}"
            )
        extracted_tasks = response.json()

    created_tasks = []
    for task_data in extracted_tasks:
        task_create = TaskCreate(
            title=task_data.get("title", ""),
            description=task_data.get("description"),
            status=task_data.get("status", "todo"),
            priority=task_data.get("priority", "medium"),
        )
        created_task = task_service.create_task(db, user_id=DEV_USER_ID, task=task_create)
        created_tasks.append(created_task)

    return created_tasks
