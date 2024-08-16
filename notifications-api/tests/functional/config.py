from pathlib import Path
from pydantic_settings import BaseSettings

from utils.advlogger import CustomizeLogger
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_host: str
    app_port: int

    api_root_path: str
    api_version: str

    log_file_path: Path
    log_level: str
    log_format: str
    log_rotation: str
    log_retention: str
    logger: CustomizeLogger | None = None

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str

    rabbitmq_url: str
    celery_url: str

    debug: bool

    class Config:
        env_file = ".env"
        extra = "ignore"

    def setup(self):
        self.logger = CustomizeLogger.customize_logging(
            self.log_file_path,
            self.log_level,
            self.log_rotation,
            self.log_retention,
            self.log_format,
        )


@lru_cache(maxsize=None)
def get_settings():
    settings = Settings()
    settings.setup()
    return settings
