from datetime import datetime

from pydantic import BaseModel


class SendMessageResponse(BaseModel):
    id: str
    session_id: str
    content: str
    created_at: datetime
