from datetime import datetime

from celery import Celery
from celery.result import AsyncResult
import config

settings = config.get_settings()
logger = settings.logger


class CeleryClient:
    def __init__(
        self,
        celery_broker_url: str = settings.celery_broker_url,
        celery_backend_url: str = settings.celery_backend_url,
    ):
        self.celery_broker_url = celery_broker_url
        self.celery_backend_url = celery_backend_url
        self.celery_app: Celery | None = None

    async def __aenter__(self):
        self.celery_app = Celery(broker=self.celery_broker_url, backend=self.celery_backend_url)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.celery_app = None

    def send_task_to_celery(
        self, task_name: str, args: list = None, kwargs=None, eta: datetime = None
    ) -> AsyncResult:
        result = self.celery_app.send_task(task_name, args=args, kwargs=kwargs, eta=eta)
        logger.debug(f"Task {task_name} sent with id {result.id}.")
        return result

    def get_task_result(self, task_id: str) -> AsyncResult:
        result = AsyncResult(task_id, app=self.celery_app)
        logger.debug(f"Fetched result for task id {task_id}.")
        return result


async def get_celery_session():
    async with CeleryClient() as session:
        try:
            yield session
        except Exception as e:
            logger.error(str(e))
