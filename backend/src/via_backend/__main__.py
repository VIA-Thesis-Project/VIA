"""Run the VIA API with its development server defaults."""

import uvicorn


def main() -> None:
    """Start the VIA API."""
    uvicorn.run("via_backend.main:app", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
