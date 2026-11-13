from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path.resolve().parent[2] / ".env"

class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")
    DATABASE_URL : str


setting = Setting()