from loguru import logger
from redis import asyncio as aioredis

from src.core.settings import settings

KeyType = bytes | str | memoryview
ValueType = bytes | str | memoryview | int | float


class Redis:
    @staticmethod
    async def set(*, key: KeyType, value: ValueType) -> None:
        redis = aioredis.from_url(settings.redis_dsn)

        async with redis.client() as connection:
            await connection.set(key, value)

        logger.info(f"Key {key} was set")

    @staticmethod
    async def get(*, key: KeyType) -> ValueType:
        redis = aioredis.from_url(settings.redis_dsn)

        async with redis.client() as connection:
            encoded = await connection.get(key)

        logger.info(f"Key {key} was read")

        return encoded

    @staticmethod
    async def delete(*, key: KeyType) -> None:
        redis = aioredis.from_url(settings.redis_dsn)

        async with redis.client() as connection:
            await connection.delete(key)

        logger.info(f"Key {key} was deleted")

    @staticmethod
    async def exists(*, key: KeyType) -> bool:
        redis = aioredis.from_url(settings.redis_dsn)

        async with redis.client() as connection:
            return bool(await connection.exists(key))

    @staticmethod
    async def flush_all() -> None:
        redis = aioredis.from_url(settings.redis_dsn)

        async with redis.client() as connection:
            await connection.flushall()

        logger.info("Redis database was flushed")
