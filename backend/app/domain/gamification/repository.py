"""Gamification Domain — Repository."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy import select, func
from app.db.base_repository import BaseRepository
from app.domain.gamification.models import XPLog, Level, Achievement, AchievementDefinition, Streak, Leaderboard


class XPLogRepository(BaseRepository[XPLog]):
    model = XPLog

    async def get_user_total(self, user_id: UUID) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.sum(XPLog.amount), 0)).where(XPLog.user_id == user_id)
        )
        return result.scalar_one()

    async def get_user_logs(self, user_id: UUID, limit: int = 50):
        result = await self.db.execute(
            select(XPLog).where(XPLog.user_id == user_id).order_by(XPLog.created_at.desc()).limit(limit)
        )
        return result.scalars().all()


class LevelRepository(BaseRepository[Level]):
    model = Level

    async def get_all_ordered(self):
        result = await self.db.execute(select(Level).order_by(Level.level_number.asc()))
        return result.scalars().all()


class AchievementRepository(BaseRepository[Achievement]):
    model = Achievement

    async def get_user_achievements(self, user_id: UUID):
        result = await self.db.execute(
            select(Achievement).where(Achievement.user_id == user_id).order_by(Achievement.unlocked_at.desc())
        )
        return result.scalars().all()


class AchievementDefinitionRepository(BaseRepository[AchievementDefinition]):
    model = AchievementDefinition


class StreakRepository(BaseRepository[Streak]):
    model = Streak

    async def get_user_streaks(self, user_id: UUID):
        result = await self.db.execute(select(Streak).where(Streak.user_id == user_id))
        return result.scalars().all()

    async def get_user_streak(self, user_id: UUID, streak_type: str) -> Streak | None:
        result = await self.db.execute(
            select(Streak).where(Streak.user_id == user_id, Streak.streak_type == streak_type)
        )
        return result.scalars().first()


class LeaderboardRepository(BaseRepository[Leaderboard]):
    model = Leaderboard

    async def get_top(self, score_type: str, period: str, org_id: UUID | None = None, limit: int = 50):
        stmt = select(Leaderboard).where(
            Leaderboard.score_type == score_type, Leaderboard.period == period
        )
        if org_id:
            stmt = stmt.where(Leaderboard.org_id == org_id)
        stmt = stmt.order_by(Leaderboard.rank.asc()).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
