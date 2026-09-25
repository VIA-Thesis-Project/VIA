"""Small S3-compatible SDK boundary shared by scientific object stores."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, cast


class S3CompatibleClient(Protocol):
    """Subset of the boto3 S3 client used by VIA infrastructure adapters."""

    def download_file(self, *, Bucket: str, Key: str, Filename: str) -> None: ...

    def upload_file(
        self,
        *,
        Filename: str,
        Bucket: str,
        Key: str,
        ExtraArgs: Mapping[str, Any] | None = None,
    ) -> None: ...

    def head_object(self, *, Bucket: str, Key: str) -> Mapping[str, Any]: ...


def create_s3_compatible_client(
    *,
    endpoint_url: str,
    region_name: str,
    access_key_id: str,
    secret_access_key: str,
) -> S3CompatibleClient:
    """Create the production S3-compatible client without leaking SDK types upward."""
    try:
        import boto3
    except ImportError as error:  # pragma: no cover - packaging contract protects production
        raise RuntimeError("boto3 is required for the S3 scientific storage backend.") from error

    return cast(
        S3CompatibleClient,
        boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        ),
    )
