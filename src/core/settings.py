from functools import lru_cache

from pydantic import BaseModel, Field, RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.paths import ENV_PATH

settings_config_dict = SettingsConfigDict(
    env_file=ENV_PATH, env_file_encoding='utf-8', validate_default=False, extra="ignore",
)


class RedisSettings(BaseSettings):
    model_config = settings_config_dict

    host: str = Field(validation_alias="REDIS_HOST")
    port: str = Field(validation_alias="REDIS_PORT")


class PostgresSettings(BaseSettings):
    model_config = settings_config_dict

    user: str = Field(validation_alias="DB_USER")
    password: str = Field(validation_alias="DB_PASS")
    host: str = Field(validation_alias="DB_HOST")
    port: str = Field(validation_alias="DB_PORT")
    name: str = Field(validation_alias="DB_NAME")


class TelegramSettings(BaseSettings):
    model_config = settings_config_dict

    api_id: int = Field(validation_alias="API_ID")
    api_hash: str = Field(validation_alias="API_HASH")
    token: str = Field(validation_alias="TOKEN")
    phone: str = Field(validation_alias="PHONE")


class LoggingSettings(BaseModel):
    file: str = "backend.log"
    rotation: str = "2MB"
    compression: str = "zip"


class PrefixSettings(BaseModel):
    posts: str = "posts"


class Settings(BaseModel):
    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()
    telegram: TelegramSettings = TelegramSettings()

    prefixes: PrefixSettings = PrefixSettings()
    logging: LoggingSettings = LoggingSettings()

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres.user}:{self.postgres.password}@"
            f"{self.postgres.host}:{self.postgres.port}/"
            f"{self.postgres.name}"
        )

    @property
    def redis_dsn(self) -> RedisDsn:
        return f"redis://{self.redis.host}:{self.redis.port}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
