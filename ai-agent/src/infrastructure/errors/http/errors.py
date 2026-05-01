from fastapi import Request, status
from fastapi.responses import JSONResponse

from domain.errors import DomainError
from domain.session.errors import InvalidSessionId, SessionRepositoryError


_DOMAIN_ERROR_TO_HTTP: dict[type[DomainError], int] = {
    InvalidSessionId: status.HTTP_422_UNPROCESSABLE_ENTITY,
    SessionRepositoryError: status.HTTP_500_INTERNAL_SERVER_ERROR,
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
