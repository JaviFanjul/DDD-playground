from domain.session.errors import InvalidSessionId


class SessionId:
    _value: str

    def __init__(self, value: str) -> None:
        self._set_value(value)

    def _set_value(self, value: str) -> None:
        self._ensure_value_is_not_empty(value)
        self._value = value.strip()

    @staticmethod
    def _ensure_value_is_not_empty(value: str) -> None:
        if value is None or not isinstance(value, str) or not value.strip():
            raise InvalidSessionId("SessionId must be a non-empty string")

    @property
    def value(self) -> str:
        return self._value

