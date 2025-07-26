import os
from abc import ABC, abstractmethod

import redis.asyncio as redis


class Cache(ABC):
    @abstractmethod
    async def delete(self, key: str) -> None:
        pass


class RedisCache(Cache):
    def __init__(self):
        self.redis_url = os.getenv("CACHE_URL")
        self.client = redis.from_url(self.redis_url, decode_responses=True)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)
