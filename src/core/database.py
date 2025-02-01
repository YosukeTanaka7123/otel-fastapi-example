from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import get_settings

settings = get_settings()
async_engine = create_async_engine(settings.db_url)


async def create_db_and_tables():
    import tables  # noqa F401

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def dispose_db():
    await async_engine.dispose()


async def get_async_session():
    async with AsyncSession(async_engine, expire_on_commit=False) as async_session:
        try:
            yield async_session
            await async_session.commit()
        except Exception as e:
            await async_session.rollback()
            raise e


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
