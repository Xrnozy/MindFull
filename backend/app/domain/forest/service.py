"""Forest Domain — Service."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.forest.models import Forest, Tree, GreenPointLog
from app.domain.forest.repository import ForestRepository, TreeRepository, GreenPointLogRepository, CommunityGoalRepository, CampaignRepository
from app.domain.forest.schemas import PlantTreeRequest


class ForestService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.forest_repo = ForestRepository(db)
        self.tree_repo = TreeRepository(db)
        self.gp_repo = GreenPointLogRepository(db)
        self.goal_repo = CommunityGoalRepository(db)
        self.campaign_repo = CampaignRepository(db)

    async def get_or_create_forest(self, user_id: UUID) -> Forest:
        forest = await self.forest_repo.get_by_user(user_id)
        if not forest:
            forest = Forest(user_id=user_id)
            forest = await self.forest_repo.create(forest)
        return forest

    async def plant_tree(self, user_id: UUID, data: PlantTreeRequest) -> Tree:
        forest = await self.get_or_create_forest(user_id)
        tree = Tree(forest_id=forest.id, species=data.species)
        tree = await self.tree_repo.create(tree)
        await self.forest_repo.update(forest, {"total_trees": forest.total_trees + 1})
        return tree

    async def get_trees(self, user_id: UUID):
        forest = await self.get_or_create_forest(user_id)
        return await self.tree_repo.get_by_forest(forest.id)

    async def award_green_points(self, user_id: UUID, amount: int, source: str, reference_id: UUID | None = None):
        forest = await self.get_or_create_forest(user_id)
        log = GreenPointLog(user_id=user_id, amount=amount, source=source, reference_id=reference_id)
        await self.gp_repo.create(log)
        await self.forest_repo.update(forest, {"green_points": forest.green_points + amount})
        return forest

    async def get_community_goals(self):
        return await self.goal_repo.get_active()

    async def get_campaigns(self):
        return await self.campaign_repo.get_active()
