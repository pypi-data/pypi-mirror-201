"""Flywheel client configuration."""

import re
import typing as t

from fw_http_client import HttpConfig
from pydantic import root_validator, validator

__all__ = ["FWClientConfig"]

# regex to match api keys with (to extract the host if it's embedded)
API_KEY_RE = re.compile(
    r"(?i)"
    r"((?P<api_key_type>bearer|scitran-user) )?"
    r"((?P<scheme>https?://)?(?P<host>[^:]+)(?P<port>:\d+)?:)?"
    r"(?P<api_key>.+)"
)


class FWClientConfig(HttpConfig):
    """Flywheel API connection and authentication configuration."""

    api_key: t.Optional[str]
    url: t.Optional[str]
    io_proxy_url: t.Optional[str]
    snapshot_url: t.Optional[str]
    xfer_url: t.Optional[str]
    drone_secret: t.Optional[str]
    device_type: t.Optional[str]
    device_label: t.Optional[str]
    defer_auth: bool = False

    @root_validator
    @classmethod
    def validate_config(cls, values: dict) -> dict:
        """Validate client configuration or raise AssertionError.

        Authentication options:
         * api_key prefixed with the site URL (from the profile page)
         * url and api_key without the site URL (from the device page)
         * url and drone_secret with device_label (auto-creates device key)
         * defer_auth set to True, deferring auth to request-time
        """
        api_key, url = values.get("api_key"), values.get("url")
        assert api_key or url, "api_key or url required"
        # extract any additional key info "[type ][scheme://]host[:port]:key"
        if api_key:
            match = API_KEY_RE.match(t.cast(str, api_key))
            assert match, f"invalid api_key: {api_key!r}"
            info = match.groupdict()
            # clean the key of extras (enhanced keys don't allow any)
            api_key = values["api_key"] = info["api_key"]
            # use site url prefixed on the key if otherwise not provided
            if not url:
                assert info["host"], "api_key with host required"
                scheme = info["scheme"] or "https://"
                host = info["host"]
                port = info["port"] or ""
                url = f"{scheme}{host}{port}"
        # prefix url with https:// if only a domain/host is passed
        assert url
        if not url.startswith("http"):
            url = f"https://{url}"
        # strip url /api path suffix if present to accommodate other apis
        url = values["baseurl"] = re.sub(r"(/api)?/?$", "", url)
        # require auth (unless it's deferred via defer_auth)
        drone_secret = values.get("drone_secret")
        creds = api_key or drone_secret
        if values.get("defer_auth"):
            assert not creds, "api_key and drone_secret not allowed with defer_auth"
        else:
            assert creds, "api_key or drone_secret required"
        # default device_type to client_name and require device_label
        if not api_key and drone_secret:
            if not values.get("device_type"):
                values["device_type"] = values.get("client_name")
            assert values.get("device_label"), "device_label required"
        headers = values.setdefault("headers", {})
        headers.setdefault("X-Accept-Feature", "Safe-Redirect")
        return values

    @validator("io_proxy_url", "snapshot_url", "xfer_url")
    @classmethod
    def validate_urls(cls, val: str) -> str:
        """Strip trailing slash from urls."""
        return val.rstrip("/") if val else val
