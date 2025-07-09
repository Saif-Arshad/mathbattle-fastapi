from typing import List
from bson import ObjectId
from datetime import datetime
from ..database import db
from ..schemas.progress import Progress
from ..schemas.user import User

collection = db.progress

def progress_helper(d: dict) -> dict:
    created = d.get("created_at") or datetime.utcnow()
    return {
        "id": str(d["_id"]),
        "student_id": str(d["student_id"]),
        "subject_id": str(d["subject_id"]),
        "points": d.get("points", 0),
        "created_at": created
    }

async def record_progress(p: Progress) -> dict:
    doc = p.dict(by_alias=True, exclude_unset=True)
    if not doc.get("created_at"):
        doc["created_at"] = datetime.utcnow()
    result = await collection.insert_one(doc)
    saved = await collection.find_one({"_id": result.inserted_id})
    return progress_helper(saved)

async def get_student_progress(student_id: str) -> List[dict]:
    cursor = collection.find({"student_id": ObjectId(student_id)})
    return [progress_helper(d) async for d in cursor]

async def get_leaderboard_by_subject(subject_id: str, limit: int = 20):
    pipeline = [
        {"$match": {"subject_id": ObjectId(subject_id)}},
        {"$group": {
            "_id": "$student_id",
            "score": {"$sum": "$points"}
        }},
        {"$sort": {"score": -1}},
        {"$limit": limit},
        {"$lookup": {
            "from": "users",
            "localField": "_id",
            "foreignField": "_id",
            "as": "user"
        }},
        {"$unwind": {"path": "$user", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 0,
            "username": "$user.full_name",
            "score": 1
        }}
    ]
    results = await db.progress.aggregate(pipeline).to_list(length=limit)
    return results
