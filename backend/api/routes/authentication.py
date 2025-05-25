from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.database.models import JWTToken, UserCreate, UserPublic
from api.dependencies import DatabaseDep
from api.logic import user_logic, exceptions


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=JWTToken)
def login_user(
    data: Annotated[OAuth2PasswordRequestForm, Depends()], session: DatabaseDep
):
    user = user_logic.get_authenticated_user(data.username, data.password, session)
    if user is None:
        raise HTTPException(400, "User not found or invalid password")
    return user_logic.create_user_token(user)


# Хеширование пароля лучше делать на стороне клиента, все таки
# Но тут не знаю как лучше, если честно
@router.post(
    "/register",
    response_model=UserPublic,
    responses={
        400: {
            "description": "User with that email already exists or that username already in use"
        }
    },
)
def register_user(data: UserCreate, session: DatabaseDep):
    try:
        return user_logic.create_user(data, session)
    except exceptions.NotPossibleToCreateUser as e:
        raise HTTPException(400, str(e))
