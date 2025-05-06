# app/crud/challenge.py
from typing import List, Optional
from bson import ObjectId
from pymongo import ReturnDocument
from ..database import db
from ..schemas.challenge import Challenge

collection = db.challenges

async def challenge_helper(d: dict) -> dict:
    return {
        "_id": str(d["_id"]),
        "subject_id": str(d["subject_id"]),
        "question": d["question"],
        "correctOption": d["correctOption"],
        "options": d.get("options", [])
    }
async def create_challenge(data: Challenge) -> dict:
    payload = {
        "subject_id": data.subject_id,
        "question": data.question,
        "correctOption": data.correctOption,
        "options": [o.dict() for o in data.options],
    }
    result = await collection.insert_one(payload)
    saved = await collection.find_one({"_id": result.inserted_id})
    return await challenge_helper(saved)
async def list_challenges_by_subject(subject_id: str) -> List[dict]:
    docs = await collection.find({"subject_id": ObjectId(subject_id)}).to_list(length=None)
    return [await challenge_helper(d) for d in docs]

async def get_challenge(challenge_id: str) -> Optional[dict]:
    d = await collection.find_one({"_id": ObjectId(challenge_id)})
    return await challenge_helper(d) if d else None

async def update_challenge(challenge_id: str, data: Challenge) -> Optional[dict]:
    updated = await collection.find_one_and_update(
        {"_id": ObjectId(challenge_id)},
        {"$set": data.dict(by_alias=True, exclude={"id"})},
        return_document=ReturnDocument.AFTER
    )
    return await challenge_helper(updated) if updated else None

async def delete_challenge(challenge_id: str) -> Optional[dict]:
    deleted = await collection.find_one_and_delete({"_id": ObjectId(challenge_id)})
    return await challenge_helper(deleted) if deleted else None
