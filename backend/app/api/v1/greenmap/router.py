"""GreenMap Router."""
from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.domain.users.models import User
from app.domain.greenmap.service import GreenMapService
from app.domain.greenmap.schemas import *

router = APIRouter()

@router.get("/profiles", response_model=List[BusinessProfileResponse])
async def list_profiles(db: AsyncSession = Depends(get_db)):
    return await GreenMapService(db).get_public_profiles()

@router.get("/profiles/{profile_id}", response_model=BusinessProfileResponse)
async def get_profile(profile_id: UUID, db: AsyncSession = Depends(get_db)):
    return await GreenMapService(db).get_profile(profile_id)

@router.put("/profiles/{profile_id}", response_model=BusinessProfileResponse)
async def update_profile(profile_id: UUID, data: BusinessProfileUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await GreenMapService(db).update_profile(profile_id, data)

@router.get("/profiles/{profile_id}/certifications", response_model=List[CertificationResponse])
async def get_certifications(profile_id: UUID, db: AsyncSession = Depends(get_db)):
    return await GreenMapService(db).get_certifications(profile_id)
