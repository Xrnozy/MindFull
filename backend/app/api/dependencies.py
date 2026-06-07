"""
FastAPI Dependencies for Authentication, Authorization, and Pagination.

Provides dependency injection functions for:
- JWT-based authentication (Supabase)
- API key authentication
- Role-based access control (RBAC)
- Tenant context extraction
- Cursor-based pagination parameters
"""
from __future__ import annotations

import uuid
from typing import Annotated, Optional, Sequence

from fastapi import Depends, HTTPException, Header, Query, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AuthenticationError, PermissionDeniedError
from app.core.security import verify_supabase_jwt, hash_api_key
from app.db.session import get_db
from app.domain.users.models import User
from app.middleware.tenant_context import set_tenant_context

reusable_oauth2 = HTTPBearer(auto_error=False)


# ──────────────────────────────────────────────
# Pagination
# ──────────────────────────────────────────────
class PaginationParams(BaseModel):
    """Cursor-based pagination parameters."""
    cursor: uuid.UUID | None = None
    limit: int = 50

    class Config:
        frozen = True


def get_pagination(
    cursor: Annotated[str | None, Query(description="Cursor ID for pagination")] = None,
    limit: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 50,
) -> PaginationParams:
    """Parse pagination query parameters."""
    parsed_cursor = None
    if cursor:
        try:
            parsed_cursor = uuid.UUID(cursor)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid cursor value: {cursor} is not a valid UUID",
            )
    return PaginationParams(cursor=parsed_cursor, limit=limit)


# ──────────────────────────────────────────────
# JWT Authentication
# ──────────────────────────────────────────────
async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials | None = Depends(reusable_oauth2),
) -> User:
    """
    Validates the Supabase JWT and returns the current user.
    Auto-provisions user record on first login.
    Sets tenant context on request state.
    """
    if token is None:
        raise AuthenticationError("Authorization header missing")

    payload = verify_supabase_jwt(token.credentials)

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise AuthenticationError("Invalid token payload — missing 'sub'")

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise AuthenticationError("Invalid user ID format in token")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        # Auto-provision on first JWT verification
        email = payload.get("email", "unknown@mindfull.local")
        user = User(id=user_id, email=email, role="user")
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Check soft-delete
    if hasattr(user, "deleted_at") and user.deleted_at is not None:
        raise AuthenticationError("Account has been deactivated")

    # Populate tenant context for downstream middleware/logging
    set_tenant_context(request, user_id=user.id, org_id=user.org_id, role=user.role)

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current user, ensuring they are active (not soft-deleted)."""
    if not current_user.is_active:
        raise PermissionDeniedError("Inactive user account")
    return current_user


# ──────────────────────────────────────────────
# API Key Authentication
# ──────────────────────────────────────────────
async def get_api_key_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_api_key: str | None = Header(None, alias="X-API-Key"),
) -> User:
    """
    Authenticate via API key (used by browser extension, 3rd-party integrations).
    Looks up the hashed key in the api_keys table and returns the associated user.
    """
    if not x_api_key:
        raise AuthenticationError("X-API-Key header required")

    key_hash = hash_api_key(x_api_key)

    # Import here to avoid circular imports at module level
    from app.domain.reporting.models import APIKey

    result = await db.execute(
        select(APIKey).where(
            APIKey.key_hash == key_hash,
            APIKey.is_active.is_(True),
        )
    )
    api_key = result.scalars().first()

    if not api_key:
        raise AuthenticationError("Invalid API key")

    # Check expiration
    from datetime import datetime, timezone
    if api_key.expires_at and api_key.expires_at < datetime.now(timezone.utc):
        raise AuthenticationError("API key has expired")

    # Load the associated user
    user_result = await db.execute(select(User).where(User.id == api_key.user_id))
    user = user_result.scalars().first()

    if not user:
        raise AuthenticationError("API key user not found")

    set_tenant_context(request, user_id=user.id, org_id=user.org_id, role=user.role)

    # Update last_used_at
    api_key.last_used_at = datetime.now(timezone.utc)
    await db.commit()

    return user


# ──────────────────────────────────────────────
# RBAC
# ──────────────────────────────────────────────
def require_role(allowed_roles: Sequence[str]):
    """
    Dependency factory for role-based access control.

    Usage:
        @router.get("/admin", dependencies=[Depends(require_role(["super_admin", "org_admin"]))])
    """
    async def _check_role(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise PermissionDeniedError(
                f"Role '{current_user.role}' is not authorized. Required: {', '.join(allowed_roles)}"
            )
        return current_user
    return _check_role


# ──────────────────────────────────────────────
# Org Extractor
# ──────────────────────────────────────────────
async def get_current_org(
    current_user: User = Depends(get_current_user),
) -> uuid.UUID:
    """Extract the org_id from the current user. Raises if user has no org."""
    if not current_user.org_id:
        raise PermissionDeniedError("User is not part of any organization")
    return current_user.org_id
