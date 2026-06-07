import jwt
import asyncio
from datetime import datetime, timedelta, timezone
import uuid
import sys
from app.core.config import settings
from app.db.session import async_session_maker
from app.domain.users.models import User

# Import all models to ensure they are registered in SQLAlchemy mapper
from app.domain.organizations.models import Organization, Membership
from app.domain.forest.models import Forest
from app.domain.gamification.models import XPLog, Achievement, Streak

from sqlalchemy import select

async def generate_token_for_email(email: str):
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            print(f"Error: User with email {email} not found.")
            return None
        
        user_id = str(user.id)

    secret = settings.SUPABASE_JWT_SECRET or settings.SUPABASE_KEY
    if not secret:
        print("Error: SUPABASE_JWT_SECRET not set in .env")
        return None
    
    payload = {
        "sub": user_id,
        "email": email,
        "role": "authenticated",
        "aud": "authenticated",
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }
    
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_token.py <email>")
        print("Example: python scripts/generate_token.py standard.user@example.com")
    else:
        email = sys.argv[1]
        token = asyncio.run(generate_token_for_email(email))
        if token:
            print(f"\nToken for {email}:")
            print(f"{token}")
            print("\nCopy the token above and paste it into the 'Value' field in the Swagger 'Authorize' dialog.")
