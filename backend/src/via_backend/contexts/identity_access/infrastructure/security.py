"""Security primitive adapters for Identity Access."""

from __future__ import annotations

import hashlib
import secrets

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


class Argon2PasswordHasher:
    """Hash passwords with Argon2id through pwdlib."""

    def __init__(self) -> None:
        self._password_hash = PasswordHash((Argon2Hasher(),))

    def hash(self, password: str) -> str:
        return self._password_hash.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        return self._password_hash.verify(password, password_hash)


class SecretsOpaqueTokenGenerator:
    """Generate URL-safe opaque tokens with 256 bits of entropy."""

    TOKEN_BYTES = 32

    def generate(self) -> str:
        return secrets.token_urlsafe(self.TOKEN_BYTES)


class Sha256TokenHasher:
    """Create the deterministic digest persisted for an opaque token."""

    def hash(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
