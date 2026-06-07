"""
Async Redis Client and Caching Utilities.

Provides a connection pool-backed async Redis client and helper functions
for caching patterns (get/set/invalidate) used across the application.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Optional

import redis.asyncio as aioredis

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("mindfull.redis")

# Module-level connection pool — initialized on app startup
_redis_pool: Optional[aioredis.Redis] = None


async def init_redis(max_retries: int = 5, retry_delay: float = 2.0) -> aioredis.Redis:
    """Initialize the Redis connection pool with retry logic.

    Retries with exponential backoff to handle startup race conditions
    where Redis might not be ready when the API container starts.
    """
    global _redis_pool

    for attempt in range(1, max_retries + 1):
        try:
            _redis_pool = aioredis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                max_connections=50,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30,
            )
            # Verify connection is actually working
            await _redis_pool.ping()
            logger.info("redis_connected", url=settings.REDIS_URL, attempt=attempt)
            return _redis_pool
        except Exception as e:
            logger.warning(
                "redis_connection_failed",
                attempt=attempt,
                max_retries=max_retries,
                error=str(e),
            )
            if attempt < max_retries:
                await asyncio.sleep(retry_delay * attempt)
            else:
                logger.error(
                    "redis_connection_exhausted",
                    error=str(e),
                    msg="Proceeding without verified Redis connection — will retry on use",
                )
                # Return pool anyway — redis-py will retry on actual use
                return _redis_pool


async def close_redis() -> None:
    """Close the Redis connection pool. Called during app shutdown."""
    global _redis_pool
    if _redis_pool:
        await _redis_pool.close()
        _redis_pool = None
        logger.info("redis_disconnected")


def get_redis() -> aioredis.Redis:
    """Get the Redis client. Raises if not initialized."""
    if _redis_pool is None:
        raise RuntimeError("Redis pool not initialized. Call init_redis() during app startup.")
    return _redis_pool


# ──────────────────────────────────────────────
# Caching helpers
# ──────────────────────────────────────────────
async def get_cached(key: str) -> Optional[Any]:
    """Retrieve a JSON-serialized cached value by key."""
    client = get_redis()
    raw = await client.get(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw


async def set_cached(key: str, value: Any, ttl: int | None = None) -> None:
    """Store a JSON-serialized value in cache with optional TTL (seconds)."""
    client = get_redis()
    ttl = ttl or settings.REDIS_DEFAULT_TTL
    serialized = json.dumps(value, default=str)
    await client.set(key, serialized, ex=ttl)


async def invalidate(pattern: str) -> int:
    """Invalidate (delete) all keys matching a pattern. Returns count deleted."""
    client = get_redis()
    count = 0
    async for key in client.scan_iter(match=pattern, count=100):
        await client.delete(key)
        count += 1
    return count


async def increment_counter(key: str, ttl: int = 60) -> int:
    """Atomic increment for rate limiting / counters. Sets TTL on first create."""
    client = get_redis()
    pipe = client.pipeline()
    pipe.incr(key)
    pipe.expire(key, ttl)
    results = await pipe.execute()
    return results[0]  # current count
