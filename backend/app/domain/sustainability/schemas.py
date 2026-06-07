"""
Sustainability Domain — Pydantic Schemas.
"""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ── Prompt Log ──
class PromptLogRequest(BaseModel):
    model: str
    input_tokens: int
    output_tokens: int
    duration_ms: int | None = None
    client_source: str = "web"
    session_id: UUID | None = None


class SustainabilityMetricResponse(BaseModel):
    carbon_g: float
    water_ml: float
    electricity_wh: float
    cost_usd: float
    model_config = ConfigDict(from_attributes=True)


class PromptLogResponse(BaseModel):
    id: UUID
    sustainability: SustainabilityMetricResponse
    gamification: dict | None = None


# ── Score ──
class SustainabilityScoreResponse(BaseModel):
    score: float
    total_prompts: int
    total_carbon_g: float
    total_water_ml: float
    total_electricity_wh: float
    total_cost_usd: float
    period: str = "all_time"


# ── History ──
class DailyAggregateResponse(BaseModel):
    date: date
    total_prompts: int
    total_input_tokens: int
    total_output_tokens: int
    total_carbon_g: float
    total_water_ml: float
    total_electricity_wh: float
    total_cost_usd: float
    sustainability_score: float
    model_config = ConfigDict(from_attributes=True)


# ── Token Usage ──
class TokenUsageResponse(BaseModel):
    model_used: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
