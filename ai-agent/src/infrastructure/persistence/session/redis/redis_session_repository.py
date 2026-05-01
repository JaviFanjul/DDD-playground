from infrastructure.persistence.session.redis.redis_client import RedisClient


class RedisSessionRepository:
    def __init__(self, client: RedisClient) -> None:
        self._client = client
