from uuid import UUID

from pydantic import BaseModel


class NotificationPreferences(BaseModel):
    email: bool
    sms: bool
    websocket: bool


class UserProfile(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    email: str
    timezone: str
    notification_preferences: NotificationPreferences


class UserProfilesPage(BaseModel):
    profiles: list[UserProfile]
    total: int
    page: int
    size: int
    pages: int
