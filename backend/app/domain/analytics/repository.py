"""Analytics Domain — Repository."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy import select, func
from app.db.base_repository import BaseRepository
from app.domain.analytics.models import Event, EventAggregate


class EventRepository(BaseRepository[Event]):
    model = Event

    async def count_by_type(self, org_id: UUID | None = None):
        stmt = select(Event.event_type, func.count(Event.id)).group_by(Event.event_type)
        if org_id:
            stmt = stmt.where(Event.org_id == org_id)
        result = await self.db.execute(stmt)
        return {row[0]: row[1] for row in result.all()}


class EventAggregateRepository(BaseRepository[EventAggregate]):
    model = EventAggregate

    async def get_trends(self, event_type: str, period: str, org_id: UUID | None = None, limit: int = 30):
        stmt = select(EventAggregate).where(
            EventAggregate.event_type == event_type, EventAggregate.period == period
        )
        if org_id:
            stmt = stmt.where(EventAggregate.org_id == org_id)
        stmt = stmt.order_by(EventAggregate.period_start.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
