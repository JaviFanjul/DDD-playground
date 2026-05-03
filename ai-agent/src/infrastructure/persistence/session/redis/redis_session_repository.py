from redis.exceptions import RedisError

from domain.session.errors import SessionRepositoryError
from domain.session.session import Session
from domain.session.session_id import SessionId
from domain.session.session_repository import SessionRepository
from infrastructure.persistence.session.redis.redis_client import RedisClient
from infrastructure.persistence.session.redis.redis_session_mapper import (
    RedisSessionMapper,
)


_KEY_PREFIX = "session:"


class RedisSessionRepository(SessionRepository):
    def __init__(self, client: RedisClient) -> None:
        self._client = client

    async def get(self, session_id: SessionId) -> Session:
        payload: str | None = await self._load_payload(session_id)
        if payload is None:
            return Session(session_id)
        return RedisSessionMapper.from_json(payload, session_id)

    async def _load_payload(self, session_id: SessionId) -> str | None:
        try:
            return await self._client.get(self._key_for(session_id))
        except RedisError as error:
            raise SessionRepositoryError(
                f"Failed to load session {session_id.value}: {error}"
            ) from error
        
    async def save(self, session: Session) -> None:
        payload: str = RedisSessionMapper.to_json(session)
        await self._store_payload(session.id, payload)

    async def _store_payload(self, session_id: SessionId, payload: str) -> None:
        try:
            await self._client.set(self._key_for(session_id), payload)
        except RedisError as error:
            raise SessionRepositoryError(
                f"Failed to save session {session_id.value}: {error}"
            ) from error

    @staticmethod
    def _key_for(session_id: SessionId) -> str:
        return f"{_KEY_PREFIX}{session_id.value}"
