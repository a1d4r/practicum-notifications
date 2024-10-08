import logging
import os

from datetime import UTC, datetime

import requests

from celery import Celery, shared_task
from django.apps import apps
from django.conf import settings
from django.db import IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

logger = logging.getLogger(__name__)


def update_date(notification_content_id: str) -> None:
    Notifications = apps.get_model("notifications", "Notifications")

    try:
        obj = Notifications.objects.get(content_id=notification_content_id)
        obj.last_sent_at = datetime.now(UTC)
        obj.save()
    except Notifications.DoesNotExist:
        try:
            Notifications.objects.create(content_id=notification_content_id)
        except IntegrityError as err:
            logger.error(err)


@shared_task
def task_notification_api(notification_content_id: str) -> None:
    try:
        data = {"notification_content_id": notification_content_id}
        response = requests.post(settings.NOTIFICATION_API, json=data, timeout=60)
        response.raise_for_status()
        logger.info(response.json())

    except requests.RequestException as err:
        logger.error(err)

    finally:
        update_date(notification_content_id)
