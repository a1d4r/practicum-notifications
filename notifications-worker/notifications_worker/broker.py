from faststream.rabbit import RabbitBroker

from notifications_worker.handlers import router
from notifications_worker.settings import rabbitmq_settings

broker = RabbitBroker(rabbitmq_settings.url)
broker.include_router(router)
