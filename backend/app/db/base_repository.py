"""
Generic Async CRUD Repository.

Provides a base class for all domain repositories with:
- Standard CRUD operations
- Tenant-scoped queries
- Cursor-based pagination
- Soft-delete support
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import Select, func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """
    Generic async CRUD repository.

    Subclasses set `model` to their SQLAlchemy model class.
    All queries automatically scope to org_id when the model has it.
    """

    model: Type[ModelT]

    def __init__(self, db: AsyncSession):
        self.db = db

    # ──────────────────────────────────────────────
    # Read
    # ──────────────────────────────────────────────
    async def get_by_id(
        self,
        entity_id: uuid.UUID,
        org_id: uuid.UUID | None = None,
    ) -> ModelT | None:
        """Get a single entity by its primary key, optionally scoped to org."""
        stmt = select(self.model).where(self.model.id == entity_id)
        stmt = self._apply_tenant(stmt, org_id)
        stmt = self._exclude_deleted(stmt)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_all(
        self,
        org_id: uuid.UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[ModelT]:
        """Get all entities, optionally scoped to org with limit/offset."""
        stmt = select(self.model)
        stmt = self._apply_tenant(stmt, org_id)
        stmt = self._exclude_deleted(stmt)
        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_paginated(
        self,
        org_id: uuid.UUID | None = None,
        cursor: uuid.UUID | None = None,
        limit: int = 50,
        filters: list[Any] | None = None,
    ) -> tuple[Sequence[ModelT], uuid.UUID | None]:
        """
        Cursor-based pagination.

        Returns (items, next_cursor). next_cursor is None if no more pages.
        """
        stmt = select(self.model)
        stmt = self._apply_tenant(stmt, org_id)
        stmt = self._exclude_deleted(stmt)

        if filters:
            stmt = stmt.where(and_(*filters))

        if cursor is not None:
            stmt = stmt.where(self.model.id > cursor)

        stmt = stmt.order_by(self.model.id).limit(limit + 1)
        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        next_cursor = None
        if len(items) > limit:
            items = items[:limit]
            next_cursor = items[-1].id

        return items, next_cursor

    async def count(self, org_id: uuid.UUID | None = None) -> int:
        """Count entities, optionally scoped to org."""
        stmt = select(func.count()).select_from(self.model)
        stmt = self._apply_tenant(stmt, org_id)
        stmt = self._exclude_deleted(stmt)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    # ──────────────────────────────────────────────
    # Write
    # ──────────────────────────────────────────────
    async def create(self, entity: ModelT) -> ModelT:
        """Persist a new entity."""
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def create_many(self, entities: list[ModelT]) -> list[ModelT]:
        """Bulk-insert multiple entities."""
        self.db.add_all(entities)
        await self.db.commit()
        for e in entities:
            await self.db.refresh(e)
        return entities

    async def update(self, entity: ModelT, updates: dict[str, Any]) -> ModelT:
        """Update an existing entity with a dict of changes."""
        for key, value in updates.items():
            setattr(entity, key, value)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity: ModelT, soft: bool = True) -> None:
        """Delete an entity. Soft-delete by default if model supports it."""
        if soft and hasattr(entity, "deleted_at"):
            entity.deleted_at = datetime.now(timezone.utc)
            await self.db.commit()
        else:
            await self.db.delete(entity)
            await self.db.commit()

    # ──────────────────────────────────────────────
    # Internal helpers
    # ──────────────────────────────────────────────
    def _apply_tenant(self, stmt: Select, org_id: uuid.UUID | None) -> Select:
        """Add org_id filter if the model has an org_id column and one was provided."""
        if org_id is not None and hasattr(self.model, "org_id"):
            stmt = stmt.where(self.model.org_id == org_id)
        return stmt

    def _exclude_deleted(self, stmt: Select) -> Select:
        """Exclude soft-deleted rows if the model has a deleted_at column."""
        if hasattr(self.model, "deleted_at"):
            stmt = stmt.where(self.model.deleted_at.is_(None))
        return stmt
