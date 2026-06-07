import asyncio
import uuid
from sqlalchemy import select
from app.db.session import async_session_maker, engine
from app.domain.users.models import User
from app.domain.organizations.models import Organization, Membership

# Import all models to ensure they are registered in SQLAlchemy mapper
from app.domain.forest.models import Forest
from app.domain.gamification.models import XPLog, Achievement, Streak

async def seed_users():
    async with async_session_maker() as session:
        # 1. Create Organizations
        orgs_to_create = [
            Organization(name="Education Institution", slug="edu-inst", tier="education", is_educational=True),
            Organization(name="Premium Personal", slug="premium-personal", tier="pro"),
            Organization(name="Standard Org", slug="standard-org", tier="free"),
            Organization(name="Enterprise Corp", slug="enterprise-corp", tier="enterprise"),
        ]
        
        for org in orgs_to_create:
            q = select(Organization).where(Organization.slug == org.slug)
            existing = (await session.execute(q)).scalars().first()
            if not existing:
                session.add(org)
            else:
                # Use existing org for linking
                org.id = existing.id
        
        await session.commit()
        
        # Reload orgs to get IDs if they already existed
        org_map = {}
        for org in orgs_to_create:
            q = select(Organization).where(Organization.slug == org.slug)
            db_org = (await session.execute(q)).scalars().first()
            org_map[org.slug] = db_org

        # 2. Create Users
        users_data = [
            {"email": "standard.user@example.com", "role": "user", "org_slug": None, "label": "User"},
            {"email": "student@example.com", "role": "user", "org_slug": "edu-inst", "label": "Student"},
            {"email": "premium.user@example.com", "role": "user", "org_slug": "premium-personal", "label": "Premium User"},
            {"email": "org.user@example.com", "role": "user", "org_slug": "standard-org", "label": "Org User"},
            {"email": "premium.org.user@example.com", "role": "org_admin", "org_slug": "enterprise-corp", "label": "Premium Org User"},
        ]

        for u_data in users_data:
            q = select(User).where(User.email == u_data["email"])
            existing_user = (await session.execute(q)).scalars().first()
            
            if not existing_user:
                new_user = User(
                    email=u_data["email"],
                    role=u_data["role"],
                    org_id=org_map[u_data["org_slug"]].id if u_data["org_slug"] else None,
                    full_name=u_data["label"]
                )
                session.add(new_user)
                await session.flush() # Get ID
                
                # Add Membership if it's an org user
                if u_data["org_slug"]:
                    membership = Membership(
                        user_id=new_user.id,
                        org_id=org_map[u_data["org_slug"]].id,
                        role="org_admin" if u_data["role"] == "org_admin" else "member"
                    )
                    session.add(membership)
                
                print(f"Created {u_data['label']}: {u_data['email']}")
            else:
                print(f"User {u_data['email']} already exists")

        await session.commit()
    print("Seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_users())
