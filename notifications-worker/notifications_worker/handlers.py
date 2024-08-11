from typing import Annotated

from email.message import EmailMessage
from uuid import UUID

import aiosmtplib

from fast_depends import Depends

from notifications_worker.broker import broker
from notifications_worker.dependencies import provide_smtp_client
from notifications_worker.settings import queues_settings, smtp_settings


@broker.subscriber(queues_settings.notifications_queue_name)
async def handle_notification(notification_id: UUID) -> None:  # noqa: ARG001
    pass


@broker.subscriber(queues_settings.email_queue_name)
async def handle_email(
    message_content: str,
    email: str,
    smtp_client: Annotated[aiosmtplib.SMTP, Depends(provide_smtp_client)],
) -> None:
    message = EmailMessage()
    message["From"] = smtp_settings.username
    message["To"] = email
    message["Subject"] = "Hello World!"
    message.set_content(message_content)
    await smtp_client.send_message(message)
