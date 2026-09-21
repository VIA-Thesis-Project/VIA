"""Security primitive ports for Identity Access application code."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str: ...

    def verify(self, password: str, password_hash: str) -> bool: ...


class OpaqueTokenGenerator(Protocol):
    def generate(self) -> str: ...


class TokenHasher(Protocol):
    def hash(self, token: str) -> str: ...


class Clock(Protocol):
    def now(self) -> datetime: ...
