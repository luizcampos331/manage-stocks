import os

from app.infra.services.cache import RedisCache

implementations = {
    "redis": RedisCache,
}


class CacheFactory:
    @staticmethod
    def make():
        implementation = os.getenv("CACHE_IMPLEMENTATION")
        if implementation not in implementations:
            raise ValueError(f"Unsupported CACHE_IMPLEMENTATION: {implementation}")

        return implementations[implementation]()
