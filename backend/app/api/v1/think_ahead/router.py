"""Think-A-Head Router."""
from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.domain.users.models import User
from app.domain.think_ahead.service import ThinkAheadService
from app.domain.think_ahead.schemas import *

router = APIRouter()

@router.post("/reflect", response_model=ReflectionResponse)
async def reflect(data: ReflectionRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ThinkAheadService(db).generate_reflection(current_user.id, data)

@router.post("/confidence")
async def track_confidence(data: ConfidenceTrackRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await ThinkAheadService(db).track_confidence(current_user.id, data)
    return {"status": "tracked"}

@router.get("/retention", response_model=List[LearningRetentionResponse])
async def get_retention(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ThinkAheadService(db).get_retention(current_user.id)

@router.get("/dependency-score", response_model=DependencyScoreResponse)
async def get_dependency(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await ThinkAheadService(db).get_dependency_score(current_user.id)
    if isinstance(result, dict):
        return DependencyScoreResponse(**result)
    return result
