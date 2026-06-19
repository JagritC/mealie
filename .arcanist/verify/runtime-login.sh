#!/usr/bin/env bash
set -euo pipefail

base_url="${ARCANIST_BASE_URL:-http://localhost:9091}"
auth_state_path="${ARCANIST_AUTH_STATE_PATH:-$(mktemp)}"
export ARCANIST_BASE_URL="$base_url"
export ARCANIST_AUTH_STATE_PATH="$auth_state_path"

startup_info="$(curl -fsS "$base_url/api/app/about/startup-info")"
printf '%s' "$startup_info" | python3 -c 'import json,sys; data=json.load(sys.stdin); assert "isFirstLogin" in data'

python3 .arcanist/auth/write_default_user_storage_state.py >/tmp/arcanist-runtime-login.out
test -s "$auth_state_path"
