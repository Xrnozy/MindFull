"""
Audit Logging Middleware.

Logs all mutating HTTP requests (POST, PUT, PATCH, DELETE) with
user context, IP address, request body hash, and timing information.
"""
from __future__ import annotations

import hashlib
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import get_logger

logger = get_logger("mindfull.audit")

_MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Log mutating API requests for compliance and security auditing."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method not in _MUTATING_METHODS:
            return await call_next(request)

        start_time = time.monotonic()

        # Read and hash request body (for tamper detection without storing PII)
        body = await request.body()
        body_hash = hashlib.sha256(body).hexdigest() if body else None

        response = await call_next(request)

        duration_ms = round((time.monotonic() - start_time) * 1000, 2)

        # Extract context set by auth middleware
        user_id = getattr(request.state, "user_id", None)
        org_id = getattr(request.state, "org_id", None)

        logger.info(
            "audit_log",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            user_id=str(user_id) if user_id else None,
            org_id=str(org_id) if org_id else None,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent", ""),
            request_body_hash=body_hash,
            duration_ms=duration_ms,
        )

        return response
