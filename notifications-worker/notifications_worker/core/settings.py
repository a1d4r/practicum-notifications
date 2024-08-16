import sys

from pathlib import Path

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RABBITMQ_", extra="ignore")

    username: SecretStr
    password: SecretStr
    host: str
    port: int

    @property
    def url(self) -> str:
        return f"amqp://{self.username.get_secret_value()}:{self.password.get_secret_value()}@{self.host}:{self.port}"


class QueuesSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    prefix: str = "notifications_"
    notifications_queue_name: str = "general"
    email_queue_name: str = "email"
    sms_queue_name: str = "sms"
    websocket_queue_name: str = "websocket"


class SMTPSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SMTP_", extra="ignore")

    hostname: str
    port: int
    username: str
    password: SecretStr
    use_tls: bool = True
    cert_bundle: Path | None = None  # path to cert.pem

    @field_validator("cert_bundle")
    @classmethod
    def validate_cert_bundle(cls, cert_bundle: Path | None) -> Path | None:
        if cert_bundle is None:
            return cert_bundle
        if cert_bundle.is_absolute():
            return cert_bundle
        return (PROJECT_PATH / cert_bundle).resolve()


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_", extra="ignore")

    dialect: str = "postgresql"
    driver: str = "asyncpg"
    username: str
    password: SecretStr
    host: str
    port: int
    name: str

    @property
    def url(self) -> str:
        """URL for SQLAlchemy engine.

        Format: dialect+driver://username:password@host:port/database
        More info: https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
        """
        return (
            f"{self.dialect}+{self.driver}://{self.username}:"
            f"{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"
        )


class ProfilesSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PROFILES_", extra="ignore")

    base_url: str


env_file = PROJECT_PATH / "envs" / (".env.test" if "pytest" in sys.modules else ".env")
rabbitmq_settings = RabbitMQSettings(_env_file=env_file)
queues_settings = QueuesSettings(_env_file=env_file)
smtp_settings = SMTPSettings(_env_file=env_file)
database_settings = DatabaseSettings(_env_file=env_file)
profiles_settings = ProfilesSettings(_env_file=env_file)
