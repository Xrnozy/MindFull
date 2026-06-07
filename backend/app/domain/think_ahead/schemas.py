"""Think-A-Head Domain — Pydantic Schemas."""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ReflectionRequest(BaseModel):
    prompt_text: str
    confidence_before: float | None = None


class ReflectionResponse(BaseModel):
    id: UUID
    reflection_questions: list[str]
    model_config = ConfigDict(from_attributes=True)


class ConfidenceTrackRequest(BaseModel):
    reflection_id: UUID
    confidence_after: float
    did_proceed: bool
    delay_seconds: int = 0


class LearningRetentionResponse(BaseModel):
    id: UUID
    topic: str
    retention_score: float
    last_tested_at: datetime | None = None
    decay_rate: float
    model_config = ConfigDict(from_attributes=True)


class DependencyScoreResponse(BaseModel):
    score: float
    period_start: date
    period_end: date
    calculation_data: dict | None = None
    model_config = ConfigDict(from_attributes=True)
