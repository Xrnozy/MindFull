"""
Security Utilities.

JWT verification, API key management, HMAC request signing,
device fingerprinting, and password hashing.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("mindfull.security")

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# ──────────────────────────────────────────────
# JWT Verification (Supabase)
# ──────────────────────────────────────────────
def verify_supabase_jwt(token: str) -> dict:
    """
    Verifies the Supabase JWT or a local dev JWT.
    """
    try:
        # Try local JWT first for our simple frontend tests
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.InvalidTokenError:
            pass # Fall back to Supabase logic
            
        secret = settings.SUPABASE_JWT_SECRET or settings.SUPABASE_KEY
        if not secret:
            # Mock successful validation for local testing when no key is set
            logger.warning("jwt_mock_mode", detail="No Supabase secret configured — using mock JWT payload")
            return {
                "sub": "00000000-0000-0000-0000-000000000001",
                "email": "dev@mindfull.local",
                "role": "authenticated",
                "app_metadata": {},
                "user_metadata": {},
            }

        payload = jwt.decode(
            token,
            secret,
            algorithms=[settings.JWT_ALGORITHM],
            audience="authenticated",
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ──────────────────────────────────────────────
# Internal JWT (for refresh tokens, API-to-API)
# ──────────────────────────────────────────────
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a short-lived JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Create a long-lived refresh token with rotation support."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": user_id,
        "type": "refresh",
        "jti": str(uuid.uuid4()),  # unique token ID for rotation tracking
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_refresh_token(token: str) -> dict:
    """Verify and decode a refresh token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


# ──────────────────────────────────────────────
# API Key Management
# ──────────────────────────────────────────────
def generate_api_key() -> tuple[str, str, str]:
    """
    Generate a new API key.

    Returns:
        tuple: (full_key, key_prefix_display, key_hash)
            - full_key: The full API key (shown ONCE to the user) e.g. mf_live_abc123...
            - key_prefix_display: First 12 chars for display  e.g. mf_live_abc1...
            - key_hash: SHA-256 hash stored in the database
    """
    raw = secrets.token_urlsafe(32)
    full_key = f"{settings.API_KEY_PREFIX}{raw}"
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()
    prefix_display = full_key[:16] + "..."
    return full_key, prefix_display, key_hash


def verify_api_key(provided_key: str, stored_hash: str) -> bool:
    """Verify an API key against its stored SHA-256 hash."""
    computed_hash = hashlib.sha256(provided_key.encode()).hexdigest()
    return hmac.compare_digest(computed_hash, stored_hash)


def hash_api_key(key: str) -> str:
    """Hash an API key with SHA-256 for storage."""
    return hashlib.sha256(key.encode()).hexdigest()


# ──────────────────────────────────────────────
# HMAC Request Signing (Browser Extension)
# ──────────────────────────────────────────────
def verify_request_signature(
    payload: bytes,
    signature: str,
    device_secret: str,
    timestamp: str,
    max_age_seconds: int = 300,
) -> bool:
    """
    Verify an HMAC-SHA256 request signature from the browser extension.

    The extension signs: HMAC(device_secret, timestamp + "." + body)
    This prevents replay attacks and request tampering.
    """
    # Check timestamp freshness (prevent replay)
    try:
        ts = int(timestamp)
        now = int(datetime.now(timezone.utc).timestamp())
        if abs(now - ts) > max_age_seconds:
            logger.warning("request_signature_expired", timestamp=timestamp)
            return False
    except (ValueError, TypeError):
        return False

    # Compute expected signature
    message = f"{timestamp}.".encode() + payload
    expected = hmac.new(
        device_secret.encode(),
        message,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


# ──────────────────────────────────────────────
# Device Fingerprint
# ──────────────────────────────────────────────
def generate_device_secret() -> str:
    """Generate a unique device secret for HMAC request signing."""
    return secrets.token_urlsafe(48)


def hash_fingerprint(fingerprint: str) -> str:
    """Hash a device fingerprint for storage comparison."""
    return hashlib.sha256(fingerprint.encode()).hexdigest()
