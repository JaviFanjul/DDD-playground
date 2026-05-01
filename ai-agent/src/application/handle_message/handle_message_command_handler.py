from application.handle_message.handle_message_command import HandleMessageCommand
from domain.session.session_repository import SessionRepository


class HandleMessageCommandHandler:
    def __init__(self, session_repository: SessionRepository) -> None:
        self._session_repository = session_repository

    async def execute(self, command: HandleMessageCommand) -> None:
        raise NotImplementedError
