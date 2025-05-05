from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from .user import PyObjectId

class Subject(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    category:str
    discription:str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
