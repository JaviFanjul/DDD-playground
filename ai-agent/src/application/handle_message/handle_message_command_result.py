from dataclasses import dataclass


@dataclass(frozen=True)
class HandleMessageCommandResult:
    session_id: str
    reply: str
