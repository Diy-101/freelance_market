from aiogram.utils.web_app import safe_parse_webapp_init_data
from fastapi import HTTPException, status

from src.dependencies import get_repository
from src.settings import get_settings
from src.user_service.models.users import UserModel
from src.user_service.schemas.users import LoginResponse, User
from src.user_service.services.pyjwt_service import PyJWTService
from src.utils.logger import logger

cfg = get_settings()


class MainUserService:
    """
    The main service to work with users
    """

    def __init__(
        self,
    ) -> None:
        self._repository = get_repository(UserModel, User, "tg_id")
        self._jwt_service = PyJWTService()

    # ============= CRUD =============
    async def create_user(self, user: User) -> User:
        await self._repository.create(user)
        created = await self._repository.get_by_id(user.tg_id)
        if created is None:
            raise ValueError("User not found after creation")
        return created

    async def get_user(self, tg_id: int) -> User | None:
        return await self._repository.get_by_id(tg_id)

    async def get_all_users(self) -> list[User]:
        return await self._repository.get_all()

    async def update_user(self, tg_id: int, user: User) -> User:
        current_user = await self.get_user(tg_id)
        if current_user is None:
            raise ValueError(f"User with tg_id {tg_id} not found")

        values = {
            k: v for k, v in user.model_dump().items() if v is not None and k != "tg_id"
        }

        # Check for changes
        changes = {}
        for key, new_value in values.items():
            current_value = getattr(current_user, key)
            if current_value != new_value:
                changes[key] = {"old": current_value, "new": new_value}

        if not changes:
            logger.info(f"No changes needed for user {tg_id}")
            return current_user

        logger.info(f"Updating user {tg_id} with changes: {changes}")
        return await self._repository.update(tg_id, values)

    async def delete_user(self, tg_id: int) -> User:
        return await self._repository.delete(tg_id)

    # ========== Auth ===========
    def check_init_data(self, init_data: str) -> User:
        try:
            web_app_init_data = safe_parse_webapp_init_data(
                init_data=init_data, token=cfg.bot_token
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Can't parse initData: {e}",
            )
        web_app_user = web_app_init_data.user
        if web_app_user is None:
            raise ValueError("User is not in InitData")
        web_app_user_dict = web_app_user.model_dump()
        logger.debug(web_app_user_dict)
        web_app_user_dict["tg_id"] = web_app_user_dict["id"]
        del web_app_user_dict["id"]

        return User(**web_app_user_dict)

    def create_token(self, tg_id: str) -> str:
        return self._jwt_service.create_access_token(tg_id)

    def token_required_dep(self):
        return self._jwt_service.token_required()

    async def login_user(self, init_data: str):
        try:
            user = self.check_init_data(init_data=init_data)
            tg_id = user.tg_id
        except Exception as e:
            logger.debug(f"Error during checking init_data from frontend: {e}")
            raise

        try:
            if await self.get_user(tg_id=tg_id):
                user = await self.update_user(tg_id=tg_id, user=user)
            else:
                user = await self.create_user(user=user)
        except Exception as e:
            logger.debug(f"Database error: {e}")
            raise

        try:
            access_token = self.create_token(str(user.tg_id))
        except Exception as e:
            logger.debug(f"Can't make access_token: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Can't make access_token: {e}",
            )

        return LoginResponse(user=user, access_token=access_token)
