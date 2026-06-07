"""
Forest Domain — SQLAlchemy Models (Mindfull Forest™).

User forests, trees, green points, community goals, campaigns, sponsorships.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, TenantMixin


class Forest(Base, TimestampMixin):
    __tablename__ = "forests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    green_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_trees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_carbon_offset_g: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    user = relationship("User", back_populates="forest")
    trees = relationship("Tree", back_populates="forest", lazy="selectin")


class Tree(Base, TimestampMixin):
    __tablename__ = "trees"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("forests.id", ondelete="CASCADE"), nullable=False, index=True)
    species: Mapped[str] = mapped_column(String(100), default="Oak", nullable=False)
    growth_stage: Mapped[str] = mapped_column(String(50), default="seed", nullable=False)  # seed | sapling | young | mature | ancient
    health: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)  # 0–1
    planted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_watered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    carbon_absorbed_g: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    forest = relationship("Forest", back_populates="trees")


class GreenPointLog(Base, TimestampMixin):
    __tablename__ = "green_point_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)  # sustainability_action | prompt_efficiency | quiz | streak
    reference_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)


class CommunityGoal(Base, TimestampMixin):
    __tablename__ = "community_goals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_trees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_trees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    target_carbon_g: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    current_carbon_g: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Campaign(Base, TimestampMixin):
    __tablename__ = "campaigns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sponsor_org_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)
    goal_type: Mapped[str] = mapped_column(String(50), nullable=False)  # trees | carbon | points
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Sponsorship(Base, TimestampMixin):
    __tablename__ = "sponsorships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    amount_pledged: Mapped[float] = mapped_column(Float, nullable=False)
    amount_fulfilled: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
