"""Provider-neutral scientific source storage and local materialization."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from threading import Lock
from typing import Protocol
from uuid import uuid4

from .s3_compatible import S3CompatibleClient

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ScientificSourceStorageError(RuntimeError):
    """Base error for scientific source storage/materialization failures."""


class ScientificSourceIntegrityError(ScientificSourceStorageError):
    """Raised when materialized bytes do not match the declared identity."""


@dataclass(frozen=True, slots=True)
class ScientificSourceObject:
    """One immutable source object, independent from its physical provider."""

    object_key: str
    relative_path: str
    sha256: str
    size_bytes: int
    media_type: str = "application/octet-stream"

    def __post_init__(self) -> None:
        _validated_relative_reference(self.object_key, "object_key")
        _validated_relative_reference(self.relative_path, "relative_path")
        if _SHA256.fullmatch(self.sha256) is None:
            raise ValueError(
                "sha256 must be a 64-character lowercase hexadecimal SHA-256."
            )
        if isinstance(self.size_bytes, bool) or not isinstance(self.size_bytes, int):
            raise ValueError("size_bytes must be an integer.")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be non-negative.")
        if not self.media_type or self.media_type != self.media_type.strip():
            raise ValueError("media_type must be a non-empty trimmed string.")


class ScientificSourceStore(Protocol):
    """Copy immutable source bytes from a configured physical provider."""

    def copy_to(self, source: ScientificSourceObject, destination: Path) -> None: ...


class FilesystemScientificSourceStore:
    """Read scientific source objects from one deployment-owned directory."""

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    def copy_to(self, source: ScientificSourceObject, destination: Path) -> None:
        reference = _validated_relative_reference(source.object_key, "object_key")
        source_path = self._root.joinpath(*reference.parts).resolve()
        if not _is_within(source_path, self._root):
            raise ScientificSourceStorageError(
                "Scientific source object escapes the configured filesystem root."
            )
        if not source_path.is_file():
            raise ScientificSourceStorageError(
                f"Scientific source object does not exist: {source.object_key}"
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copyfile(source_path, destination)
        except OSError as error:
            raise ScientificSourceStorageError(
                f"Could not copy scientific source object {source.object_key}."
            ) from error


class R2ScientificSourceStore:
    """Cloudflare R2 source store through its S3-compatible API."""

    def __init__(self, client: S3CompatibleClient, bucket: str) -> None:
        if not bucket or bucket != bucket.strip():
            raise ValueError("Scientific source bucket must be a non-empty trimmed string.")
        self._client = client
        self._bucket = bucket

    def copy_to(self, source: ScientificSourceObject, destination: Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._client.download_file(
                Bucket=self._bucket,
                Key=source.object_key,
                Filename=str(destination),
            )
        except Exception as error:
            raise ScientificSourceStorageError(
                f"Could not download scientific source object {source.object_key}."
            ) from error


class ScientificSourceMaterializer:
    """Materialize immutable source objects into a rebuildable local cache."""

    def __init__(self, store: ScientificSourceStore, cache_root: Path) -> None:
        self._store = store
        self._cache_root = cache_root.resolve()
        self._cache_root.mkdir(parents=True, exist_ok=True)
        self._locks_guard = Lock()
        self._locks: dict[str, Lock] = {}

    def materialize(self, source: ScientificSourceObject) -> Path:
        """Return a verified content-addressed local copy of ``source``."""
        with self._lock_for(source.sha256):
            destination = self._cache_root / "sha256" / source.sha256
            destination.parent.mkdir(parents=True, exist_ok=True)

            if destination.is_file():
                if _matches_identity(destination, source):
                    return destination
                destination.unlink()

            temporary = destination.parent / f".{source.sha256}.{uuid4().hex}.tmp"
            try:
                self._store.copy_to(source, temporary)
                _fsync_file(temporary)
                _require_identity(temporary, source)
                os.replace(temporary, destination)
                _require_identity(destination, source)
                return destination
            finally:
                if temporary.exists():
                    temporary.unlink()

    def materialize_view(
        self,
        sources: tuple[ScientificSourceObject, ...],
        view_root: Path,
    ) -> Path:
        """Build a local path hierarchy backed by verified cached source bytes."""
        resolved_view = view_root.resolve()
        resolved_view.mkdir(parents=True, exist_ok=True)

        seen_paths: dict[PurePosixPath, str] = {}
        for source in sources:
            relative = _validated_relative_reference(source.relative_path, "relative_path")
            previous_hash = seen_paths.get(relative)
            if previous_hash is not None and previous_hash != source.sha256:
                raise ScientificSourceStorageError(
                    "Scientific source view contains conflicting content for "
                    f"{relative.as_posix()}."
                )
            seen_paths[relative] = source.sha256

            cached = self.materialize(source)
            destination = resolved_view.joinpath(*relative.parts)
            if not _is_within(destination, resolved_view):
                raise ScientificSourceStorageError(
                    "Scientific source relative path escapes the materialized view."
                )
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                if _matches_identity(destination, source):
                    continue
                destination.unlink()
            try:
                os.link(cached, destination)
            except OSError:
                shutil.copyfile(cached, destination)
            _require_identity(destination, source)

        return resolved_view

    def _lock_for(self, sha256: str) -> Lock:
        # The worker is currently one process. This prevents duplicate downloads
        # inside that process; a future multi-process worker should replace this
        # with a cross-process lock without changing the public materializer API.
        with self._locks_guard:
            return self._locks.setdefault(sha256, Lock())


def _validated_relative_reference(value: str, name: str) -> PurePosixPath:
    if not value or value != value.strip() or "\\" in value:
        raise ValueError(f"{name} must be a non-empty normalized POSIX relative path.")
    reference = PurePosixPath(value)
    if reference.is_absolute() or any(part in {"", ".", ".."} for part in reference.parts):
        raise ValueError(f"{name} must be relative and cannot contain traversal segments.")
    return reference


def _file_identity(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    try:
        with path.open("rb") as source:
            while chunk := source.read(1024 * 1024):
                digest.update(chunk)
                size += len(chunk)
    except OSError as error:
        raise ScientificSourceStorageError(
            f"Could not read materialized scientific source {path}."
        ) from error
    return digest.hexdigest(), size


def _matches_identity(path: Path, source: ScientificSourceObject) -> bool:
    try:
        sha256, size_bytes = _file_identity(path)
    except ScientificSourceStorageError:
        return False
    return sha256 == source.sha256 and size_bytes == source.size_bytes


def _require_identity(path: Path, source: ScientificSourceObject) -> None:
    sha256, size_bytes = _file_identity(path)
    if sha256 != source.sha256:
        raise ScientificSourceIntegrityError(
            f"Scientific source SHA-256 mismatch for {source.object_key}."
        )
    if size_bytes != source.size_bytes:
        raise ScientificSourceIntegrityError(
            f"Scientific source size mismatch for {source.object_key}."
        )


def _fsync_file(path: Path) -> None:
    try:
        # Windows requires a writable handle for fsync; the file contents are
        # already complete and are not modified here.
        with path.open("rb+") as source:
            os.fsync(source.fileno())
    except OSError as error:
        raise ScientificSourceStorageError(
            f"Could not fsync materialized scientific source {path}."
        ) from error


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
    except ValueError:
        return False
    return True
