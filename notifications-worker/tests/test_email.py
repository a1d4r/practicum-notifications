import pydantic
import pytest

from faststream.rabbit import TestRabbitBroker

from notifications_worker.broker import broker


@pytest.mark.asyncio()
async def test_correct():
    async with TestRabbitBroker(broker) as br:
        await br.publish({"user": "John", "user_id": 1}, "in-queue")


@pytest.mark.asyncio()
async def test_invalid():
    async with TestRabbitBroker(broker) as br:
        with pytest.raises(pydantic.ValidationError):
            await br.publish("wrong message", "in-queue")
