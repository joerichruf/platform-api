from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
  app_name: str = Field(default='platform-api')  
  debug: bool = Field(default=False)
  log_level: str = Field(default='INFO')
  github_token: str = Field(required=True)
  k8s_namespace: str = Field(default='default')
  model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_settings() -> Settings:
    return Settings()
