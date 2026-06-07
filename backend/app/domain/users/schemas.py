"""
Users Domain — Pydantic Schemas (DTOs).

Request/response schemas for the Users API.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ──────────────────────────────────────────────
# Base
# ──────────────────────────────────────────────
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    full_name: str | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    avatar_url: str | None = None


# ──────────────────────────────────────────────
# Response
# ──────────────────────────────────────────────
class UserResponse(UserBase):
    id: UUID
    full_name: str | None = None
    avatar_url: str | None = None
    role: str
    is_active: bool
    total_xp: int
    level: int
    dependency_score: float
    org_id: UUID | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserProfile(UserResponse):
    """Extended profile with computed stats."""
    sustainability_score: float = 0.0
    total_prompts: int = 0
    total_carbon_saved_g: float = 0.0
    streak_days: int = 0


class UserStats(BaseModel):
    """Aggregated user statistics for dashboard."""
    total_xp: int = 0
    level: int = 1
    total_prompts: int = 0
    total_carbon_g: float = 0.0
    total_water_ml: float = 0.0
    total_electricity_wh: float = 0.0
    sustainability_score: float = 0.0
    dependency_score: float = 0.0
    green_points: int = 0
    trees_planted: int = 0
    current_streak: int = 0
    achievements_count: int = 0
