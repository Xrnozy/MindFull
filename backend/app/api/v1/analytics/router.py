"""Analytics Router."""
from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.domain.users.models import User
from app.domain.analytics.service import AnalyticsService
from app.domain.analytics.schemas import BatchEventsRequest

router = APIRouter()

@router.post("/events")
async def ingest_events(data: BatchEventsRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    count = await AnalyticsService(db).ingest_batch(current_user.id, current_user.org_id, data)
    return {"ingested": count}

@router.get("/dashboard")
async def dashboard(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await AnalyticsService(db).get_dashboard(current_user.org_id)

@router.get("/trends")
async def trends(event_type: str = Query("prompt_logged"), period: str = Query("daily"), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await AnalyticsService(db).get_trends(event_type, period, current_user.org_id)
