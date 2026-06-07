"""Forest Router."""
from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.domain.users.models import User
from app.domain.forest.service import ForestService
from app.domain.forest.schemas import *

router = APIRouter()

@router.get("/", response_model=ForestResponse)
async def get_forest(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ForestService(db).get_or_create_forest(current_user.id)

@router.post("/plant", response_model=TreeResponse)
async def plant_tree(data: PlantTreeRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ForestService(db).plant_tree(current_user.id, data)

@router.get("/trees", response_model=List[TreeResponse])
async def list_trees(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ForestService(db).get_trees(current_user.id)

@router.get("/community-goals", response_model=List[CommunityGoalResponse])
async def community_goals(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ForestService(db).get_community_goals()

@router.get("/campaigns", response_model=List[CampaignResponse])
async def campaigns(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ForestService(db).get_campaigns()
