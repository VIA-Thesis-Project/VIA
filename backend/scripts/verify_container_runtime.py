"""Fail fast when the VIA container lacks its complete scientific runtime."""

from __future__ import annotations

import argparse
import importlib
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCIENTIFIC_IMPORTS = (
    "numpy",
    "scipy",
    "matplotlib",
    "rasterio",
    "xarray",
    "numba",
    "rio_cogeo",
    "cartopy",
    "dask",
    "distributed",
    "netCDF4",
    "PIL",
    "psutil",
    "pyproj",
    "shapely",
    "skimage",
    "tqdm",
)

REQUIRED_CONSOLE_SCRIPTS = ("via-backend", "via-worker")
REQUIRED_CROPSUITE_FILES = (
    "CropSuite.py",
    "run_cropsuitelite.py",
    "src/multicrop.py",
    "scripts/run_evaluation_engine.py",
)


def _require_writable_directory(path: Path, *, variable: str) -> None:
    if not path.is_dir():
        raise RuntimeError(f"{variable} must point to an existing directory: {path}")
    try:
        with tempfile.NamedTemporaryFile(dir=path, prefix=".via-smoke-"):
            pass
    except OSError as exc:
        raise RuntimeError(f"{variable} must be writable by the runtime user: {path}") from exc


def _run_pip_check() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "pip", "check"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        details = (completed.stdout + completed.stderr).strip()
        raise RuntimeError(f"python -m pip check failed:\n{details}")


def verify_runtime(*, require_linux: bool) -> None:
    """Verify the interpreter used by the worker can import the complete runtime."""
    if sys.version_info < (3, 11):  # noqa: UP036 - container contract check
        raise RuntimeError("VIA container requires Python 3.11 or newer.")
    if require_linux and platform.system() != "Linux":
        raise RuntimeError("VIA production container verification must run on Linux.")
    if require_linux and os.geteuid() == 0:
        raise RuntimeError("VIA container runtime must use a non-root user.")

    configured_python = Path(os.environ.get("VIA_CROPSUITE_PYTHON", "")).resolve()
    current_python = Path(sys.executable).resolve()
    if not configured_python.is_file():
        raise RuntimeError("VIA_CROPSUITE_PYTHON must point to an existing interpreter.")
    if configured_python != current_python:
        raise RuntimeError(
            "VIA_CROPSUITE_PYTHON must identify the interpreter running the "
            "scientific dependency verification."
        )

    importlib.import_module("via_backend")
    importlib.import_module("via_backend.worker")
    for module_name in SCIENTIFIC_IMPORTS:
        importlib.import_module(module_name)

    for script_name in REQUIRED_CONSOLE_SCRIPTS:
        if shutil.which(script_name) is None:
            raise RuntimeError(f"Required console script is not installed: {script_name}")

    engine_root = Path(os.environ.get("VIA_CROPSUITE_ROOT", "")).resolve()
    missing_files = [
        relative_path
        for relative_path in REQUIRED_CROPSUITE_FILES
        if not (engine_root / relative_path).is_file()
    ]
    if missing_files:
        raise RuntimeError(
            "VIA_CROPSUITE_ROOT is missing required CropSuiteLite files: "
            + ", ".join(missing_files)
        )
    if os.access(engine_root, os.W_OK) or os.access(engine_root / "src" / "multicrop.py", os.W_OK):
        raise RuntimeError("CropSuiteLite source must not be writable by the runtime user.")

    workspace = Path(os.environ.get("VIA_CROPSUITE_WORKSPACE", "")).resolve()
    artifacts = Path(os.environ.get("VIA_ARTIFACTS_ROOT", "")).resolve()
    _require_writable_directory(workspace, variable="VIA_CROPSUITE_WORKSPACE")
    _require_writable_directory(artifacts, variable="VIA_ARTIFACTS_ROOT")

    sys.path.insert(0, str(engine_root))
    try:
        importlib.import_module("src.multicrop")
    finally:
        sys.path.pop(0)

    _run_pip_check()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-linux", action="store_true")
    arguments = parser.parse_args()
    verify_runtime(require_linux=arguments.require_linux)
    print("VIA container runtime verification passed (including pip check).")


if __name__ == "__main__":
    main()
