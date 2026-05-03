from ollama import AsyncClient, ResponseError

from config.config import OllamaConfig
from domain.agent.agent import Agent
from domain.agent.errors import AgentInvocationError
from domain.session.message.message import Message
from domain.session.message.message_content import MessageContent
from infrastructure.adapters.agent.ollama.ollama_mapper import OllamaMapper


class OllamaAgent(Agent):
    def __init__(self, config: OllamaConfig) -> None:
        self._client: AsyncClient = AsyncClient(host=config.host)
        self._model: str = config.model

    async def ainvoke(self, conversation: tuple[Message, ...]) -> MessageContent:
        messages: list[dict[str, str]] = [
            OllamaMapper.to_ollama_message(m) for m in conversation
        ]
        try:
            response = await self._client.chat(model=self._model, messages=messages)
        except (ResponseError, ConnectionError, TimeoutError) as error:
            raise AgentInvocationError(f"Ollama agent invocation failed: {error}") from error
        return MessageContent(response.message.content)
