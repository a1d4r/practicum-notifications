from collections.abc import AsyncIterator

import httpx


async def provide_http_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient() as client:
        yield client
