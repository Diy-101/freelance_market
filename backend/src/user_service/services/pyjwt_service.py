from datetime import datetime, timedelta, timezone
from typing import Any, Callable

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.settings import get_settings

cfg = get_settings()


class PyJWTService:
    def __init__(self):
        self._secret_key = cfg.jwt_secret_key
        self._algorithm = cfg.jwt_algorithm
        self.access_token_expire_minutes = 15
        self._bearer = HTTPBearer()

    def create_access_token(self, uid: str) -> str:
        """Create JWT access token"""
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
        """Return dependency"""

        async def dependency(
            credentials: HTTPAuthorizationCredentials = Depends(self._bearer),
        ) -> dict[str, Any]:
            try:
                payload = jwt.decode(
                    credentials.credentials,
                    self._secret_key,
                    algorithms=[self._algorithm],
                )

                # check token type
                if payload.get("type") != "access":
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token type",
                    )

                return {
                    "user_id": payload.get("sub"),
                    "exp": payload.get("exp"),
                    "iat": payload.get("iat"),
                    "type": payload.get("type"),
                }
            except Exception as e:
                match e:
                    case jwt.ExpiredSignatureError:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token has expired",
                        )
                    case jwt.InvalidTokenError:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token",
                        )
                    case _:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token validation failed",
                        )

        return dependency
