"""Organizations Router."""
from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user, require_role
from app.domain.users.models import User
from app.domain.organizations.service import OrganizationService
from app.domain.organizations.schemas import *

router = APIRouter()

@router.post("/", response_model=OrganizationResponse)
async def create_org(data: OrganizationCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await OrganizationService(db).create_org(data, current_user.id)

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_org(org_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await OrganizationService(db).get_org(org_id)

@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_org(org_id: UUID, data: OrganizationUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role(["super_admin", "org_admin"]))):
    return await OrganizationService(db).update_org(org_id, data)

@router.delete("/{org_id}")
async def delete_org(org_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role(["super_admin", "org_admin"]))):
    await OrganizationService(db).delete_org(org_id)
    return {"status": "deleted"}

@router.post("/{org_id}/teams", response_model=TeamResponse)
async def create_team(org_id: UUID, data: TeamCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role(["super_admin", "org_admin"]))):
    return await OrganizationService(db).create_team(org_id, data)

@router.get("/{org_id}/teams", response_model=List[TeamResponse])
async def list_teams(org_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await OrganizationService(db).get_teams(org_id)

@router.get("/{org_id}/members", response_model=List[MembershipResponse])
async def list_members(org_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await OrganizationService(db).get_members(org_id)

@router.post("/{org_id}/members", response_model=MembershipResponse)
async def add_member(org_id: UUID, data: MembershipCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role(["super_admin", "org_admin"]))):
    return await OrganizationService(db).add_member(org_id, data.user_id, data.role, data.team_id, current_user.id)

@router.post("/{org_id}/invitations", response_model=InvitationResponse)
async def create_invitation(org_id: UUID, data: InvitationCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role(["super_admin", "org_admin"]))):
    return await OrganizationService(db).create_invitation(org_id, data, current_user.id)

@router.post("/invitations/{token}/accept")
async def accept_invitation(token: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    membership = await OrganizationService(db).accept_invitation(token, current_user.id)
    return {"status": "accepted", "membership_id": str(membership.id)}
