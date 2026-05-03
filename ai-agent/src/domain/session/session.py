from domain.session.errors import InvalidMessageOrder
from domain.session.message.assistant_message import AssistantMessage
from domain.session.message.message import Message
from domain.session.message.message_content import MessageContent
from domain.session.message.user_message import UserMessage
from domain.session.session_id import SessionId


class Session:
    _id: SessionId
    _messages: list[Message]

    def __init__(self, session_id: SessionId) -> None:
        self._id = session_id
        self._messages = []

    @property
    def id(self) -> SessionId:
        return self._id

    @property
    def messages(self) -> tuple[Message, ...]:
        return tuple(self._messages)

    def append_user_message(self, content: MessageContent) -> None:
        self._ensure_user_message_can_be_appended()
        self._messages.append(UserMessage(content))

    def append_assistant_message(self, content: MessageContent) -> None:
        self._ensure_assistant_message_can_be_appended()
        self._messages.append(AssistantMessage(content))

    def _ensure_user_message_can_be_appended(self) -> None:
        if self._last_message_is_from_user():
            raise InvalidMessageOrder(
                "A UserMessage cannot follow another UserMessage"
            )

    def _ensure_assistant_message_can_be_appended(self) -> None:
        if self._has_no_messages():
            raise InvalidMessageOrder(
                "Session must start with a UserMessage"
            )
        if self._last_message_is_from_assistant():
            raise InvalidMessageOrder(
                "An AssistantMessage cannot follow another AssistantMessage"
            )

    def _has_no_messages(self) -> bool:
        return not self._messages

    def _last_message_is_from_user(self) -> bool:
        return bool(self._messages) and isinstance(self._messages[-1], UserMessage)

    def _last_message_is_from_assistant(self) -> bool:
        return bool(self._messages) and isinstance(
            self._messages[-1], AssistantMessage
        )
