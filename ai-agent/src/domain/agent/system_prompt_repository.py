from typing import Protocol

from domain.agent.system_prompt import SystemPrompt


class SystemPromptRepository(Protocol):

    async def get(self) -> SystemPrompt:
        ...

    async def save(self, system_prompt: SystemPrompt) -> None:
        ...