from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class BaseSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.now)


class NotificationContent(BaseSchema):
    event_type: str
    template_variables: dict
    user_id: uuid.UUID
    user_group_id: uuid.UUID
    updated_at: datetime = Field(default_factory=datetime.now)


class Notification(BaseSchema):
    content_id: uuid.UUID
    sent_at: datetime


class NotificationTemplate(BaseSchema):
    event_type: str
    template_text: str
    channels: list[str]
    updated_at: datetime = Field(default_factory=datetime.now)


class SendNotificationRequest(BaseModel):
    notification_content_id: uuid.UUID


class SendNotificationResponse(BaseModel):
    notification_id: uuid.UUID


class CreateNotificationRequest(BaseModel):
    user_id: uuid.UUID
    user_group_id: uuid.UUID
    notification_template_id: uuid.UUID
    template_variables: dict
    planned_at: datetime | None = None
