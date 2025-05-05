from typing import List, Optional
from bson import ObjectId
from pymongo import ReturnDocument
from ..database import db
from ..schemas.subject import Subject

collection = db.subjects

async def subject_helper(d) -> dict:
    return {
        "id": str(d["_id"]),
        "name": d["name"],
        "category": d.get("category"),
        "discription": d.get("discription")
    }

async def create_subject(subject_in: Subject) -> dict:
    doc = subject_in.dict(by_alias=True, exclude={"id"})
    result = await collection.insert_one(doc)
    saved = await collection.find_one({"_id": result.inserted_id})
    return await subject_helper(saved)

async def list_subjects() -> List[dict]:
    docs = await collection.find().to_list(length=None)
    return [await subject_helper(d) for d in docs]

async def get_subject(subject_id: str) -> Optional[dict]:
    d = await collection.find_one({"_id": ObjectId(subject_id)})
    return await subject_helper(d) if d else None

async def update_subject(subject_id: str, subject_in: Subject) -> Optional[dict]:
    updated = await collection.find_one_and_update(
        {"_id": ObjectId(subject_id)},
        {"$set": subject_in.dict(by_alias=True, exclude={"id"})},
        return_document=ReturnDocument.AFTER
    )
    return await subject_helper(updated) if updated else None

async def delete_subject(subject_id: str) -> Optional[dict]:
    deleted = await collection.find_one_and_delete({"_id": ObjectId(subject_id)})
    return await subject_helper(deleted) if deleted else None
