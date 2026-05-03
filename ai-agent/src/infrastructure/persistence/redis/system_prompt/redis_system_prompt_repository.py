import structlog
from redis.exceptions import RedisError

from domain.agent.errors import SystemPromptNotConfigured, SystemPromptRepositoryError
from domain.agent.system_prompt import SystemPrompt
from domain.agent.system_prompt_repository import SystemPromptRepository
from infrastructure.persistence.redis.redis_client import RedisClient


_KEY = "system_prompt"
logger = structlog.get_logger(__name__)


class RedisSystemPromptRepository(SystemPromptRepository):
    def __init__(self, client: RedisClient) -> None:
        self._client = client

    async def get(self) -> SystemPrompt:
        logger.info("Retrieving system prompt")
        value: str | None = await self._load_value()
        if value is None:
            raise SystemPromptNotConfigured("System prompt has not been configured")
        logger.info("System prompt retrieved successfully")
        return SystemPrompt(value)
    
    async def _load_value(self) -> str | None:
        try:
            return await self._client.get(_KEY)
        except RedisError as error:
            raise SystemPromptRepositoryError(
                f"Failed to load system prompt: {error}"
            ) from error
    
    async def save(self, system_prompt: SystemPrompt) -> None:
        logger.info("Saving system prompt")
        await self._store_value(system_prompt.value)
        logger.info("System prompt saved successfully")


    async def _store_value(self, value: str) -> None:
        try:
            await self._client.set(_KEY, value)
        except RedisError as error:
            raise SystemPromptRepositoryError(
                f"Failed to save system prompt: {error}"
            ) from error
