from fastapi import APIRouter, HTTPException, status
from typing import List
from ..crud.progress import record_progress, get_student_progress
from ..schemas.progress import Progress

router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("/", response_model=Progress, status_code=status.HTTP_201_CREATED)
async def new_progress(p: Progress):
    """Record new progress entry"""
    return await record_progress(p)

@router.get("/student/{student_id}", response_model=List[Progress])
async def progress(student_id: str):
    """Get all progress entries for a given student"""
    entries = await get_student_progress(student_id)
    if entries is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No progress found for this student")
    return entries