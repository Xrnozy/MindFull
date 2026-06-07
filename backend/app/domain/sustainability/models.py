"""
Sustainability Domain — SQLAlchemy Models.

AI session tracking, prompt logging, sustainability metrics, and daily aggregates.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, TenantMixin


class AISession(Base, TimestampMixin, TenantMixin):
    __tablename__ = "ai_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    model_provider: Mapped[str] = mapped_column(String(100), nullable=False)  # openai, anthropic, google
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)      # gpt-4o, claude-3.5, gemini-pro
    session_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    session_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    total_input_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_output_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    client_source: Mapped[str] = mapped_column(String(50), default="web", nullable=False)  # extension | web | mobile | api

    # Relationships
    prompts = relationship("Prompt", back_populates="session", lazy="noload")


class Prompt(Base, TimestampMixin, TenantMixin):
    __tablename__ = "prompts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_sessions.id", ondelete="SET NULL"), nullable=True)
    model_used: Mapped[str] = mapped_column(String(100), nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    client_source: Mapped[str] = mapped_column(String(50), default="web", nullable=False)
    prompt_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)  # SHA-256 of prompt text

    # Relationships
    session = relationship("AISession", back_populates="prompts")
    sustainability_metric = relationship("SustainabilityMetric", back_populates="prompt", uselist=False, lazy="selectin")
    analysis = relationship("PromptAnalysis", back_populates="prompt", uselist=False, lazy="noload")


class SustainabilityMetric(Base, TimestampMixin, TenantMixin):
    __tablename__ = "sustainability_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("prompts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    carbon_g: Mapped[float] = mapped_column(Float, nullable=False)
    water_ml: Mapped[float] = mapped_column(Float, nullable=False)
    electricity_wh: Mapped[float] = mapped_column(Float, nullable=False)
    cost_usd: Mapped[float] = mapped_column(Float, nullable=False)
    grid_region: Mapped[str] = mapped_column(String(50), default="US-AVG", nullable=False)
    pue_factor: Mapped[float] = mapped_column(Float, default=1.1, nullable=False)

    # Relationships
    prompt = relationship("Prompt", back_populates="sustainability_metric")


class SustainabilityDailyAggregate(Base, TenantMixin):
    __tablename__ = "sustainability_daily_aggregates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    total_prompts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_input_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_output_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_carbon_g: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_water_ml: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_electricity_wh: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    sustainability_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)


class TokenUsageLog(Base, TimestampMixin, TenantMixin):
    __tablename__ = "token_usage_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    model_used: Mapped[str] = mapped_column(String(100), nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_usd: Mapped[float] = mapped_column(Float, nullable=False)
