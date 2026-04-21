from pydantic import BaseModel, field_validator
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
    tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    @field_validator("tags", mode="before")
    @classmethod
    def ensure_list(cls, v):
        return v if v is not None else []

    class Config:
        from_attributes = True
