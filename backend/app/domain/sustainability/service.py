"""
Sustainability Domain — Service.
"""
from __future__ import annotations

import hashlib
from datetime import date, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.sustainability.engine import (
    calculate_carbon_g, calculate_electricity_wh,
    calculate_water_ml, calculate_cost_usd,
    calculate_sustainability_score,
)
from app.domain.sustainability.models import Prompt, SustainabilityMetric, TokenUsageLog
from app.domain.sustainability.repository import (
    PromptRepository, SustainabilityMetricRepository,
    DailyAggregateRepository, TokenUsageLogRepository,
)
from app.domain.sustainability.schemas import PromptLogRequest, PromptLogResponse, SustainabilityMetricResponse


class SustainabilityService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.prompt_repo = PromptRepository(db)
        self.metric_repo = SustainabilityMetricRepository(db)
        self.daily_repo = DailyAggregateRepository(db)
        self.token_repo = TokenUsageLogRepository(db)

    async def log_prompt(
        self, user_id: UUID, org_id: UUID | None, data: PromptLogRequest
    ) -> PromptLogResponse:
        """Log a prompt and calculate all sustainability metrics."""

        # 1. Create prompt record
        prompt = Prompt(
            user_id=user_id,
            org_id=org_id,
            session_id=data.session_id,
            model_used=data.model,
            input_tokens=data.input_tokens,
            output_tokens=data.output_tokens,
            duration_ms=data.duration_ms,
            client_source=data.client_source,
        )
        prompt = await self.prompt_repo.create(prompt)

        # 2. Calculate sustainability metrics
        electricity = calculate_electricity_wh(data.input_tokens, data.output_tokens, data.model)
        carbon = calculate_carbon_g(data.input_tokens, data.output_tokens, data.model)
        water = calculate_water_ml(electricity)
        cost = calculate_cost_usd(data.input_tokens, data.output_tokens, data.model)

        metric = SustainabilityMetric(
            prompt_id=prompt.id,
            user_id=user_id,
            org_id=org_id,
            carbon_g=carbon,
            water_ml=water,
            electricity_wh=electricity,
            cost_usd=cost,
        )
        await self.metric_repo.create(metric)

        # 3. Log token usage
        token_log = TokenUsageLog(
            user_id=user_id,
            org_id=org_id,
            model_used=data.model,
            input_tokens=data.input_tokens,
            output_tokens=data.output_tokens,
            cost_usd=cost,
        )
        await self.token_repo.create(token_log)

        return PromptLogResponse(
            id=prompt.id,
            sustainability=SustainabilityMetricResponse(
                carbon_g=carbon,
                water_ml=water,
                electricity_wh=electricity,
                cost_usd=cost,
            ),
        )

    async def get_score(self, user_id: UUID, org_id: UUID | None = None):
        """Calculate the user's current sustainability score."""
        totals = await self.metric_repo.get_user_totals(user_id, org_id)
        score = calculate_sustainability_score(
            total_prompts=totals["total_prompts"],
            avg_efficiency_score=70.0,  # TODO: integrate with prompt coach
            total_carbon_g=totals["total_carbon_g"],
        )
        return {**totals, "score": score}

    async def get_history(
        self, user_id: UUID, start_date: date | None = None, end_date: date | None = None
    ):
        """Get daily sustainability history."""
        end = end_date or date.today()
        start = start_date or (end - timedelta(days=30))
        return await self.daily_repo.get_user_history(user_id, start, end)

    async def get_prompts(self, user_id: UUID, limit: int = 50, offset: int = 0):
        return await self.prompt_repo.get_user_prompts(user_id, limit, offset)
