"""Domain errors raised by Decision Support invariants."""


class DomainValidationError(ValueError):
    """Raised when decision evidence violates a domain invariant."""

class PolicyVersionConflictError(RuntimeError):
    """Raised when one immutable policy reference is bound to different thresholds."""
