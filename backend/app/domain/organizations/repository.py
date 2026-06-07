"""
Organizations Domain — Repository.
"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_repository import BaseRepository
from app.domain.organizations.models import Organization, Team, Membership, Invitation


class OrganizationRepository(BaseRepository[Organization]):
    model = Organization

    async def get_by_slug(self, slug: str) -> Organization | None:
        result = await self.db.execute(
            select(Organization).where(Organization.slug == slug, Organization.deleted_at.is_(None))
        )
        return result.scalars().first()


class TeamRepository(BaseRepository[Team]):
    model = Team

    async def get_by_org(self, org_id: UUID):
        result = await self.db.execute(
            select(Team).where(Team.org_id == org_id)
        )
        return result.scalars().all()


class MembershipRepository(BaseRepository[Membership]):
    model = Membership

    async def get_by_user_and_org(self, user_id: UUID, org_id: UUID) -> Membership | None:
        result = await self.db.execute(
            select(Membership).where(
                Membership.user_id == user_id,
                Membership.org_id == org_id,
            )
        )
        return result.scalars().first()

    async def get_org_members(self, org_id: UUID):
        result = await self.db.execute(
            select(Membership).where(Membership.org_id == org_id)
        )
        return result.scalars().all()


class InvitationRepository(BaseRepository[Invitation]):
    model = Invitation

    async def get_by_token(self, token: str) -> Invitation | None:
        result = await self.db.execute(
            select(Invitation).where(Invitation.token == token)
        )
        return result.scalars().first()
