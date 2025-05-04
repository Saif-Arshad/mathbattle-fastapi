from fastapi import APIRouter
from typing import List
from ..crud.progress import record_progress, get_student_progress
from ..schemas.progress import Progress

router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("/", response_model=dict)
async def new_progress(p: Progress):
    return await record_progress(p)

@router.get("/student/{student_id}", response_model=List[dict])
async def progress(student_id: str):
    return await get_student_progress(student_id)
