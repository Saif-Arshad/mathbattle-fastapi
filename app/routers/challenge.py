# app/routers/challenge.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from ..crud.challenge import (
    create_challenge,
    list_challenges_by_subject,
    get_challenge,
    update_challenge,
    delete_challenge
)
from ..schemas.challenge import Challenge

router = APIRouter(prefix="/challenges", tags=["challenges"])

@router.post("/", response_model=Challenge, status_code=status.HTTP_201_CREATED)
async def new_challenge(challenge: Challenge):
    return await create_challenge(challenge)

@router.get("/subject/{subject_id}", response_model=List[Challenge])
async def challenges_by_subject(subject_id: str):
    return await list_challenges_by_subject(subject_id)

@router.get("/{challenge_id}", response_model=Challenge)
async def read_challenge(challenge_id: str):
    c = await get_challenge(challenge_id)
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")
    return c

@router.put("/{challenge_id}", response_model=Challenge)
async def edit_challenge(challenge_id: str, challenge: Challenge):
    updated = await update_challenge(challenge_id, challenge)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")
    return updated

@router.delete("/{challenge_id}", response_model=Challenge)
async def remove_challenge(challenge_id: str):
    deleted = await delete_challenge(challenge_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")
    return deleted
