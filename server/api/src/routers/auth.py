from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(req: LoginRequest):
    # TODO: Implement actual auth
    return {"access_token": "dev-token", "token_type": "bearer"}

@router.get("/me")
async def get_me():
    return {"id": "dev-user", "email": "dev@notehermes.com", "name": "Developer"}
