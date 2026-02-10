import logging
import logging.config
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_PATH = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_PATH),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO"
    )
    api_url: str = Field(
        default="https://jsonplaceholder.typicode.com",
        alias="jsonplaceholder_api_url",
    )
    postgres_user: str = Field(default="user")
    postgres_password: SecretStr
    postgres_db: str = Field(default="postgres")
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    sqla_db_echo: bool = Field(default=False)

    @property
    def sqlalchemy_pg_conn_uri(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password.get_secret_value()}@"
            f"{self.postgres_host}:{self.postgres_port}/"
            f"{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def setup_logging():
    settings = get_settings()

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "": {
                "level": "WARNING",
                "handlers": ["console"],
            },
            "homework_04": {
                "level": settings.log_level,
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(logging_config)


if __name__ == "__main__":
    settings = Settings()
    print(settings.model_dump())
    print(settings.sqlalchemy_pg_conn_uri)
