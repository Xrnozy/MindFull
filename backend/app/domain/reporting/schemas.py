"""Reporting Domain — Schemas."""
from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class ReportGenerateRequest(BaseModel):
    report_type: str  # esg | sustainability | wellness | campus
    format: str = "json"
    parameters: dict | None = None

class ReportResponse(BaseModel):
    id: UUID
    report_type: str
    format: str
    status: str
    file_url: str | None = None
    created_at: datetime
    completed_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)

class AuditLogResponse(BaseModel):
    id: UUID
    user_id: UUID | None = None
    action: str
    resource_type: str
    resource_id: str | None = None
    ip_address: str | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class APIKeyCreateRequest(BaseModel):
    name: str
    scopes: dict | None = None

class APIKeyResponse(BaseModel):
    id: UUID
    key_prefix: str
    name: str
    scopes: dict | None = None
    is_active: bool
    last_used_at: datetime | None = None
    expires_at: datetime | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class APIKeyCreatedResponse(APIKeyResponse):
    """Returned only at creation time — includes the full key."""
    full_key: str
