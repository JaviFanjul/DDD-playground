import structlog
from fastapi import Request, status
from fastapi.responses import JSONResponse

from domain.agent.errors import (
    AgentInvocationError,
    InvalidSystemPrompt,
    SystemPromptNotConfigured,
    SystemPromptRepositoryError,
)
from domain.errors import DomainError
from domain.session.errors import (
    InvalidMessageOrder,
    InvalidSessionId,
    SessionRepositoryError,
)
from domain.session.message.errors import InvalidMessageContent


logger = structlog.get_logger(__name__)


_DOMAIN_ERROR_TO_HTTP: dict[type[DomainError], int] = {
    InvalidSessionId: status.HTTP_422_UNPROCESSABLE_CONTENT,
    InvalidMessageContent: status.HTTP_422_UNPROCESSABLE_CONTENT,
    InvalidSystemPrompt: status.HTTP_422_UNPROCESSABLE_CONTENT,
    InvalidMessageOrder: status.HTTP_409_CONFLICT,
    SessionRepositoryError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    AgentInvocationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    SystemPromptRepositoryError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    SystemPromptNotConfigured: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    status_code: int = _DOMAIN_ERROR_TO_HTTP.get(
        type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    logger.error(
        "Error",
        error_type=type(exc).__name__,
        message=str(exc),
        status_code=status_code,
        path=request.url.path,
    )
    return JSONResponse(
        status_code=status_code,
        content={"message": str(exc)},
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "Unhandled exception",
        error_type=type(exc).__name__,
        path=request.url.path,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred"},
    )
