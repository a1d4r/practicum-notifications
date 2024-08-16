from faststream.rabbit import RabbitBroker

from notifications_worker.core.settings import rabbitmq_settings

broker = RabbitBroker(rabbitmq_settings.url)
