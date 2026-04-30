from typing import Protocol

from domain.session.session import Session
from domain.session.session_id import SessionId


class SessionRepository(Protocol):

    async def get_by_id(self, session_id: SessionId) -> Session:
        ...

    async def save(self, session: Session) -> None:
        ...
