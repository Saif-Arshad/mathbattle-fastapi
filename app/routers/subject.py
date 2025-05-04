from fastapi import APIRouter, Depends
from typing import List
from ..crud.subject import create_subject, list_subjects
from ..schemas.subject import Subject

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.post("/", response_model=Subject)
async def new_subject(name: str):
    return await create_subject(name)

@router.get("/", response_model=List[Subject])
async def get_subjects():
    return await list_subjects()
