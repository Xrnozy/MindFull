import jwt
from datetime import datetime, timedelta, timezone
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str = "your-256-bit-secret-key-change-this-in-production-mindfull-dev"
    JWT_ALGORITHM: str = "HS256"
    SUPABASE_JWT_SECRET: str = "your-supabase-jwt-secret"
    SUPABASE_KEY: str = "your-supabase-anon-key"
    ENVIRONMENT: str = "development"

settings = Settings()

def verify_supabase_jwt(token: str) -> dict:
    try:
        # Try local JWT first - with the fix: options={"verify_aud": False}
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_aud": False}
            )
        except jwt.InvalidTokenError as e:
            print(f"Local decode failed: {e}")
            pass
            
        secret = settings.SUPABASE_JWT_SECRET or settings.SUPABASE_KEY
        return jwt.decode(
            token,
            secret,
            algorithms=[settings.JWT_ALGORITHM],
            audience="authenticated",
        )
    except Exception as e:
        print(f"Fallback decode failed: {e}")
        raise

# Test 1: Token with audience signed with local secret
payload = {"sub": "test-user", "aud": "authenticated", "exp": datetime.now(timezone.utc) + timedelta(hours=1)}
token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

try:
    decoded = verify_supabase_jwt(token)
    print(f"SUCCESS: Decoded token with audience using local secret: {decoded['sub']}")
except Exception as e:
    print(f"FAILED: {e}")

# Test 2: Token without audience signed with local secret
payload2 = {"sub": "test-user-no-aud", "exp": datetime.now(timezone.utc) + timedelta(hours=1)}
token2 = jwt.encode(payload2, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

try:
    decoded2 = verify_supabase_jwt(token2)
    print(f"SUCCESS: Decoded token without audience using local secret: {decoded2['sub']}")
except Exception as e:
    print(f"FAILED: {e}")
