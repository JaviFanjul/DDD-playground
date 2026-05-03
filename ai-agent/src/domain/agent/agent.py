from typing import Protocol

from domain.agent.system_prompt import SystemPrompt
from domain.session.message.message import Message
from domain.session.message.message_content import MessageContent


class Agent(Protocol):

    async def ainvoke(
        self,
        conversation: tuple[Message, ...],
        system_prompt: SystemPrompt,
    ) -> MessageContent:
        ...
