from typing import Annotated

from datetime import UTC, datetime
from email.message import EmailMessage
from uuid import UUID

import aiosmtplib

from fast_depends import Depends
from faststream.exceptions import NackMessage
from faststream.rabbit import RabbitRouter
from inscriptis import get_text
from jinja2 import BaseLoader, Environment
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from notifications_worker.broker import broker
from notifications_worker.core.database import get_session
from notifications_worker.core.settings import queues_settings, smtp_settings
from notifications_worker.dependencies.profiles_service import provide_profiles_service
from notifications_worker.dependencies.smtp_client import provide_smtp_client
from notifications_worker.models import Notification, NotificationContent, NotificationTemplate
from notifications_worker.schemas import EmailBody
from notifications_worker.services.profiles_service import ProfilesService

router = RabbitRouter(prefix="notifications_")


@router.subscriber(queues_settings.notifications_queue_name)
async def handle_notification(
    session: Annotated[AsyncSession, Depends(get_session)],
    profiles_service: Annotated[ProfilesService, Depends(provide_profiles_service)],
    notification_id: UUID,
    sentinel: str | None = None,  # noqa: ARG001
) -> None:
    notification = await session.get(Notification, notification_id)
    if notification is None:
        logger.error(
            "Notification with id={notification_id} not found", notification_id=notification_id
        )
        raise NackMessage
    logger.info("Received notification {notification_id}", notification_id=notification_id)

    content: NotificationContent = notification.content
    template: NotificationTemplate = content.template

    users = []
    if content.user_group_id:
        users = await profiles_service.get_users_by_group(content.user_group_id)
    elif content.user_id:
        users = [await profiles_service.get_user(content.user_id)]

    users_for_email = [user for user in users if user.notification_preferences.email]

    logger.debug("Users for email: {users_for_email}", users_for_email=users_for_email)

    if not users_for_email:
        logger.warning(
            "No users found for email notification {notification_id}",
            notification_id=notification_id,
        )
        return

    for user in users_for_email:
        template_env = Environment(loader=BaseLoader(), autoescape=True).from_string(
            template.template_text
        )
        rendered_message = template_env.render(
            content.template_variables
            | {"first_name": user.first_name, "last_name": user.last_name}
        )
        logger.debug(f"Rendered message: {rendered_message}", rendered_message=rendered_message)
        text_message = get_text(rendered_message)
        await broker.publish(
            EmailBody(email=user.email, html=rendered_message, text=text_message),
            queues_settings.prefix + queues_settings.email_queue_name,
        )
        logger.debug("Sent email notification {notification_id}", notification_id=notification_id)
        notification.last_sent_at = datetime.now(UTC)
        await session.commit()


@router.subscriber(queues_settings.email_queue_name)
async def send_email(
    smtp_client: Annotated[aiosmtplib.SMTP, Depends(provide_smtp_client)], body: EmailBody
) -> None:
    logger.debug("Going to send email at {email}", email=body.email)
    message = EmailMessage()

    if body.subject is not None:
        message["Subject"] = body.subject
    message["From"] = smtp_settings.username
    message["To"] = body.email
    if body.text is None:
        if body.html is None:
            logger.error("Either text or html must be provided")
            raise NackMessage
        body.text = get_text(body.html)
    message.set_content(body.text)
    if body.html is not None:
        message.add_alternative(body.html, subtype="html")

    try:
        await smtp_client.send_message(message)
    except Exception as exc:
        logger.exception("Failed to send email at {email}", email=body.email)
        raise NackMessage from exc
    else:
        logger.info("Successfully sent message at {email}", email=body.email)
