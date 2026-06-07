"""Auth Router — Login, refresh tokens, API keys, device registration."""
from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.domain.users.models import User
from app.domain.reporting.service import ReportingService
from app.domain.reporting.schemas import APIKeyCreateRequest, APIKeyCreatedResponse, APIKeyResponse
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token

router = APIRouter()


from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from app.core.security import verify_password, get_password_hash

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(
    data: UserRegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user (Local implementation for testing)."""
    # Check if user exists
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalars().first():
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=get_password_hash(data.password),
        role="user"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Generate tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(str(user.id))
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer",
        "user": {"id": str(user.id), "email": user.email}
    }


@router.post("/login")
async def login(
    data: UserLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Local login implementation."""
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalars().first()
    
    from fastapi import HTTPException
    if not user or not user.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(str(user.id))
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer",
        "user": {"id": str(user.id), "email": user.email}
    }



@router.post("/api-keys", response_model=APIKeyCreatedResponse)
async def create_api_key(
    data: APIKeyCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a new API key for the current user."""
    service = ReportingService(db)
    api_key, full_key = await service.create_api_key(current_user.id, current_user.org_id, data)
    return APIKeyCreatedResponse(
        id=api_key.id, key_prefix=api_key.key_prefix, name=api_key.name,
        scopes=api_key.scopes, is_active=api_key.is_active,
        last_used_at=api_key.last_used_at, expires_at=api_key.expires_at,
        created_at=api_key.created_at, full_key=full_key,
    )


@router.delete("/api-keys/{key_id}")
async def revoke_api_key(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Revoke an API key."""
    from uuid import UUID
    service = ReportingService(db)
    await service.revoke_api_key(UUID(key_id), current_user.id)
    return {"status": "revoked"}


@router.post("/device-register")
async def register_device(current_user: User = Depends(get_current_user)):
    """Register a device fingerprint and receive a device secret for HMAC signing."""
    from app.core.security import generate_device_secret
    secret = generate_device_secret()
    return {"device_secret": secret, "message": "Store this secret securely on the device."}
