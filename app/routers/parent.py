from typing import List
from fastapi import APIRouter, HTTPException, status
from ..crud.user import get_parent_children
# note: user_helper etc. stay untouched

router = APIRouter(prefix="/parent", tags=["parent"])

@router.get(
    "/{parent_id}/children",
    status_code=status.HTTP_200_OK,
    summary="List students linked to a parent"
)
async def list_parent_children(parent_id: str):
    """
    Fetch all students linked to the given parent ID.
    """
    children = await get_parent_children(parent_id)
    print(children)
    if not children:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No students found for parent {parent_id}"
        )
    return children
