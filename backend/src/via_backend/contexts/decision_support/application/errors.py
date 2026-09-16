"""Application errors for Decision Support policy configuration."""


class DefaultViabilityPolicyNotConfiguredError(LookupError):
    """Raised when VIA has no default viability policy configured."""


class ViabilityPolicyVersionNotFoundError(LookupError):
    """Raised when a requested persisted policy version does not exist."""