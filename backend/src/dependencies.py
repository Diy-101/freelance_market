from src.analytics_service.services.analytics_service import AnalyticsService
from src.notification_service.services.notification_service import NotificationService
from src.order_service.services.order_service import OrderService
from src.proposal_service.services.proposal_service import ProposalService
from src.search_service.services.search_service import SearchService
from src.skill_service.services.skill_service import SkillService
from src.user_service.services.main_service import MainUserService


def get_order_service() -> OrderService:
    return OrderService()


def get_main_service() -> MainUserService:
    return MainUserService()


def get_skill_service() -> SkillService:
    return SkillService()


def get_proposal_service() -> ProposalService:
    return ProposalService()


def get_notification_service() -> NotificationService:
    return NotificationService()


def get_search_service() -> SearchService:
    return SearchService()


def get_analytics_service() -> AnalyticsService:
    return AnalyticsService()
