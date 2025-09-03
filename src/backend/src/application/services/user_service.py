from typing import Callable

from src.domain.entities.user import User
from src.domain.interfaces import (
    AbstractRepository,
    JWTInterface,
    UserServiceInterface,
)
from src.domain.models.users import UserModel
from src.infrastructure.mapper import MapperFactory
from src.settings import get_settings

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
        self._mapper = MapperFactory.get_mapper(User, UserModel)

    # ============= CRUD =============
    async def create_user(self, user: User) -> User:
        new_user_dict = await self._repository.create(user)
        new_user = self._mapper.dict_to_entity(new_user_dict)
        return new_user

    async def get_user_by_tg_id(self, user_id: int) -> User | None:
        user_dict = await self._repository.get_by_id(user_id)

        if user_dict is None:
            return None

        user = self._mapper.dict_to_entity(user_dict)
        return user

    async def get_all_users(self) -> list[User]:
        users_dict = await self._repository.get_all()

        users = []
        for user_dict in users_dict:
            user = self._mapper.dict_to_entity(user_dict)
            users.append(user)

        return users

    async def update_user_by_tg_id(self, user_id: int, new_data: User) -> User:
        current_user_dict = await self._repository.get_by_id(user_id)
        if current_user_dict is None:
            raise ValueError(f"The user with {user_id} id doesn't exist")

        try:
            new_data_dict = new_data.to_dict()  # type: ignore
            fields_to_update = {
                f: new_val
                for f, curr_val in current_user_dict.items()
                for _, new_val in new_data_dict.items()
                if curr_val != new_val
            }
        except Exception as e:
            raise ValueError(f"Can't map the fields: {e}")

        if fields_to_update:
            updated_user_dict = await self._repository.update(user_id, fields_to_update)
            return self._mapper.dict_to_entity(updated_user_dict)
        return self._mapper.dict_to_entity(current_user_dict)

    async def delete_user_by_tg_id(self, user_id: int) -> User:
        try:
            deleted_user_dict = await self._repository.delete(user_id)
        except Exception as e:
            raise ValueError(
                f"Can't update the user with the following {user_id} id: {e}"
            )
        return self._mapper.dict_to_entity(deleted_user_dict)

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
