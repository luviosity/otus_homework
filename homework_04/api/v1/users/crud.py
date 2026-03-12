"""
Модуль для работы с запросами в базу данных
"""

import logging

from models import User
from schemas import UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


class Crud:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self):
        stm = select(User).order_by(User.name)
        log.info("Getting all users.")
        users = await self.session.scalars(stm)
        return list(users)

    async def get_user(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def create_user(
        self,
        user_create: UserCreate,
    ) -> User:
        user = User(
            **user_create.model_dump(),
        )
        self.session.add(user)
        await self.session.commit()
        # await self.session.refresh(user)
        return user
