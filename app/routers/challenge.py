from fastapi import APIRouter
from typing import List
from ..crud.challenge import create_challenge, list_challenges_by_subject
from ..schemas.challenge import Challenge

router = APIRouter(prefix="/challenges", tags=["challenges"])

@router.post("/", response_model=dict)
async def new_challenge(challenge: Challenge):
    return await create_challenge(challenge)

@router.get("/subject/{subject_id}", response_model=List[dict])
async def challenges_by_subject(subject_id: str):
    return await list_challenges_by_subject(subject_id)
