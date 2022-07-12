from enum import Enum, auto
from datetime import datetime, timedelta
from jose import jwt

from fastapi import Depends, Request
from fastapi.openapi.models import HTTPBearer
from fastapi.security.base import SecurityBase

from models import User
from utils.environment import ALGORITHM, SECRET_KEY
from utils.exceptions import InvalidTokenError, PermissionDeniedError


def get_token(request: Request) -> str:
    authorization: str = request.headers.get("Authorization", "")
    return authorization.removeprefix("Bearer ")


class PermissionLevel(Enum):
    USER = auto()
    ADMIN = auto()


class UserAuth(SecurityBase):
    def __init__(self, min_level: PermissionLevel) -> None:
        self.model = HTTPBearer()
        self.scheme_name = self.__class__.__name__
        self.min_level: PermissionLevel = min_level

    async def __call__(self, request: Request) -> bool:
        token = get_token(request)
        user = await User.get_user_by_token(token)
        if not token or not user:
            raise InvalidTokenError

        if self.min_level == PermissionLevel.ADMIN and not user.admin:
            raise PermissionDeniedError

        return True


user_auth = Depends(UserAuth(PermissionLevel.USER))
admin_auth = Depends(UserAuth(PermissionLevel.ADMIN))


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta or timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
