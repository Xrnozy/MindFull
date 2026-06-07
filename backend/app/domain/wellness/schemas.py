"""Wellness Domain — Schemas."""
from __future__ import annotations
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class DailyGoalResponse(BaseModel):
    id: UUID
    date: date
    prompt_limit: int
    prompts_used: int
    is_completed: bool
    model_config = ConfigDict(from_attributes=True)

class DailyGoalUpdate(BaseModel):
    prompt_limit: int

class UsageLimitResponse(BaseModel):
    id: UUID
    max_daily_prompts: int
    max_daily_tokens: int
    max_daily_cost_usd: float
    cooldown_minutes: int
    model_config = ConfigDict(from_attributes=True)

class UsageLimitUpdate(BaseModel):
    max_daily_prompts: int | None = None
    max_daily_tokens: int | None = None
    max_daily_cost_usd: float | None = None
    cooldown_minutes: int | None = None

class WellnessReportResponse(BaseModel):
    id: UUID
    period_start: date
    period_end: date
    total_prompts: int
    avg_daily_prompts: float
    dependency_trend: str
    wellness_score: float
    recommendations: dict | None = None
    model_config = ConfigDict(from_attributes=True)
