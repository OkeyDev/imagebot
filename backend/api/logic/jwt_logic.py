from typing import TypedDict
import uuid
import jwt

from datetime import datetime, timedelta, timezone
from api.config import settings
from api.logic.exceptions import InvalidTokenError


class JWTData(TypedDict):
    sub: str
    exp: int
    jti: str | None


def create_access_token(data: dict, expires_minutes: int) -> tuple[str, datetime]:
    to_encode = data.copy()
    to_encode["jti"] = uuid.uuid4().hex
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt, expire


def decode_access_token(token: str) -> JWTData:
    try:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
            options={"require": ["exp", "sub"]},
        )
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        raise InvalidTokenError(token)
