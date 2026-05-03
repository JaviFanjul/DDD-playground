from unittest.mock import AsyncMock

import pytest

from application.handle_message.handle_message_command import HandleMessageCommand
from application.handle_message.handle_message_command_handler import (
    HandleMessageCommandHandler,
)
from domain.agent.agent import Agent
from domain.agent.errors import SystemPromptNotConfigured
from domain.agent.system_prompt import SystemPrompt
from domain.agent.system_prompt_repository import SystemPromptRepository
from domain.session.message.assistant_message import AssistantMessage
from domain.session.message.message_content import MessageContent
from domain.session.message.user_message import UserMessage
from domain.session.session import Session
from domain.session.session_id import SessionId
from domain.session.session_repository import SessionRepository


def _a_command(session_id: str = "abc-123", content: str = "hi") -> HandleMessageCommand:
    return HandleMessageCommand(session_id=session_id, content=content)


def _a_system_prompt() -> SystemPrompt:
    return SystemPrompt("you are helpful")


def _build_handler(
    session_repository: AsyncMock,
    system_prompt_repository: AsyncMock,
    agent: AsyncMock,
) -> HandleMessageCommandHandler:
    return HandleMessageCommandHandler(
        session_repository=session_repository,
        system_prompt_repository=system_prompt_repository,
        agent=agent,
    )


async def test_given_an_empty_session_when_handling_a_message_then_returns_result_with_session_id_and_reply() -> None:
    session_repository = AsyncMock(spec=SessionRepository)
    system_prompt_repository = AsyncMock(spec=SystemPromptRepository)
    agent = AsyncMock(spec=Agent)
    session_repository.get.return_value = Session(SessionId("abc-123"))
    system_prompt_repository.get.return_value = _a_system_prompt()
    agent.ainvoke.return_value = MessageContent("hello user")

    result = await _build_handler(session_repository, system_prompt_repository, agent).execute(
        _a_command(session_id="abc-123", content="hi")
    )

    assert result.session_id == "abc-123"
    assert result.reply == "hello user"


async def test_given_a_message_when_handling_then_invokes_agent_with_conversation_and_system_prompt() -> None:
    session_repository = AsyncMock(spec=SessionRepository)
    system_prompt_repository = AsyncMock(spec=SystemPromptRepository)
    agent = AsyncMock(spec=Agent)
    session_repository.get.return_value = Session(SessionId("abc-123"))
    system_prompt = _a_system_prompt()
    system_prompt_repository.get.return_value = system_prompt
    agent.ainvoke.return_value = MessageContent("hello user")

    await _build_handler(session_repository, system_prompt_repository, agent).execute(
        _a_command(content="hi")
    )

    agent.ainvoke.assert_awaited_once()
    conversation, prompt_arg = agent.ainvoke.await_args.args
    assert prompt_arg is system_prompt
    assert len(conversation) == 1
    assert isinstance(conversation[0], UserMessage)
    assert conversation[0].content.value == "hi"


async def test_given_a_message_when_handling_then_saves_session_with_user_and_assistant_messages() -> None:
    session_repository = AsyncMock(spec=SessionRepository)
    system_prompt_repository = AsyncMock(spec=SystemPromptRepository)
    agent = AsyncMock(spec=Agent)
    session_repository.get.return_value = Session(SessionId("abc-123"))
    system_prompt_repository.get.return_value = _a_system_prompt()
    agent.ainvoke.return_value = MessageContent("hello user")

    await _build_handler(session_repository, system_prompt_repository, agent).execute(
        _a_command(content="hi")
    )

    session_repository.save.assert_awaited_once()
    saved_session: Session = session_repository.save.await_args.args[0]
    assert len(saved_session.messages) == 2
    assert isinstance(saved_session.messages[0], UserMessage)
    assert saved_session.messages[0].content.value == "hi"
    assert isinstance(saved_session.messages[1], AssistantMessage)
    assert saved_session.messages[1].content.value == "hello user"


async def test_given_an_existing_session_when_handling_a_message_then_appends_to_existing_messages() -> None:
    session_repository = AsyncMock(spec=SessionRepository)
    system_prompt_repository = AsyncMock(spec=SystemPromptRepository)
    agent = AsyncMock(spec=Agent)
    existing = Session(SessionId("abc-123"))
    existing.append_user_message(MessageContent("previous user"))
    existing.append_assistant_message(MessageContent("previous assistant"))
    session_repository.get.return_value = existing
    system_prompt_repository.get.return_value = _a_system_prompt()
    agent.ainvoke.return_value = MessageContent("new reply")

    await _build_handler(session_repository, system_prompt_repository, agent).execute(
        _a_command(content="new user")
    )

    saved_session: Session = session_repository.save.await_args.args[0]
    assert [m.content.value for m in saved_session.messages] == [
        "previous user",
        "previous assistant",
        "new user",
        "new reply",
    ]


async def test_given_no_system_prompt_configured_when_handling_then_propagates_error_and_does_not_save() -> None:
    session_repository = AsyncMock(spec=SessionRepository)
    system_prompt_repository = AsyncMock(spec=SystemPromptRepository)
    agent = AsyncMock(spec=Agent)
    system_prompt_repository.get.side_effect = SystemPromptNotConfigured("not set")

    with pytest.raises(SystemPromptNotConfigured):
        await _build_handler(session_repository, system_prompt_repository, agent).execute(
            _a_command()
        )

    session_repository.save.assert_not_awaited()
    agent.ainvoke.assert_not_awaited()
