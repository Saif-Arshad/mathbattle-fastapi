from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..schemas.user import UserCreate, User
from ..crud.user import (
    get_all_users,
    create_user,
    delete_user,
    add_teacher,
    add_parent
)

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/all-users", response_model=List[User])
async def get_users():
    """Retrieve all users"""
    return await get_all_users()

@router.post("/user", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(user_in: UserCreate):
    """Create a new user"""
    return await create_user(user_in)

@router.post("/{user_id}/teacher", response_model=User)
async def assign_teacher(user_id: str, teacher_id: str):
    """Assign a teacher to a user"""
    updated = await add_teacher(user_id, teacher_id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User or teacher not found"
        )
    return updated

@router.delete("/{user_id}", response_model=User)
async def remove_user(user_id: str):
    """Delete a user by ID"""
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return deleted

@router.post("/{user_id}/parent", response_model=User)
async def assign_parent(user_id: str, parent_id: str):
    """Assign a parent to a user"""
    updated = await add_parent(user_id, parent_id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User or parent not found"
        )
    return updated
