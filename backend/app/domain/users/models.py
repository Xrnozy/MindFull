"""
Users Domain — SQLAlchemy Models.

Core user entity with profile, RBAC, gamification stats, and org membership.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, SoftDeleteMixin


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(
        String(50), default="user", nullable=False, index=True
    )  # super_admin | org_admin | team_manager | user
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Gamification stats (denormalized for fast reads)
    total_xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    dependency_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Organization membership
    org_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationships
    organization = relationship("Organization", back_populates="users", lazy="selectin")
    memberships = relationship("Membership", back_populates="user", lazy="selectin")
    forest = relationship("Forest", back_populates="user", uselist=False, lazy="selectin")
    xp_logs = relationship("XPLog", back_populates="user", lazy="noload")
    achievements = relationship("Achievement", back_populates="user", lazy="noload")
    streaks = relationship("Streak", back_populates="user", lazy="noload")
