from typing import Any, Callable

from src.domain.entities.user import User
from src.domain.interfaces import (
    AbstractRepository,
    JWTInterface,
    UserServiceInterface,
)
from src.domain.models.users import UserModel
from src.settings import get_settings
from src.utils import logger

cfg = get_settings()


class UserService(UserServiceInterface):
    """
    Объединенный сервис для управления пользователями и аутентификации
    Включает CRUD операции с пользователями + функции аутентификации
    """

    def __init__(
        self,
        repository: AbstractRepository[UserModel, User],
        jwt_adapter: JWTInterface,
    ) -> None:
        self._repository = repository
        self._jwt_adapter = jwt_adapter

    # ============= CRUD =============
    async def create_user(self, user: dict[str, Any]) -> User:
        new_user_dict = await self._repository.create(user)
        new_user = User(**new_user_dict)
        return new_user

    async def get_user_by_tg_id(self, user_id: int) -> User | None:
        user_dict = await self._repository.get_by_id(user_id)

        if user_dict is None:
            return None

        user = User(**user_dict)
        return user

    async def get_all_users(self) -> list[User]:
        users_dict = await self._repository.get_all()

        users = []
        for user_dict in users_dict:
            user = User(**user_dict)
            users.append(user)

        return users

    async def update_user_by_tg_id(
        self, user_id: int, new_data: dict[str, Any]
    ) -> User:
        current_user_dict = await self._repository.get_by_id(user_id)
        if current_user_dict is None:
            raise ValueError(f"The user with {user_id} id doesn't exist")

        try:
            new_data_dict = new_data  # type: ignore
            fields_to_update = {}
            for i, v in new_data_dict.items():
                if i != "uuid" and new_data_dict[i] != current_user_dict[i]:
                    fields_to_update[i] = v
        except Exception as e:
            raise ValueError(f"Can't map the fields: {e}")

        if cfg.debug:
            logger.debug(f"fields to update: {fields_to_update}")

        if fields_to_update:
            updated_user_dict = await self._repository.update(user_id, fields_to_update)
            return User(**updated_user_dict)
        return User(**current_user_dict)

    async def delete_user_by_tg_id(self, user_id: int) -> User:
        try:
            deleted_user_dict = await self._repository.delete(user_id)
        except Exception as e:
            raise ValueError(
                f"Can't update the user with the following {user_id} id: {e}"
            )
        return User(**deleted_user_dict)

    # ============= Аутентификация и авторизация =============
    def create_token(self, user_id: int) -> str:
        """Create an access jwt_token

        Args:
            user_id (int): User id required to create a token

        Returns:
            str: token string
        """
        token = self._jwt_adapter.create_access_token(str(user_id))
        return token

    def get_token_dependency(self) -> Callable:
        """Returning a dependency function which FastAPI uses in Depends

        Returns:
            Callable: a dependency function to check a token in protected routers
        """
        return self._jwt_adapter.token_required()
