"""Production HTTP process host for VIA."""

from __future__ import annotations

import os
from dataclasses import dataclass

import uvicorn

from via_backend.config import Settings

PRODUCTION_FACTORY = "via_backend.app:create_production_app"


@dataclass(frozen=True, slots=True)
class ApiServerSettings:
    """Provider-neutral Uvicorn bind settings for the production API process."""

    host: str = "0.0.0.0"
    port: int = 8000

    def __post_init__(self) -> None:
        if not isinstance(self.host, str) or not self.host.strip():
            raise ValueError("VIA_API_HOST must be a non-empty string.")
        if isinstance(self.port, bool) or not isinstance(self.port, int):
            raise ValueError("VIA_API_PORT must be an integer.")
        if not 1 <= self.port <= 65535:
            raise ValueError("VIA_API_PORT must be between 1 and 65535.")

    @classmethod
    def from_env(cls) -> ApiServerSettings:
        """Load API bind settings from the process environment."""
        host = os.getenv("VIA_API_HOST") or "0.0.0.0"
        raw_port = os.getenv("VIA_API_PORT")
        if raw_port is None or raw_port == "":
            port = 8000
        else:
            try:
                port = int(raw_port)
            except ValueError as error:
                raise ValueError("VIA_API_PORT must be an integer.") from error
        return cls(host=host, port=port)


def main() -> None:
    """Validate production configuration and run one Uvicorn API process."""
    server = ApiServerSettings.from_env()
    Settings.from_env().require_production()
    uvicorn.run(
        PRODUCTION_FACTORY,
        factory=True,
        host=server.host,
        port=server.port,
    )


if __name__ == "__main__":
    main()
