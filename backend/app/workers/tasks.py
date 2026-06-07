"""
Background Workers — Celery / AsyncIO Task Stubs.

These workers handle async background jobs:
- Daily aggregation of sustainability metrics
- Leaderboard recalculation
- Forest growth simulation
- Wellness report generation
- Report file generation
- Campus analytics aggregation
"""
from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker
from app.core.config import settings
from celery import Celery

celery = Celery(
    "mindfull_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

def run_async(coro):
    import asyncio
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        return asyncio.ensure_future(coro)
    return asyncio.run(coro)


# ──────────────────────────────────────────────
# Sustainability & Gamification (4.2, 4.3, 4.4)
# ──────────────────────────────────────────────

@celery.task
def aggregate_daily_sustainability_sync(target_date: str | None = None):
    """Sync wrapper for Celery."""
    td = date.fromisoformat(target_date) if target_date else None
    run_async(aggregate_daily_sustainability(td))

async def aggregate_daily_sustainability(target_date: date | None = None):
    """
    Aggregate per-user sustainability metrics for the given day.
    Called nightly via scheduler (cron or manual trigger).
    """
    from app.domain.sustainability.models import SustainabilityMetric, SustainabilityDailyAggregate

    target = target_date or (date.today() - timedelta(days=1))

    async with async_session_maker() as db:
        # Group by user_id for the target date
        stmt = select(
            SustainabilityMetric.user_id,
            SustainabilityMetric.org_id,
            func.count(SustainabilityMetric.id).label("total_prompts"),
            func.sum(SustainabilityMetric.carbon_g).label("total_carbon_g"),
            func.sum(SustainabilityMetric.water_ml).label("total_water_ml"),
            func.sum(SustainabilityMetric.electricity_wh).label("total_electricity_wh"),
            func.sum(SustainabilityMetric.cost_usd).label("total_cost_usd"),
        ).where(
            func.date(SustainabilityMetric.created_at) == target
        ).group_by(SustainabilityMetric.user_id, SustainabilityMetric.org_id)

        result = await db.execute(stmt)
        rows = result.all()

        for row in rows:
            agg = SustainabilityDailyAggregate(
                user_id=row.user_id,
                org_id=row.org_id,
                date=target,
                total_prompts=row.total_prompts,
                total_input_tokens=0,  # Populated separately if needed
                total_output_tokens=0,
                total_carbon_g=float(row.total_carbon_g or 0),
                total_water_ml=float(row.total_water_ml or 0),
                total_electricity_wh=float(row.total_electricity_wh or 0),
                total_cost_usd=float(row.total_cost_usd or 0),
            )
            db.add(agg)

        await db.commit()


@celery.task
def recalculate_leaderboards_sync():
    run_async(recalculate_leaderboards())

async def recalculate_leaderboards():
    """Recalculate weekly and monthly leaderboards."""
    from app.domain.gamification.models import Leaderboard
    from app.domain.users.models import User

    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    async with async_session_maker() as db:
        # Clear existing entries for current week
        from sqlalchemy import delete
        await db.execute(
            delete(Leaderboard).where(
                Leaderboard.period == "weekly",
                Leaderboard.period_start == week_start,
            )
        )

        # Rank users by XP for the week
        users = await db.execute(
            select(User).where(User.is_active.is_(True)).order_by(User.total_xp.desc())
        )
        for rank, user in enumerate(users.scalars().all(), start=1):
            lb = Leaderboard(
                user_id=user.id,
                org_id=user.org_id,
                period="weekly",
                score_type="xp",
                score=float(user.total_xp),
                rank=rank,
                period_start=week_start,
                period_end=week_start + timedelta(days=6),
            )
            db.add(lb)

        await db.commit()


@celery.task
def simulate_forest_growth_sync():
    run_async(simulate_forest_growth())

async def simulate_forest_growth():
    """Grow trees in all forests based on elapsed time."""
    from app.domain.forest.models import Tree
    from app.domain.forest.engine import calculate_growth_stage

    async with async_session_maker() as db:
        result = await db.execute(select(Tree))
        trees = result.scalars().all()

        now = datetime.now(timezone.utc)
        for tree in trees:
            days_alive = (now - tree.planted_at).days
            if days_alive <= 0:
                continue
            new_absorption = days_alive * 0.05  # Simplified
            new_stage = calculate_growth_stage(new_absorption)
            tree.carbon_absorbed_g = new_absorption
            tree.growth_stage = new_stage

        await db.commit()


# ──────────────────────────────────────────────
# Reporting & Analytics (4.5, 4.6)
# ──────────────────────────────────────────────

@celery.task
def process_report_queue_sync():
    run_async(process_report_queue())

async def process_report_queue():
    """Process pending reports in the queue and generate files."""
    from app.domain.reporting.models import Report
    import json

    async with async_session_maker() as db:
        # Find pending reports
        result = await db.execute(
            select(Report).where(Report.status == "pending")
        )
        reports = result.scalars().all()

        for report in reports:
            report.status = "processing"
            await db.commit()

            try:
                # Stub: Generate report logic goes here
                # Example: If format == 'json', dump the parameters or fetch data
                # Upload to S3/Supabase storage and get URL
                report.file_url = f"https://storage.mindfull.local/reports/{report.id}.{report.format}"
                report.status = "completed"
                report.completed_at = datetime.now(timezone.utc)
            except Exception:
                report.status = "failed"

        await db.commit()


@celery.task
def aggregate_analytics_sync():
    run_async(aggregate_analytics())

async def aggregate_analytics():
    """Aggregate raw events into event_aggregates."""
    from app.domain.analytics.models import Event, EventAggregate

    today = date.today()
    period_start = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)
    
    async with async_session_maker() as db:
        # Very simple aggregation stub: sum events per type
        stmt = select(
            Event.user_id,
            Event.org_id,
            Event.event_type,
            func.count(Event.id).label("count")
        ).where(
            Event.created_at >= period_start
        ).group_by(Event.user_id, Event.org_id, Event.event_type)

        result = await db.execute(stmt)
        
        for row in result.all():
            agg = EventAggregate(
                user_id=row.user_id,
                org_id=row.org_id,
                event_type=row.event_type,
                period="daily",
                count=row.count,
                period_start=period_start,
                period_end=period_start + timedelta(days=1),
            )
            db.add(agg)

        await db.commit()


# ──────────────────────────────────────────────
# Wellness & Education (4.7, 4.8)
# ──────────────────────────────────────────────

@celery.task
def generate_wellness_reports_sync():
    run_async(generate_wellness_reports())

async def generate_wellness_reports():
    """Generate weekly wellness reports for all users."""
    from app.domain.wellness.models import WellnessReport
    from app.domain.users.models import User

    today = date.today()
    week_start = today - timedelta(days=7)

    async with async_session_maker() as db:
        users = await db.execute(select(User).where(User.is_active.is_(True)))
        
        for user in users.scalars().all():
            # Stub generation logic
            report = WellnessReport(
                user_id=user.id,
                period_start=week_start,
                period_end=today,
                total_prompts=50,  # Stubbed
                avg_daily_prompts=7.1,
                dependency_trend="stable",
                wellness_score=85.0,
                recommendations={"msg": "Take more breaks between sessions."}
            )
            db.add(report)

        await db.commit()


@celery.task
def compile_campus_analytics_sync():
    run_async(compile_campus_analytics())

async def compile_campus_analytics():
    """Compile analytics for educational institutions."""
    from app.domain.education.models import CampusAnalytics, Institution

    async with async_session_maker() as db:
        institutions = await db.execute(select(Institution))
        
        for inst in institutions.scalars().all():
            analytics = CampusAnalytics(
                institution_id=inst.id,
                period="weekly",
                total_students_active=120,
                avg_sustainability_score=78.5,
                avg_retention_score=0.9,
                total_carbon_saved_g=15000.0,
            )
            db.add(analytics)

        await db.commit()
