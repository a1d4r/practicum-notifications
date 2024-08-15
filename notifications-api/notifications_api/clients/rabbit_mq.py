import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractIncomingMessage
from typing import Callable, Awaitable
import config

settings = config.get_settings()
logger = settings.logger


class RabbitMQClient:
    def __init__(self, rabbitmq_url: str = settings.rabbitmq_url):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None

    async def __aenter__(self):
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.channel.close()
        await self.connection.close()

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        logger.debug("Connected to RabbitMQ.")

    async def declare_queue(self, queue_name: str, durable: bool = True):
        return await self.channel.declare_queue(queue_name, durable=durable)

    async def declare_exchange(
        self,
        exchange_name: str,
        exchange_type: ExchangeType = ExchangeType.DIRECT,
        durable: bool = True,
    ):
        return await self.channel.declare_exchange(
            exchange_name, exchange_type=exchange_type, durable=durable
        )

    async def publish_message(self, queue_name: str, message_body: str):
        queue = await self.declare_queue(queue_name)
        message = aio_pika.Message(body=message_body.encode())
        await self.channel.default_exchange.publish(message, routing_key=queue.name)
        logger.debug(f"Message sent to queue {queue_name}: {message_body}")

    async def consume_messages(
        self, queue_name: str, callback: Callable[[AbstractIncomingMessage], Awaitable[None]]
    ):
        queue = await self.declare_queue(queue_name)
        await queue.consume(callback)
        logger.debug(f"Started consuming messages from queue {queue_name}")

    async def close(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
        logger.debug("Disconnected from RabbitMQ")


async def get_rabbit_session():
    async with RabbitMQClient() as session:
        try:
            yield session
        except Exception as e:
            logger.error(str(e))
