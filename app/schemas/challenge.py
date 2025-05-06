from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from .user import PyObjectId

class Option(BaseModel):
    text: str

class Challenge(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    subject_id: PyObjectId
    question: str
    correctOption:str
    options: List[Option]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
