#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Prepare this container's SSH identity without publishing host private keys.
sudo install -d -m 0755 /run/sshd
sudo ssh-keygen -A
sudo /usr/sbin/sshd -t
git submodule update --init --recursive
with-moose ./tools/setup-agent-workflows
with-moose python3 scripts/prebuilt_app.py startup
