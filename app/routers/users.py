from fastapi import APIRouter

router = APIRouter()

# stub endpoints - later connect with database.py
@router.post("/register")
async def register_user(username: str, password: str):
    return {"message": f"User {username} registered"}

@router.get("/me")
async def get_profile():
    return {"user": "demo", "role": "student"}
