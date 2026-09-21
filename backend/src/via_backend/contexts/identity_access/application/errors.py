"""Application-level Identity Access failures."""


class AuthenticationError(RuntimeError):
    """Raised when supplied authentication material is not valid."""


class PasswordPolicyError(ValueError):
    """Raised when an administratively supplied password violates policy."""


class IdentityUserNotFoundError(LookupError):
    """Raised when an administrative user reference cannot be resolved."""
