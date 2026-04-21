from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.note import NoteResponse, NoteCreate
from src.services import note_service
import uuid

router = APIRouter()

# Mock user ID for dev
DEV_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")

@router.get("/", response_model=List[NoteResponse])
async def list_notes(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return note_service.get_notes(db, user_id=DEV_USER_ID, skip=skip, limit=limit)

@router.post("/", response_model=NoteResponse)
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return note_service.create_note(db, user_id=DEV_USER_ID, note=note)

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: uuid.UUID, db: Session = Depends(get_db)):
    note = note_service.get_note(db, user_id=DEV_USER_ID, note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: uuid.UUID, note: NoteCreate, db: Session = Depends(get_db)):
    updated = note_service.update_note(db, user_id=DEV_USER_ID, note_id=note_id, note=note)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

@router.delete("/{note_id}")
async def delete_note(note_id: uuid.UUID, db: Session = Depends(get_db)):
    if not note_service.delete_note(db, user_id=DEV_USER_ID, note_id=note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    return {"status": "deleted"}
