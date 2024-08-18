import json
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clients.celery_client import get_celery_session, CeleryClient
from clients.database import get_pg_session
from clients.rabbit_mq import get_rabbit_session, RabbitMQClient
from schemas.entity import Notification, NotificationContent, NotificationTemplate
from sqlalchemy.future import select


class NotificationsServiceBase(ABC):
    @abstractmethod
    async def create_notification(
        self,
        user_id: uuid.UUID,
        user_group_id: uuid.UUID,
        event_type: str,
        template_variables: dict,
        planned_at: datetime,
    ) -> Notification:
        pass

    @abstractmethod
    async def send_notification(self, content_id: uuid.UUID) -> Notification:
        pass


class NotificationService(NotificationsServiceBase):
    def __init__(
        self,
        database_session: AsyncSession,
        rabbit_session: RabbitMQClient,
        celery_session: CeleryClient,
    ):
        self._db: AsyncSession = database_session
        self._rabbit: RabbitMQClient = rabbit_session
        self._celery: celery_session = celery_session

    async def get_notification_content(self, content_id: uuid.UUID):
        result = await self._db.execute(
            select(NotificationContent).where(NotificationContent.id == content_id)
        )
        return result.scalars().first()

    async def get_notification_template(self, template_id: uuid.UUID):
        result = await self._db.execute(
            select(NotificationTemplate).where(NotificationTemplate.id == template_id)
        )
        return result.scalars().first()

    async def create_notification(
        self,
        user_id: uuid.UUID,
        user_group_id: uuid.UUID,
        notification_template_id: str,
        template_variables: dict,
        planned_at: datetime | None,
    ) -> Notification:
        notification_content = NotificationContent(
            notification_template_id=notification_template_id,
            template_variables=template_variables,
            user_id=user_id,
            user_group_id=user_group_id,
        )
        self._db.add(notification_content)
        await self._db.flush()

        notification = Notification(content_id=notification_content.id)
        self._db.add(notification)

        await self._db.commit()

        if not planned_at or planned_at < datetime.now(timezone.utc):
            await self.send_message_to_rabbit(
                message_body=json.dumps({"notification_id": str(notification.id)})
            )
        else:
            await self._celery.send_task_to_celery(
                task_name=json.dumps({"notification_id": str(notification.id)}), eta=planned_at
            )
        return notification

    async def send_notification(self, content_id: uuid.UUID) -> Notification:
        notification = Notification(content_id=content_id)
        self._db.add(notification)
        await self._db.commit()
        await self.send_message_to_rabbit(
            message_body=json.dumps({"notification_id": str(notification.id)})
        )
        return notification

    async def send_message_to_rabbit(self, message_body: str):
        await self._rabbit.publish_message(
            queue_name="notifications.general", message_body=message_body
        )


def get_notification_service(
    database_session: AsyncSession = Depends(get_pg_session),
    rabbit_session: RabbitMQClient = Depends(get_rabbit_session),
    celery_session: CeleryClient = Depends(get_celery_session),
) -> NotificationService:
    return NotificationService(
        database_session=database_session,
        rabbit_session=rabbit_session,
        celery_session=celery_session,
    )
