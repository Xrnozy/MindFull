"""
Organizations Domain — Pydantic Schemas.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ── Organization ──
class OrganizationCreate(BaseModel):
    name: str
    slug: str
    tier: str = "free"
    is_educational: bool = False
    max_members: int = 10


class OrganizationUpdate(BaseModel):
    name: str | None = None
    logo_url: str | None = None
    tier: str | None = None
    max_members: int | None = None
    settings: dict | None = None


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    tier: str
    logo_url: str | None = None
    is_educational: bool
    max_members: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ── Team ──
class TeamCreate(BaseModel):
    name: str
    department: str | None = None


class TeamResponse(BaseModel):
    id: UUID
    org_id: UUID
    name: str
    department: str | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ── Membership ──
class MembershipCreate(BaseModel):
    user_id: UUID
    role: str = "member"
    team_id: UUID | None = None


class MembershipResponse(BaseModel):
    id: UUID
    user_id: UUID
    org_id: UUID
    team_id: UUID | None = None
    role: str
    joined_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ── Invitation ──
class InvitationCreate(BaseModel):
    email: str
    role: str = "member"


class InvitationResponse(BaseModel):
    id: UUID
    org_id: UUID
    email: str
    role: str
    expires_at: datetime
    accepted_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
