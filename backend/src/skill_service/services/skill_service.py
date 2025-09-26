from typing import List, Optional

from src.repository import get_repository
from src.skill_service.models.skills import SkillModel
from src.skill_service.schemas.skills import Skill, SkillCreate, SkillUpdate


class SkillService:
    """Service for managing skills"""

    def __init__(self):
        self._repository = get_repository(SkillModel, Skill, "id")

    async def create_skill(self, skill_data: SkillCreate) -> Skill:
        """Create a new skill"""
        skill = Skill(
            id=0,  # Will be set by database
            name=skill_data.name,
            description=skill_data.description,
            category=skill_data.category,
        )
        skill_id = await self._repository.create(skill)
        return await self.get_skill_by_id(skill_id)

    async def get_all_skills(self, category: Optional[str] = None) -> List[Skill]:
        """Get all skills, optionally filtered by category"""
        skills = await self._repository.get_all()
        if category:
            return [skill for skill in skills if skill.category == category]
        return skills

    async def get_skill_by_id(self, skill_id: int) -> Optional[Skill]:
        """Get skill by ID"""
        return await self._repository.get_by_id(skill_id)

    async def update_skill(self, skill_id: int, skill_data: SkillUpdate) -> Skill:
        """Update skill by ID"""
        values = {k: v for k, v in skill_data.model_dump().items() if v is not None}
        return await self._repository.update(skill_id, values)

    async def delete_skill(self, skill_id: int) -> None:
        """Delete skill by ID"""
        await self._repository.delete(skill_id)
