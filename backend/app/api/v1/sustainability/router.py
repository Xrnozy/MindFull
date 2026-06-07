"""Sustainability Router."""
from __future__ import annotations
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.domain.users.models import User
from app.domain.sustainability.service import SustainabilityService
from app.domain.sustainability.schemas import *

router = APIRouter()

@router.post("/log", response_model=PromptLogResponse)
async def log_prompt(data: PromptLogRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await SustainabilityService(db).log_prompt(current_user.id, current_user.org_id, data)

@router.get("/score", response_model=SustainabilityScoreResponse)
async def get_score(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await SustainabilityService(db).get_score(current_user.id, current_user.org_id)
    return SustainabilityScoreResponse(**result)

@router.get("/history", response_model=List[DailyAggregateResponse])
async def get_history(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SustainabilityService(db).get_history(current_user.id, start_date, end_date)
