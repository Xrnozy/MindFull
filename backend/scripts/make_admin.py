import asyncio
from app.db.session import async_session_maker
from app.domain.users.models import User
from sqlalchemy import select

# Ensure all models are loaded for SQLAlchemy
from app.domain.organizations.models import Organization, Membership
from app.domain.forest.models import Forest
from app.domain.gamification.models import XPLog, Achievement, Streak

async def make_admin():
    async with async_session_maker() as session:
        # Standard user
        result = await session.execute(select(User).where(User.email == 'standard.user@example.com'))
        u1 = result.scalars().first()
        if u1:
            u1.role = 'super_admin'
            print("Successfully updated standard.user@example.com to super_admin")

        # dom@gmail.com
        result = await session.execute(select(User).where(User.email == 'dom@gmail.com'))
        u2 = result.scalars().first()
        if u2:
            u2.role = 'super_admin'
            print("Successfully updated dom@gmail.com to super_admin")
            
        await session.commit()

if __name__ == "__main__":
    asyncio.run(make_admin())
