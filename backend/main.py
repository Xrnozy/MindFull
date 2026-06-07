from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1 import api_v1_router
from app.core.events import on_startup, on_shutdown
from app.core.exceptions import register_exception_handlers
from prometheus_fastapi_instrumentator import Instrumentator

# Middlewares
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.tenant_context import TenantContextMiddleware
from app.middleware.audit_log import AuditLogMiddleware
from app.middleware.device_fingerprint import DeviceFingerprintMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize Redis, logging, telemetry
    await on_startup()
    yield
    # Shutdown: close Redis, dispose engine
    await on_shutdown()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Instrument Prometheus metrics
if settings.ENABLE_METRICS:
    Instrumentator().instrument(app).expose(app, include_in_schema=False, should_gzip=True)

# CORS — wildcard origins cannot be used with allow_credentials=True
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Middlewares (applied in reverse order of execution)
app.add_middleware(AuditLogMiddleware)
app.add_middleware(TenantContextMiddleware)
app.add_middleware(DeviceFingerprintMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestIDMiddleware)

# Routes
app.include_router(api_v1_router)

# Register exception handlers (must be after routes/middleware setup)
register_exception_handlers(app)


@app.get("/health/liveness")
def health_liveness():
    """Basic liveness probe — am I running?"""
    return {"status": "ok"}


@app.get("/health/readiness")
async def health_readiness():
    """Readiness probe — can I serve traffic? Checks DB + Redis."""
    from app.core.redis import get_redis
    from app.db.session import engine
    from sqlalchemy import text
    from starlette.responses import JSONResponse

    checks = {}

    # Redis check
    try:
        redis = get_redis()
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"

    # Database check
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"

    all_ok = all(v == "ok" for v in checks.values())
    status_code = 200 if all_ok else 503

    return JSONResponse(
        status_code=status_code,
        content={"status": "ok" if all_ok else "degraded", "checks": checks},
    )
