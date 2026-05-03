from dataclasses import dataclass
from functools import lru_cache
from typing import ClassVar

from config.base import BaseConfig


@dataclass
class ServerConfig():
    yaml_key: ClassVar[str] = "server"
    host: str
    port: int

@dataclass
class RedisConfig():
    yaml_key: ClassVar[str] = "redis"
    host: str
    port: int
    db: int

@dataclass
class OllamaConfig():
    yaml_key: ClassVar[str] = "ollama"
    host: str
    model: str

@dataclass
class Config(BaseConfig):
    server: ServerConfig
    redis: RedisConfig
    ollama: OllamaConfig
 
@lru_cache
def get_config() -> Config:
    return Config.load()
