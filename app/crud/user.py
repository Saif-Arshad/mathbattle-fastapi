from typing import Optional, List
from bson import ObjectId
from passlib.context import CryptContext
from pymongo import ReturnDocument
from ..database import db
from ..schemas.user import UserCreate, PyObjectId
from ..core.security import get_password_hash
import asyncio
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
collection = db.users

async def user_helper(u) -> dict:
    return {
        "id": str(u["_id"]),
        "email": u["email"],
        "full_name": u.get("full_name"),
        "role": u["role"],
        "teacher": str(u.get("teacher")) if u.get("teacher") else None,
        "parent": str(u.get("parent")) if u.get("parent") else None
    }

async def create_user(user_in: UserCreate) -> dict:
    hashed = get_password_hash(user_in.password)
    doc = {**user_in.dict(exclude={"password"}), "hashed_password": hashed}
    result = await collection.insert_one(doc)
    saved = await collection.find_one({"_id": result.inserted_id})
    return await user_helper(saved)

async def get_user_by_email(email: str) -> Optional[dict]:
    doc = await collection.find_one({"email": email})
    return await user_helper(doc) if doc else None

async def get_user(user_id: str) -> Optional[dict]:
    doc = await collection.find_one({"_id": ObjectId(user_id)})
    return await user_helper(doc) if doc else None

async def get_all_users() -> List[dict]:
    docs = await collection.find().to_list(length=None)
    users = []
    for d in docs:
        users.append(await user_helper(d))
    return users

async def add_teacher(user_id: str, teacher_id: str) -> Optional[dict]:
    updated = await collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": {"teacher": ObjectId(teacher_id)}},
        return_document=ReturnDocument.AFTER
    )
    return await user_helper(updated) if updated else None

async def add_parent(user_id: str, parent_id: str) -> Optional[dict]:
    updated = await collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": {"parent": ObjectId(parent_id)}},
        return_document=ReturnDocument.AFTER
    )
    return await user_helper(updated) if updated else None

async def delete_user(user_id: str) -> Optional[dict]:
    deleted = await collection.find_one_and_delete({"_id": ObjectId(user_id)})
    return await user_helper(deleted) if deleted else None

async def get_teacher_children(teacher_id: str) -> List[dict]:
    tid = ObjectId(teacher_id)
    docs = await collection.find({"teacher": tid}).to_list(length=None)

    coros = [user_helper(d) for d in docs]
    children: List[dict] = await asyncio.gather(*coros)
    return children

async def get_parent_children(parent_id: str) -> List[dict]:
    tid = ObjectId(parent_id)
    docs = await collection.find({"parent": tid}).to_list(length=None)
    coros = [user_helper(d) for d in docs]
    children: List[dict] = await asyncio.gather(*coros)
    return children