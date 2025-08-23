from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.interfaces.jwt_interface import JWTInterface
from src.settings import get_settings

cfg = get_settings()


class PyJWTAdapter(JWTInterface):
    """
    Адаптер для библиотеки PyJWT, реализующий JWT интерфейс
    """

    def __init__(self):
        self.secret_key = cfg.jwt_secret_key
        self.algorithm = cfg.jwt_algorithm
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
            payload=to_encode, key=self.secret_key, algorithm=self.algorithm
        )
        return encoded_jwt

    def token_required(self) -> Callable[..., Any]:
        """Возвращает dependency для проверки JWT токена"""

        async def dependency(
                credentials: HTTPAuthorizationCredentials = Depends(self._bearer),
        ) -> Dict[str, Any]:
            try:
                payload = jwt.decode(
                    credentials.credentials,
                    self.secret_key,
                    algorithms=[self.algorithm],
                )

                # Проверяем тип токена
                if payload.get("type") != "access":
                    raise HTTPException(status_code=401, detail="Invalid token type")

                return {
                    "user_id": payload.get("sub"),
                    "exp": payload.get("exp"),
                    "iat": payload.get("iat"),
                    "type": payload.get("type"),
                }

            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
            except Exception:
                raise HTTPException(status_code=401, detail="Token validation failed")

        return dependency
