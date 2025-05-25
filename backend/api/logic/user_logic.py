from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, or_, select

from api.database.models import JWTToken, User, UserCreate
from api.config import settings
from api.dependencies import pwd_context
from api.logic.exceptions import (
    InvalidTokenError,
    EmailAlreadyUsed,
    TryAgainError,
    UsernameAlreadyUsed,
)
from api.logic import jwt_logic


def get_user_by_email_or_username(
    email_or_username: str, session: Session
) -> User | None:
    return session.scalar(
        select(User).where(
            or_(User.email == email_or_username, User.username == email_or_username)
        )
    )


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_authenticated_user(email_or_username: str, password: str, session: Session):
    user = get_user_by_email_or_username(email_or_username, session)

    # Защита от Timing атак
    pass_hash = user.hashed_password if user else "some_dummy_password_hash"
    if not verify_password(password, pass_hash):
        return None

    return user


def create_user(data: UserCreate, session: Session):
    # На практике такое часто было, что пользователь не находило, хотя он был в БД
    # и я не знал, что делать с этой ошибкой. Буду надеяться что теперь таких проблем не будет
    existing_user = session.scalar(
        select(User).where(
            or_(User.email == data.email, User.username == data.username)
        )
    )
    if existing_user:
        if existing_user.email == data.email:
            raise EmailAlreadyUsed(data.email)
        raise UsernameAlreadyUsed(data.username)

    hashed_password = pwd_context.hash(data.password)
    extra_data = {"hashed_password": hashed_password}

    user = User.model_validate(data, update=extra_data)

    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise TryAgainError()
    session.refresh(user)

    return user


def create_user_token(user: User):
    jwt, expire = jwt_logic.create_access_token(
        data={"sub": str(user.pk)},
        expires_minutes=settings.access_token_expire_minutes,
    )
    expire = int(expire.timestamp())
    return JWTToken(access_token=jwt, token_type="Bearer", expire_at=expire)


def get_user_by_token(token: str, session: Session):
    payload = jwt_logic.decode_access_token(token)
    user_pk = payload.get("sub")
    if user_pk is None:
        raise InvalidTokenError(token)
    user = session.get(User, int(user_pk))
    if user is None:
        raise InvalidTokenError(token)

    return user
