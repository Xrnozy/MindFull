import pytest
import jwt
from httpx import AsyncClient

# Secret must match the one we decode with, but since SUPABASE_KEY is empty in test
# security.py mocks the validation. So we just need to ensure the headers are sent.
# However, if we actually want to test the JWT parsing, we need to mock or set SUPABASE_KEY.

@pytest.mark.asyncio
async def test_unauthorized_without_token(async_client: AsyncClient):
    # Missing authorization header
    response = await async_client.get("/api/v1/users/me")
    assert response.status_code == 403 # HTTPBearer returns 403 when no credentials are provided

@pytest.mark.asyncio
async def test_invalid_token(async_client: AsyncClient, monkeypatch):
    from app.core.config import settings
    # Force security to actually validate instead of mocking
    monkeypatch.setattr(settings, "SUPABASE_KEY", "test-secret")
    
    # Sign with a wrong secret
    bad_token = jwt.encode({"sub": "invalid-uuid"}, "wrong-secret", algorithm="HS256")
    
    response = await async_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {bad_token}"}
    )
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]

@pytest.mark.asyncio
async def test_valid_token_creates_user(async_client: AsyncClient, monkeypatch):
    from app.core.config import settings
    monkeypatch.setattr(settings, "SUPABASE_KEY", "test-secret")
    
    valid_uuid = "12345678-1234-5678-1234-567812345678"
    valid_token = jwt.encode(
        {"sub": valid_uuid, "email": "test@mindfull.com"}, 
        "test-secret", 
        algorithm="HS256"
    )
    
    response = await async_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Should auto-provision the user
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@mindfull.com"
    assert data["id"] == valid_uuid
