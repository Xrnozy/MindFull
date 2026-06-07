import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from app.core.config import settings
from app.db.base import Base

# Import all models here so Alembic can see them!
from app.domain.users.models import User
from app.domain.organizations.models import Organization, Team, Membership, Invitation
from app.domain.sustainability.models import AISession, Prompt, SustainabilityMetric, SustainabilityDailyAggregate, TokenUsageLog
from app.domain.prompt_coach.models import PromptAnalysis, ModelBenchmark
from app.domain.think_ahead.models import ReflectionPrompt, LearningRetention, DependencyScore
from app.domain.wellness.models import DailyGoal, UsageLimit, WellnessReport
from app.domain.gamification.models import XPLog, Level, AchievementDefinition, Achievement, Streak, Leaderboard
from app.domain.forest.models import Forest, Tree, GreenPointLog, CommunityGoal, Campaign, Sponsorship
from app.domain.greenmap.models import BusinessProfile, PublicMetric, Certification
from app.domain.education.models import Institution, Course, Enrollment, Competition, CompetitionEntry, Quiz, QuizAttempt, CampusAnalytics
from app.domain.reporting.models import Report, AuditLog, APIKey
from app.domain.analytics.models import Event, EventAggregate

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def get_url():
    # Sync driver url for alembic if needed, but we use async_engine_from_config
    return settings.DATABASE_URL

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
