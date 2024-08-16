from typing import Annotated

import httpx

from fast_depends import Depends

from notifications_worker.core.settings import profiles_settings
from notifications_worker.dependencies.http_client import provide_http_client
from notifications_worker.services.profiles_service import ProfilesService


def provide_profiles_service(
    http_client: Annotated[httpx.AsyncClient, Depends(provide_http_client)],
) -> ProfilesService:
    return ProfilesService(profiles_settings.base_url, http_client)
