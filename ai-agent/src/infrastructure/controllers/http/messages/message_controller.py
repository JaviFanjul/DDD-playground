import structlog
from fastapi import APIRouter, status
from fastapi_injector import Injected

from application.handle_message.handle_message_command import HandleMessageCommand
from application.handle_message.handle_message_command_handler import (
    HandleMessageCommandHandler,
)
from infrastructure.controllers.http.messages.requests import SendMessageRequest

router = APIRouter(tags=["messages"])
logger = structlog.get_logger(__name__)


@router.post("/messages", status_code=status.HTTP_202_ACCEPTED)
async def send_message(
    payload: SendMessageRequest,
    handler: HandleMessageCommandHandler = Injected(HandleMessageCommandHandler),
) -> None:
    command = HandleMessageCommand(
        session_id=payload.session_id,
        content=payload.content,
    )
    logger.info("Handling message", id=payload.session_id)
    await handler.execute(command)
