"""Health Check Router."""
from __future__ import annotations
from fastapi import APIRouter
from app.core.redis import get_redis
from app.db.session import engine

router = APIRouter()

@router.get("/liveness")
async def liveness():
    """Basic liveness probe."""
    return {"status": "ok"}

@router.get("/readiness")
async def readiness():
    """Deep readiness probe — checks DB and Redis connectivity."""
    checks = {}

    # Database check
    try:
        async with engine.connect() as conn:
            await conn.execute(type(conn).get_raw_connection)
        checks["database"] = "ok"
    except Exception:
        try:
            from sqlalchemy import text
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            checks["database"] = "ok"
        except Exception as e:
            checks["database"] = f"error: {str(e)}"

    # Redis check
    try:
        redis = get_redis()
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"

    all_ok = all(v == "ok" for v in checks.values())
    return {"status": "ready" if all_ok else "degraded", "checks": checks}
