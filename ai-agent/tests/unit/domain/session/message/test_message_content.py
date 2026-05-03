import pytest

from domain.session.message.errors import InvalidMessageContent
from domain.session.message.message_content import MessageContent


def test_given_a_non_falsy_value_when_creating_message_content_then_does_not_raise() -> None:
    MessageContent("hello world")


@pytest.mark.parametrize("value", ["", "   "])
def test_given_an_empty_value_when_creating_message_content_then_raises_invalid_message_content(value: str) -> None:
    with pytest.raises(InvalidMessageContent):
        MessageContent(value)


@pytest.mark.parametrize("value", [None, 123, 12.5, True, [], {}, ("a",), object()])
def test_given_a_non_string_value_when_creating_message_content_then_raises_invalid_message_content(value: object) -> None:
    with pytest.raises(InvalidMessageContent):
        MessageContent(value)  # type: ignore[arg-type]


def test_given_a_value_with_surrounding_whitespace_when_creating_message_content_then_value_is_trimmed() -> None:
    content = MessageContent("  hello  ")

    assert content.value == "hello"
