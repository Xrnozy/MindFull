"""
Prompt Coach Domain — Pydantic Schemas.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PromptAnalyzeRequest(BaseModel):
    prompt_text: str
    intended_model: str = "gpt-4o"


class PromptAnalysisResponse(BaseModel):
    id: UUID | None = None
    efficiency_score: float
    clarity_score: float
    specificity_score: float
    context_ratio: float
    repetition_penalty: float
    token_prediction: int
    cost_prediction: float
    carbon_prediction: float
    suggestions: list[str]
    recommended_model: str
    model_config = ConfigDict(from_attributes=True)


class ModelBenchmarkResponse(BaseModel):
    model_name: str
    provider: str
    avg_tokens_per_watt: float
    cost_per_1k_tokens_in: float
    cost_per_1k_tokens_out: float
    carbon_per_1k_tokens: float
    model_config = ConfigDict(from_attributes=True)
