from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.client import close_async_client, create_async_client
from core.database import create_db_and_tables, dispose_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await create_db_and_tables()
    await create_async_client()

    yield

    # Shutdown code
    await dispose_db()
    await close_async_client()
