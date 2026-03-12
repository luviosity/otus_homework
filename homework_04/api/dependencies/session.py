from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from models import async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


GetAsyncSession = Annotated[
    AsyncSession,
    Depends(get_async_session),
]
