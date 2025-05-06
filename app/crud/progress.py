from typing import List
from bson import ObjectId
from datetime import datetime
from ..database import db
from ..schemas.progress import Progress

collection = db.progress

def progress_helper(d: dict) -> dict:
    # Ensure created_at is never None
    created = d.get("created_at") or datetime.utcnow()
    return {
        "id": str(d["_id"]),
        "student_id": str(d["student_id"]),
        "subject_id": str(d["subject_id"]),
        "points": d.get("points", 0),
        "created_at": created
    }

async def record_progress(p: Progress) -> dict:
    # Build document, auto-populate created_at
    doc = p.dict(by_alias=True, exclude_unset=True)
    # Populate created_at if missing or None
    if not doc.get("created_at"):
        doc["created_at"] = datetime.utcnow()
    result = await collection.insert_one(doc)
    saved = await collection.find_one({"_id": result.inserted_id})
    return progress_helper(saved)

async def get_student_progress(student_id: str) -> List[dict]:
    cursor = collection.find({"student_id": ObjectId(student_id)})
    return [progress_helper(d) async for d in cursor]
