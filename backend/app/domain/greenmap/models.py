"""
GreenMap Domain — SQLAlchemy Models.

Public business profiles, sustainability metrics, and certifications.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class BusinessProfile(Base, TimestampMixin):
    __tablename__ = "business_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    website: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    public_metrics = relationship("PublicMetric", back_populates="profile", lazy="selectin")
    certifications = relationship("Certification", back_populates="profile", lazy="selectin")


class PublicMetric(Base, TimestampMixin):
    __tablename__ = "public_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("business_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    period: Mapped[str] = mapped_column(String(20), nullable=False)  # monthly | quarterly | yearly
    total_carbon_saved_g: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_prompts_optimized: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sustainability_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    efficiency_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    profile = relationship("BusinessProfile", back_populates="public_metrics")


class Certification(Base, TimestampMixin):
    __tablename__ = "certifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("business_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    certification_name: Mapped[str] = mapped_column(String(255), nullable=False)
    issuer: Mapped[str] = mapped_column(String(255), nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    document_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    profile = relationship("BusinessProfile", back_populates="certifications")
