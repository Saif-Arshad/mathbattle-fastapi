from fastapi import APIRouter, HTTPException, status
from typing import List
from ..crud.user import get_teacher_children
from ..schemas.user import User

router = APIRouter(prefix="/teacher", tags=["teacher"])

@router.get(
    "/{teacher_id}/children",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="List students linked to a teacher"
)
async def list_teacher_children(teacher_id: str):
    """
    Fetch all students linked to the given teacher ID.
    """
    children = await get_teacher_children(teacher_id)
    if not children:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No students found for teacher {teacher_id}"
        )
    return children
