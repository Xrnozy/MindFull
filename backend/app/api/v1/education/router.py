"""Education Router."""
from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user, get_current_org
from app.domain.users.models import User
from app.domain.education.service import EducationService
from app.domain.education.schemas import *

router = APIRouter()

@router.post("/institutions", response_model=InstitutionResponse)
async def create_institution(data: InstitutionCreate, org_id: UUID = Depends(get_current_org), db: AsyncSession = Depends(get_db)):
    return await EducationService(db).create_institution(org_id, data)

@router.get("/institutions/{inst_id}/courses", response_model=List[CourseResponse])
async def list_courses(inst_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await EducationService(db).get_courses(inst_id)

@router.post("/institutions/{inst_id}/courses", response_model=CourseResponse)
async def create_course(inst_id: UUID, data: CourseCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await EducationService(db).create_course(inst_id, data, current_user.id)

@router.get("/quizzes", response_model=List[QuizResponse])
async def list_quizzes(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await EducationService(db).get_quizzes(current_user.id)

@router.post("/quizzes/{quiz_id}/attempt", response_model=QuizAttemptResponse)
async def submit_attempt(quiz_id: UUID, data: QuizAttemptRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await EducationService(db).submit_quiz_attempt(quiz_id, current_user.id, data)

@router.get("/competitions", response_model=List[CompetitionResponse])
async def list_competitions(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await EducationService(db).get_competitions()

@router.get("/campus-analytics/{inst_id}", response_model=List[CampusAnalyticsResponse])
async def campus_analytics(inst_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await EducationService(db).get_campus_analytics(inst_id)
