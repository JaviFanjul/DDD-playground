from pydantic import BaseModel


class RedisMessageDto(BaseModel):
    role: str
    content: str


class RedisSessionDto(BaseModel):
    id: str
    messages: list[RedisMessageDto]
