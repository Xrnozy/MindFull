"""Wellness Domain — Service."""
from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.domain.wellness.models import DailyGoal, UsageLimit
from app.domain.wellness.repository import DailyGoalRepository, UsageLimitRepository, WellnessReportRepository
from app.domain.wellness.schemas import DailyGoalUpdate, UsageLimitUpdate


class WellnessService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.goal_repo = DailyGoalRepository(db)
        self.limit_repo = UsageLimitRepository(db)
        self.report_repo = WellnessReportRepository(db)

    async def get_or_create_daily_goal(self, user_id: UUID) -> DailyGoal:
        today = date.today()
        goal = await self.goal_repo.get_today(user_id, today)
        if not goal:
            limits = await self.limit_repo.get_for_user(user_id)
            prompt_limit = limits.max_daily_prompts if limits else 100
            goal = DailyGoal(user_id=user_id, date=today, prompt_limit=prompt_limit)
            goal = await self.goal_repo.create(goal)
        return goal

    async def update_daily_goal(self, user_id: UUID, data: DailyGoalUpdate) -> DailyGoal:
        goal = await self.get_or_create_daily_goal(user_id)
        return await self.goal_repo.update(goal, {"prompt_limit": data.prompt_limit})

    async def increment_usage(self, user_id: UUID) -> DailyGoal:
        goal = await self.get_or_create_daily_goal(user_id)
        new_count = goal.prompts_used + 1
        is_completed = new_count >= goal.prompt_limit
        return await self.goal_repo.update(goal, {"prompts_used": new_count, "is_completed": is_completed})

    async def get_limits(self, user_id: UUID) -> UsageLimit:
        limits = await self.limit_repo.get_for_user(user_id)
        if not limits:
            limits = UsageLimit(user_id=user_id)
            limits = await self.limit_repo.create(limits)
        return limits

    async def update_limits(self, user_id: UUID, data: UsageLimitUpdate) -> UsageLimit:
        limits = await self.get_limits(user_id)
        updates = data.model_dump(exclude_unset=True)
        return await self.limit_repo.update(limits, updates)

    async def get_reports(self, user_id: UUID, limit: int = 10):
        return await self.report_repo.get_user_reports(user_id, limit)
