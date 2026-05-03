import structlog
from fastapi import APIRouter, status
from fastapi_injector import Injected

from application.set_system_prompt.set_system_prompt_command import (
    SetSystemPromptCommand,
)
from application.set_system_prompt.set_system_prompt_command_handler import (
    SetSystemPromptCommandHandler,
)
from infrastructure.controllers.http.system_prompt.requests import (
    SetSystemPromptRequest,
)

router = APIRouter(tags=["system_prompt"])
logger = structlog.get_logger(__name__)


@router.post("/system-prompt", status_code=status.HTTP_204_NO_CONTENT)
async def set_system_prompt(
    payload: SetSystemPromptRequest,
    handler: SetSystemPromptCommandHandler = Injected(SetSystemPromptCommandHandler),
) -> None:
    command: SetSystemPromptCommand = SetSystemPromptCommand(content=payload.content)
    logger.info("Setting system prompt")
    await handler.execute(command)
    logger.info("System prompt set successfully")
