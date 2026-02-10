"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio
import logging

from config import setup_logging
from jsonplaceholder_requests import API_RESPONSE_TYPE, fetch_users_and_posts
from models import Post, User, async_session
from sqlalchemy.ext.asyncio import AsyncSession

setup_logging()
log = logging.getLogger("homework_04")


async def load_users(
    session: AsyncSession,
    users: API_RESPONSE_TYPE,
) -> None:
    if not users:
        return

    log.info("Loading users")
    users_to_add: list[User] = []
    for user in users:
        new_user = User(
            external_id=user["id"],
            name=user["name"],
            username=user["username"],
            email=user["email"],
        )
        users_to_add.append(new_user)
    session.add_all(users_to_add)
    await session.commit()


async def load_posts(session: AsyncSession, posts: API_RESPONSE_TYPE) -> None:
    if not posts:
        return

    log.info("Loading posts")
    posts_to_add: list[Post] = []
    for post in posts:
        new_post = Post(
            external_id=post["id"],
            user_id=post["userId"],
            title=post["title"],
            body=post["body"],
        )
        posts_to_add.append(new_post)
    session.add_all(posts_to_add)
    await session.commit()


async def async_main():
    users, posts = await fetch_users_and_posts()
    async with async_session() as session:
        await load_users(session, users)
        await load_posts(session, posts)


if __name__ == "__main__":
    asyncio.run(async_main())
