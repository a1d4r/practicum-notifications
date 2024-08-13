import sys

from pathlib import Path

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_PATH = Path(__file__).parent.parent.resolve()


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

    notifications_queue_name: str = "notifications.general"
    email_queue_name: str = "notifications.email"
    sms_queue_name: str = "notifications.sms"
    websocket_queue_name: str = "notifications.websocket"


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


env_file = "./envs/.env.test" if "pytest" in sys.modules else "./envs/.env"
rabbitmq_settings = RabbitMQSettings(_env_file=env_file)
queues_settings = QueuesSettings(_env_file=env_file)
smtp_settings = SMTPSettings(_env_file=env_file)
