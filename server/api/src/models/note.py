from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class NoteBase(BaseModel):
    title: Optional[str] = None
    content: str

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: uuid.UUID
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
