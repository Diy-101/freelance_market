from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.skill_service.schemas.skills import Skill, SkillCreate, SkillUpdate
from src.skill_service.services.skill_service import SkillService
from src.dependencies import get_skill_service

skill_router = APIRouter(
    prefix="/api/skills",
    tags=["skills"],
)


@skill_router.post("/", response_model=Skill)
async def create_skill(
    skill_data: SkillCreate,
    skill_service: SkillService = Depends(get_skill_service),
) -> Skill:
    """Create a new skill"""
    try:
        return await skill_service.create_skill(skill_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create skill: {e}",
        )


@skill_router.get("/", response_model=List[Skill])
async def get_all_skills(
    category: str = None,
    skill_service: SkillService = Depends(get_skill_service),
) -> List[Skill]:
    """Get all skills, optionally filtered by category"""
    return await skill_service.get_all_skills(category)


@skill_router.get("/{skill_id}", response_model=Skill)
async def get_skill(
    skill_id: int,
    skill_service: SkillService = Depends(get_skill_service),
) -> Skill:
    """Get skill by ID"""
    skill = await skill_service.get_skill_by_id(skill_id)
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )
    return skill


@skill_router.put("/{skill_id}", response_model=Skill)
async def update_skill(
    skill_id: int,
    skill_data: SkillUpdate,
    skill_service: SkillService = Depends(get_skill_service),
) -> Skill:
    """Update skill by ID"""
    try:
        return await skill_service.update_skill(skill_id, skill_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update skill: {e}",
        )


@skill_router.delete("/{skill_id}")
async def delete_skill(
    skill_id: int,
    skill_service: SkillService = Depends(get_skill_service),
) -> dict:
    """Delete skill by ID"""
    try:
        await skill_service.delete_skill(skill_id)
        return {"message": "Skill deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete skill: {e}",
        )
