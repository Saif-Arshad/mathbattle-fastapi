from fastapi import APIRouter, HTTPException, status
from typing import List
from ..crud.subject import (
    create_subject,
    list_subjects,
    get_subject,
    update_subject,
    delete_subject
)
from ..schemas.subject import Subject

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.post("/", response_model=Subject, status_code=status.HTTP_201_CREATED)
async def new_subject(subject: Subject):
    """Create a new subject"""
    return await create_subject(subject)

@router.get("/", response_model=List[Subject])
async def read_subjects():
    """List all subjects"""
    return await list_subjects()

@router.get("/{subject_id}", response_model=Subject)
async def read_subject(subject_id: str):
    """Get a subject by ID"""
    s = await get_subject(subject_id)
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    return s

@router.put("/{subject_id}", response_model=Subject)
async def edit_subject(subject_id: str, subject: Subject):
    """Update a subject"""
    updated = await update_subject(subject_id, subject)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    return updated

@router.delete("/{subject_id}", response_model=Subject)
async def remove_subject(subject_id: str):
    """Delete a subject"""
    deleted = await delete_subject(subject_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    return deleted
