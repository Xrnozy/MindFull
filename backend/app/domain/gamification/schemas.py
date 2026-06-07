"""Gamification Domain — Schemas."""
from __future__ import annotations
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class XPLogResponse(BaseModel):
    id: UUID
    amount: int
    source: str
    reference_id: UUID | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class LevelResponse(BaseModel):
    level_number: int
    xp_required: int
    title: str
    badge_icon: str | None = None
    perks: dict | None = None
    model_config = ConfigDict(from_attributes=True)

class AchievementResponse(BaseModel):
    id: UUID
    achievement_type: str
    title: str
    description: str | None = None
    icon: str | None = None
    unlocked_at: datetime
    model_config = ConfigDict(from_attributes=True)

class StreakResponse(BaseModel):
    id: UUID
    streak_type: str
    current_count: int
    longest_count: int
    last_activity_date: date
    model_config = ConfigDict(from_attributes=True)

class LeaderboardEntry(BaseModel):
    user_id: UUID
    score: float
    rank: int
    period: str
    score_type: str
    model_config = ConfigDict(from_attributes=True)
