"""
Users Domain — Service (Business Logic).
"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, DuplicateError
from app.domain.users.models import User
from app.domain.users.repository import UserRepository
from app.domain.users.schemas import UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.db = db

    async def get_user(self, user_id: UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", str(user_id))
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repo.get_by_email(email)

    async def update_user(self, user: User, updates: UserUpdate) -> User:
        update_data = updates.model_dump(exclude_unset=True)
        return await self.repo.update(user, update_data)

    async def deactivate_user(self, user: User) -> None:
        await self.repo.update(user, {"is_active": False})

    async def get_org_users(self, org_id: UUID, limit: int = 100, offset: int = 0):
        return await self.repo.get_by_org(org_id, limit, offset)

    async def add_xp(self, user: User, amount: int) -> User:
        """Add XP and recalculate level."""
        new_xp = user.total_xp + amount
        new_level = self._calculate_level(new_xp)
        return await self.repo.update(user, {"total_xp": new_xp, "level": new_level})

    @staticmethod
    def _calculate_level(total_xp: int) -> int:
        """XP-to-level mapping: Level N requires N*100 cumulative XP."""
        level = 1
        xp_needed = 100
        remaining = total_xp
        while remaining >= xp_needed:
            remaining -= xp_needed
            level += 1
            xp_needed = level * 100
        return level
