from datetime import date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class TimeRange(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class UserStats(BaseModel):
    total_orders: int
    completed_orders: int
    active_orders: int
    total_earnings: int  # in kopecks
    average_rating: float
    total_proposals: int
    accepted_proposals: int


class OrderStats(BaseModel):
    total_orders: int
    active_orders: int
    completed_orders: int
    cancelled_orders: int
    average_order_value: int  # in kopecks
    orders_by_status: Dict[str, int]
    orders_by_category: Dict[str, int]


class PlatformStats(BaseModel):
    total_users: int
    active_users: int
    total_orders: int
    total_proposals: int
    platform_revenue: int  # in kopecks
    average_order_value: int  # in kopecks


class RevenueStats(BaseModel):
    total_revenue: int  # in kopecks
    platform_commission: int  # in kopecks
    freelancer_earnings: int  # in kopecks
    revenue_by_month: List[Dict[str, Any]]
    top_earning_skills: List[Dict[str, Any]]


class SkillStats(BaseModel):
    most_popular_skills: List[Dict[str, Any]]
    highest_paying_skills: List[Dict[str, Any]]
    skill_demand_trends: List[Dict[str, Any]]
    skills_by_category: Dict[str, int]
