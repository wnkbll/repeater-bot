from functools import lru_cache

from pydantic import Field, RedisDsn, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.paths import ENV_PATH

settings_config_dict = SettingsConfigDict(
    env_file=ENV_PATH, env_file_encoding='utf-8', validate_default=False, extra="ignore",
)


class TelegramSettings(BaseSettings):
    model_config = settings_config_dict

    api_id: int = Field(validation_alias="API_ID")
    api_hash: str = Field(validation_alias="API_HASH")
    token: str = Field(validation_alias="TOKEN")
    phone: str = Field(validation_alias="PHONE")


class RedisSettings(BaseSettings):
    model_config = settings_config_dict

    host: str = Field(validation_alias="REDIS_HOST")
    port: str = Field(validation_alias="REDIS_PORT")


class Settings(BaseModel):
    telegram: TelegramSettings = TelegramSettings()
    redis: RedisSettings = RedisSettings()

    @property
    def redis_dsn(self) -> RedisDsn:
        return f"redis://{self.redis.host}:{self.redis.port}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
