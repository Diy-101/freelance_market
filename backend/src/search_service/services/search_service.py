from math import ceil
from typing import Dict, List

from src.order_service.models.orders import OrderModel
from src.order_service.schemas.orders import Order
from src.repository import get_repository
from src.search_service.schemas.search import SearchFilters, SearchResponse
from src.user_service.models.users import UserModel
from src.user_service.schemas.users import User


class SearchService:
    """Service for search functionality"""

    def __init__(self):
        self._order_repository = get_repository(OrderModel, Order, "uuid")
        self._user_repository = get_repository(UserModel, User, "tg_id")

    async def search_orders(self, filters: SearchFilters) -> SearchResponse:
        """Search orders with filters"""
        orders = await self._order_repository.get_all()

        # Apply filters
        filtered_orders = []
        for order in orders:
            if filters.query and filters.query.lower() not in order.title.lower():
                continue
            if filters.category and filters.category not in order.skills:
                continue
            if filters.min_price and order.primary_responses < filters.min_price:
                continue
            if filters.max_price and order.primary_responses > filters.max_price:
                continue
            if filters.status and order.status != filters.status:
                continue
            filtered_orders.append(order.model_dump())

        # Pagination
        total = len(filtered_orders)
        start = (filters.page - 1) * filters.limit
        end = start + filters.limit
        items = filtered_orders[start:end]
        total_pages = ceil(total / filters.limit) if total > 0 else 0

        return SearchResponse(
            items=items,
            total=total,
            page=filters.page,
            limit=filters.limit,
            total_pages=total_pages,
        )

    async def search_freelancers(self, filters: SearchFilters) -> SearchResponse:
        """Search freelancers with filters"""
        users = await self._user_repository.get_all()

        # Apply filters
        filtered_users = []
        for user in users:
            if filters.query and filters.query.lower() not in user.first_name.lower():
                continue
            filtered_users.append(user.model_dump())

        # Pagination
        total = len(filtered_users)
        start = (filters.page - 1) * filters.limit
        end = start + filters.limit
        items = filtered_users[start:end]
        total_pages = ceil(total / filters.limit) if total > 0 else 0

        return SearchResponse(
            items=items,
            total=total,
            page=filters.page,
            limit=filters.limit,
            total_pages=total_pages,
        )

    async def get_suggestions(self, query: str, type: str) -> Dict[str, List[str]]:
        """Get search suggestions"""
        suggestions = {"orders": [], "freelancers": [], "skills": [], "categories": []}

        if type in ["all", "orders"]:
            orders = await self._order_repository.get_all()
            suggestions["orders"] = [
                order.title for order in orders if query.lower() in order.title.lower()
            ][:5]

        if type in ["all", "freelancers"]:
            users = await self._user_repository.get_all()
            suggestions["freelancers"] = [
                user.first_name
                for user in users
                if query.lower() in user.first_name.lower()
            ][:5]

        return suggestions
