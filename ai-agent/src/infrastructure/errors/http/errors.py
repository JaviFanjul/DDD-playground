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
    return JSONResponse(
        status_code=_DOMAIN_ERROR_TO_HTTP.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR),
        content={"message": str(exc)},
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred"},
    )
