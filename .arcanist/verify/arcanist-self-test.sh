#!/usr/bin/env bash
set -euo pipefail

bash -n .arcanist/setup.sh
bash -n .arcanist/verify/runtime-login.sh
python3 -m py_compile .arcanist/auth/write_default_user_storage_state.py
docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml -f docker/docker-compose.arcanist.yml config >/dev/null

python3 - <<'PY'
import json
from pathlib import Path

config = json.loads(Path(".arcanist.json").read_text(encoding="utf-8"))

assert set(config) <= {"appRuntime", "verify", "pr"}
assert config["appRuntime"]["kind"] == "web"
assert config["appRuntime"]["runner"] == "docker"
assert config["appRuntime"]["entry"]["type"] == "compose"
assert config["appRuntime"]["entry"]["service"] == "mealie"
assert config["appRuntime"]["url"]["hostPort"] == 9091
assert config["appRuntime"]["portMapping"]["containerPort"] == 9000
assert config["appRuntime"]["ready"]["path"] == "/api/app/about/startup-info"
assert config["appRuntime"]["auth"]["validatePath"] == "/admin/setup"
assert "test" in config["verify"]
assert config["pr"]["templatePath"] == ".github/pull_request_template.md"
assert "e2e" not in config["appRuntime"]
PY
