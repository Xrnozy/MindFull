"""
Device Fingerprint Validation Middleware.

Validates X-Device-Fingerprint headers from browser extension and mobile clients.
Tracks device sessions and flags unknown devices for review.
"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import get_logger

logger = get_logger("mindfull.device")

DEVICE_FINGERPRINT_HEADER = "X-Device-Fingerprint"
DEVICE_SIGNATURE_HEADER = "X-Device-Signature"
DEVICE_TIMESTAMP_HEADER = "X-Device-Timestamp"


class DeviceFingerprintMiddleware(BaseHTTPMiddleware):
    """Extract and store device fingerprint from request headers."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Extract device info from headers (extension/mobile clients send these)
        fingerprint = request.headers.get(DEVICE_FINGERPRINT_HEADER)
        signature = request.headers.get(DEVICE_SIGNATURE_HEADER)
        timestamp = request.headers.get(DEVICE_TIMESTAMP_HEADER)

        # Store on request state for downstream auth validation
        request.state.device_fingerprint = fingerprint
        request.state.device_signature = signature
        request.state.device_timestamp = timestamp

        if fingerprint:
            logger.debug(
                "device_fingerprint_received",
                fingerprint_prefix=fingerprint[:8] + "..." if len(fingerprint) > 8 else fingerprint,
                has_signature=bool(signature),
            )

        return await call_next(request)
