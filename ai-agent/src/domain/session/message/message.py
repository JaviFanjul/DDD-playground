from abc import ABC

from domain.session.message.message_content import MessageContent


class Message(ABC):
    _content: MessageContent

    def __init__(self, content: MessageContent) -> None:
        self._content = content

    @property
    def content(self) -> MessageContent:
        return self._content
