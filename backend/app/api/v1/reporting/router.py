"""Reporting Router."""
from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user, get_current_org
from app.domain.users.models import User
from app.domain.reporting.service import ReportingService
from app.domain.reporting.schemas import *

router = APIRouter()

@router.post("/generate", response_model=ReportResponse)
async def generate_report(data: ReportGenerateRequest, org_id: UUID = Depends(get_current_org), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReportingService(db).queue_report(org_id, current_user.id, data)

@router.get("/", response_model=List[ReportResponse])
async def list_reports(org_id: UUID = Depends(get_current_org), db: AsyncSession = Depends(get_db)):
    return await ReportingService(db).get_reports(org_id)

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ReportingService(db).get_report(report_id)

@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(action: str | None = Query(None), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReportingService(db).search_audit_logs(current_user.org_id, action)
