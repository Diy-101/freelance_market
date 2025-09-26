from datetime import datetime
from typing import List, Optional

from src.notification_service.models.notifications import NotificationModel
from src.notification_service.schemas.notifications import (
    Notification,
    NotificationCreate,
)
from src.repository import get_repository


class NotificationService:
    """Service for managing notifications"""

    def __init__(self):
        self._repository = get_repository(NotificationModel, Notification, "id")

    async def create_notification(
        self, notification_data: NotificationCreate
    ) -> Notification:
        """Create a new notification"""
        notification = Notification(
            id=0,  # Will be set by database
            user_id=notification_data.user_id,
            title=notification_data.title,
            message=notification_data.message,
            type=notification_data.type,
            is_read=False,
            created_at=datetime.now(),
        )
        notification_id = await self._repository.create(notification)
        return await self.get_notification_by_id(notification_id)

    async def get_user_notifications(
        self, user_id: int, unread_only: bool = False
    ) -> List[Notification]:
        """Get notifications for a user"""
        notifications = await self._repository.get_all()
        user_notifications = [n for n in notifications if n.user_id == user_id]
        if unread_only:
            user_notifications = [n for n in user_notifications if not n.is_read]
        return user_notifications

    async def get_notification_by_id(
        self, notification_id: int
    ) -> Optional[Notification]:
        """Get notification by ID"""
        return await self._repository.get_by_id(notification_id)

    async def mark_as_read(self, notification_id: int) -> None:
        """Mark notification as read"""
        await self._repository.update(notification_id, {"is_read": True})

    async def delete_notification(self, notification_id: int) -> None:
        """Delete notification"""
        await self._repository.delete(notification_id)
