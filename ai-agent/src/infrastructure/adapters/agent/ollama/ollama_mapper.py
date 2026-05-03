from typing import ClassVar

from domain.session.message.assistant_message import AssistantMessage
from domain.session.message.message import Message
from domain.session.message.user_message import UserMessage


class OllamaMapper:
    _ROLE_BY_MESSAGE_TYPE: ClassVar[dict[type[Message], str]] = {
        UserMessage: "user",
        AssistantMessage: "assistant",
    }

    @staticmethod
    def to_ollama_message(message: Message) -> dict[str, str]:
        return {
            "role": OllamaMapper._ROLE_BY_MESSAGE_TYPE[type(message)],
            "content": message.content.value,
        }
