"""Durable filesystem storage for scientific artifacts."""

from __future__ import annotations

import hashlib
import os
import shutil
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Protocol
from uuid import uuid4

from .s3_compatible import S3CompatibleClient


class ScientificArtifactStorageError(RuntimeError):
    """Base error for durable scientific artifact storage failures."""


class ScientificArtifactConflictError(ScientificArtifactStorageError):
    """Raised when an immutable artifact reference already has different content."""


@dataclass(frozen=True, slots=True)
class PublishedScientificArtifact:
    """Storage result without exposing the filesystem root."""

    storage_reference: str
    sha256: str
    size_bytes: int


class ScientificArtifactIntegrityError(ScientificArtifactStorageError):
    """Raised when published bytes do not match the expected scientific checksum."""

class ScientificArtifactStore(Protocol):
    """Publish immutable scientific files behind opaque logical references."""

    def resolve(
        self,
        storage_reference: str,
        *,
        expected_sha256: str,
        expected_size_bytes: int,
    ) -> ResolvedScientificArtifact: ...

    def publish(
        self,
        source: Path,
        storage_reference: str,
        *,
        expected_sha256: str | None = None,
    ) -> PublishedScientificArtifact: ...


class FilesystemScientificArtifactStore:
    """Filesystem-backed immutable artifact store."""

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    def resolve(
        self,
        storage_reference: str,
        *,
        expected_sha256: str,
        expected_size_bytes: int,
    ) -> ResolvedScientificArtifact:
        reference = _validated_reference(storage_reference)
        path = self._root.joinpath(*reference.parts).resolve()

        if not _is_within(path, self._root):
            raise ScientificArtifactStorageError(
                "Scientific artifact reference escapes the configured storage root."
            )

        if not path.is_file():
            raise ScientificArtifactStorageError(
                "Durable scientific artifact does not exist."
            )

        sha256, size_bytes = _file_identity(path)

        if sha256 != expected_sha256:
            raise ScientificArtifactIntegrityError(
                "Durable scientific artifact SHA-256 does not match persisted metadata."
            )

        if size_bytes != expected_size_bytes:
            raise ScientificArtifactIntegrityError(
                "Durable scientific artifact size does not match persisted metadata."
            )

        return ResolvedScientificArtifact(
            path=path,
            sha256=sha256,
            size_bytes=size_bytes,
        )

    def publish(
        self,
        source: Path,
        storage_reference: str,
        *,
        expected_sha256: str | None = None,
    ) -> PublishedScientificArtifact:
        source_path = source.resolve()
        if not source_path.is_file():
            raise ScientificArtifactStorageError(
                f"Scientific artifact source does not exist or is not a file: {source}"
            )

        reference = _validated_reference(storage_reference)
        destination = self._root.joinpath(*reference.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)

        if not _is_within(destination, self._root):
            raise ScientificArtifactStorageError(
                "Scientific artifact reference escapes the configured storage root."
            )

        temporary = destination.parent / f".{destination.name}.{uuid4().hex}.tmp"

        try:
            with source_path.open("rb") as source_file, temporary.open("xb") as target_file:
                shutil.copyfileobj(source_file, target_file)
                target_file.flush()
                os.fsync(target_file.fileno())

            candidate_sha256, candidate_size = _file_identity(temporary)

            if expected_sha256 is not None and candidate_sha256 != expected_sha256:
                raise ScientificArtifactIntegrityError(
                    "Scientific artifact content does not match the expected SHA-256."
                )

            if destination.exists():
                stored_sha256, stored_size = _file_identity(destination)
                if (
                    stored_sha256 != candidate_sha256
                    or stored_size != candidate_size
                ):
                    raise ScientificArtifactConflictError(
                        "Scientific artifact reference already exists with different content."
                    )

                temporary.unlink()
                return PublishedScientificArtifact(
                    storage_reference=reference.as_posix(),
                    sha256=stored_sha256,
                    size_bytes=stored_size,
                )

            os.replace(temporary, destination)

            durable_sha256, durable_size = _file_identity(destination)
            if (
                durable_sha256 != candidate_sha256
                or durable_size != candidate_size
            ):
                raise ScientificArtifactStorageError(
                    "Durable scientific artifact failed post-publication integrity verification."
                )

            return PublishedScientificArtifact(
                storage_reference=reference.as_posix(),
                sha256=durable_sha256,
                size_bytes=durable_size,
            )
        finally:
            if temporary.exists():
                temporary.unlink()


class R2ScientificArtifactStore:
    """Cloudflare R2-backed immutable artifacts with a rebuildable local cache."""

    _SHA256_METADATA_KEY = "via-sha256"
    _SIZE_METADATA_KEY = "via-size-bytes"

    def __init__(
        self,
        client: S3CompatibleClient,
        bucket: str,
        cache_root: Path,
    ) -> None:
        if not bucket or bucket != bucket.strip():
            raise ValueError("Scientific artifact bucket must be a non-empty trimmed string.")
        self._client = client
        self._bucket = bucket
        self._cache_root = cache_root.resolve()
        self._cache_root.mkdir(parents=True, exist_ok=True)

    def resolve(
        self,
        storage_reference: str,
        *,
        expected_sha256: str,
        expected_size_bytes: int,
    ) -> ResolvedScientificArtifact:
        reference = _validated_reference(storage_reference)
        destination = self._cache_root / "sha256" / expected_sha256
        destination.parent.mkdir(parents=True, exist_ok=True)

        if destination.is_file():
            sha256, size_bytes = _file_identity(destination)
            if sha256 == expected_sha256 and size_bytes == expected_size_bytes:
                return ResolvedScientificArtifact(destination, sha256, size_bytes)
            destination.unlink()

        temporary = destination.parent / f".{expected_sha256}.{uuid4().hex}.tmp"
        try:
            try:
                self._client.download_file(
                    Bucket=self._bucket,
                    Key=reference.as_posix(),
                    Filename=str(temporary),
                )
            except Exception as error:
                raise ScientificArtifactStorageError(
                    "Could not download durable scientific artifact."
                ) from error

            sha256, size_bytes = _file_identity(temporary)
            if sha256 != expected_sha256:
                raise ScientificArtifactIntegrityError(
                    "Durable scientific artifact SHA-256 does not match persisted metadata."
                )
            if size_bytes != expected_size_bytes:
                raise ScientificArtifactIntegrityError(
                    "Durable scientific artifact size does not match persisted metadata."
                )

            os.replace(temporary, destination)
            durable_sha256, durable_size = _file_identity(destination)
            if durable_sha256 != expected_sha256 or durable_size != expected_size_bytes:
                raise ScientificArtifactStorageError(
                    "Cached scientific artifact failed post-materialization verification."
                )
            return ResolvedScientificArtifact(
                destination,
                durable_sha256,
                durable_size,
            )
        finally:
            if temporary.exists():
                temporary.unlink()

    def publish(
        self,
        source: Path,
        storage_reference: str,
        *,
        expected_sha256: str | None = None,
    ) -> PublishedScientificArtifact:
        source_path = source.resolve()
        if not source_path.is_file():
            raise ScientificArtifactStorageError(
                f"Scientific artifact source does not exist or is not a file: {source}"
            )
        reference = _validated_reference(storage_reference)
        candidate_sha256, candidate_size = _file_identity(source_path)
        if expected_sha256 is not None and candidate_sha256 != expected_sha256:
            raise ScientificArtifactIntegrityError(
                "Scientific artifact content does not match the expected SHA-256."
            )

        existing = self._head_object(reference.as_posix())
        if existing is not None:
            self._require_existing_identity(
                existing,
                candidate_sha256=candidate_sha256,
                candidate_size=candidate_size,
            )
            return PublishedScientificArtifact(
                reference.as_posix(), candidate_sha256, candidate_size
            )

        metadata = {
            self._SHA256_METADATA_KEY: candidate_sha256,
            self._SIZE_METADATA_KEY: str(candidate_size),
        }
        try:
            self._client.upload_file(
                Filename=str(source_path),
                Bucket=self._bucket,
                Key=reference.as_posix(),
                ExtraArgs={"Metadata": metadata},
            )
        except Exception as error:
            raise ScientificArtifactStorageError(
                "Could not upload durable scientific artifact."
            ) from error

        published = self._head_object(reference.as_posix())
        if published is None:
            raise ScientificArtifactStorageError(
                "Published scientific artifact could not be verified in object storage."
            )
        self._require_existing_identity(
            published,
            candidate_sha256=candidate_sha256,
            candidate_size=candidate_size,
        )
        return PublishedScientificArtifact(
            reference.as_posix(), candidate_sha256, candidate_size
        )

    def _head_object(self, key: str) -> Mapping[str, Any] | None:
        try:
            return self._client.head_object(Bucket=self._bucket, Key=key)
        except Exception as error:
            if _is_not_found_error(error):
                return None
            raise ScientificArtifactStorageError(
                "Could not inspect durable scientific artifact metadata."
            ) from error

    def _require_existing_identity(
        self,
        metadata: Mapping[str, Any],
        *,
        candidate_sha256: str,
        candidate_size: int,
    ) -> None:
        raw_metadata = metadata.get("Metadata")
        object_metadata = raw_metadata if isinstance(raw_metadata, Mapping) else {}
        stored_sha256 = object_metadata.get(self._SHA256_METADATA_KEY)
        stored_size = object_metadata.get(self._SIZE_METADATA_KEY)
        content_length = metadata.get("ContentLength")
        if (
            stored_sha256 != candidate_sha256
            or stored_size != str(candidate_size)
            or content_length != candidate_size
        ):
            raise ScientificArtifactConflictError(
                "Scientific artifact reference already exists with different or "
                "unverifiable content."
            )


def _validated_reference(storage_reference: str) -> PurePosixPath:
    if (
        not storage_reference
        or storage_reference != storage_reference.strip()
        or "\\" in storage_reference
    ):
        raise ScientificArtifactStorageError(
            "Scientific artifact reference must be a non-empty normalized POSIX path."
        )

    reference = PurePosixPath(storage_reference)
    if reference.is_absolute() or any(part in {"", ".", ".."} for part in reference.parts):
        raise ScientificArtifactStorageError(
            "Scientific artifact reference must be relative and cannot contain traversal segments."
        )

    return reference


def _file_identity(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0

    with path.open("rb") as artifact:
        while chunk := artifact.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)

    return digest.hexdigest(), size


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def _is_not_found_error(error: Exception) -> bool:
    response = getattr(error, "response", None)
    if not isinstance(response, Mapping):
        return False
    raw_error = response.get("Error")
    if not isinstance(raw_error, Mapping):
        return False
    code = str(raw_error.get("Code", "")).casefold()
    return code in {"404", "nosuchkey", "notfound", "nosuchobject"}


@dataclass(frozen=True, slots=True)
class ResolvedScientificArtifact:
    """Verified local artifact available only inside Infrastructure."""

    path: Path
    sha256: str
    size_bytes: int
