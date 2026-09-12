"""Domain errors raised by Farm Management invariants."""


class DomainValidationError(ValueError):
    """Raised when a Farm Management value violates a domain invariant."""


class ParcelVersionConflictError(RuntimeError):
    """Raised when persisted parcel history changed before a revision was saved."""
