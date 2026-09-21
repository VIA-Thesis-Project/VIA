"""Identity Access domain errors."""


class IdentityValidationError(ValueError):
    """Raised when an Identity Access domain object is invalid."""


class IdentityConflictError(RuntimeError):
    """Raised when identity persistence would violate an existing identity."""
