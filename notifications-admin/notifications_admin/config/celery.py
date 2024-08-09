from __future__ import absolute_import, unicode_literals

import logging
import os

import requests
from celery import Celery, shared_task
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

logger = logging.getLogger(__name__)


@shared_task
def task_notification_api(notification_content_id: str):
    try:
        data = {
            "notification_content_id": notification_content_id
        }
        response = requests.post(settings.NOTIFICATION_API, json=data)
        response.raise_for_status()
        logger.info(response.json())
    except requests.RequestException as err:
        logger.error(err)
