from domain.session.session_id import SessionId


class Session:
    _id: SessionId

    def __init__(self, session_id: SessionId) -> None:
        self._id = session_id

    @property
    def id(self) -> SessionId:
        return self._id
