from typing import Annotated

from email.message import EmailMessage
from uuid import UUID

import aiosmtplib

from fast_depends import Depends
from faststream.exceptions import NackMessage
from inscriptis import get_text
from loguru import logger

from notifications_worker.broker import broker
from notifications_worker.dependencies import provide_smtp_client
from notifications_worker.settings import queues_settings, smtp_settings


@broker.subscriber(queues_settings.notifications_queue_name)
async def handle_notification(notification_id: UUID) -> None:  # noqa: ARG001
    pass


@broker.subscriber(queues_settings.email_queue_name)
async def handle_email(
    smtp_client: Annotated[aiosmtplib.SMTP, Depends(provide_smtp_client)],
    email: str,
    subject: str | None = None,
    text: str | None = None,
    html: str | None = None,
) -> None:
    message = EmailMessage()

    if subject is not None:
        message["Subject"] = subject
    message["From"] = smtp_settings.username
    message["To"] = email
    if text is None:
        if html is None:
            logger.error("Either text or html must be provided")
            raise NackMessage
        text = get_text(html)
    message.set_content(text)
    if html is not None:
        message.add_alternative(html, subtype="html")

    try:
        await smtp_client.send_message(message)
    except Exception as exc:
        logger.exception("Failed to send email at {email}", email=email)
        raise NackMessage from exc
    else:
        logger.info("Successfully sent message at {email}", email=email)
