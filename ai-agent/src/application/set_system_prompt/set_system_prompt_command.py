from dataclasses import dataclass


@dataclass(frozen=True)
class SetSystemPromptCommand:
    content: str
