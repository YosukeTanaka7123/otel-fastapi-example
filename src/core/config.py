from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    log_level: str = "INFO"
    db_url: str = "sqlite+aiosqlite:///./local.db"
    api_url: str = "https://jsonplaceholder.typicode.com"

    model_config = SettingsConfigDict(env_file=".env.local")


@lru_cache
def get_settings():
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
