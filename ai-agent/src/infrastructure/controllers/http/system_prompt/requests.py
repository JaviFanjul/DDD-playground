from pydantic import BaseModel


class SetSystemPromptRequest(BaseModel):
    content: str
