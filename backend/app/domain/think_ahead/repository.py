"""Think-A-Head Domain — Repository."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from app.db.base_repository import BaseRepository
from app.domain.think_ahead.models import ReflectionPrompt, LearningRetention, DependencyScore


class ReflectionRepository(BaseRepository[ReflectionPrompt]):
    model = ReflectionPrompt


class LearningRetentionRepository(BaseRepository[LearningRetention]):
    model = LearningRetention

    async def get_user_topics(self, user_id: UUID):
        result = await self.db.execute(
            select(LearningRetention).where(LearningRetention.user_id == user_id)
            .order_by(LearningRetention.retention_score.asc())
        )
        return result.scalars().all()


class DependencyScoreRepository(BaseRepository[DependencyScore]):
    model = DependencyScore

    async def get_latest(self, user_id: UUID) -> DependencyScore | None:
        result = await self.db.execute(
            select(DependencyScore).where(DependencyScore.user_id == user_id)
            .order_by(DependencyScore.period_end.desc()).limit(1)
        )
        return result.scalars().first()
