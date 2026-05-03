from application.set_system_prompt.set_system_prompt_command import (
    SetSystemPromptCommand,
)
from domain.agent.system_prompt import SystemPrompt
from domain.agent.system_prompt_repository import SystemPromptRepository


class SetSystemPromptCommandHandler:
    def __init__(self, system_prompt_repository: SystemPromptRepository) -> None:
        self._system_prompt_repository = system_prompt_repository

    async def execute(self, command: SetSystemPromptCommand) -> None:
        prompt: SystemPrompt = SystemPrompt(command.content)
        await self._system_prompt_repository.save(prompt)
