"""Focused tests for provider-neutral scientific source materialization."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    FilesystemScientificSourceStore,
    ScientificSourceIntegrityError,
    ScientificSourceMaterializer,
    ScientificSourceObject,
)


def _source(content: bytes, *, object_key: str = "huaura/source.tif") -> ScientificSourceObject:
    return ScientificSourceObject(
        object_key=object_key,
        relative_path="environment/source.tif",
        sha256=hashlib.sha256(content).hexdigest(),
        size_bytes=len(content),
        media_type="image/tiff",
    )


class CountingStore:
    def __init__(self, content: bytes) -> None:
        self.content = content
        self.calls = 0

    def copy_to(self, source: ScientificSourceObject, destination: Path) -> None:
        del source
        self.calls += 1
        destination.write_bytes(self.content)


def test_cache_miss_downloads_and_cache_hit_avoids_redownload(tmp_path: Path) -> None:
    content = b"scientific-source-v1"
    store = CountingStore(content)
    materializer = ScientificSourceMaterializer(store, tmp_path / "cache")
    source = _source(content)

    first = materializer.materialize(source)
    second = materializer.materialize(source)

    assert first == second
    assert first.read_bytes() == content
    assert first.name == source.sha256
    assert store.calls == 1


def test_hash_mismatch_fails_and_does_not_commit_partial_cache(tmp_path: Path) -> None:
    expected = _source(b"expected")
    materializer = ScientificSourceMaterializer(
        CountingStore(b"corrupted"),
        tmp_path / "cache",
    )

    with pytest.raises(ScientificSourceIntegrityError, match="SHA-256 mismatch"):
        materializer.materialize(expected)

    destination = tmp_path / "cache" / "sha256" / expected.sha256
    assert not destination.exists()
    assert list(destination.parent.glob("*.tmp")) == []


def test_size_mismatch_fails_even_when_declared_hash_matches(tmp_path: Path) -> None:
    content = b"expected"
    source = ScientificSourceObject(
        object_key="huaura/source.tif",
        relative_path="environment/source.tif",
        sha256=hashlib.sha256(content).hexdigest(),
        size_bytes=len(content) + 1,
        media_type="image/tiff",
    )
    materializer = ScientificSourceMaterializer(
        CountingStore(content),
        tmp_path / "cache",
    )

    with pytest.raises(ScientificSourceIntegrityError, match="size mismatch"):
        materializer.materialize(source)


def test_invalid_cached_partial_file_is_replaced_from_store(tmp_path: Path) -> None:
    content = b"complete-source"
    source = _source(content)
    store = CountingStore(content)
    cache_root = tmp_path / "cache"
    destination = cache_root / "sha256" / source.sha256
    destination.parent.mkdir(parents=True)
    destination.write_bytes(b"partial")

    materialized = ScientificSourceMaterializer(store, cache_root).materialize(source)

    assert materialized.read_bytes() == content
    assert store.calls == 1


def test_filesystem_store_reads_only_under_configured_root(tmp_path: Path) -> None:
    root = tmp_path / "sources"
    source_path = root / "huaura" / "source.tif"
    source_path.parent.mkdir(parents=True)
    source_path.write_bytes(b"filesystem-source")
    source = _source(b"filesystem-source")
    destination = tmp_path / "download.tmp"

    FilesystemScientificSourceStore(root).copy_to(source, destination)

    assert destination.read_bytes() == b"filesystem-source"


def test_materialized_view_preserves_relative_path(tmp_path: Path) -> None:
    content = b"scientific-source-v1"
    source = _source(content)
    materializer = ScientificSourceMaterializer(
        CountingStore(content),
        tmp_path / "cache",
    )

    view = materializer.materialize_view((source,), tmp_path / "view")

    assert (view / "environment" / "source.tif").read_bytes() == content
