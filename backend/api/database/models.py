import uuid
from datetime import datetime, timezone

from pydantic import EmailStr, field_validator
from sqlmodel import Field, Relationship, SQLModel, table


class CreatedAtMixin(SQLModel):
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)


# # Почему я использую pk и UUID?
# # Потому что: https://stackoverflow.com/questions/52414414/best-practices-on-primary-key-auto-increment-and-uuid-in-sql-databases
# class Image(CreatedAtMixin, table=True):
#     pk: int | None = Field(default=None, primary_key=True)
#     id: uuid.UUID = Field(unique=True, index=True, default_factory=uuid.uuid4)
#     owner_pk: int = Field(foreign_key="user.pk", ondelete="CASCADE")
#     access_image_id: str = Field(unique=True)
#
#     owner: "User" = Relationship(back_populates="images")
#


# Возможно будет хорошей идеей перенести email и hashed_password в отдельную таблицу
# чтобы отслеживать как менялись пароль и почта пользователя
# но это усложнит структуру, поэтому я решил так не делать
class UserInfo(SQLModel):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True)

    @field_validator("username")
    def name_must_not_be_empty(cls, v):
        if v.strip() == "":
            raise ValueError("Name cannot be an empty string")
        return v


class User(CreatedAtMixin, UserInfo, table=True):
    pk: int | None = Field(default=None, primary_key=True)
    hashed_password: str

    # images: list["Image"] = Relationship(back_populates="owner", cascade_delete=True)


class UserCreate(UserInfo):
    password: str


class UserPublic(UserInfo):
    pass


# Я же могу использовать SQLModel вместо BaseModel?
class JWTToken(SQLModel):
    access_token: str
    token_type: str
    expire_at: int
