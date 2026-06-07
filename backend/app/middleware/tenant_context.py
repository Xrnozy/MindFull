"""
Multi-Tenant Context Middleware.

Extracts org_id from the JWT claims and stores it on request.state
so downstream handlers can enforce tenant-scoped queries.
"""
from __future__ import annotations

from uuid import UUID

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import get_logger

logger = get_logger("mindfull.tenant")


class TenantContextMiddleware(BaseHTTPMiddleware):
    """Extract tenant (org_id) from JWT and set on request state."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # org_id will be set after auth dependency resolves;
        # this middleware sets the default to None so it's always present.
        request.state.org_id = None
        request.state.user_id = None
        request.state.user_role = None

        response = await call_next(request)
        return response


def set_tenant_context(request: Request, user_id: UUID | None, org_id: UUID | None, role: str | None) -> None:
    """Called by auth dependencies to populate the tenant context after JWT is verified."""
    request.state.user_id = user_id
    request.state.org_id = org_id
    request.state.user_role = role

    # Bind to structlog so all subsequent log lines include tenant info
    structlog.contextvars.bind_contextvars(
        user_id=str(user_id) if user_id else None,
        org_id=str(org_id) if org_id else None,
    )
