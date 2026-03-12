import logging.config
from logging import getLevelNamesMapping
from typing import Any, Literal

from pydantic import BaseModel


class LoggingConfig(BaseModel):
    format: str = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    @property
    def log_level(self) -> int:
        return getLevelNamesMapping()[self.level]

    def setup(self):
        config: dict[str, Any] = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": self.format,
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
                "blog_app": {
                    "level": self.log_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
        }
        logging.config.dictConfig(config)
