from ..database import db
from ..schemas.progress import Progress
from bson import ObjectId

collection = db.progress

def progress_helper(d):
    return {"id": str(d["_id"]), "student_id": str(d["student_id"]), "challenge_id": str(d["challenge_id"]), "score": d["score"], "created_at": d["created_at"]}

async def record_progress(p: Progress):
    doc = p.dict(by_alias=True)
    result = await collection.insert_one(doc)
    saved = await collection.find_one({"_id": result.inserted_id})
    return progress_helper(saved)

async def get_student_progress(student_id: str):
    cursor = collection.find({"student_id": ObjectId(student_id)})
    return [progress_helper(d) async for d in cursor]
