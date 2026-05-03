from domain.session.message.assistant_message import AssistantMessage
from domain.session.message.message_content import MessageContent
from domain.session.message.user_message import UserMessage
from infrastructure.adapters.agent.ollama.ollama_mapper import OllamaMapper


def test_given_a_user_message_when_mapping_to_ollama_then_role_is_user() -> None:
    message = UserMessage(MessageContent("hi"))

    result = OllamaMapper.to_ollama_message(message)

    assert result == {"role": "user", "content": "hi"}


def test_given_an_assistant_message_when_mapping_to_ollama_then_role_is_assistant() -> None:
    message = AssistantMessage(MessageContent("hello"))

    result = OllamaMapper.to_ollama_message(message)

    assert result == {"role": "assistant", "content": "hello"}

