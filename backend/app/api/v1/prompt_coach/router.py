"""Prompt Coach Router."""
from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.domain.users.models import User
from app.domain.prompt_coach.service import PromptCoachService
from app.domain.prompt_coach.schemas import PromptAnalyzeRequest, PromptAnalysisResponse, ModelBenchmarkResponse

router = APIRouter()

@router.post("/analyze", response_model=PromptAnalysisResponse)
async def analyze(data: PromptAnalyzeRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await PromptCoachService(db).analyze(current_user.id, data)
    return PromptAnalysisResponse(**result.__dict__)

@router.get("/history", response_model=List[PromptAnalysisResponse])
async def history(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await PromptCoachService(db).get_history(current_user.id)

@router.get("/models", response_model=List[ModelBenchmarkResponse])
async def models(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await PromptCoachService(db).get_model_benchmarks()
