from typing import Optional
from bson import ObjectId
from passlib.context import CryptContext
from ..database import db
from ..schemas.user import UserCreate, User, PyObjectId
from ..core.security import get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
collection = db.users

def user_helper(u) -> dict:
    return {"id": str(u["_id"]), "email": u["email"], "full_name": u.get("full_name"), "role": u["role"]}

async def create_user(user_in: UserCreate):
    hashed = get_password_hash(user_in.password)
    doc = {**user_in.dict(exclude={"password"}), "hashed_password": hashed}
    result = await collection.insert_one(doc)
    saved = await collection.find_one({"_id": result.inserted_id})
    return user_helper(saved)

async def get_user_by_email(email: str) -> Optional[dict]:
    doc = await collection.find_one({"email": email})
    return user_helper(doc) if doc else None

async def get_user(id: str) -> Optional[dict]:
    doc = await collection.find_one({"_id": ObjectId(id)})
    return user_helper(doc) if doc else None
