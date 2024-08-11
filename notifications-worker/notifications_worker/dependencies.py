from collections.abc import AsyncIterator

import aiosmtplib

from notifications_worker.settings import smtp_settings


async def provide_smtp_client() -> AsyncIterator[aiosmtplib.SMTP]:
    async with aiosmtplib.SMTP(
        hostname=smtp_settings.hostname,
        port=smtp_settings.port,
        use_tls=smtp_settings.use_tls,
        cert_bundle=smtp_settings.cert_bundle,
    ) as client:
        await client.login(smtp_settings.username, smtp_settings.password.get_secret_value())
        yield client
