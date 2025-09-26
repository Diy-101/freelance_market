from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel


class OrderStatus(str, Enum):
    MODERATION = "moderation"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderBase(BaseModel):
    title: str
    description: str
    author_id: str
    status: OrderStatus
    primary_responses: int
    skills: List[str] = []


class OrderCreateRequest(BaseModel):
    title: str
    description: str
    author_id: str
    status: Optional[str] = "moderation"
    primary_responses: int = 0
    skills: List[str] = []


class OrderUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    primary_responses: Optional[int] = None
    skills: Optional[List[str]] = None


class Order(OrderBase):
    uuid: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    order: Order
