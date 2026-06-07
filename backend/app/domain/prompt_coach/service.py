"""Prompt Coach Domain — Service."""
from __future__ import annotations

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.prompt_coach.analyzer import analyze_prompt, AnalysisResult
from app.domain.prompt_coach.models import PromptAnalysis
from app.domain.prompt_coach.repository import PromptAnalysisRepository, ModelBenchmarkRepository
from app.domain.prompt_coach.schemas import PromptAnalyzeRequest


class PromptCoachService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.analysis_repo = PromptAnalysisRepository(db)
        self.benchmark_repo = ModelBenchmarkRepository(db)

    async def analyze(self, user_id: UUID, data: PromptAnalyzeRequest) -> AnalysisResult:
        """Analyze prompt efficiency and persist the result."""
        result = analyze_prompt(data.prompt_text, data.intended_model)

        analysis = PromptAnalysis(
            user_id=user_id,
            efficiency_score=result.efficiency_score,
            clarity_score=result.clarity_score,
            specificity_score=result.specificity_score,
            context_ratio=result.context_ratio,
            repetition_penalty=result.repetition_penalty,
            token_prediction=result.token_prediction,
            cost_prediction=result.cost_prediction,
            carbon_prediction=result.carbon_prediction,
            suggestions=result.suggestions,
            recommended_model=result.recommended_model,
        )
        await self.analysis_repo.create(analysis)
        return result

    async def get_history(self, user_id: UUID, limit: int = 50, offset: int = 0):
        return await self.analysis_repo.get_user_analyses(user_id, limit, offset)

    async def get_model_benchmarks(self):
        return await self.benchmark_repo.get_active_models()
