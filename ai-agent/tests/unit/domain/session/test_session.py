import pytest

from domain.session.errors import InvalidMessageOrder
from domain.session.message.assistant_message import AssistantMessage
from domain.session.message.message_content import MessageContent
from domain.session.message.user_message import UserMessage
from domain.session.session import Session
from domain.session.session_id import SessionId


def _a_session() -> Session:
    return Session(SessionId("abc-123"))


def _content(value: str = "hello") -> MessageContent:
    return MessageContent(value)


def test_given_a_new_session_when_created_then_has_no_messages() -> None:
    session = _a_session()

    assert session.messages == ()


def test_given_an_empty_session_when_appending_a_user_message_then_message_is_added() -> None:
    session = _a_session()

    session.append_user_message(_content("hi"))

    assert len(session.messages) == 1
    assert isinstance(session.messages[0], UserMessage)
    assert session.messages[0].content.value == "hi"


def test_given_a_session_with_a_user_message_when_appending_an_assistant_message_then_message_is_added() -> None:
    session = _a_session()
    session.append_user_message(_content("hi"))

    session.append_assistant_message(_content("hello"))

    assert len(session.messages) == 2
    assert isinstance(session.messages[1], AssistantMessage)
    assert session.messages[1].content.value == "hello"


def test_given_a_session_with_a_user_message_when_appending_another_user_message_then_raises_invalid_message_order() -> None:
    session = _a_session()
    session.append_user_message(_content("hi"))

    with pytest.raises(InvalidMessageOrder):
        session.append_user_message(_content("hi again"))


def test_given_an_empty_session_when_appending_an_assistant_message_then_raises_invalid_message_order() -> None:
    session = _a_session()

    with pytest.raises(InvalidMessageOrder):
        session.append_assistant_message(_content("hello"))


def test_given_a_session_ending_in_assistant_message_when_appending_another_assistant_message_then_raises_invalid_message_order() -> None:
    session = _a_session()
    session.append_user_message(_content("hi"))
    session.append_assistant_message(_content("hello"))

    with pytest.raises(InvalidMessageOrder):
        session.append_assistant_message(_content("hello again"))

