import dataclasses
import typing
from dataclasses import dataclass
from importlib.resources import files
from typing import ClassVar

import yaml

CONFIG_RESOURCE = files("resources") / "config.yaml"


@dataclass
class BaseConfig:
    yaml_key: ClassVar[str]

    @classmethod
    def load(cls) -> typing.Self:
        with CONFIG_RESOURCE.open("r", encoding="utf-8") as config_file:
            document = yaml.safe_load(config_file) or {}
        return cls._build(document)

    @classmethod
    def _build(cls, document: dict) -> typing.Self:
        field_types = typing.get_type_hints(cls)
        return cls(**{
            field.name: field_types[field.name](**document[field_types[field.name].yaml_key])
            for field in dataclasses.fields(cls)
        })
