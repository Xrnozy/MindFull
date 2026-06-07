"""
API v1 Router Aggregator.

Mounts all domain routers under /api/v1/<domain>.
"""
from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users.router import router as users_router
from app.api.v1.organizations.router import router as orgs_router
from app.api.v1.sustainability.router import router as sustainability_router
from app.api.v1.prompt_coach.router import router as prompt_coach_router
from app.api.v1.think_ahead.router import router as think_ahead_router
from app.api.v1.wellness.router import router as wellness_router
from app.api.v1.gamification.router import router as gamification_router
from app.api.v1.forest.router import router as forest_router
from app.api.v1.greenmap.router import router as greenmap_router
from app.api.v1.education.router import router as education_router
from app.api.v1.reporting.router import router as reporting_router
from app.api.v1.analytics.router import router as analytics_router
from app.api.v1.health.router import router as health_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_v1_router.include_router(users_router, prefix="/users", tags=["Users"])
api_v1_router.include_router(orgs_router, prefix="/organizations", tags=["Organizations"])
api_v1_router.include_router(sustainability_router, prefix="/sustainability", tags=["Sustainability"])
api_v1_router.include_router(prompt_coach_router, prefix="/prompt-coach", tags=["Prompt Coach"])
api_v1_router.include_router(think_ahead_router, prefix="/think-ahead", tags=["Think-A-Head"])
api_v1_router.include_router(wellness_router, prefix="/wellness", tags=["Wellness"])
api_v1_router.include_router(gamification_router, prefix="/gamification", tags=["Gamification"])
api_v1_router.include_router(forest_router, prefix="/forest", tags=["Forest"])
api_v1_router.include_router(greenmap_router, prefix="/greenmap", tags=["GreenMap"])
api_v1_router.include_router(education_router, prefix="/education", tags=["Education"])
api_v1_router.include_router(reporting_router, prefix="/reporting", tags=["Reporting"])
api_v1_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
api_v1_router.include_router(health_router, prefix="/health", tags=["Health"])
