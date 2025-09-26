from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.notification_service.schemas.notifications import Notification, NotificationCreate
from src.notification_service.services.notification_service import NotificationService
from src.dependencies import get_notification_service

notification_router = APIRouter(
    prefix="/api/notifications",
    tags=["notifications"],
)


@notification_router.post("/", response_model=Notification)
async def create_notification(
    notification_data: NotificationCreate,
    notification_service: NotificationService = Depends(get_notification_service),
) -> Notification:
    """Create a new notification"""
    try:
        return await notification_service.create_notification(notification_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create notification: {e}",
        )


@notification_router.get("/", response_model=List[Notification])
async def get_user_notifications(
    user_id: int,
    unread_only: bool = False,
    notification_service: NotificationService = Depends(get_notification_service),
) -> List[Notification]:
    """Get notifications for a user"""
    return await notification_service.get_user_notifications(user_id, unread_only)


@notification_router.get("/{notification_id}", response_model=Notification)
async def get_notification(
    notification_id: int,
    notification_service: NotificationService = Depends(get_notification_service),
) -> Notification:
    """Get notification by ID"""
    notification = await notification_service.get_notification_by_id(notification_id)
    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    return notification


@notification_router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    notification_service: NotificationService = Depends(get_notification_service),
) -> dict:
    """Mark notification as read"""
    try:
        await notification_service.mark_as_read(notification_id)
        return {"message": "Notification marked as read"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to mark notification as read: {e}",
        )


@notification_router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    notification_service: NotificationService = Depends(get_notification_service),
) -> dict:
    """Delete notification"""
    try:
        await notification_service.delete_notification(notification_id)
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete notification: {e}",
        )
