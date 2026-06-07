"""
Wellness Domain — SQLAlchemy Models.

Daily goals, usage limits, and wellness reports.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, TenantMixin


class DailyGoal(Base, TimestampMixin):
    __tablename__ = "daily_goals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    prompt_limit: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    prompts_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class UsageLimit(Base, TimestampMixin, TenantMixin):
    __tablename__ = "usage_limits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    max_daily_prompts: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    max_daily_tokens: Mapped[int] = mapped_column(Integer, default=500000, nullable=False)
    max_daily_cost_usd: Mapped[float] = mapped_column(Float, default=10.0, nullable=False)
    cooldown_minutes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class WellnessReport(Base, TimestampMixin):
    __tablename__ = "wellness_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    total_prompts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_daily_prompts: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    dependency_trend: Mapped[str] = mapped_column(default="stable", nullable=False)  # improving | stable | worsening
    wellness_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    recommendations: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
