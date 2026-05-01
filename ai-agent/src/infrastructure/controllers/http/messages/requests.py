from pydantic import BaseModel


class SendMessageRequest(BaseModel):
    session_id: str
    content: str
