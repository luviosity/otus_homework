"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""

import asyncio
import functools
import logging
from typing import Any, TypeAlias

import aiohttp
from config import get_settings
from errors import ApiError

settings = get_settings()
USERS_DATA_URL = f"{settings.api_url}/users"
POSTS_DATA_URL = f"{settings.api_url}/posts"

log = logging.getLogger("homework_04")

API_RESPONSE_TYPE: TypeAlias = list[dict[str, Any]]


def retry_with_backoff(retries: int = 3, backoff_in_ms: int = 100):
    """Decorator to retry api calls with exponential backoff"""

    def wrapper(f):
        @functools.wraps(f)
        async def wrapped(*args, **kwargs):
            n: int = 0
            while True:
                try:
                    log.debug("Retry attempt %d for %s", n + 1, f.__name__)
                    return await f(*args, **kwargs)
                except (aiohttp.ClientError, asyncio.TimeoutError, Exception) as e:
                    n += 1
                    if n >= retries:
                        log.error(
                            "All %d retries failed for %s: %s", retries, f.__name__, e
                        )
                        raise ApiError(f"Failed after {retries} retries") from e
                    delay: int = backoff_in_ms * 2**n
                    await asyncio.sleep(delay / 1000)

        return wrapped

    return wrapper


async def fetch_json(url: str) -> API_RESPONSE_TYPE:
    """Fetch json response from api call"""
    log.info("Fetching %s", url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            log.debug("Fetched data from %s: %s", url, result)
            return result


@retry_with_backoff()
async def fetch_user_data():
    return await fetch_json(USERS_DATA_URL)


@retry_with_backoff()
async def fetch_posts_data():
    return await fetch_json(POSTS_DATA_URL)


async def fetch_users_and_posts() -> tuple[API_RESPONSE_TYPE, API_RESPONSE_TYPE]:
    users, posts = await asyncio.gather(
        fetch_user_data(),
        fetch_posts_data(),
    )
    return users, posts


if __name__ == "__main__":
    from pprint import pprint

    fetched_users, fetched_posts = asyncio.run(fetch_users_and_posts())
    pprint(f"USERS: {fetched_users}")
    pprint(f"POSTS: {fetched_posts}")
