from typing import Protocol

from domain.session.message.message import Message
from domain.session.message.message_content import MessageContent


class Agent(Protocol):

    async def ainvoke(self, conversation: tuple[Message, ...]) -> MessageContent:
        ...
