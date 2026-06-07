"""Education Domain — Service."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError
from app.domain.education.models import Institution, Course, Enrollment, Quiz, QuizAttempt
from app.domain.education.repository import *
from app.domain.education.schemas import InstitutionCreate, CourseCreate, QuizAttemptRequest


class EducationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.inst_repo = InstitutionRepository(db)
        self.course_repo = CourseRepository(db)
        self.enrollment_repo = EnrollmentRepository(db)
        self.quiz_repo = QuizRepository(db)
        self.attempt_repo = QuizAttemptRepository(db)
        self.competition_repo = CompetitionRepository(db)
        self.campus_repo = CampusAnalyticsRepository(db)

    async def create_institution(self, org_id: UUID, data: InstitutionCreate) -> Institution:
        inst = Institution(org_id=org_id, **data.model_dump())
        return await self.inst_repo.create(inst)

    async def get_institution(self, inst_id: UUID) -> Institution:
        inst = await self.inst_repo.get_by_id(inst_id)
        if not inst:
            raise NotFoundError("Institution", str(inst_id))
        return inst

    async def create_course(self, institution_id: UUID, data: CourseCreate, instructor_id: UUID | None = None) -> Course:
        course = Course(institution_id=institution_id, instructor_user_id=instructor_id, **data.model_dump())
        return await self.course_repo.create(course)

    async def get_courses(self, institution_id: UUID):
        return await self.course_repo.get_by_institution(institution_id)

    async def enroll(self, course_id: UUID, user_id: UUID) -> Enrollment:
        enrollment = Enrollment(course_id=course_id, user_id=user_id)
        return await self.enrollment_repo.create(enrollment)

    async def get_quizzes(self, user_id: UUID):
        return await self.quiz_repo.get_user_quizzes(user_id)

    async def submit_quiz_attempt(self, quiz_id: UUID, user_id: UUID, data: QuizAttemptRequest) -> QuizAttempt:
        quiz = await self.quiz_repo.get_by_id(quiz_id)
        if not quiz:
            raise NotFoundError("Quiz", str(quiz_id))
        score = self._grade_quiz(quiz.questions, data.answers)
        attempt = QuizAttempt(quiz_id=quiz_id, user_id=user_id, answers=data.answers, score=score)
        return await self.attempt_repo.create(attempt)

    async def get_competitions(self):
        return await self.competition_repo.get_all()

    async def get_campus_analytics(self, institution_id: UUID):
        return await self.campus_repo.get_by_institution(institution_id)

    @staticmethod
    def _grade_quiz(questions: dict, answers: dict) -> float:
        """Simple auto-grading: compare answers to correct values in questions."""
        items = questions.get("items", [])
        if not items:
            return 0.0
        correct = 0
        for i, q in enumerate(items):
            correct_answer = q.get("correct")
            user_answer = answers.get(str(i))
            if user_answer == correct_answer:
                correct += 1
        return round((correct / len(items)) * 100, 1)
