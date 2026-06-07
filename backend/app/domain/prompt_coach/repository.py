"""Prompt Coach Domain — Repository."""
from __future__ import annotations

from uuid import UUID
from sqlalchemy import select
from app.db.base_repository import BaseRepository
from app.domain.prompt_coach.models import PromptAnalysis, ModelBenchmark


class PromptAnalysisRepository(BaseRepository[PromptAnalysis]):
    model = PromptAnalysis

    async def get_user_analyses(self, user_id: UUID, limit: int = 50, offset: int = 0):
        result = await self.db.execute(
            select(PromptAnalysis)
            .where(PromptAnalysis.user_id == user_id)
            .order_by(PromptAnalysis.created_at.desc())
            .limit(limit).offset(offset)
        )
        return result.scalars().all()


class ModelBenchmarkRepository(BaseRepository[ModelBenchmark]):
    model = ModelBenchmark

    async def get_active_models(self):
        result = await self.db.execute(
            select(ModelBenchmark).where(ModelBenchmark.is_active.is_(True))
        )
        return result.scalars().all()
