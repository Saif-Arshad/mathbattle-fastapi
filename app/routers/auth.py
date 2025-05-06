from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..crud.user import create_user, get_user_by_email
from ..schemas.user import UserCreate
from ..core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user_in: UserCreate):
    user = await get_user_by_email(user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created = await create_user(user_in)
    token = create_access_token(created["id"])
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(form.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    from ..database import db
    raw = await db.users.find_one({"email": form.username})
    if not verify_password(form.password, raw["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(user["id"])
    return {"access_token": token, "token_type": "bearer","role":    user["role"],"userId":user["id"]}
