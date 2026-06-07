"""
Organizations Domain — Service.
"""
from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DuplicateError, NotFoundError, PermissionDeniedError
from app.domain.organizations.models import Organization, Team, Membership, Invitation
from app.domain.organizations.repository import (
    OrganizationRepository, TeamRepository, MembershipRepository, InvitationRepository
)
from app.domain.organizations.schemas import OrganizationCreate, OrganizationUpdate, TeamCreate, InvitationCreate


class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.org_repo = OrganizationRepository(db)
        self.team_repo = TeamRepository(db)
        self.member_repo = MembershipRepository(db)
        self.invite_repo = InvitationRepository(db)

    # ── Orgs ──
    async def create_org(self, data: OrganizationCreate, creator_id: UUID) -> Organization:
        existing = await self.org_repo.get_by_slug(data.slug)
        if existing:
            raise DuplicateError("Organization slug")

        org = Organization(**data.model_dump())
        org = await self.org_repo.create(org)

        # Auto-add creator as org_admin
        membership = Membership(user_id=creator_id, org_id=org.id, role="org_admin")
        await self.member_repo.create(membership)
        return org

    async def get_org(self, org_id: UUID) -> Organization:
        org = await self.org_repo.get_by_id(org_id)
        if not org:
            raise NotFoundError("Organization", str(org_id))
        return org

    async def update_org(self, org_id: UUID, data: OrganizationUpdate) -> Organization:
        org = await self.get_org(org_id)
        updates = data.model_dump(exclude_unset=True)
        return await self.org_repo.update(org, updates)

    async def delete_org(self, org_id: UUID) -> None:
        org = await self.get_org(org_id)
        await self.org_repo.delete(org, soft=True)

    # ── Teams ──
    async def create_team(self, org_id: UUID, data: TeamCreate) -> Team:
        team = Team(org_id=org_id, **data.model_dump())
        return await self.team_repo.create(team)

    async def get_teams(self, org_id: UUID):
        return await self.team_repo.get_by_org(org_id)

    # ── Memberships ──
    async def add_member(self, org_id: UUID, user_id: UUID, role: str = "member", team_id: UUID | None = None, invited_by: UUID | None = None) -> Membership:
        existing = await self.member_repo.get_by_user_and_org(user_id, org_id)
        if existing:
            raise DuplicateError("Membership")
        membership = Membership(user_id=user_id, org_id=org_id, role=role, team_id=team_id, invited_by=invited_by)
        return await self.member_repo.create(membership)

    async def get_members(self, org_id: UUID):
        return await self.member_repo.get_org_members(org_id)

    async def remove_member(self, org_id: UUID, user_id: UUID) -> None:
        membership = await self.member_repo.get_by_user_and_org(user_id, org_id)
        if not membership:
            raise NotFoundError("Membership")
        await self.member_repo.delete(membership, soft=False)

    # ── Invitations ──
    async def create_invitation(self, org_id: UUID, data: InvitationCreate, invited_by: UUID) -> Invitation:
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            org_id=org_id, email=data.email, role=data.role,
            token=token, expires_at=expires_at,
        )
        return await self.invite_repo.create(invitation)

    async def accept_invitation(self, token: str, user_id: UUID) -> Membership:
        invitation = await self.invite_repo.get_by_token(token)
        if not invitation:
            raise NotFoundError("Invitation")
        if invitation.accepted_at:
            raise DuplicateError("Invitation already accepted")
        if invitation.expires_at < datetime.now(timezone.utc):
            raise PermissionDeniedError("Invitation has expired")

        invitation.accepted_at = datetime.now(timezone.utc)
        await self.db.commit()

        return await self.add_member(
            org_id=invitation.org_id, user_id=user_id,
            role=invitation.role, invited_by=None,
        )
