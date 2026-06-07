"""Think-A-Head Domain — Service."""
from __future__ import annotations

import hashlib
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.think_ahead.models import ReflectionPrompt, LearningRetention
from app.domain.think_ahead.repository import ReflectionRepository, LearningRetentionRepository, DependencyScoreRepository
from app.domain.think_ahead.schemas import ReflectionRequest, ConfidenceTrackRequest
from app.core.exceptions import NotFoundError


class ThinkAheadService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.reflection_repo = ReflectionRepository(db)
        self.retention_repo = LearningRetentionRepository(db)
        self.dependency_repo = DependencyScoreRepository(db)

    async def generate_reflection(self, user_id: UUID, data: ReflectionRequest):
        """Generate reflection questions for a user before they submit a prompt."""
        questions = self._generate_questions(data.prompt_text)
        prompt_hash = hashlib.sha256(data.prompt_text.encode()).hexdigest()

        reflection = ReflectionPrompt(
            user_id=user_id,
            original_prompt_text_hash=prompt_hash,
            reflection_questions=questions,
            confidence_before=data.confidence_before,
        )
        return await self.reflection_repo.create(reflection)

    async def track_confidence(self, user_id: UUID, data: ConfidenceTrackRequest):
        """Track confidence after reflection."""
        reflection = await self.reflection_repo.get_by_id(data.reflection_id)
        if not reflection or reflection.user_id != user_id:
            raise NotFoundError("Reflection")
        return await self.reflection_repo.update(reflection, {
            "confidence_after": data.confidence_after,
            "did_proceed": data.did_proceed,
            "delay_seconds": data.delay_seconds,
        })

    async def get_retention(self, user_id: UUID):
        return await self.retention_repo.get_user_topics(user_id)

    async def get_dependency_score(self, user_id: UUID):
        score = await self.dependency_repo.get_latest(user_id)
        if not score:
            return {"score": 0.0, "period_start": None, "period_end": None}
        return score

    @staticmethod
    def _generate_questions(prompt_text: str) -> list[str]:
        """Generate reflection questions based on prompt content (heuristic)."""
        questions = [
            "Do you already know part of the answer to this question?",
            "Could you find this information through a quick search instead?",
            "What would you learn by attempting this yourself first?",
        ]
        words = prompt_text.lower().split()
        if any(w in words for w in ["code", "write", "implement", "create", "build"]):
            questions.append("Have you tried writing a basic version yourself first?")
        if any(w in words for w in ["explain", "what", "how", "why"]):
            questions.append("Could you explain your current understanding of this topic?")
        if len(words) > 50:
            questions.append("Could this be split into smaller, more focused questions?")
        return questions[:5]  # Max 5 questions
