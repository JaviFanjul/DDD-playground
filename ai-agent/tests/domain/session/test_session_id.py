import pytest

from domain.session.errors import InvalidSessionId
from domain.session.session_id import SessionId


def test_when_value_is_not_falsy_then_does_not_raise() -> None:
    SessionId("abc-123")


@pytest.mark.parametrize("value", ["", "   ", None])
def test_when_value_is_falsy_then_raises_invalid_session_id(value: str) -> None:
    with pytest.raises(InvalidSessionId):
        SessionId(value)
