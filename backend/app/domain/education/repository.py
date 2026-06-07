"""Education Domain — Repository."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from app.db.base_repository import BaseRepository
from app.domain.education.models import Institution, Course, Enrollment, Quiz, QuizAttempt, Competition, CampusAnalytics

class InstitutionRepository(BaseRepository[Institution]):
    model = Institution

class CourseRepository(BaseRepository[Course]):
    model = Course

    async def get_by_institution(self, institution_id: UUID):
        result = await self.db.execute(select(Course).where(Course.institution_id == institution_id))
        return result.scalars().all()

class EnrollmentRepository(BaseRepository[Enrollment]):
    model = Enrollment

class QuizRepository(BaseRepository[Quiz]):
    model = Quiz

    async def get_user_quizzes(self, user_id: UUID):
        result = await self.db.execute(select(Quiz).where(Quiz.user_id == user_id).order_by(Quiz.created_at.desc()))
        return result.scalars().all()

class QuizAttemptRepository(BaseRepository[QuizAttempt]):
    model = QuizAttempt

class CompetitionRepository(BaseRepository[Competition]):
    model = Competition

class CampusAnalyticsRepository(BaseRepository[CampusAnalytics]):
    model = CampusAnalytics

    async def get_by_institution(self, institution_id: UUID):
        result = await self.db.execute(
            select(CampusAnalytics).where(CampusAnalytics.institution_id == institution_id)
            .order_by(CampusAnalytics.created_at.desc())
        )
        return result.scalars().all()
