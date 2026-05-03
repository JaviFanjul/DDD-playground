import structlog
from ollama import AsyncClient, ResponseError

from config.config import OllamaConfig
from domain.agent.agent import Agent
from domain.agent.errors import AgentInvocationError
from domain.agent.system_prompt import SystemPrompt
from domain.session.message.message import Message
from domain.session.message.message_content import MessageContent
from infrastructure.adapters.agent.ollama.ollama_mapper import OllamaMapper


logger = structlog.get_logger(__name__)


class OllamaAgent(Agent):
    def __init__(self, config: OllamaConfig) -> None:
        self._client: AsyncClient = AsyncClient(host=config.host)
        self._model: str = config.model

    async def ainvoke(
        self,
        conversation: tuple[Message, ...],
        system_prompt: SystemPrompt,
    ) -> MessageContent:
        messages: list[dict[str, str]] = [
            OllamaMapper.to_ollama_system_message(system_prompt),
            *(OllamaMapper.to_ollama_message(m) for m in conversation),
        ]
        logger.info("Invoking Ollama agent")
        try:
            response = await self._client.chat(model=self._model, messages=messages)
        except (ResponseError, ConnectionError, TimeoutError) as error:
            raise AgentInvocationError(f"Ollama agent invocation failed: {error}") from error
        logger.info("Ollama agent responded successfully")
        return MessageContent(response.message.content)
