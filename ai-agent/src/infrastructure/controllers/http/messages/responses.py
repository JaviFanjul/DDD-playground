from pydantic import BaseModel


class SendMessageResponse(BaseModel):
    session_id: str
    reply: str
