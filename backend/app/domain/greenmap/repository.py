"""GreenMap Domain — Repository."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from app.db.base_repository import BaseRepository
from app.domain.greenmap.models import BusinessProfile, PublicMetric, Certification


class BusinessProfileRepository(BaseRepository[BusinessProfile]):
    model = BusinessProfile

    async def get_by_org(self, org_id: UUID) -> BusinessProfile | None:
        result = await self.db.execute(
            select(BusinessProfile).where(BusinessProfile.org_id == org_id)
        )
        return result.scalars().first()

    async def get_public(self, limit: int = 50, offset: int = 0):
        result = await self.db.execute(
            select(BusinessProfile).where(BusinessProfile.is_public.is_(True))
            .limit(limit).offset(offset)
        )
        return result.scalars().all()


class PublicMetricRepository(BaseRepository[PublicMetric]):
    model = PublicMetric


class CertificationRepository(BaseRepository[Certification]):
    model = Certification
