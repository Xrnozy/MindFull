"""
Sustainability Domain — Repository.
"""
from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_repository import BaseRepository
from app.domain.sustainability.models import (
    AISession, Prompt, SustainabilityMetric,
    SustainabilityDailyAggregate, TokenUsageLog,
)


class PromptRepository(BaseRepository[Prompt]):
    model = Prompt

    async def get_user_prompts(self, user_id: UUID, limit: int = 50, offset: int = 0):
        result = await self.db.execute(
            select(Prompt)
            .where(Prompt.user_id == user_id)
            .order_by(Prompt.created_at.desc())
            .limit(limit).offset(offset)
        )
        return result.scalars().all()


class SustainabilityMetricRepository(BaseRepository[SustainabilityMetric]):
    model = SustainabilityMetric

    async def get_user_totals(self, user_id: UUID, org_id: UUID | None = None) -> dict:
        stmt = select(
            func.count(SustainabilityMetric.id).label("total_prompts"),
            func.coalesce(func.sum(SustainabilityMetric.carbon_g), 0).label("total_carbon_g"),
            func.coalesce(func.sum(SustainabilityMetric.water_ml), 0).label("total_water_ml"),
            func.coalesce(func.sum(SustainabilityMetric.electricity_wh), 0).label("total_electricity_wh"),
            func.coalesce(func.sum(SustainabilityMetric.cost_usd), 0).label("total_cost_usd"),
        ).where(SustainabilityMetric.user_id == user_id)

        if org_id:
            stmt = stmt.where(SustainabilityMetric.org_id == org_id)

        result = await self.db.execute(stmt)
        row = result.one()
        return {
            "total_prompts": row.total_prompts,
            "total_carbon_g": float(row.total_carbon_g),
            "total_water_ml": float(row.total_water_ml),
            "total_electricity_wh": float(row.total_electricity_wh),
            "total_cost_usd": float(row.total_cost_usd),
        }


class DailyAggregateRepository(BaseRepository[SustainabilityDailyAggregate]):
    model = SustainabilityDailyAggregate

    async def get_user_history(
        self, user_id: UUID, start_date: date, end_date: date
    ):
        result = await self.db.execute(
            select(SustainabilityDailyAggregate)
            .where(
                SustainabilityDailyAggregate.user_id == user_id,
                SustainabilityDailyAggregate.date >= start_date,
                SustainabilityDailyAggregate.date <= end_date,
            )
            .order_by(SustainabilityDailyAggregate.date.asc())
        )
        return result.scalars().all()


class AISessionRepository(BaseRepository[AISession]):
    model = AISession


class TokenUsageLogRepository(BaseRepository[TokenUsageLog]):
    model = TokenUsageLog
