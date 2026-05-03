from unittest.mock import AsyncMock

import pytest

from application.set_system_prompt.set_system_prompt_command import (
    SetSystemPromptCommand,
)
from application.set_system_prompt.set_system_prompt_command_handler import (
    SetSystemPromptCommandHandler,
)
from domain.agent.errors import InvalidSystemPrompt
from domain.agent.system_prompt import SystemPrompt
from domain.agent.system_prompt_repository import SystemPromptRepository


def _build_handler(repository: AsyncMock) -> SetSystemPromptCommandHandler:
    return SetSystemPromptCommandHandler(system_prompt_repository=repository)


async def test_given_a_valid_content_when_setting_system_prompt_then_saves_a_system_prompt() -> None:
    repository = AsyncMock(spec=SystemPromptRepository)

    await _build_handler(repository).execute(
        SetSystemPromptCommand(content="you are helpful")
    )

    repository.save.assert_awaited_once()
    saved_prompt: SystemPrompt = repository.save.await_args.args[0]
    assert isinstance(saved_prompt, SystemPrompt)
    assert saved_prompt.value == "you are helpful"

@pytest.mark.parametrize("content", ["", "   "])
async def test_given_an_empty_content_when_setting_system_prompt_then_raises_and_does_not_save(content: str) -> None:
    repository = AsyncMock(spec=SystemPromptRepository)

    with pytest.raises(InvalidSystemPrompt):
        await _build_handler(repository).execute(SetSystemPromptCommand(content=content))

    repository.save.assert_not_awaited()
