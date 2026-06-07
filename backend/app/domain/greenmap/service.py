"""GreenMap Domain — Service."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError
from app.domain.greenmap.models import BusinessProfile
from app.domain.greenmap.repository import BusinessProfileRepository, CertificationRepository
from app.domain.greenmap.schemas import BusinessProfileUpdate


class GreenMapService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.profile_repo = BusinessProfileRepository(db)
        self.cert_repo = CertificationRepository(db)

    async def get_public_profiles(self, limit: int = 50, offset: int = 0):
        return await self.profile_repo.get_public(limit, offset)

    async def get_profile(self, profile_id: UUID) -> BusinessProfile:
        profile = await self.profile_repo.get_by_id(profile_id)
        if not profile:
            raise NotFoundError("BusinessProfile", str(profile_id))
        return profile

    async def get_profile_by_org(self, org_id: UUID) -> BusinessProfile:
        profile = await self.profile_repo.get_by_org(org_id)
        if not profile:
            raise NotFoundError("BusinessProfile for org", str(org_id))
        return profile

    async def update_profile(self, profile_id: UUID, data: BusinessProfileUpdate) -> BusinessProfile:
        profile = await self.get_profile(profile_id)
        updates = data.model_dump(exclude_unset=True)
        return await self.profile_repo.update(profile, updates)

    async def get_certifications(self, profile_id: UUID):
        profile = await self.get_profile(profile_id)
        return profile.certifications
