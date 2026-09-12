"""Domain errors raised by Environmental Information invariants."""


class DomainValidationError(ValueError):
    """Raised when environmental metadata violates a domain invariant."""


class DatasetVersionConflictError(RuntimeError):
    """Raised when a dataset version identifier has already been registered."""
