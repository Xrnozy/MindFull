"""Reporting Domain — Repository."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from app.db.base_repository import BaseRepository
from app.domain.reporting.models import Report, AuditLog, APIKey


class ReportRepository(BaseRepository[Report]):
    model = Report

    async def get_by_org(self, org_id: UUID, limit: int = 50):
        result = await self.db.execute(
            select(Report).where(Report.org_id == org_id).order_by(Report.created_at.desc()).limit(limit)
        )
        return result.scalars().all()


class AuditLogRepository(BaseRepository[AuditLog]):
    model = AuditLog

    async def search(self, org_id: UUID | None = None, action: str | None = None, limit: int = 100):
        stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        if org_id:
            stmt = stmt.where(AuditLog.org_id == org_id)
        if action:
            stmt = stmt.where(AuditLog.action == action)
        result = await self.db.execute(stmt)
        return result.scalars().all()


class APIKeyRepository(BaseRepository[APIKey]):
    model = APIKey

    async def get_by_hash(self, key_hash: str) -> APIKey | None:
        result = await self.db.execute(
            select(APIKey).where(APIKey.key_hash == key_hash, APIKey.is_active.is_(True))
        )
        return result.scalars().first()

    async def get_user_keys(self, user_id: UUID):
        result = await self.db.execute(
            select(APIKey).where(APIKey.user_id == user_id).order_by(APIKey.created_at.desc())
        )
        return result.scalars().all()
