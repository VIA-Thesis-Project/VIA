"""Provider-mocked tests for Cloudflare R2 scientific storage adapters."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from via_backend.contexts.agroclimatic_evaluation.infrastructure.scientific_artifact_store import (
    R2ScientificArtifactStore,
    ScientificArtifactConflictError,
    ScientificArtifactStorageError,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.scientific_source_store import (
    R2ScientificSourceStore,
    ScientificSourceObject,
    ScientificSourceStorageError,
)


class FakeNotFound(Exception):
    response = {"Error": {"Code": "NoSuchKey"}}


class FakeS3Client:
    def __init__(self) -> None:
        self.objects: dict[tuple[str, str], bytes] = {}
        self.metadata: dict[tuple[str, str], dict[str, str]] = {}
        self.download_calls: list[tuple[str, str, str]] = []
        self.upload_calls: list[tuple[str, str, str]] = []
        self.fail_download = False
        self.fail_upload = False

    def download_file(self, *, Bucket: str, Key: str, Filename: str) -> None:
        self.download_calls.append((Bucket, Key, Filename))
        if self.fail_download:
            raise RuntimeError("provider download failure")
        try:
            content = self.objects[(Bucket, Key)]
        except KeyError as error:
            raise FakeNotFound from error
        Path(Filename).write_bytes(content)

    def upload_file(
        self,
        *,
        Filename: str,
        Bucket: str,
        Key: str,
        ExtraArgs: Mapping[str, Any] | None = None,
    ) -> None:
        self.upload_calls.append((Bucket, Key, Filename))
        if self.fail_upload:
            raise RuntimeError("provider upload failure")
        self.objects[(Bucket, Key)] = Path(Filename).read_bytes()
        raw_metadata = (ExtraArgs or {}).get("Metadata", {})
        self.metadata[(Bucket, Key)] = dict(raw_metadata)

    def head_object(self, *, Bucket: str, Key: str) -> Mapping[str, Any]:
        try:
            content = self.objects[(Bucket, Key)]
        except KeyError as error:
            raise FakeNotFound from error
        return {
            "ContentLength": len(content),
            "Metadata": self.metadata.get((Bucket, Key), {}),
        }


def test_r2_source_store_downloads_expected_bucket_and_key(tmp_path: Path) -> None:
    client = FakeS3Client()
    content = b"source-raster"
    client.objects[("via-sources", "huaura/precipitation.tif")] = content
    source = ScientificSourceObject(
        object_key="huaura/precipitation.tif",
        relative_path="climate/precipitation.tif",
        sha256=hashlib.sha256(content).hexdigest(),
        size_bytes=len(content),
        media_type="image/tiff",
    )
    destination = tmp_path / "download.tmp"

    R2ScientificSourceStore(client, "via-sources").copy_to(source, destination)

    assert destination.read_bytes() == content
    assert client.download_calls == [
        ("via-sources", "huaura/precipitation.tif", str(destination))
    ]


def test_r2_source_store_wraps_provider_errors(tmp_path: Path) -> None:
    client = FakeS3Client()
    client.fail_download = True
    source = ScientificSourceObject(
        object_key="huaura/precipitation.tif",
        relative_path="climate/precipitation.tif",
        sha256="a" * 64,
        size_bytes=1,
        media_type="image/tiff",
    )

    with pytest.raises(ScientificSourceStorageError, match="Could not download"):
        R2ScientificSourceStore(client, "via-sources").copy_to(
            source, tmp_path / "download.tmp"
        )


def test_r2_artifact_store_publishes_metadata_and_resolves_verified_bytes(
    tmp_path: Path,
) -> None:
    client = FakeS3Client()
    store = R2ScientificArtifactStore(client, "via-artifacts", tmp_path / "cache")
    source = tmp_path / "crop_suitability.tif"
    source.write_bytes(b"artifact-raster")
    reference = "evaluations/eval-1/crops/maize/crop_suitability.tif"

    published = store.publish(source, reference)
    resolved = store.resolve(
        reference,
        expected_sha256=published.sha256,
        expected_size_bytes=published.size_bytes,
    )

    assert client.objects[("via-artifacts", reference)] == b"artifact-raster"
    assert client.metadata[("via-artifacts", reference)] == {
        "via-sha256": published.sha256,
        "via-size-bytes": str(published.size_bytes),
    }
    assert resolved.path.read_bytes() == b"artifact-raster"
    assert resolved.path.parent.name == "sha256"


def test_r2_artifact_store_is_idempotent_for_same_remote_identity(tmp_path: Path) -> None:
    client = FakeS3Client()
    store = R2ScientificArtifactStore(client, "via-artifacts", tmp_path / "cache")
    source = tmp_path / "artifact.tif"
    source.write_bytes(b"same-content")
    reference = "evaluations/eval-1/artifact.tif"

    first = store.publish(source, reference)
    second = store.publish(source, reference)

    assert second == first
    assert len(client.upload_calls) == 1


def test_r2_artifact_store_rejects_existing_reference_with_different_content(
    tmp_path: Path,
) -> None:
    client = FakeS3Client()
    store = R2ScientificArtifactStore(client, "via-artifacts", tmp_path / "cache")
    first = tmp_path / "first.tif"
    first.write_bytes(b"first")
    second = tmp_path / "second.tif"
    second.write_bytes(b"second")
    reference = "evaluations/eval-1/artifact.tif"
    store.publish(first, reference)

    with pytest.raises(ScientificArtifactConflictError):
        store.publish(second, reference)


def test_r2_artifact_store_wraps_provider_upload_error(tmp_path: Path) -> None:
    client = FakeS3Client()
    client.fail_upload = True
    store = R2ScientificArtifactStore(client, "via-artifacts", tmp_path / "cache")
    source = tmp_path / "artifact.tif"
    source.write_bytes(b"content")

    with pytest.raises(ScientificArtifactStorageError, match="Could not upload"):
        store.publish(source, "evaluations/eval-1/artifact.tif")
