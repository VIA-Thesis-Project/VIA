from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from via_backend.contexts.agroclimatic_evaluation.infrastructure.scientific_artifact_store import (
    FilesystemScientificArtifactStore,
    ResolvedScientificArtifact,
    ScientificArtifactConflictError,
    ScientificArtifactIntegrityError,
    ScientificArtifactStorageError,
)


def test_publish_creates_durable_artifact_with_opaque_reference(tmp_path: Path) -> None:
    source = tmp_path / "source.tif"
    source.write_bytes(b"scientific-raster")

    root = tmp_path / "artifacts"
    store = FilesystemScientificArtifactStore(root)

    published = store.publish(
        source,
        "evaluations/eval-1/crops/maize/crop_suitability.tif",
    )

    expected = root / "evaluations/eval-1/crops/maize/crop_suitability.tif"

    assert expected.read_bytes() == b"scientific-raster"
    assert published.storage_reference == (
        "evaluations/eval-1/crops/maize/crop_suitability.tif"
    )
    assert published.sha256 == hashlib.sha256(b"scientific-raster").hexdigest()
    assert published.size_bytes == len(b"scientific-raster")


def test_publish_is_idempotent_for_identical_content(tmp_path: Path) -> None:
    source = tmp_path / "source.tif"
    source.write_bytes(b"same-content")

    store = FilesystemScientificArtifactStore(tmp_path / "artifacts")
    reference = "evaluations/eval-1/crops/maize/crop_suitability.tif"

    first = store.publish(source, reference)
    second = store.publish(source, reference)

    assert second == first


def test_publish_rejects_different_content_for_existing_reference(
    tmp_path: Path,
) -> None:
    first_source = tmp_path / "first.tif"
    first_source.write_bytes(b"first")

    second_source = tmp_path / "second.tif"
    second_source.write_bytes(b"second")

    root = tmp_path / "artifacts"
    store = FilesystemScientificArtifactStore(root)
    reference = "evaluations/eval-1/crops/maize/crop_suitability.tif"

    store.publish(first_source, reference)

    with pytest.raises(ScientificArtifactConflictError):
        store.publish(second_source, reference)

    assert (root / reference).read_bytes() == b"first"


@pytest.mark.parametrize(
    "reference",
    [
        "../outside.tif",
        "evaluations/../../outside.tif",
        "/absolute/outside.tif",
        r"evaluations\eval-1\outside.tif",
        "",
        " ",
    ],
)
def test_publish_rejects_unsafe_storage_reference(
    tmp_path: Path,
    reference: str,
) -> None:
    source = tmp_path / "source.tif"
    source.write_bytes(b"content")

    store = FilesystemScientificArtifactStore(tmp_path / "artifacts")

    with pytest.raises(ScientificArtifactStorageError):
        store.publish(source, reference)


def test_publish_rejects_missing_source(tmp_path: Path) -> None:
    store = FilesystemScientificArtifactStore(tmp_path / "artifacts")

    with pytest.raises(ScientificArtifactStorageError):
        store.publish(
            tmp_path / "missing.tif",
            "evaluations/eval-1/crops/maize/crop_suitability.tif",
        )

def test_publish_rejects_content_that_does_not_match_expected_checksum(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.tif"
    source.write_bytes(b"actual-content")

    root = tmp_path / "artifacts"
    store = FilesystemScientificArtifactStore(root)

    with pytest.raises(ScientificArtifactIntegrityError):
        store.publish(
            source,
            "evaluations/eval-1/crops/maize/crop_suitability.tif",
            expected_sha256="0" * 64,
        )

    assert not (
        root / "evaluations/eval-1/crops/maize/crop_suitability.tif"
    ).exists()

def test_resolve_returns_verified_durable_artifact(tmp_path: Path) -> None:
    content = b"scientific-raster"
    checksum = hashlib.sha256(content).hexdigest()

    source = tmp_path / "source.tif"
    source.write_bytes(content)

    root = tmp_path / "artifacts"
    store = FilesystemScientificArtifactStore(root)

    published = store.publish(
        source,
        "evaluations/eval-1/crops/maize/crop_suitability.tif",
    )

    resolved = store.resolve(
        published.storage_reference,
        expected_sha256=checksum,
        expected_size_bytes=len(content),
    )

    assert isinstance(resolved, ResolvedScientificArtifact)
    assert resolved.path.read_bytes() == content
    assert resolved.sha256 == checksum
    assert resolved.size_bytes == len(content)


def test_resolve_rejects_modified_durable_artifact(tmp_path: Path) -> None:
    source = tmp_path / "source.tif"
    source.write_bytes(b"original")

    root = tmp_path / "artifacts"
    store = FilesystemScientificArtifactStore(root)

    published = store.publish(
        source,
        "evaluations/eval-1/crops/maize/crop_suitability.tif",
    )

    durable = root.joinpath(*published.storage_reference.split("/"))
    durable.write_bytes(b"tampered")

    with pytest.raises(
        ScientificArtifactIntegrityError,
        match="SHA-256",
    ):
        store.resolve(
            published.storage_reference,
            expected_sha256=published.sha256,
            expected_size_bytes=published.size_bytes,
        )


def test_resolve_rejects_missing_durable_artifact(tmp_path: Path) -> None:
    store = FilesystemScientificArtifactStore(tmp_path / "artifacts")

    with pytest.raises(
        ScientificArtifactStorageError,
        match="does not exist",
    ):
        store.resolve(
            "evaluations/eval-1/crops/maize/crop_suitability.tif",
            expected_sha256="a" * 64,
            expected_size_bytes=10,
        )
def test_resolve_rejects_unsafe_reference(tmp_path: Path) -> None:
    store = FilesystemScientificArtifactStore(tmp_path / "artifacts")

    with pytest.raises(ScientificArtifactStorageError):
        store.resolve(
            "../outside.tif",
            expected_sha256="a" * 64,
            expected_size_bytes=1,
        )