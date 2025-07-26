import os
from abc import ABC, abstractmethod
from typing import Any, Optional, TypedDict

import redis.asyncio as redis


class SetCache(TypedDict):
    key: str
    value: str
    ttl: Optional[int]


class Cache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    async def set(self, data: SetCache) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def ping(self) -> bool:
        pass


class RedisCache(Cache):
    def __init__(self):
        self.redis_url = os.getenv("CACHE_URL")
        self.client = redis.from_url(self.redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        value = await self.client.get(key)
        return value or None

    async def set(self, data: SetCache) -> None:
        await self.client.set(name=data["key"], value=data["value"], ex=data["ttl"])

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def ping(self) -> bool:
        await self.client.ping()
