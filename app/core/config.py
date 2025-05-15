import os
from enum import Enum

from pydantic_settings import BaseSettings
from starlette.config import Config

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", "..", ".env")
config = Config(env_path)


class AppSettings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default="FastAPI app")
    APP_DESCRIPTION: str | None = config("APP_DESCRIPTION", default=None)
    APP_VERSION: str | None = config("APP_VERSION", default=None)
    LICENSE_NAME: str | None = config("LICENSE", default=None)
    CONTACT_NAME: str | None = config("CONTACT_NAME", default=None)
    CONTACT_EMAIL: str | None = config("CONTACT_EMAIL", default=None)


class CryptSettings(BaseSettings):
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_DAYS: int = config("ACCESS_TOKEN_EXPIRE_DAYS", default=1)
    REFRESH_TOKEN_EXPIRE_DAYS: int = config("REFRESH_TOKEN_EXPIRE_DAYS", default=30)


class PostgresSettings(BaseSettings):
    POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="postgres")
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="localhost")
    POSTGRES_PORT: int = config("POSTGRES_PORT", default=5432)
    POSTGRES_DB: str = config("POSTGRES_DB", default="postgres")
    POSTGRES_SYNC_PREFIX: str = config("POSTGRES_SYNC_PREFIX", default="postgresql://")
    POSTGRES_ASYNC_PREFIX: str = config(
        "POSTGRES_ASYNC_PREFIX", default="postgresql+asyncpg://"
    )
    POSTGRES_URI: str = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"  # NOQA
    POSTGRES_URL: str | None = config("POSTGRES_URL", default=None)


class FirstUserSettings(BaseSettings):
    ADMIN_NAME: str = config("ADMIN_NAME", default="admin")
    ADMIN_EMAIL: str = config("ADMIN_EMAIL", default="admin@admin.com")
    ADMIN_USERNAME: str = config("ADMIN_USERNAME", default="admin")
    ADMIN_PASSWORD: str = config("ADMIN_PASSWORD", default="!Ch4ng3Th1sP4ssW0rd!")


class RedisCacheSettings(BaseSettings):
    REDIS_CACHE_HOST: str = config("REDIS_CACHE_HOST", default="localhost")
    REDIS_CACHE_PORT: int = config("REDIS_CACHE_PORT", default=6379)
    REDIS_CACHE_URL: str = f"redis://{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}"


class RedisQueueSettings(BaseSettings):
    REDIS_QUEUE_HOST: str = config("REDIS_QUEUE_HOST", default="localhost")
    REDIS_QUEUE_PORT: int = config("REDIS_QUEUE_PORT", default=6379)


class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: str = config("CELERY_BROKER_URL", default="redis://redis:6379/0")
    CELERY_RESULT_BACKEND: str = config(
        "CELERY_RESULT_BACKEND", default="redis://redis:6379/0"
    )


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default="local")


class EmailSettings(BaseSettings):
    SMTP_KEY: str = config("SMTP_KEY", default="local")
    SMTP_LOGIN: str = config("SMTP_LOGIN", default="local")
    SMTP_SERVER: str = config("SMTP_SERVER", default="local")
    SMTP_PORT: str = config("SMTP_PORT", default="local")
    MAIL_FROM: str = config("MAIL_FROM", default="local")
    WEB_URL: str = config("WEB_URL", default="example.com")
    EMAIL_EXPIRE_HOURS: int = config("EMAIL_EXPIRE_HOURS", default=1)


class Settings(
    AppSettings,
    PostgresSettings,
    CryptSettings,
    FirstUserSettings,
    RedisCacheSettings,
    RedisQueueSettings,
    CelerySettings,
    EnvironmentSettings,
    EmailSettings,
):
    pass


settings = Settings()
