"""Shared technical infrastructure used by the application composition root."""

from .database import NAMING_CONVENTION, SessionFactory, create_database

__all__ = ["NAMING_CONVENTION", "SessionFactory", "create_database"]
