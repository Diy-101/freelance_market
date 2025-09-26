from src.analytics_service.schemas.analytics import (
    OrderStats,
    PlatformStats,
    RevenueStats,
    SkillStats,
    TimeRange,
    UserStats,
)
from src.order_service.models.orders import OrderModel
from src.order_service.schemas.orders import Order
from src.proposal_service.models.proposals import ProposalModel
from src.proposal_service.schemas.proposals import Proposal
from src.repository import get_repository
from src.skill_service.models.skills import SkillModel
from src.skill_service.schemas.skills import Skill
from src.user_service.models.users import UserModel
from src.user_service.schemas.users import User


class AnalyticsService:
    """Service for analytics and statistics"""

    def __init__(self):
        self._user_repository = get_repository(UserModel, User, "tg_id")
        self._order_repository = get_repository(OrderModel, Order, "uuid")
        self._skill_repository = get_repository(SkillModel, Skill, "id")
        self._proposal_repository = get_repository(ProposalModel, Proposal, "id")

    async def get_user_stats(self, user_id: int, time_range: TimeRange) -> UserStats:
        """Get user statistics"""
        orders = await self._order_repository.get_all()
        proposals = await self._proposal_repository.get_all()

        user_orders = [o for o in orders if o.author_id == str(user_id)]
        user_proposals = [p for p in proposals if p.freelancer_id == user_id]

        return UserStats(
            total_orders=len(user_orders),
            completed_orders=len([o for o in user_orders if o.status == "completed"]),
            active_orders=len([o for o in user_orders if o.status == "active"]),
            total_earnings=sum(
                p.price for p in user_proposals if p.status == "accepted"
            ),
            average_rating=0.0,  # TODO: Implement rating system
            total_proposals=len(user_proposals),
            accepted_proposals=len(
                [p for p in user_proposals if p.status == "accepted"]
            ),
        )

    async def get_order_stats(self, time_range: TimeRange) -> OrderStats:
        """Get order statistics"""
        orders = await self._order_repository.get_all()

        status_counts = {}
        for order in orders:
            status_counts[order.status] = status_counts.get(order.status, 0) + 1

        return OrderStats(
            total_orders=len(orders),
            active_orders=status_counts.get("active", 0),
            completed_orders=status_counts.get("completed", 0),
            cancelled_orders=status_counts.get("cancelled", 0),
            average_order_value=sum(o.primary_responses for o in orders) // len(orders)
            if orders
            else 0,
            orders_by_status=status_counts,
            orders_by_category={},  # TODO: Implement category stats
        )

    async def get_platform_stats(self, time_range: TimeRange) -> PlatformStats:
        """Get platform statistics"""
        users = await self._user_repository.get_all()
        orders = await self._order_repository.get_all()
        proposals = await self._proposal_repository.get_all()

        return PlatformStats(
            total_users=len(users),
            active_users=len(users),  # TODO: Implement active user logic
            total_orders=len(orders),
            total_proposals=len(proposals),
            platform_revenue=0,  # TODO: Implement revenue calculation
            average_order_value=sum(o.primary_responses for o in orders) // len(orders)
            if orders
            else 0,
        )

    async def get_revenue_stats(self, time_range: TimeRange) -> RevenueStats:
        """Get revenue statistics"""
        proposals = await self._proposal_repository.get_all()
        accepted_proposals = [p for p in proposals if p.status == "accepted"]

        total_revenue = sum(p.price for p in accepted_proposals)
        platform_commission = int(total_revenue * 0.1)  # 10% commission
        freelancer_earnings = total_revenue - platform_commission

        return RevenueStats(
            total_revenue=total_revenue,
            platform_commission=platform_commission,
            freelancer_earnings=freelancer_earnings,
            revenue_by_month=[],  # TODO: Implement monthly breakdown
            top_earning_skills=[],  # TODO: Implement skill revenue stats
        )

    async def get_skill_stats(self, time_range: TimeRange) -> SkillStats:
        """Get skill statistics"""
        skills = await self._skill_repository.get_all()
        orders = await self._order_repository.get_all()

        # Count skill usage in orders
        skill_usage = {}
        for order in orders:
            for skill in order.skills:
                skill_usage[skill] = skill_usage.get(skill, 0) + 1

        most_popular = sorted(skill_usage.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]

        return SkillStats(
            most_popular_skills=[
                {"skill": skill, "count": count} for skill, count in most_popular
            ],
            highest_paying_skills=[],  # TODO: Implement skill pricing
            skill_demand_trends=[],  # TODO: Implement trend analysis
            skills_by_category={},  # TODO: Implement category breakdown
        )
