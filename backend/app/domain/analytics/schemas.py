"""Analytics Domain — Schemas."""
from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class EventCreate(BaseModel):
    event_type: str
    event_data: dict | None = None
    client_source: str = "web"
    session_id: str | None = None

class BatchEventsRequest(BaseModel):
    events: list[EventCreate]

class EventResponse(BaseModel):
    id: UUID
    event_type: str
    event_data: dict | None = None
    client_source: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DashboardMetrics(BaseModel):
    total_events: int = 0
    total_prompts: int = 0
    total_carbon_g: float = 0.0
    total_users_active: int = 0
    avg_sustainability_score: float = 0.0

class TrendPoint(BaseModel):
    period_start: datetime
    count: int
    sum_value: float
    avg_value: float
    model_config = ConfigDict(from_attributes=True)
