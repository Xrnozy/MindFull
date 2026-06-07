"""Enhanced Users Router."""
from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user, get_pagination, PaginationParams
from app.domain.users.models import User
from app.domain.users.schemas import UserResponse, UserUpdate, UserStats
from app.domain.users.service import UserService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user profile."""
    service = UserService(db)
    return await service.update_user(current_user, data)


@router.get("/me/stats", response_model=UserStats)
async def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user dashboard stats."""
    return UserStats(
        total_xp=current_user.total_xp,
        level=current_user.level,
        dependency_score=current_user.dependency_score,
    )


@router.get("/", response_model=List[UserResponse])
async def list_users(
    pagination: PaginationParams = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List users (org-scoped)."""
    service = UserService(db)
    if current_user.org_id:
        return await service.get_org_users(current_user.org_id, limit=pagination.limit)
    return []
