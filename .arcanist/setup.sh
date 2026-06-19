#!/usr/bin/env bash
set -euo pipefail

if ! dpkg -s libsasl2-dev libldap2-dev libssl-dev >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y libsasl2-dev libldap2-dev libssl-dev
fi

uv sync --group dev --extra pgsql

(
  cd frontend
  yarn install --frozen-lockfile
)
