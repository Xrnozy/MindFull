"""
Prompt Coach Domain — SQLAlchemy Models.

Prompt efficiency analysis results and model benchmark data.
"""
from __future__ import annotations

import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class PromptAnalysis(Base, TimestampMixin):
    __tablename__ = "prompt_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("prompts.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    efficiency_score: Mapped[float] = mapped_column(Float, nullable=False)  # 0–100
    clarity_score: Mapped[float] = mapped_column(Float, nullable=False)
    specificity_score: Mapped[float] = mapped_column(Float, nullable=False)
    context_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    repetition_penalty: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    token_prediction: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cost_prediction: Mapped[float | None] = mapped_column(Float, nullable=True)
    carbon_prediction: Mapped[float | None] = mapped_column(Float, nullable=True)
    suggestions: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    recommended_model: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    prompt = relationship("Prompt", back_populates="analysis")


class ModelBenchmark(Base, TimestampMixin):
    __tablename__ = "model_benchmarks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    avg_tokens_per_watt: Mapped[float] = mapped_column(Float, nullable=False)
    cost_per_1k_tokens_in: Mapped[float] = mapped_column(Float, nullable=False)
    cost_per_1k_tokens_out: Mapped[float] = mapped_column(Float, nullable=False)
    carbon_per_1k_tokens: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
