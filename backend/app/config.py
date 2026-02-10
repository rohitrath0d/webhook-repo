import os
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class FlaskAppEnvConfigs(BaseSettings):
  database_url: SecretStr = Field(alias="DATABASE_URL")
  allowed_origins: str = Field(alias="ALLOWED_ORIGINS")
  database_name: SecretStr = Field(alias="DATABASE_NAME")
  webhook_secret: SecretStr = Field(alias="WEBHOOK_SECRET")
  celery_broker_url: SecretStr = Field(alias="CELERY_BROKER_URL")
  celery_result_backend: SecretStr = Field(alias="CELERY_RESULT_BACKEND")
  
  # connecting to .env
  model_config = SettingsConfigDict(env_file=".env", env_ignored_empty=True) 