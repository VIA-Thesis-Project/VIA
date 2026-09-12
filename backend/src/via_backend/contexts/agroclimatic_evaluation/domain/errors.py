"""Domain errors for Agroclimatic Evaluation."""


class DomainValidationError(ValueError):
    """Raised when evaluation data violates a domain invariant."""


class EvaluationConflictError(RuntimeError):
    """Raised when an evaluation identity already exists."""
