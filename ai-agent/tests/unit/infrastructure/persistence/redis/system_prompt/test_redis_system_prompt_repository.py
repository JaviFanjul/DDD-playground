from unittest.mock import AsyncMock

import pytest
from redis.exceptions import RedisError

from domain.agent.errors import SystemPromptNotConfigured, SystemPromptRepositoryError
from domain.agent.system_prompt import SystemPrompt
from infrastructure.persistence.redis.redis_client import RedisClient
from infrastructure.persistence.redis.system_prompt.redis_system_prompt_repository import (
    RedisSystemPromptRepository,
)


async def test_given_a_stored_value_when_getting_then_returns_system_prompt() -> None:
    client = AsyncMock(spec=RedisClient)
    client.get.return_value = "you are helpful"

    prompt = await RedisSystemPromptRepository(client).get()

    assert isinstance(prompt, SystemPrompt)
    assert prompt.value == "you are helpful"


async def test_given_no_stored_value_when_getting_then_raises_system_prompt_not_configured() -> None:
    client = AsyncMock(spec=RedisClient)
    client.get.return_value = None

    with pytest.raises(SystemPromptNotConfigured):
        await RedisSystemPromptRepository(client).get()


async def test_given_redis_fails_when_getting_then_raises_system_prompt_repository_error() -> None:
    client = AsyncMock(spec=RedisClient)
    client.get.side_effect = RedisError("connection refused")

    with pytest.raises(SystemPromptRepositoryError):
        await RedisSystemPromptRepository(client).get()


async def test_given_a_system_prompt_when_saving_then_writes_raw_value_under_fixed_key() -> None:
    client = AsyncMock(spec=RedisClient)
    prompt = SystemPrompt("be concise")

    await RedisSystemPromptRepository(client).save(prompt)

    client.set.assert_awaited_once_with("system_prompt", "be concise")


async def test_given_redis_fails_when_saving_then_raises_system_prompt_repository_error() -> None:
    client = AsyncMock(spec=RedisClient)
    client.set.side_effect = RedisError("connection refused")

    with pytest.raises(SystemPromptRepositoryError):
        await RedisSystemPromptRepository(client).save(SystemPrompt("be concise"))
