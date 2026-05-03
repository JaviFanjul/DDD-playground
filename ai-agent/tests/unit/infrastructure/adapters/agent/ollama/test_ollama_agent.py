from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from ollama import AsyncClient, ResponseError

from config.config import OllamaConfig
from domain.agent.errors import AgentInvocationError
from domain.agent.system_prompt import SystemPrompt
from domain.session.message.message_content import MessageContent
from domain.session.message.user_message import UserMessage
from infrastructure.adapters.agent.ollama.ollama_agent import OllamaAgent


def _build_agent_with_mocked_client(client: AsyncMock) -> OllamaAgent:
    agent = OllamaAgent(OllamaConfig(host="http://localhost", model="test-model"))
    agent._client = client
    return agent


def _ollama_response(content: str) -> SimpleNamespace:
    return SimpleNamespace(message=SimpleNamespace(content=content))


async def test_given_a_conversation_and_system_prompt_when_invoking_then_calls_chat_with_system_first_and_conversation_in_order() -> None:
    client = AsyncMock(spec=AsyncClient)
    client.chat.return_value = _ollama_response("reply")
    agent = _build_agent_with_mocked_client(client)
    conversation = (UserMessage(MessageContent("hi")),)

    await agent.ainvoke(conversation, SystemPrompt("you are helpful"))

    client.chat.assert_awaited_once()
    kwargs = client.chat.await_args.kwargs
    assert kwargs["model"] == "test-model"
    assert kwargs["messages"] == [
        {"role": "system", "content": "you are helpful"},
        {"role": "user", "content": "hi"},
    ]


async def test_given_an_ollama_response_when_invoking_then_returns_message_content_with_reply() -> None:
    client = AsyncMock(spec=AsyncClient)
    client.chat.return_value = _ollama_response("hello user")
    agent = _build_agent_with_mocked_client(client)

    reply = await agent.ainvoke(
        (UserMessage(MessageContent("hi")),), SystemPrompt("be helpful")
    )

    assert isinstance(reply, MessageContent)
    assert reply.value == "hello user"


@pytest.mark.parametrize(
    "error",
    [
        ResponseError("model not found"),
        ConnectionError("refused"),
        TimeoutError("timeout"),
    ],
)
async def test_given_ollama_fails_when_invoking_then_raises_agent_invocation_error(error: Exception) -> None:
    client = AsyncMock(spec=AsyncClient)
    client.chat.side_effect = error
    agent = _build_agent_with_mocked_client(client)

    with pytest.raises(AgentInvocationError):
        await agent.ainvoke(
            (UserMessage(MessageContent("hi")),), SystemPrompt("be helpful")
        )
