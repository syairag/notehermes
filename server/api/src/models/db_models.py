from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, JSON, Integer, ARRAY, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Email(Base):
    __tablename__ = "emails"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    message_id = Column(String(255), unique=True)
    subject = Column(String(500))
    from_address = Column(String(255))
    to_address = Column(String(255))
    body = Column(Text)
    summary = Column(Text)
    received_at = Column(DateTime(timezone=True))
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String(500))
    content = Column(Text)
    tags = Column(ARRAY(String))  # Requires Postgres array support
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String(500), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="todo")
    priority = Column(String(20), default="medium")
    due_date = Column(DateTime(timezone=True))
    source_type = Column(String(20))
    source_id = Column(UUID(as_uuid=True))
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class EntityLink(Base):
    __tablename__ = "entity_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type = Column(String(20), nullable=False)
    source_id = Column(UUID(as_uuid=True), nullable=False)
    target_type = Column(String(20), nullable=False)
    target_id = Column(UUID(as_uuid=True), nullable=False)
    link_type = Column(String(20))
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
