import redis

from core.config import settings


def cache():
    return redis.Redis(
        host=settings.redis_server,
        port=settings.redis_port,
    )
