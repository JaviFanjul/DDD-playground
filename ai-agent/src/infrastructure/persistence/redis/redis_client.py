from redis.asyncio import Redis

from config.config import RedisConfig


class RedisClient:
    def __init__(self, config: RedisConfig) -> None:
        self._redis: Redis = Redis(
            host=config.host,
            port=config.port,
            db=config.db,
            decode_responses=True,
        )

    async def get(self, key: str) -> str | None:
        return await self._redis.get(key)

    async def set(self, key: str, value: str) -> None:
        await self._redis.set(key, value)
