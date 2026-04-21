from sqlalchemy.orm import Session
from src.models.db_models import Task
from src.models.task import TaskCreate, TaskResponse
from typing import List, Optional
import uuid

def get_tasks(db: Session, user_id: uuid.UUID, status: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[Task]:
    query = db.query(Task).filter(Task.user_id == user_id)
    if status:
        query = query.filter(Task.status == status)
    return query.offset(skip).limit(limit).all()

def create_task(db: Session, user_id: uuid.UUID, task: TaskCreate) -> Task:
    db_task = Task(user_id=user_id, **task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, user_id: uuid.UUID, task_id: uuid.UUID) -> Task:
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

def update_task(db: Session, user_id: uuid.UUID, task_id: uuid.UUID, task_data: dict) -> Task:
    db_task = get_task(db, user_id, task_id)
    if db_task:
        for key, value in task_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, user_id: uuid.UUID, task_id: uuid.UUID) -> bool:
    db_task = get_task(db, user_id, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False
