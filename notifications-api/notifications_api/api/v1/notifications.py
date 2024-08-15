from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status as http_status

from schemas.api_models import (
    SendNotificationResponse,
    SendNotificationRequest,
    CreateNotificationRequest,
)
from services.auth import security_jwt
from services.notification import NotificationService, get_notification_service
import config

settings = config.get_settings()


logger = settings.logger

router = APIRouter(
    prefix=f"{settings.api_root_path}/{settings.api_version}/scripts", tags=["scripts"]
)


@router.post(
    path="/notifications/send",
    status_code=http_status.HTTP_200_OK,
    response_model=SendNotificationResponse,
)
async def send_notification(
    # user: Annotated[dict, Depends(security_jwt(required_roles=[]))],
    request_param: SendNotificationRequest,
    notification_service: NotificationService = Depends(get_notification_service),
) -> SendNotificationResponse:
    """Send notification to RabbitMQ."""
    result = await notification_service.send_notification(
        content_id=request_param.notification_content_id
    )
    return SendNotificationResponse(**{"notification_content_id": result.id})


@router.post(
    path="/notifications",
    status_code=http_status.HTTP_200_OK,
    response_model=SendNotificationResponse,
)
async def create_notification(
    # user: Annotated[dict, Depends(security_jwt(required_roles=[]))],
    request_param: CreateNotificationRequest,
    notification_service: NotificationService = Depends(get_notification_service),
) -> SendNotificationResponse:
    """Create notification for RabbitMQ."""
    result = await notification_service.create_notification(**request_param.model_dump())
    return SendNotificationResponse(**{"notification_content_id": result.id})
