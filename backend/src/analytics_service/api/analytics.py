from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from datetime import datetime, date

from src.analytics_service.schemas.analytics import (
    UserStats, OrderStats, PlatformStats, 
    RevenueStats, SkillStats, TimeRange
)
from src.analytics_service.services.analytics_service import AnalyticsService
from src.dependencies import get_analytics_service

analytics_router = APIRouter(
    prefix="/api/analytics",
    tags=["analytics"],
)


@analytics_router.get("/user/{user_id}/stats", response_model=UserStats)
async def get_user_stats(
    user_id: int,
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> UserStats:
    """Get user statistics"""
    try:
        time_range = TimeRange(start_date=start_date, end_date=end_date)
        return await analytics_service.get_user_stats(user_id, time_range)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get user stats: {e}",
        )


@analytics_router.get("/orders/stats", response_model=OrderStats)
async def get_order_stats(
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> OrderStats:
    """Get order statistics"""
    try:
        time_range = TimeRange(start_date=start_date, end_date=end_date)
        return await analytics_service.get_order_stats(time_range)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get order stats: {e}",
        )


@analytics_router.get("/platform/stats", response_model=PlatformStats)
async def get_platform_stats(
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> PlatformStats:
    """Get platform statistics"""
    try:
        time_range = TimeRange(start_date=start_date, end_date=end_date)
        return await analytics_service.get_platform_stats(time_range)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get platform stats: {e}",
        )


@analytics_router.get("/revenue/stats", response_model=RevenueStats)
async def get_revenue_stats(
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> RevenueStats:
    """Get revenue statistics"""
    try:
        time_range = TimeRange(start_date=start_date, end_date=end_date)
        return await analytics_service.get_revenue_stats(time_range)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get revenue stats: {e}",
        )


@analytics_router.get("/skills/stats", response_model=SkillStats)
async def get_skill_stats(
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> SkillStats:
    """Get skill statistics"""
    try:
        time_range = TimeRange(start_date=start_date, end_date=end_date)
        return await analytics_service.get_skill_stats(time_range)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get skill stats: {e}",
        )
