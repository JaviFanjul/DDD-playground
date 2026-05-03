import pytest

from domain.agent.errors import InvalidSystemPrompt
from domain.agent.system_prompt import SystemPrompt


def test_given_a_non_falsy_value_when_creating_system_prompt_then_does_not_raise() -> None:
    SystemPrompt("you are a helpful assistant")


@pytest.mark.parametrize("value", ["", "   "])
def test_given_an_empty_value_when_creating_system_prompt_then_raises_invalid_system_prompt(value: str) -> None:
    with pytest.raises(InvalidSystemPrompt):
        SystemPrompt(value)


@pytest.mark.parametrize("value", [None, 123, 12.5, True, [], {}, ("a",), object()])
def test_given_a_non_string_value_when_creating_system_prompt_then_raises_invalid_system_prompt(value: object) -> None:
    with pytest.raises(InvalidSystemPrompt):
        SystemPrompt(value)  # type: ignore[arg-type]


def test_given_a_value_with_surrounding_whitespace_when_creating_system_prompt_then_value_is_trimmed() -> None:
    prompt = SystemPrompt("  be concise  ")

    assert prompt.value == "be concise"
