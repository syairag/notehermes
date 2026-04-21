from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class EmailBase(BaseModel):
    subject: Optional[str] = None
    from_address: str
    to_address: str
    body: str

class EmailCreate(EmailBase):
    pass

class EmailResponse(EmailBase):
    id: uuid.UUID
    message_id: Optional[str] = None
    summary: Optional[str] = None
    received_at: Optional[datetime] = None

    class Config:
        from_attributes = True
