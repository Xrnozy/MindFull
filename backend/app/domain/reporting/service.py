"""Reporting Domain — Service."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError
from app.core.security import generate_api_key
from app.domain.reporting.models import Report, APIKey
from app.domain.reporting.repository import ReportRepository, AuditLogRepository, APIKeyRepository
from app.domain.reporting.schemas import ReportGenerateRequest, APIKeyCreateRequest


class ReportingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.report_repo = ReportRepository(db)
        self.audit_repo = AuditLogRepository(db)
        self.api_key_repo = APIKeyRepository(db)

    # ── Reports ──
    async def queue_report(self, org_id: UUID, user_id: UUID, data: ReportGenerateRequest) -> Report:
        report = Report(
            org_id=org_id, report_type=data.report_type,
            format=data.format, parameters=data.parameters,
            generated_by=user_id, status="pending",
        )
        return await self.report_repo.create(report)

    async def get_reports(self, org_id: UUID, limit: int = 50):
        return await self.report_repo.get_by_org(org_id, limit)

    async def get_report(self, report_id: UUID) -> Report:
        report = await self.report_repo.get_by_id(report_id)
        if not report:
            raise NotFoundError("Report", str(report_id))
        return report

    # ── Audit Logs ──
    async def search_audit_logs(self, org_id: UUID | None = None, action: str | None = None, limit: int = 100):
        return await self.audit_repo.search(org_id, action, limit)

    # ── API Keys ──
    async def create_api_key(self, user_id: UUID, org_id: UUID | None, data: APIKeyCreateRequest) -> tuple[APIKey, str]:
        full_key, prefix_display, key_hash = generate_api_key()
        api_key = APIKey(
            user_id=user_id, org_id=org_id,
            key_prefix=prefix_display, key_hash=key_hash,
            name=data.name, scopes=data.scopes,
        )
        api_key = await self.api_key_repo.create(api_key)
        return api_key, full_key

    async def revoke_api_key(self, key_id: UUID, user_id: UUID) -> None:
        api_key = await self.api_key_repo.get_by_id(key_id)
        if not api_key or api_key.user_id != user_id:
            raise NotFoundError("APIKey", str(key_id))
        await self.api_key_repo.update(api_key, {"is_active": False})

    async def get_user_api_keys(self, user_id: UUID):
        return await self.api_key_repo.get_user_keys(user_id)
