from unittest.mock import AsyncMock

import pytest
from redis.exceptions import RedisError

from domain.session.errors import SessionRepositoryError
from domain.session.message.assistant_message import AssistantMessage
from domain.session.message.message_content import MessageContent
from domain.session.message.user_message import UserMessage
from domain.session.session import Session
from domain.session.session_id import SessionId
from infrastructure.persistence.redis.redis_client import RedisClient
from infrastructure.persistence.redis.session.redis_session_mapper import (
    RedisSessionMapper,
)
from infrastructure.persistence.redis.session.redis_session_repository import (
    RedisSessionRepository,
)


def _a_session_id() -> SessionId:
    return SessionId("abc-123")


async def test_given_no_existing_payload_when_getting_then_returns_empty_session() -> None:
    client = AsyncMock(spec=RedisClient)
    client.get.return_value = None

    session = await RedisSessionRepository(client).get(_a_session_id())

    assert session.id.value == "abc-123"
    assert session.messages == ()


async def test_given_an_existing_payload_when_getting_then_returns_rehydrated_session() -> None:
    client = AsyncMock(spec=RedisClient)
    stored = Session(_a_session_id())
    stored.append_user_message(MessageContent("hi"))
    stored.append_assistant_message(MessageContent("hello"))
    client.get.return_value = RedisSessionMapper.to_json(stored)

    session = await RedisSessionRepository(client).get(_a_session_id())

    assert session.id.value == "abc-123"
    assert len(session.messages) == 2
    assert isinstance(session.messages[0], UserMessage)
    assert session.messages[0].content.value == "hi"
    assert isinstance(session.messages[1], AssistantMessage)
    assert session.messages[1].content.value == "hello"


async def test_given_redis_fails_when_getting_then_raises_session_repository_error() -> None:
    client = AsyncMock(spec=RedisClient)
    client.get.side_effect = RedisError("connection refused")

    with pytest.raises(SessionRepositoryError):
        await RedisSessionRepository(client).get(_a_session_id())


async def test_given_a_session_when_saving_then_writes_serialized_payload_under_prefixed_key() -> None:
    client = AsyncMock(spec=RedisClient)
    session = Session(_a_session_id())
    session.append_user_message(MessageContent("hi"))

    await RedisSessionRepository(client).save(session)

    client.set.assert_awaited_once()
    key, payload = client.set.await_args.args
    assert key == "session:abc-123"
    assert payload == RedisSessionMapper.to_json(session)


async def test_given_redis_fails_when_saving_then_raises_session_repository_error() -> None:
    client = AsyncMock(spec=RedisClient)
    client.set.side_effect = RedisError("connection refused")
    session = Session(_a_session_id())

    with pytest.raises(SessionRepositoryError):
        await RedisSessionRepository(client).save(session)
