from fastapi import APIRouter, HTTPException
from typing import List
from src.models.note import NoteResponse, NoteCreate

router = APIRouter()

@router.get("/", response_model=List[NoteResponse])
async def list_notes(skip: int = 0, limit: int = 20):
    # TODO: Fetch from DB
    return []

@router.post("/", response_model=NoteResponse)
async def create_note(note: NoteCreate):
    # TODO: Save to DB
    return note

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str):
    raise HTTPException(status_code=404, detail="Note not found")

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, note: NoteCreate):
    raise HTTPException(status_code=404, detail="Note not found")

@router.delete("/{note_id}")
async def delete_note(note_id: str):
    return {"status": "deleted"}
