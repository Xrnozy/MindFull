"""
Think-A-Head Domain — SQLAlchemy Models.

Reflection questions, learning retention tracking, AI dependency scoring.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class ReflectionPrompt(Base, TimestampMixin):
    __tablename__ = "reflection_prompts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    original_prompt_text_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reflection_questions: Mapped[dict] = mapped_column(JSONB, nullable=False)
    confidence_before: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0–1
    confidence_after: Mapped[float | None] = mapped_column(Float, nullable=True)
    did_proceed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    delay_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class LearningRetention(Base, TimestampMixin):
    __tablename__ = "learning_retention"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    retention_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)  # 0–1 decays over time
    last_tested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    decay_rate: Mapped[float] = mapped_column(Float, default=0.1, nullable=False)


class DependencyScore(Base, TimestampMixin):
    __tablename__ = "dependency_scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)  # 0–100 (higher = more dependent)
    calculation_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
