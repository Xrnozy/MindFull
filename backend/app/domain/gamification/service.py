"""Gamification Domain — Service."""
from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.gamification.models import XPLog, Achievement, Streak
from app.domain.gamification.repository import (
    XPLogRepository, LevelRepository, AchievementRepository,
    StreakRepository, LeaderboardRepository,
)


class GamificationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.xp_repo = XPLogRepository(db)
        self.level_repo = LevelRepository(db)
        self.achievement_repo = AchievementRepository(db)
        self.streak_repo = StreakRepository(db)
        self.leaderboard_repo = LeaderboardRepository(db)

    async def award_xp(self, user_id: UUID, amount: int, source: str, reference_id: UUID | None = None) -> XPLog:
        log = XPLog(user_id=user_id, amount=amount, source=source, reference_id=reference_id)
        return await self.xp_repo.create(log)

    async def get_xp_history(self, user_id: UUID, limit: int = 50):
        return await self.xp_repo.get_user_logs(user_id, limit)

    async def get_achievements(self, user_id: UUID):
        return await self.achievement_repo.get_user_achievements(user_id)

    async def get_streaks(self, user_id: UUID):
        return await self.streak_repo.get_user_streaks(user_id)

    async def update_streak(self, user_id: UUID, streak_type: str) -> Streak:
        """Update or create a streak for today."""
        today = date.today()
        streak = await self.streak_repo.get_user_streak(user_id, streak_type)

        if not streak:
            streak = Streak(
                user_id=user_id, streak_type=streak_type,
                current_count=1, longest_count=1, last_activity_date=today,
            )
            return await self.streak_repo.create(streak)

        if streak.last_activity_date == today:
            return streak  # Already updated today

        from datetime import timedelta
        if streak.last_activity_date == today - timedelta(days=1):
            # Consecutive day — increment
            new_count = streak.current_count + 1
            longest = max(streak.longest_count, new_count)
            return await self.streak_repo.update(streak, {
                "current_count": new_count,
                "longest_count": longest,
                "last_activity_date": today,
            })
        else:
            # Broken streak — reset
            return await self.streak_repo.update(streak, {
                "current_count": 1,
                "last_activity_date": today,
            })

    async def get_leaderboard(self, score_type: str = "xp", period: str = "weekly", org_id: UUID | None = None, limit: int = 50):
        return await self.leaderboard_repo.get_top(score_type, period, org_id, limit)

    async def get_levels(self):
        return await self.level_repo.get_all_ordered()
