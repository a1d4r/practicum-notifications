from typing import Any

from collections.abc import AsyncIterator, Iterator
from unittest.mock import AsyncMock

import aiosmtplib
import pytest

from fast_depends import dependency_provider
from faststream import ContextRepo
from faststream.rabbit import RabbitBroker, TestRabbitBroker

from notifications_worker.broker import broker
from notifications_worker.dependencies.smtp_client import provide_smtp_client


@pytest.fixture()
def smtp_client_mock() -> Iterator[AsyncMock]:
    mock = AsyncMock(spec=aiosmtplib.SMTP)

    def provide_fake_smtp_client(context: ContextRepo) -> Any:  # noqa: ARG001
        return mock

    with dependency_provider.scope(provide_smtp_client, provide_fake_smtp_client):
        yield mock


@pytest.fixture()
async def test_broker() -> AsyncIterator[RabbitBroker]:
    async with TestRabbitBroker(broker) as br:
        yield br
