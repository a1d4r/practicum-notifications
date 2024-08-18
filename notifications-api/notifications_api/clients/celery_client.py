import asyncio
from datetime import datetime, timedelta

from celery import Celery
from celery.result import AsyncResult
import config

settings = config.get_settings()
logger = settings.logger


class CeleryClient:
    def __init__(self, celery_broker_url: str = settings.rabbitmq_url):
        self.celery_broker_url = celery_broker_url
        self.celery_app: Celery | None = None

    async def __aenter__(self):
        self.celery_app = Celery(broker=self.celery_broker_url)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.celery_app = None

    async def send_task_to_celery(
        self, task_name: str, args: list = None, kwargs=None, eta: datetime = None
    ) -> AsyncResult:
        loop = asyncio.get_running_loop()

        result = await loop.run_in_executor(
            None, self._send_task_sync, task_name, args, kwargs, eta
        )

        logger.debug(f"Task {task_name} sent with id {result.id}. ETA: {eta}.")
        return result

    def _send_task_sync(
        self, task_name: str, args: list = None, kwargs=None, eta: datetime = None
    ) -> AsyncResult:
        return self.celery_app.send_task(task_name, args=args, kwargs=kwargs, eta=eta)

    def get_task_result(self, task_id: str) -> AsyncResult:
        result = AsyncResult(task_id, app=self.celery_app)
        logger.debug(f"Fetched result for task id {task_id}.")
        return result


async def get_celery_session():
    async with CeleryClient() as session:
        yield session
