"""Gamification Router."""
from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.domain.users.models import User
from app.domain.gamification.service import GamificationService
from app.domain.gamification.schemas import *

router = APIRouter()

@router.get("/xp", response_model=List[XPLogResponse])
async def get_xp(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await GamificationService(db).get_xp_history(current_user.id)

@router.get("/achievements", response_model=List[AchievementResponse])
async def get_achievements(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await GamificationService(db).get_achievements(current_user.id)

@router.get("/streaks", response_model=List[StreakResponse])
async def get_streaks(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await GamificationService(db).get_streaks(current_user.id)

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    score_type: str = Query("xp"), period: str = Query("weekly"),
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
):
    return await GamificationService(db).get_leaderboard(score_type, period, current_user.org_id)

@router.get("/levels", response_model=List[LevelResponse])
async def get_levels(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await GamificationService(db).get_levels()
