#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
git submodule update --init --recursive
with-moose ./tools/setup-agent-workflows
with-moose python3 scripts/prebuilt_app.py startup
