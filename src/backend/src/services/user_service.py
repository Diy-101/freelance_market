from typing import Callable

from src.domain.interfaces import JWTInterface, UserServiceInterface
from src.domain.models.users import UserModel
from src.domain.schemas.users import TelegramInitData, TelegramUser
from src.repositories import AbstractRepository
from src.settings import get_settings
from src.utils.telegram_validator import TelegramValidator

cfg = get_settings()


class UserService(UserServiceInterface):
    """
    Объединенный сервис для управления пользователями и аутентификации
    Включает CRUD операции с пользователями + функции аутентификации
    """

    def __init__(
        self,
        repository: AbstractRepository[UserModel, TelegramUser],
        jwt_adapter: JWTInterface,
        telegram_validator: TelegramValidator,
    ):
        self.repository = repository
        self.jwt_adapter = jwt_adapter
        self.telegram_validator = telegram_validator

    # ============= CRUD =============
    async def get_user(self, user_id: int) -> TelegramUser | None:
        user = await self.repository.get(user_id)
        if user is None:
            return None
        return user

    async def create_user(self, user: TelegramUser) -> TelegramUser:
        new_user = await self.repository.create(user)
        return new_user

    async def update_user(
        self, user_id: int, user: TelegramUser
    ) -> TelegramUser | None:
        current_user = await self.repository.get(user_id)
        if current_user is None:
            return None
        user_dict = user.model_dump()
        current_user_dict = current_user.model_dump()
        fields_to_update = {
            f: new_val
            for f, curr_val in current_user_dict.items()
            for _, new_val in user_dict.items()
            if curr_val != new_val
        }
        return await self.repository.update(current_user.id, fields_to_update)

    async def delete_user(self, user_id: int) -> TelegramUser | None:
        return await self.repository.delete(user_id)

    # ============= Аутентификация и авторизация =============
    def check_init_data(self, init_data: str) -> TelegramInitData:
        """
        Проверка Telegram initData с полной валидацией
        """
        try:
            # Валидируем initData
            validated_data = self.telegram_validator.validate_init_data(
                init_data, max_age_seconds=1000000
            )
            return validated_data
        except ValueError as e:
            raise ValueError(f"Can't validate initData: {e}")

    def authenticate_user_from_init_data(self, init_data: str) -> TelegramUser:
        """
        Аутентификация пользователя через Telegram initData
        """
        # Валидируем initData
        validated_data = self.check_init_data(init_data)

        # Извлекаем данные пользователя
        telegram_user = validated_data.user
        if not telegram_user:
            raise ValueError("No user data found in init data")

        return telegram_user

    def create_token(self, user_id) -> str:
        token = self.jwt_adapter.create_access_token(str(user_id))
        return token

    def get_token_dependency(self) -> Callable:
        """
        Возвращает dependency для проверки JWT токена в FastAPI
        Используется в роутах как Depends(user_service.get_token_dependency())
        """
        return self.jwt_adapter.token_required()

    async def get_current_user_from_token(self, token_data: dict) -> TelegramUser:
        """
        Получение текущего пользователя из данных токена
        token_data приходит от JWT dependency
        """
        user_id = token_data.get("user_id") or token_data.get("sub")
        if not user_id:
            raise ValueError("Invalid token: no user_id found")

        user = await self.repository.get(int(user_id))
        if not user:
            raise ValueError(f"User {user_id} not found")

        return user
