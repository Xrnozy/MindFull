"""
Mindfull Custom Exception Classes.

Defines application-specific exceptions and registers FastAPI exception
handlers for consistent JSON error responses across all endpoints.
"""
from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


# ──────────────────────────────────────────────
# Base Exception
# ──────────────────────────────────────────────
class MindfullException(Exception):
    """Base exception for all Mindfull application errors."""

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


# ──────────────────────────────────────────────
# Specific Exceptions
# ──────────────────────────────────────────────
class NotFoundError(MindfullException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource", identifier: str = ""):
        detail = f"{resource} not found"
        if identifier:
            detail = f"{resource} '{identifier}' not found"
        super().__init__(
            message=detail,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
        )


class PermissionDeniedError(MindfullException):
    """Raised when a user lacks permission for the requested action."""

    def __init__(self, detail: str = "You do not have permission to perform this action"):
        super().__init__(
            message=detail,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="PERMISSION_DENIED",
        )


class TenantIsolationError(MindfullException):
    """Raised when a cross-tenant data access is attempted."""

    def __init__(self):
        super().__init__(
            message="Access denied: resource belongs to a different organization",
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="TENANT_ISOLATION_VIOLATION",
        )


class RateLimitExceededError(MindfullException):
    """Raised when a client exceeds the configured rate limit."""

    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(
            message=f"Rate limit exceeded. Retry after {retry_after} seconds.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
        )


class DuplicateError(MindfullException):
    """Raised when attempting to create a resource that already exists."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(
            message=f"{resource} already exists",
            status_code=status.HTTP_409_CONFLICT,
            error_code="DUPLICATE",
        )


class InvalidInputError(MindfullException):
    """Raised for business-rule validation failures (not schema-level)."""

    def __init__(self, detail: str = "Invalid input"):
        super().__init__(
            message=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="INVALID_INPUT",
        )


class AuthenticationError(MindfullException):
    """Raised when authentication fails."""

    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            message=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_FAILED",
        )


class UsageLimitExceededError(MindfullException):
    """Raised when a user/org exceeds usage limits (daily prompts, tokens, etc.)."""

    def __init__(self, limit_type: str = "usage"):
        super().__init__(
            message=f"Daily {limit_type} limit exceeded. Please try again tomorrow.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="USAGE_LIMIT_EXCEEDED",
        )


# ──────────────────────────────────────────────
# Exception Handlers Registration
# ──────────────────────────────────────────────
def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on the FastAPI application."""

    @app.exception_handler(MindfullException)
    async def mindfull_exception_handler(request: Request, exc: MindfullException):
        headers = {}
        if isinstance(exc, RateLimitExceededError):
            headers["Retry-After"] = str(exc.retry_after)

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                }
            },
            headers=headers,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # Log the unhandled exception — structlog will capture this
        import logging
        logging.getLogger("mindfull").exception("Unhandled exception", exc_info=exc)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred. Please try again later.",
                }
            },
        )
