import os
import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from starlette import status as http_status

import config
from schemas.notifications import SendNotificationResponse
from services.auth import security_jwt
from services.notification import NotificationService, get_notification_service

settings = config.get_settings()
logger = settings.logger

router = APIRouter(
    tags=["scripts"], prefix=f"{settings.api_root_path}/{settings.api_version}/scripts"
)


@router.post(
    path="/notifications/send",
    status_code=http_status.HTTP_200_OK,
    response_model=SendNotificationResponse,
)
async def send_notification(
    user: Annotated[dict, Depends(security_jwt(required_roles=[]))],
    notification_service: NotificationService = Depends(get_notification_service),
) -> SendNotificationResponse:
    """Send notification to RabbitMQ."""
    await notification_service.send_notification()
    return {"data": scripts, "meta": {"count": count}}


@router.post(
    path="/notifications",
    status_code=http_status.HTTP_200_OK,
    response_model=SendNotificationResponse,
)
async def create_notification(
    user: Annotated[dict, Depends(security_jwt(required_roles=[]))],
    notification_service: NotificationService = Depends(get_notification_service),
) -> SendNotificationResponse:
    """Create notification for RabbitMQ."""

    return {"data": scripts, "meta": {"count": count}}
