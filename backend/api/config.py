from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Variables support
load_dotenv()


class Settings(BaseSettings):
    redis_url: RedisDsn = Field(...)
    database_url: PostgresDsn = Field(...)
    access_token_expire_minutes: int = Field(default=15)
    secret_key: str = Field(min_length=48)

    model_config = SettingsConfigDict(env_prefix="api_", env_file=".env")


settings = Settings()  # type:ignore
