from pydantic import BaseModel
from typing import Optional
import uuid

class EntityLinkCreate(BaseModel):
    source_type: str
    source_id: uuid.UUID
    target_type: str
    target_id: uuid.UUID
    link_type: Optional[str] = "related_to"

class EntityLinkResponse(EntityLinkCreate):
    id: uuid.UUID

    class Config:
        from_attributes = True
