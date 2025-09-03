from pydantic import BaseModel

from src.domain.entities.user import User
from src.domain.entities.order import Order


class LoginResponse(BaseModel):
    user: User
    access_token: str


class OrderResponse(BaseModel):
    order: Order


class OrderCreateRequest(BaseModel):
    title: str
    description: str
    author_id: str
    status: str = "moderation"
    primary_responses: int = 0
    skills: list[str] = []


class OrderUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    primary_responses: int | None = None
    skills: list[str] | None = None
