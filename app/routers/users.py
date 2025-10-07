from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import Optional
import json
from pathlib import Path
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

router = APIRouter()

# ---------------------------
# CONFIG
# ---------------------------
DB_FILE = Path("users_db.json")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "super_secret_key_change_me"   # Replace with a secure random key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ---------------------------
# JSON DB HELPERS
# ---------------------------
def load_db() -> dict:
    if DB_FILE.exists():
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_db(data: dict):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ---------------------------
# MODELS
# ---------------------------
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: str = Field(..., description="User role (student/admin)")

class UserLoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfileResponse(BaseModel):
    username: str
    role: str


# ---------------------------
# PASSWORD HELPERS
# ---------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ---------------------------
# JWT HELPERS
# ---------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ---------------------------
# ENDPOINTS
# ---------------------------

@router.post("/register", response_model=UserProfileResponse)
async def register_user(payload: UserRegisterRequest):
    db = load_db()
    if payload.username in db:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(payload.password)
    db[payload.username] = {"password": hashed_pw, "role": payload.role}
    save_db(db)
    return UserProfileResponse(username=payload.username, role=payload.role)


@router.post("/login", response_model=TokenResponse)
async def login_user(payload: UserLoginRequest):
    """
    Verify username/password and return JWT token.
    """
    db = load_db()
    user = db.get(payload.username)
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": payload.username})
    return TokenResponse(access_token=token)


# ---------------------------
# AUTH DECORATOR / DEPENDENCY
# ---------------------------
def get_current_user(authorization: str = Header(None)):
    """
    Extract user from JWT in Authorization header.
    Usage: Authorization: Bearer <token>
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    payload = decode_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    db = load_db()
    user = db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"username": username, "role": user["role"]}


# ---------------------------
# PROTECTED ENDPOINT EXAMPLE
# ---------------------------
@router.get("/me", response_model=UserProfileResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Protected route — requires valid Bearer token.
    """
    return UserProfileResponse(username=current_user["username"], role=current_user["role"])
