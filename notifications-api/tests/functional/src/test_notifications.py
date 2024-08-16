import uuid

from sqlalchemy import text
from starlette import status as http_status
import pytest
from functional import config
from functional.clients.database import get_pg_session
from functional.schemas.entity import Notification, NotificationContent, NotificationTemplate, Base

settings = config.get_settings()


@pytest.mark.parametrize(
    "method, api_url, payload, expected_answer, test_name",
    [
        (
            "POST",
            "/send",
            {"notification_content_id": "..."},
            {"status": http_status.HTTP_200_OK, "body": {}},
            "send_notification-success",
        ),
        (
            "POST",
            "/send",
            {"notification_content_id": "..."},
            {
                "status": http_status.HTTP_400_BAD_REQUEST,
                "body": {"detail": "content_id [...] not found."},
            },
            "send_notification-failed-content_not_exists",
        ),
        (
            "POST",
            "/",
            {
                "user_id": str(uuid.uuid4()),
                "user_group_id": str(uuid.uuid4()),
                "notification_template_id": "...",
                "template_variables": {"asd": "asd"},
            },
            {"status": http_status.HTTP_200_OK, "body": {}},
            "create_notification-success",
        ),
        (
            "POST",
            "/",
            {
                "user_id": str(uuid.uuid4()),
                "user_group_id": str(uuid.uuid4()),
                "notification_template_id": "...",
                "template_variables": {"asd": "asd"},
            },
            {
                "status": http_status.HTTP_400_BAD_REQUEST,
                "body": {"detail": "template_id [...] not found."},
            },
            "create_notification-failed-content_not_exists",
        ),
    ],
)
# create group
@pytest.mark.asyncio(scope="session")
async def test_notifications(
    make_request, method: str, api_url: str, payload: dict, expected_answer: dict, test_name: str
):
    api_url_prefix = "/api/v1/notifications"

    async with get_pg_session() as client:
        await client.execute(text("DELETE FROM notification.notifications"))
        await client.execute(text("DELETE FROM notification.notification_contents"))
        await client.execute(text("DELETE FROM notification.notification_templates"))
        await client.commit()

    if test_name == "default":
        response = await make_request(
            method=method, api_url=f"{api_url_prefix}{api_url}", payload=payload
        )
    elif test_name == "send_notification-success":
        async with get_pg_session() as client:
            notification_template = NotificationTemplate(
                event_type="email", template_text="some text", channels=["asd"]
            )
            client.add(notification_template)
            await client.commit()

            notification_content = NotificationContent(
                notification_template_id=notification_template.id,
                template_variables={},
                user_id=uuid.uuid4(),
                user_group_id=uuid.uuid4(),
            )
            client.add(notification_content)
            await client.commit()
        payload["notification_content_id"] = str(notification_content.id)
        response = await make_request(
            method=method, api_url=f"{api_url_prefix}{api_url}", payload=payload
        )
    elif test_name == "send_notification-failed-content_not_exists":
        fake_id = str(uuid.uuid4())
        payload["notification_content_id"] = fake_id
        expected_answer["body"]["detail"] = expected_answer["body"]["detail"].replace(
            "...", fake_id
        )
        response = await make_request(
            method=method, api_url=f"{api_url_prefix}{api_url}", payload=payload
        )
    elif test_name == "create_notification-success":
        async with get_pg_session() as client:
            notification_template = NotificationTemplate(
                event_type="email", template_text="some text", channels=["asd"]
            )
            client.add(notification_template)
            await client.commit()
        payload["notification_template_id"] = str(notification_template.id)
        response = await make_request(
            method=method, api_url=f"{api_url_prefix}{api_url}", payload=payload
        )
    elif test_name == "create_notification-failed-content_not_exists":
        fake_id = str(uuid.uuid4())
        payload["notification_template_id"] = fake_id
        expected_answer["body"]["detail"] = expected_answer["body"]["detail"].replace(
            "...", fake_id
        )
        response = await make_request(
            method=method, api_url=f"{api_url_prefix}{api_url}", payload=payload
        )
    else:
        raise ValueError(f"Unknown test_name: {test_name}")

    if expected_answer["body"]:
        print("expected:", expected_answer["body"])
        print("response:", response["body"])
        assert response["body"] == expected_answer["body"]
    assert response["status"] == expected_answer["status"]
