from domain.errors import DomainError


class AgentInvocationError(DomainError):
    pass


class InvalidSystemPrompt(DomainError):
    pass


class SystemPromptRepositoryError(DomainError):
    pass


class SystemPromptNotConfigured(DomainError):
    pass
