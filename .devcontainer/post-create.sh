#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
git submodule update --init --recursive
./tools/setup-agent-workflows
python3 scripts/prebuilt_app.py startup
