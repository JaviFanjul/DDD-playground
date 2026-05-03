from injector import Module, provider, singleton

from application.handle_message.handle_message_command_handler import (
    HandleMessageCommandHandler,
)
from application.set_system_prompt.set_system_prompt_command_handler import (
    SetSystemPromptCommandHandler,
)
from config.config import OllamaConfig, RedisConfig, get_config
from domain.agent.agent import Agent
from domain.agent.system_prompt_repository import SystemPromptRepository
from domain.session.session_repository import SessionRepository
from infrastructure.adapters.agent.ollama.ollama_agent import OllamaAgent
from infrastructure.persistence.redis.redis_client import RedisClient
from infrastructure.persistence.redis.session.redis_session_repository import (
    RedisSessionRepository,
)
from infrastructure.persistence.redis.system_prompt.redis_system_prompt_repository import (
    RedisSystemPromptRepository,
)


class AppModule(Module):

    @singleton
    @provider
    def provide_redis_config(self) -> RedisConfig:
        return get_config().redis

    @singleton
    @provider
    def provide_redis_client(self, config: RedisConfig) -> RedisClient:
        return RedisClient(config)

    @singleton
    @provider
    def provide_session_repository(self, client: RedisClient) -> SessionRepository:
        return RedisSessionRepository(client)

    @singleton
    @provider
    def provide_system_prompt_repository(
        self, client: RedisClient
    ) -> SystemPromptRepository:
        return RedisSystemPromptRepository(client)

    @singleton
    @provider
    def provide_ollama_config(self) -> OllamaConfig:
        return get_config().ollama

    @singleton
    @provider
    def provide_agent(self, config: OllamaConfig) -> Agent:
        return OllamaAgent(config)

    @provider
    def provide_handle_message_command_handler(
        self,
        session_repository: SessionRepository,
        system_prompt_repository: SystemPromptRepository,
        agent: Agent,
    ) -> HandleMessageCommandHandler:
        return HandleMessageCommandHandler(
            session_repository, system_prompt_repository, agent
        )

    @provider
    def provide_set_system_prompt_command_handler(
        self, system_prompt_repository: SystemPromptRepository
    ) -> SetSystemPromptCommandHandler:
        return SetSystemPromptCommandHandler(system_prompt_repository)
