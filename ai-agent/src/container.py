from injector import Module, provider, singleton

from application.handle_message.handle_message_command_handler import (
    HandleMessageCommandHandler,
)
from config.config import RedisConfig, get_config
from domain.session.session_repository import SessionRepository
from infrastructure.persistence.session.redis.redis_client import RedisClient
from infrastructure.persistence.session.redis.redis_session_repository import (
    RedisSessionRepository,
)


class AppModule(Module):

    @singleton
    @provider
    def provide_redis_config(self) -> RedisConfig:
        return get_config().redis

    @singleton
    @provider
    def provide_redis_client(self, config: RedisConfig) -> RedisClient:
        return RedisClient()

    @singleton
    @provider
    def provide_session_repository(self, client: RedisClient) -> SessionRepository:
        return RedisSessionRepository(client)

    @provider
    def provide_handle_message_command_handler(
        self, session_repository: SessionRepository
    ) -> HandleMessageCommandHandler:
        return HandleMessageCommandHandler(session_repository)
