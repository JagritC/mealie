#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "http://localhost:9091"
DEFAULT_EMAIL = "changeme@example.com"
DEFAULT_PASSWORD = "MyPassword"
TOKEN_COOKIE_NAME = "mealie.access_token"


def request_json(url: str, *, data: bytes | None = None, headers: dict[str, str] | None = None) -> dict:
    request = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> None:
    base_url = os.environ.get("ARCANIST_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    auth_state_path = Path(os.environ.get("ARCANIST_AUTH_STATE_PATH", ".arcanist/auth/storage-state.json"))

    form_data = urllib.parse.urlencode({"username": DEFAULT_EMAIL, "password": DEFAULT_PASSWORD}).encode()
    token_response = request_json(
        f"{base_url}/api/auth/token",
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = token_response["access_token"]

    user = request_json(
        f"{base_url}/api/users/self",
        headers={"Authorization": f"Bearer {token}"},
    )
    if user.get("email") != DEFAULT_EMAIL or not user.get("admin"):
        raise SystemExit("seeded admin validation failed")

    parsed = urllib.parse.urlparse(base_url)
    storage_state = {
        "cookies": [
            {
                "name": TOKEN_COOKIE_NAME,
                "value": token,
                "domain": parsed.hostname or "localhost",
                "path": "/",
                "expires": int(time.time()) + 3600,
                "httpOnly": False,
                "secure": parsed.scheme == "https",
                "sameSite": "Lax",
            }
        ],
        "origins": [],
    }

    auth_state_path.parent.mkdir(parents=True, exist_ok=True)
    auth_state_path.write_text(json.dumps(storage_state), encoding="utf-8")
    print(f"wrote auth state for {user['email']} to {auth_state_path}")


if __name__ == "__main__":
    main()
