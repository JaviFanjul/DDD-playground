from typing import Protocol

from domain.session.session import Session
from domain.session.session_id import SessionId


class SessionRepository(Protocol):

    async def get(self, session_id: SessionId) -> Session:
        """Returns the session for the given id, or a new empty session if it does not exist."""
        ...

    async def save(self, session: Session) -> None:
        ...
