from ..database import db
from ..schemas.subject import Subject
from bson import ObjectId

collection = db.subjects

def subject_helper(d):
    return {"id": str(d["_id"]), "name": d["name"]}

async def create_subject(name: str):
    result = await collection.insert_one({"name": name})
    doc = await collection.find_one({"_id": result.inserted_id})
    return subject_helper(doc)

async def list_subjects():
    return [subject_helper(d) async for d in collection.find()]
