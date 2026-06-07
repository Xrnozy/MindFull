"""Wellness Router."""
from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.domain.users.models import User
from app.domain.wellness.service import WellnessService
from app.domain.wellness.schemas import *

router = APIRouter()

@router.get("/goals", response_model=DailyGoalResponse)
async def get_goals(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await WellnessService(db).get_or_create_daily_goal(current_user.id)

@router.put("/goals", response_model=DailyGoalResponse)
async def update_goals(data: DailyGoalUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await WellnessService(db).update_daily_goal(current_user.id, data)

@router.get("/limits", response_model=UsageLimitResponse)
async def get_limits(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await WellnessService(db).get_limits(current_user.id)

@router.put("/limits", response_model=UsageLimitResponse)
async def update_limits(data: UsageLimitUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await WellnessService(db).update_limits(current_user.id, data)

@router.get("/reports", response_model=List[WellnessReportResponse])
async def get_reports(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await WellnessService(db).get_reports(current_user.id)
