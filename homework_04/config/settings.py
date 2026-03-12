from pathlib import Path

from config.api import APIConfig
from config.app import AppConfig
from config.database import DatabaseConfig
from config.logging import LoggingConfig
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

CONFIG_DIR = Path(__file__).resolve().parent
ENVS_DIR = CONFIG_DIR / "envs"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        # Prefix for all environment variables from env file. It's best practice since some libraries can scan related env variables automatically. To avoid propagating wrong variables to such libraries we can specify prefix for our application variables
        env_prefix="BLOG_APP__",
        env_nested_delimiter="__",
        env_file=(
            # Consecutive scan. The values will be overwritten in order
            ENVS_DIR / ".env.example",
            ENVS_DIR / ".env",
        ),
        env_file_encoding="utf-8",
    )

    app: AppConfig = AppConfig()
    logging: LoggingConfig = LoggingConfig()
    db: DatabaseConfig = DatabaseConfig()
    api: APIConfig = APIConfig()


settings = Settings()
