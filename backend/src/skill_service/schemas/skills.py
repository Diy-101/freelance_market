from typing import Optional
from pydantic import BaseModel


class SkillBase(BaseModel):
    name: str
    description: str
    category: str


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


class Skill(SkillBase):
    id: int

    class Config:
        from_attributes = True
