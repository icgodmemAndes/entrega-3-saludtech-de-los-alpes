from pydantic import BaseSettings
from typing import Any

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()

app_configs: dict[str, Any] = {"title": "Anonimizador", "version": settings.APP_VERSION}