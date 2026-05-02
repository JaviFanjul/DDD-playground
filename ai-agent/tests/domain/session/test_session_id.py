import pytest

from domain.session.errors import InvalidSessionId
from domain.session.session_id import SessionId


def test_given_a_non_falsy_value_when_creating_session_id_then_does_not_raise() -> None:
    SessionId("abc-123")


@pytest.mark.parametrize("value", ["", "   "])
def test_given_an_empty_value_when_creating_session_id_then_raises_invalid_session_id(value: str) -> None:
    with pytest.raises(InvalidSessionId):
        SessionId(value)


@pytest.mark.parametrize("value", [None, 123, 12.5, True, [], {}, ("a",), object()])
def test_given_a_non_string_value_when_creating_session_id_then_raises_invalid_session_id(value: object) -> None:
    with pytest.raises(InvalidSessionId):
        SessionId(value)  # type: ignore[arg-type]
