from uuid import UUID

from pydantic import BaseModel


class NotificationBody(BaseModel):
    notification_id: UUID


class EmailBody(BaseModel):
    email: str
    subject: str | None = None
    text: str
    html: str
