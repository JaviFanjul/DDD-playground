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
class Config(BaseConfig):
    server: ServerConfig
 
@lru_cache
def get_config() -> Config:
    return Config.load()
