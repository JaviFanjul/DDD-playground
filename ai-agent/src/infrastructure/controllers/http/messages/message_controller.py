import structlog
from fastapi import APIRouter, status
from fastapi_injector import Injected

from application.handle_message.handle_message_command import HandleMessageCommand
from application.handle_message.handle_message_command_handler import (
    HandleMessageCommandHandler,
)
from application.handle_message.handle_message_command_result import (
    HandleMessageCommandResult,
)
from infrastructure.controllers.http.messages.requests import SendMessageRequest
from infrastructure.controllers.http.messages.responses import SendMessageResponse

router = APIRouter(tags=["messages"])
logger = structlog.get_logger(__name__)


@router.post("/chat", status_code=status.HTTP_200_OK)
async def send_message(
    payload: SendMessageRequest,
    handler: HandleMessageCommandHandler = Injected(HandleMessageCommandHandler),
) -> SendMessageResponse:
    command: HandleMessageCommand = HandleMessageCommand(
        session_id=payload.session_id,
        content=payload.content,
    )
    logger.info("Handling message", id=payload.session_id)
    result: HandleMessageCommandResult = await handler.execute(command)
    logger.info("Message handled successfully", id=payload.session_id)
    return SendMessageResponse(session_id=result.session_id, reply=result.reply)
