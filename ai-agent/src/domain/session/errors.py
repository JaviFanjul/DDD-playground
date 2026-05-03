from domain.errors import DomainError


class InvalidSessionId(DomainError):
    pass


class SessionRepositoryError(DomainError):
    pass


class InvalidMessageOrder(DomainError):
    pass
