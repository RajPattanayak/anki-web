from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

# --- Pydantic Models ---
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=6, description="User password")

class UserProfileResponse(BaseModel):
    username: str
    role: str

# --- In-memory mock DB ---
# (Will Replace with real DB later)
_fake_users_db = {}

# --- Endpoints ---
@router.post("/register", response_model=UserProfileResponse)
async def register_user(payload: UserRegisterRequest):
    if payload.username in _fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    # In real app -> hash password before storing
    _fake_users_db[payload.username] = {
        "password": payload.password,
        "role": "student"
    }

    return UserProfileResponse(username=payload.username, role="student")


@router.get("/me", response_model=UserProfileResponse)
async def get_profile(username: Optional[str] = None):
    """
    Mock profile endpoint.
    In a real app, you'd fetch from auth token or DB.
    """
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = _fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserProfileResponse(username=username, role=user["role"])