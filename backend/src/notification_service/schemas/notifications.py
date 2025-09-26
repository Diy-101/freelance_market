from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    type: str  # order, proposal, message, system


class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
