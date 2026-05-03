from pydantic import ValidationError

from domain.session.errors import SessionRepositoryError
from domain.session.message.assistant_message import AssistantMessage
from domain.session.message.message import Message
from domain.session.message.message_content import MessageContent
from domain.session.message.user_message import UserMessage
from domain.session.session import Session
from domain.session.session_id import SessionId
from infrastructure.persistence.redis.session.redis_session_dto import (
    RedisMessageDto,
    RedisSessionDto,
)


_ROLE_BY_MESSAGE_TYPE: dict[type[Message], str] = {
    UserMessage: "user",
    AssistantMessage: "assistant",
}
_MESSAGE_TYPE_BY_ROLE: dict[str, type[Message]] = {
    role: message_type for message_type, role in _ROLE_BY_MESSAGE_TYPE.items()
}


class RedisSessionMapper:

    @staticmethod
    def to_json(session: Session) -> str:
        dto = RedisSessionDto(
            id=session.id.value,
            messages=[
                RedisMessageDto(
                    role=_ROLE_BY_MESSAGE_TYPE[type(message)],
                    content=message.content.value,
                )
                for message in session.messages
            ],
        )
        return dto.model_dump_json()

    @staticmethod
    def from_json(payload: str, session_id: SessionId) -> Session:
        try:
            dto = RedisSessionDto.model_validate_json(payload)
        except ValidationError as error:
            raise SessionRepositoryError(
                f"Corrupted session payload for {session_id.value}: {error}"
            ) from error

        messages = tuple(
            _MESSAGE_TYPE_BY_ROLE[message.role](MessageContent(message.content))
            for message in dto.messages
        )
        return Session.rehydrate(session_id=session_id, messages=messages)
