from datetime import datetime, timedelta, timezone
from typing import Any, Callable

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.interfaces.jwt_interface import JWTInterface
from src.settings import get_settings

cfg = get_settings()


class PyJWTAdapter(JWTInterface):
    """
    Адаптер для библиотеки PyJWT, реализующий JWT интерфейс
    """

    def __init__(self):
        self._secret_key = cfg.jwt_secret_key
        self._algorithm = cfg.jwt_algorithm
        self.access_token_expire_minutes = 15
        self._bearer = HTTPBearer()

    def create_access_token(self, uid: str) -> str:
        """Создает JWT токен доступа"""
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_token_expire_minutes
        )

        to_encode = {
            "sub": uid,  # subject (user_id)
            "exp": expire,  # expiration time
            "iat": datetime.now(timezone.utc),  # issued at
            "type": "access",  # token type
        }

        encoded_jwt = jwt.encode(
            payload=to_encode, key=self._secret_key, algorithm=self._algorithm
        )
        return encoded_jwt

    def token_required(self) -> Callable[..., Any]:
        """Возвращает dependency для проверки JWT токена"""

        async def dependency(
            credentials: HTTPAuthorizationCredentials = Depends(self._bearer),
        ) -> dict[str, Any]:
            try:
                payload = jwt.decode(
                    credentials.credentials,
                    self._secret_key,
                    algorithms=[self._algorithm],
                )

                # Проверяем тип токена
                if payload.get("type") != "access":
                    raise ValueError("Invalid token type")

                return {
                    "user_id": payload.get("sub"),
                    "exp": payload.get("exp"),
                    "iat": payload.get("iat"),
                    "type": payload.get("type"),
                }
            except Exception as e:
                match e:
                    case jwt.ExpiredSignatureError:
                        raise ValueError("Token has expired")
                    case jwt.InvalidTokenError:
                        raise ValueError("Invalid token")
                    case _:
                        raise ValueError("Token validation failed")

        return dependency
