"""
Redis-backed Sliding Window Rate Limiter Middleware.

Enforces per-IP and per-user rate limits using a Redis counter
with configurable limits per endpoint category.
"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.config import settings
from app.core.logger import get_logger
from app.core.redis import get_redis

logger = get_logger("mindfull.rate_limit")

# Route prefix → max requests per minute
_ROUTE_LIMITS: dict[str, int] = {
    "/api/v1/auth": settings.RATE_LIMIT_AUTH_PER_MINUTE,
    "/api/v1/analytics": settings.RATE_LIMIT_ANALYTICS_PER_MINUTE,
}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Sliding window rate limiter backed by Redis."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Determine the identifier: authenticated user_id or client IP
        user_id = getattr(getattr(request, "state", None), "user_id", None)
        identifier = str(user_id) if user_id else (request.client.host if request.client else "unknown")

        # Determine the per-minute limit for this route
        limit = settings.RATE_LIMIT_DEFAULT_PER_MINUTE
        path = request.url.path
        for prefix, route_limit in _ROUTE_LIMITS.items():
            if path.startswith(prefix):
                limit = route_limit
                break

        # Redis key: rl:{identifier}:{minute_bucket}
        import time
        minute_bucket = int(time.time()) // 60
        key = f"rl:{identifier}:{minute_bucket}"

        try:
            redis = get_redis()
            pipe = redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, 120)  # TTL = 2 minutes to cover window overlap
            results = await pipe.execute()
            current_count = results[0]
        except Exception:
            # If Redis is unavailable, allow the request through (graceful degradation)
            request_id = getattr(getattr(request, "state", None), "request_id", "unknown")
            logger.warning("rate_limit_redis_unavailable", path=path, request_id=request_id)
            return await call_next(request)

        if current_count > limit:
            retry_after = 60 - (int(time.time()) % 60)
            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=path,
                count=current_count,
                limit=limit,
            )
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": f"Rate limit exceeded. Retry after {retry_after} seconds.",
                    }
                },
                headers={"Retry-After": str(retry_after)},
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, limit - current_count))
        return response
