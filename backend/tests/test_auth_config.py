from __future__ import annotations

import pytest

from via_backend.config import Settings


def test_auth_settings_have_secure_defaults() -> None:
    settings = Settings()

    assert settings.auth_access_token_ttl_seconds == 900
    assert settings.auth_refresh_token_ttl_seconds == 1_209_600
    assert settings.auth_refresh_cookie_name == "__Secure-via_refresh"
    assert settings.auth_refresh_cookie_secure is True
    assert settings.auth_refresh_cookie_samesite == "lax"


def test_secure_prefix_requires_secure_cookie() -> None:
    with pytest.raises(ValueError, match="VIA_AUTH_REFRESH_COOKIE_SECURE"):
        Settings(
            auth_refresh_cookie_name="__Secure-via_refresh",
            auth_refresh_cookie_secure=False,
        )


def test_unprefixed_cookie_name_allows_insecure_development_cookie() -> None:
    settings = Settings(
        auth_refresh_cookie_name="via_refresh",
        auth_refresh_cookie_secure=False,
    )

    assert settings.auth_refresh_cookie_name == "via_refresh"
    assert settings.auth_refresh_cookie_secure is False


def test_host_prefix_is_rejected_while_refresh_cookie_path_is_not_root() -> None:
    with pytest.raises(ValueError, match="__Host- requires Path=/"):
        Settings(auth_refresh_cookie_name="__Host-via_refresh")


def test_auth_settings_parse_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VIA_AUTH_ACCESS_TOKEN_TTL_SECONDS", "600")
    monkeypatch.setenv("VIA_AUTH_REFRESH_TOKEN_TTL_SECONDS", "3600")
    monkeypatch.setenv("VIA_AUTH_REFRESH_COOKIE_NAME", "via_refresh")
    monkeypatch.setenv("VIA_AUTH_REFRESH_COOKIE_SECURE", "false")
    monkeypatch.setenv("VIA_AUTH_REFRESH_COOKIE_SAMESITE", "STRICT")

    settings = Settings.from_env()

    assert settings.auth_access_token_ttl_seconds == 600
    assert settings.auth_refresh_token_ttl_seconds == 3600
    assert settings.auth_refresh_cookie_name == "via_refresh"
    assert settings.auth_refresh_cookie_secure is False
    assert settings.auth_refresh_cookie_samesite == "strict"


@pytest.mark.parametrize(
    ("field_name", "environment_name"),
    [
        ("auth_access_token_ttl_seconds", "VIA_AUTH_ACCESS_TOKEN_TTL_SECONDS"),
        ("auth_refresh_token_ttl_seconds", "VIA_AUTH_REFRESH_TOKEN_TTL_SECONDS"),
    ],
)
def test_auth_ttls_must_be_positive(field_name: str, environment_name: str) -> None:
    with pytest.raises(ValueError, match=environment_name):
        Settings(**{field_name: 0})  # type: ignore[arg-type]


@pytest.mark.parametrize("raw", ["", "maybe", "2"])
def test_auth_cookie_secure_environment_must_be_boolean(
    monkeypatch: pytest.MonkeyPatch,
    raw: str,
) -> None:
    monkeypatch.setenv("VIA_AUTH_REFRESH_COOKIE_SECURE", raw)

    with pytest.raises(ValueError, match="VIA_AUTH_REFRESH_COOKIE_SECURE"):
        Settings.from_env()


def test_samesite_none_requires_secure_cookie() -> None:
    with pytest.raises(ValueError, match="VIA_AUTH_REFRESH_COOKIE_SECURE"):
        Settings(
            auth_refresh_cookie_samesite="none",
            auth_refresh_cookie_secure=False,
            cors_allowed_origins=("https://frontend.example",),
        )


def test_samesite_none_requires_explicit_trusted_origins() -> None:
    with pytest.raises(ValueError, match="VIA_CORS_ALLOWED_ORIGINS"):
        Settings(auth_refresh_cookie_samesite="none")

    settings = Settings(
        auth_refresh_cookie_samesite="none",
        cors_allowed_origins=("https://frontend.example",),
    )
    assert settings.auth_refresh_cookie_secure is True


def test_auth_cookie_samesite_environment_rejects_unknown_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VIA_AUTH_REFRESH_COOKIE_SAMESITE", "unsupported")

    with pytest.raises(ValueError, match="VIA_AUTH_REFRESH_COOKIE_SAMESITE"):
        Settings.from_env()
