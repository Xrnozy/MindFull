"""Forest Domain — Repository."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from app.db.base_repository import BaseRepository
from app.domain.forest.models import Forest, Tree, GreenPointLog, CommunityGoal, Campaign


class ForestRepository(BaseRepository[Forest]):
    model = Forest

    async def get_by_user(self, user_id: UUID) -> Forest | None:
        result = await self.db.execute(select(Forest).where(Forest.user_id == user_id))
        return result.scalars().first()


class TreeRepository(BaseRepository[Tree]):
    model = Tree

    async def get_by_forest(self, forest_id: UUID):
        result = await self.db.execute(
            select(Tree).where(Tree.forest_id == forest_id).order_by(Tree.planted_at.desc())
        )
        return result.scalars().all()


class GreenPointLogRepository(BaseRepository[GreenPointLog]):
    model = GreenPointLog


class CommunityGoalRepository(BaseRepository[CommunityGoal]):
    model = CommunityGoal

    async def get_active(self):
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        result = await self.db.execute(
            select(CommunityGoal).where(
                CommunityGoal.starts_at <= now, CommunityGoal.ends_at >= now,
                CommunityGoal.is_completed.is_(False),
            )
        )
        return result.scalars().all()


class CampaignRepository(BaseRepository[Campaign]):
    model = Campaign

    async def get_active(self):
        result = await self.db.execute(
            select(Campaign).where(Campaign.is_active.is_(True))
        )
        return result.scalars().all()
