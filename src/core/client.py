from typing import Annotated, Optional

from fastapi import Depends
from httpx import AsyncClient

async_client: Optional[AsyncClient] = None


async def create_async_client():
    global async_client
    async_client = AsyncClient()


async def close_async_client():
    if async_client:
        await async_client.aclose()


async def get_async_client():
    if not async_client:
        raise Exception("AsyncClient not created")

    return async_client


AsyncClientDep = Annotated[AsyncClient, Depends(get_async_client)]
