from fastapi import APIRouter, HTTPException
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
