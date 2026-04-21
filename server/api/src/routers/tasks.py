from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.task import TaskResponse, TaskCreate
from src.services import task_service
import uuid

router = APIRouter()

DEV_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")

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

@router.put("/{task_id}/status")
async def update_task_status(task_id: uuid.UUID, status: str, db: Session = Depends(get_db)):
    updated = task_service.update_task(db, user_id=DEV_USER_ID, task_id=task_id, task_data={"status": status})
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated
