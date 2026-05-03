from application.handle_message.handle_message_command import HandleMessageCommand
from application.handle_message.handle_message_command_result import (
    HandleMessageCommandResult,
)
from domain.agent.agent import Agent
from domain.session.message.message_content import MessageContent
from domain.session.session import Session
from domain.session.session_id import SessionId
from domain.session.session_repository import SessionRepository


class HandleMessageCommandHandler:
    def __init__(self, session_repository: SessionRepository, agent: Agent) -> None:
        self._session_repository = session_repository
        self._agent = agent

    async def execute(self, command: HandleMessageCommand) -> HandleMessageCommandResult:
        session_id: SessionId = SessionId(command.session_id)
        content: MessageContent = MessageContent(command.content)

        session: Session = await self._session_repository.get(session_id=session_id)
        session.append_user_message(content)

        reply: MessageContent = await self._agent.ainvoke(session.messages)
        session.append_assistant_message(reply)

        await self._session_repository.save(session)

        return HandleMessageCommandResult(
            session_id=session_id.value,
            reply=reply.value,
        )
