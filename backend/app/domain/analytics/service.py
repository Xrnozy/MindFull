"""Analytics Domain — Service."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.analytics.models import Event
from app.domain.analytics.repository import EventRepository, EventAggregateRepository
from app.domain.analytics.schemas import EventCreate, BatchEventsRequest


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.event_repo = EventRepository(db)
        self.agg_repo = EventAggregateRepository(db)

    async def ingest_batch(self, user_id: UUID, org_id: UUID | None, data: BatchEventsRequest) -> int:
        events = [
            Event(user_id=user_id, org_id=org_id, **e.model_dump())
            for e in data.events
        ]
        await self.event_repo.create_many(events)
        return len(events)

    async def get_dashboard(self, org_id: UUID | None = None):
        counts = await self.event_repo.count_by_type(org_id)
        return {
            "total_events": sum(counts.values()),
            "event_breakdown": counts,
        }

    async def get_trends(self, event_type: str, period: str = "daily", org_id: UUID | None = None, limit: int = 30):
        return await self.agg_repo.get_trends(event_type, period, org_id, limit)
