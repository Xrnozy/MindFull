"""
Application Lifecycle Events.

Hooks for startup and shutdown — initializes Redis, logging, telemetry.
"""
from __future__ import annotations

from app.core.logger import setup_logging, get_logger
from app.core.redis import init_redis, close_redis
from app.db.session import engine

logger = get_logger("mindfull.events")


async def on_startup() -> None:
    """Executed once when the application starts."""
    setup_logging()
    logger.info("app_starting", version="0.1.0")
    await init_redis()
    logger.info("app_started")


async def on_shutdown() -> None:
    """Executed once when the application is shutting down."""
    logger.info("app_shutting_down")
    await close_redis()
    await engine.dispose()
    logger.info("app_stopped")
