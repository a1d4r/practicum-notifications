from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from faststream import ContextRepo, FastStream

from notifications_worker.broker import broker
from notifications_worker.dependencies import initialize_smtp_client


@asynccontextmanager
async def lifespan(context: ContextRepo) -> AsyncIterator[None]:
    async with initialize_smtp_client(context):
        yield


app = FastStream(broker, title="Notifications worker", version="0.1.0", lifespan=lifespan)

import notifications_worker.handlers  # noqa: F401, E402
