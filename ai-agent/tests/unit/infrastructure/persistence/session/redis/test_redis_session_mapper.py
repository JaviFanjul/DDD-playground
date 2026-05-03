import json

import pytest

from domain.session.errors import SessionRepositoryError
from domain.session.message.assistant_message import AssistantMessage
from domain.session.message.message_content import MessageContent
from domain.session.message.user_message import UserMessage
from domain.session.session import Session
from domain.session.session_id import SessionId
from infrastructure.persistence.session.redis.redis_session_mapper import (
    RedisSessionMapper,
)


def _a_session_id() -> SessionId:
    return SessionId("abc-123")


def _content(value: str) -> MessageContent:
    return MessageContent(value)


def test_given_an_empty_session_when_to_json_then_returns_payload_with_empty_messages() -> None:
    session = Session(_a_session_id())

    payload = RedisSessionMapper.to_json(session)

    assert json.loads(payload) == {"id": "abc-123", "messages": []}


def test_given_a_session_with_alternating_messages_when_to_json_then_returns_ordered_payload() -> None:
    session = Session(_a_session_id())
    session.append_user_message(_content("hi"))
    session.append_assistant_message(_content("hello"))
    session.append_user_message(_content("how are you"))

    payload = RedisSessionMapper.to_json(session)

    assert json.loads(payload) == {
        "id": "abc-123",
        "messages": [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
            {"role": "user", "content": "how are you"},
        ],
    }


def test_given_a_payload_without_messages_when_from_json_then_returns_empty_session() -> None:
    payload = json.dumps({"id": "abc-123", "messages": []})

    session = RedisSessionMapper.from_json(payload, _a_session_id())

    assert session.id.value == "abc-123"
    assert session.messages == ()


def test_given_a_payload_with_messages_when_from_json_then_returns_session_with_messages() -> None:
    payload = json.dumps({
        "id": "abc-123",
        "messages": [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
        ],
    })

    session = RedisSessionMapper.from_json(payload, _a_session_id())

    assert session.id.value == "abc-123"
    assert len(session.messages) == 2
    assert isinstance(session.messages[0], UserMessage)
    assert session.messages[0].content.value == "hi"
    assert isinstance(session.messages[1], AssistantMessage)
    assert session.messages[1].content.value == "hello"


def test_given_a_session_when_to_json_and_from_json_then_roundtrip_preserves_state() -> None:
    original = Session(_a_session_id())
    original.append_user_message(_content("hi"))
    original.append_assistant_message(_content("hello"))

    payload = RedisSessionMapper.to_json(original)
    restored = RedisSessionMapper.from_json(payload, _a_session_id())

    assert restored.id.value == original.id.value
    assert len(restored.messages) == len(original.messages)
    for restored_message, original_message in zip(restored.messages, original.messages):
        assert type(restored_message) is type(original_message)
        assert restored_message.content.value == original_message.content.value


@pytest.mark.parametrize(
    "payload",
    [
        "not-json",
        "{",
        json.dumps({"id": "abc-123"}),
        json.dumps({"messages": []}),
        json.dumps({"id": "abc-123", "messages": [{"role": "user"}]}),
        json.dumps({"id": "abc-123", "messages": [{"content": "hi"}]}),
    ],
)
def test_given_a_corrupted_payload_when_from_json_then_raises_session_repository_error(payload: str) -> None:
    with pytest.raises(SessionRepositoryError):
        RedisSessionMapper.from_json(payload, _a_session_id())


def test_given_a_payload_with_unknown_role_when_from_json_then_raises_key_error() -> None:
    payload = json.dumps({
        "id": "abc-123",
        "messages": [{"role": "system", "content": "you are helpful"}],
    })

    with pytest.raises(KeyError):
        RedisSessionMapper.from_json(payload, _a_session_id())
