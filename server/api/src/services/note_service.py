from sqlalchemy.orm import Session
from src.models.db_models import Note
from src.models.note import NoteCreate, NoteResponse
from typing import List
import uuid

def get_notes(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> List[Note]:
    return db.query(Note).filter(Note.user_id == user_id).offset(skip).limit(limit).all()

def create_note(db: Session, user_id: uuid.UUID, note: NoteCreate) -> Note:
    db_note = Note(user_id=user_id, **note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_note(db: Session, user_id: uuid.UUID, note_id: uuid.UUID) -> Note:
    return db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()

def update_note(db: Session, user_id: uuid.UUID, note_id: uuid.UUID, note: NoteCreate) -> Note:
    db_note = get_note(db, user_id, note_id)
    if db_note:
        for key, value in note.dict().items():
            setattr(db_note, key, value)
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_note(db: Session, user_id: uuid.UUID, note_id: uuid.UUID) -> bool:
    db_note = get_note(db, user_id, note_id)
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False
