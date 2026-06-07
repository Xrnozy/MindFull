"""
Users Domain — Repository (Data Access Layer).
"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_repository import BaseRepository
from app.domain.users.models import User


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email, User.deleted_at.is_(None))
        )
        return result.scalars().first()

    async def get_by_org(self, org_id: UUID, limit: int = 100, offset: int = 0):
        result = await self.db.execute(
            select(User)
            .where(User.org_id == org_id, User.deleted_at.is_(None))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
