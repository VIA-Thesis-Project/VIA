#!/usr/bin/env python3
"""Fail-fast, credential-safe post-deploy smoke for the live VIA API.

This script creates durable smoke records. Run it only with a dedicated smoke user
and a reviewed GeoJSON parcel that is completely inside the Huaura AOI.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
import time
from datetime import UTC, datetime
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import HTTPCookieProcessor, Request, build_opener


class SmokeFailure(RuntimeError):
    """Raised when one post-deploy assertion fails."""


class ApiClient:
    def __init__(self, base_url: str, timeout: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._opener = build_opener(HTTPCookieProcessor(CookieJar()))
        self._access_token: str | None = None

    def set_access_token(self, token: str) -> None:
        self._access_token = token

    def request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        expected: tuple[int, ...] = (200,),
    ) -> tuple[int, Any, dict[str, str]]:
        data = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if self._access_token is not None:
            headers["Authorization"] = f"Bearer {self._access_token}"
        request = Request(
            f"{self.base_url}{path}",
            data=data,
            headers=headers,
            method=method,
        )
        try:
            response = self._opener.open(request, timeout=self.timeout)
            status = response.status
            raw = response.read()
            response_headers = {key.casefold(): value for key, value in response.headers.items()}
        except HTTPError as error:
            status = error.code
            raw = error.read()
            response_headers = {key.casefold(): value for key, value in error.headers.items()}
        except URLError as error:
            raise SmokeFailure(
                f"{method} {path} could not reach the API: {error.reason}"
            ) from error

        body: Any = None
        if raw:
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                body = raw.decode("utf-8", errors="replace")
        if status not in expected:
            retry_after = response_headers.get("retry-after")
            suffix = f" Retry-After={retry_after}." if retry_after else ""
            detail = body.get("detail") if isinstance(body, dict) else body
            raise SmokeFailure(
                f"{method} {path} returned HTTP {status}; expected {expected}. "
                f"Detail={detail!r}.{suffix}"
            )
        return status, body, response_headers


def _load_geometry(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SmokeFailure(f"Cannot load parcel GeoJSON {path}: {error}") from error
    if payload.get("type") == "Feature":
        payload = payload.get("geometry")
    if not isinstance(payload, dict) or payload.get("type") not in {"Polygon", "MultiPolygon"}:
        raise SmokeFailure(
            "Parcel GeoJSON must be a Polygon, MultiPolygon, or Feature containing one."
        )
    if "coordinates" not in payload:
        raise SmokeFailure("Parcel GeoJSON is missing coordinates.")
    return payload


def _credentials(args: argparse.Namespace) -> tuple[str, str]:
    email = args.email or os.getenv("VIA_SMOKE_EMAIL")
    if not email:
        email = input("Smoke user email: ").strip()
    password = os.getenv("VIA_SMOKE_PASSWORD")
    if password is None:
        password = getpass.getpass("Smoke user password: ")
    if not email or not password:
        raise SmokeFailure("Smoke email and password must be non-empty.")
    return email, password


def _assert_safe_base_url(base_url: str, allow_http: bool) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise SmokeFailure("API URL must be an absolute http:// or https:// URL.")
    loopback = parsed.hostname in {"127.0.0.1", "localhost", "::1"}
    if parsed.scheme != "https" and not loopback and not allow_http:
        raise SmokeFailure("Refusing credentials over non-loopback HTTP; use HTTPS.")


def _choose_capability(
    capabilities: dict[str, Any], crop_override: str | None, regime: str
) -> tuple[str, dict[str, str]]:
    crops = capabilities.get("crops") or []
    crop = next(
        (
            item
            for item in crops
            if (crop_override is None or item.get("crop_id") == crop_override)
            and regime in (item.get("water_regimes") or [])
        ),
        None,
    )
    if crop is None:
        raise SmokeFailure("No capability matches the requested crop and water regime.")
    bindings = (
        capabilities.get("environmental_inputs", {}).get(
            "scientifically_bound_dataset_versions"
        )
        or []
    )
    if not bindings:
        raise SmokeFailure("Capabilities expose no scientifically bound dataset version.")
    return str(crop["crop_id"]), bindings[0]


def run(args: argparse.Namespace) -> None:
    base_url = args.api_url or os.getenv("VIA_SMOKE_API_URL") or "http://127.0.0.1:8000"
    _assert_safe_base_url(base_url, args.allow_http)
    geometry_path_value = args.parcel_geojson or os.getenv("VIA_SMOKE_PARCEL_GEOJSON")
    if not geometry_path_value:
        raise SmokeFailure("Pass --parcel-geojson or VIA_SMOKE_PARCEL_GEOJSON.")
    geometry = _load_geometry(Path(geometry_path_value))
    email, password = _credentials(args)
    client = ApiClient(base_url, args.request_timeout)

    client.request("GET", "/health")
    print("OK  health")

    _, login, _ = client.request(
        "POST",
        "/api/v1/auth/login",
        payload={"email": email, "password": password},
    )
    if not isinstance(login, dict) or not isinstance(login.get("access_token"), str):
        raise SmokeFailure("Login response did not contain an access token.")
    client.set_access_token(login["access_token"])
    print("OK  login (credentials, access token, and refresh cookie withheld)")

    _, me, _ = client.request("GET", "/api/v1/auth/me")
    print(f"OK  me ({me.get('email', 'authenticated user')})")

    _, capabilities, _ = client.request("GET", "/api/v1/evaluation-capabilities")
    crop_id, binding = _choose_capability(capabilities, args.crop_id, args.water_regime)
    print(f"OK  evaluation capabilities (crop={crop_id}, regime={args.water_regime})")

    suffix = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    _, project, _ = client.request(
        "POST", "/projects", payload={"name": f"post-deploy-smoke-{suffix}"}, expected=(201,)
    )
    project_id = project["id"]
    print(f"OK  project created ({project_id})")

    _, parcel, _ = client.request(
        "POST",
        f"/projects/{project_id}/parcels",
        payload={"name": f"post-deploy-smoke-parcel-{suffix}", "geometry": geometry},
        expected=(201,),
    )
    parcel_id = parcel["id"]
    parcel_version = parcel["current_version"]
    print(f"OK  parcel created ({parcel_id}, version={parcel_version})")

    evaluation_payload = {
        "parcel_reference": {
            "project_id": project_id,
            "parcel_id": parcel_id,
            "parcel_version": parcel_version,
        },
        "requested_crops": [crop_id],
        "water_regimes": [args.water_regime],
        "environmental_inputs": [
            {
                "input_key": args.input_key,
                "dataset_id": binding["dataset_id"],
                "dataset_version_id": binding["dataset_version_id"],
            }
        ],
    }
    _, evaluation, _ = client.request(
        "POST", "/api/v1/evaluations", payload=evaluation_payload, expected=(201,)
    )
    evaluation_id = evaluation["id"]
    print(f"OK  evaluation queued ({evaluation_id})")

    deadline = time.monotonic() + args.poll_timeout
    terminal = {"succeeded", "failed", "cancelled"}
    status = "queued"
    while time.monotonic() < deadline:
        _, state, _ = client.request("GET", f"/api/v1/evaluations/{evaluation_id}")
        status = state["status"]
        completed = state.get("completed_execution_count", 0)
        requested = state.get("requested_execution_count", 0)
        print(f"WAIT evaluation status={status} executions={completed}/{requested}")
        if status in terminal:
            break
        time.sleep(args.poll_interval)
    else:
        raise SmokeFailure(f"Evaluation did not finish within {args.poll_timeout} seconds.")

    for resource in ("result", "evidence", "limitations"):
        client.request("GET", f"/api/v1/evaluations/{evaluation_id}/{resource}")
        print(f"OK  evaluation {resource}")
    if status != "succeeded":
        raise SmokeFailure(f"Evaluation reached terminal non-success status {status!r}.")

    if args.decision_support != "off":
        query = urlencode({"crop_id": crop_id, "water_regime": args.water_regime})
        ds_root = f"/api/v1/decision-support/evaluations/{evaluation_id}"
        knowledge_status, _, _ = client.request(
            "GET", f"{ds_root}/knowledge?{query}", expected=(200, 503)
        )
        if knowledge_status == 503 and args.decision_support == "auto":
            print("SKIP Decision Support (provider/config unavailable)")
        else:
            if knowledge_status != 200:
                raise SmokeFailure("Decision Support knowledge is required but unavailable.")
            print("OK  Decision Support knowledge")
            recommendation_status, _, _ = client.request(
                "POST",
                f"{ds_root}/recommendations",
                payload={
                    "crop_id": crop_id,
                    "water_regime": args.water_regime,
                    "force_regenerate": False,
                },
                expected=(200, 503),
            )
            if recommendation_status == 503 and args.decision_support == "auto":
                print("SKIP Decision Support recommendation (provider/config unavailable)")
            elif recommendation_status == 200:
                print("OK  Decision Support recommendation/cache reuse")
            else:
                raise SmokeFailure("Decision Support recommendation is required but unavailable.")

    print("PASS production smoke completed; created IDs were printed for audit/cleanup.")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-url", help="API origin; defaults to VIA_SMOKE_API_URL.")
    parser.add_argument("--email", help="Smoke user email; defaults to VIA_SMOKE_EMAIL.")
    parser.add_argument(
        "--parcel-geojson",
        help="Reviewed Polygon/MultiPolygon inside Huaura; defaults to VIA_SMOKE_PARCEL_GEOJSON.",
    )
    parser.add_argument("--crop-id", help="Optional capability crop override.")
    parser.add_argument("--water-regime", choices=("rainfed", "irrigated"), default="rainfed")
    parser.add_argument("--input-key", default="post-deploy-smoke")
    parser.add_argument("--poll-timeout", type=float, default=1800.0)
    parser.add_argument("--poll-interval", type=float, default=5.0)
    parser.add_argument("--request-timeout", type=float, default=30.0)
    parser.add_argument(
        "--decision-support",
        choices=("auto", "required", "off"),
        default="auto",
        help="Auto skips only provider/config 503; required fails; off does not call it.",
    )
    parser.add_argument(
        "--allow-http",
        action="store_true",
        help="Allow credentials over non-loopback HTTP. Never use for production.",
    )
    return parser


def main() -> int:
    try:
        run(_parser().parse_args())
    except (SmokeFailure, KeyError, TypeError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
