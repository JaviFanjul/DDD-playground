from dataclasses import dataclass


@dataclass(frozen=True)
class HandleMessageCommand:
    session_id: str
    content: str
