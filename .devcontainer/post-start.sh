#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash .devcontainer/start-sshd.sh
with-moose python3 scripts/prebuilt_app.py startup
