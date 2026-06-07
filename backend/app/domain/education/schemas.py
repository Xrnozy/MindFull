"""Education Domain — Schemas."""
from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class InstitutionCreate(BaseModel):
    type: str
    name: str
    campus_code: str | None = None

class InstitutionResponse(BaseModel):
    id: UUID
    org_id: UUID
    type: str
    name: str
    campus_code: str | None = None
    model_config = ConfigDict(from_attributes=True)

class CourseCreate(BaseModel):
    name: str
    code: str | None = None
    semester: str | None = None

class CourseResponse(BaseModel):
    id: UUID
    institution_id: UUID
    name: str
    code: str | None = None
    semester: str | None = None
    model_config = ConfigDict(from_attributes=True)

class QuizResponse(BaseModel):
    id: UUID
    topic: str
    questions: dict
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class QuizAttemptRequest(BaseModel):
    answers: dict

class QuizAttemptResponse(BaseModel):
    id: UUID
    quiz_id: UUID
    score: float
    completed_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CompetitionResponse(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    metric_type: str
    starts_at: datetime
    ends_at: datetime
    prizes: dict | None = None
    model_config = ConfigDict(from_attributes=True)

class CampusAnalyticsResponse(BaseModel):
    institution_id: UUID
    period: str
    total_students_active: int
    avg_sustainability_score: float
    avg_retention_score: float
    total_carbon_saved_g: float
    model_config = ConfigDict(from_attributes=True)
