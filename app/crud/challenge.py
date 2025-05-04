from ..database import db
from ..schemas.challenge import Challenge
from bson import ObjectId

collection = db.challenges

def challenge_helper(d):
    return {"id": str(d["_id"]), "subject_id": str(d["subject_id"]), "question": d["question"], "options": d["options"]}

async def create_challenge(data: Challenge):
    doc = data.dict(by_alias=True)
    result = await collection.insert_one(doc)
    saved = await collection.find_one({"_id": result.inserted_id})
    return challenge_helper(saved)

async def list_challenges_by_subject(subject_id: str):
    cursor = collection.find({"subject_id": ObjectId(subject_id)})
    return [challenge_helper(d) async for d in cursor]
