from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aiosmtplib

from faststream import ContextRepo

from notifications_worker.settings import smtp_settings


@asynccontextmanager
async def initialize_smtp_client(context: ContextRepo) -> AsyncIterator[aiosmtplib.SMTP]:
    async with aiosmtplib.SMTP(
        hostname=smtp_settings.hostname,
        port=smtp_settings.port,
        use_tls=smtp_settings.use_tls,
        # must be specified for TLS using self-signed certs
        cert_bundle=str(smtp_settings.cert_bundle) if smtp_settings.cert_bundle else None,
    ) as client:
        await client.login(smtp_settings.username, smtp_settings.password.get_secret_value())
        context.set_global("smtp_client", client)
        yield client


def provide_smtp_client(context: ContextRepo) -> aiosmtplib.SMTP:
    return context.get("smtp_client")  # type: ignore[no-any-return]
