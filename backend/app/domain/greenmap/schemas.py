"""GreenMap Domain — Schemas."""
from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class BusinessProfileResponse(BaseModel):
    id: UUID
    org_id: UUID
    display_name: str
    description: str | None = None
    logo_url: str | None = None
    website: str | None = None
    is_public: bool
    verified_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)

class BusinessProfileUpdate(BaseModel):
    display_name: str | None = None
    description: str | None = None
    logo_url: str | None = None
    website: str | None = None
    is_public: bool | None = None

class PublicMetricResponse(BaseModel):
    period: str
    total_carbon_saved_g: float
    total_prompts_optimized: int
    sustainability_score: float
    efficiency_score: float
    model_config = ConfigDict(from_attributes=True)

class CertificationResponse(BaseModel):
    id: UUID
    certification_name: str
    issuer: str
    issued_at: datetime
    expires_at: datetime | None = None
    document_url: str | None = None
    verified: bool
    model_config = ConfigDict(from_attributes=True)
