from dataclasses import dataclass
from uuid import UUID

import httpx

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


@dataclass
class ProfilesService:
    base_url: str
    client: httpx.AsyncClient

    async def get_user(self, user_id: UUID) -> UserProfile:
        response = await self.client.get(f"{self.base_url}/api/profiles/{user_id}")
        return UserProfile.parse_raw(response.read())

    async def get_users_by_group(self, group_id: UUID) -> list[UserProfile]:
        response = await self.client.get(f"{self.base_url}/api/groups/{group_id}/profiles")
        return UserProfilesPage.parse_raw(response.read()).profiles
