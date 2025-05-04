from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime
from .user import PyObjectId

class Progress(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    student_id: PyObjectId
    challenge_id: PyObjectId
    score: int
    created_at: datetime = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
