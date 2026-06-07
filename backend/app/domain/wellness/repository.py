"""Wellness Domain — Repository."""
from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import select
from app.db.base_repository import BaseRepository
from app.domain.wellness.models import DailyGoal, UsageLimit, WellnessReport


class DailyGoalRepository(BaseRepository[DailyGoal]):
    model = DailyGoal

    async def get_today(self, user_id: UUID, today: date) -> DailyGoal | None:
        result = await self.db.execute(
            select(DailyGoal).where(DailyGoal.user_id == user_id, DailyGoal.date == today)
        )
        return result.scalars().first()


class UsageLimitRepository(BaseRepository[UsageLimit]):
    model = UsageLimit

    async def get_for_user(self, user_id: UUID) -> UsageLimit | None:
        result = await self.db.execute(
            select(UsageLimit).where(UsageLimit.user_id == user_id)
        )
        return result.scalars().first()


class WellnessReportRepository(BaseRepository[WellnessReport]):
    model = WellnessReport

    async def get_user_reports(self, user_id: UUID, limit: int = 10):
        result = await self.db.execute(
            select(WellnessReport).where(WellnessReport.user_id == user_id)
            .order_by(WellnessReport.period_end.desc()).limit(limit)
        )
        return result.scalars().all()
