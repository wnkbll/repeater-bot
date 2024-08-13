from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.paths import ENV_PATH

settings_config_dict = SettingsConfigDict(
    env_file=ENV_PATH, env_file_encoding='utf-8', validate_default=False, extra="ignore",
)

class Settings(BaseSettings):
    model_config = settings_config_dict

    api_id: int = Field(validation_alias="API_ID")
    api_hash: str = Field(validation_alias="API_HASH")
    token: str = Field(validation_alias="TOKEN")
    phone: str = Field(validation_alias="PHONE")
