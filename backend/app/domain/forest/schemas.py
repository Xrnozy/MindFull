"""Forest Domain — Schemas."""
from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ForestResponse(BaseModel):
    id: UUID
    green_points: int
    total_trees: int
    total_carbon_offset_g: float
    model_config = ConfigDict(from_attributes=True)

class TreeResponse(BaseModel):
    id: UUID
    species: str
    growth_stage: str
    health: float
    planted_at: datetime
    carbon_absorbed_g: float
    model_config = ConfigDict(from_attributes=True)

class PlantTreeRequest(BaseModel):
    species: str = "Oak"

class CommunityGoalResponse(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    target_trees: int
    current_trees: int
    target_carbon_g: float
    current_carbon_g: float
    starts_at: datetime
    ends_at: datetime
    is_completed: bool
    model_config = ConfigDict(from_attributes=True)

class CampaignResponse(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    goal_type: str
    target_value: float
    current_value: float
    starts_at: datetime
    ends_at: datetime
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
