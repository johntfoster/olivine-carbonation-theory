#!/usr/bin/env bash
set -euo pipefail
# Start before workspace lifecycle commands or remote attachment need SSH.
bash /opt/olivine/.devcontainer/start-sshd.sh
exec "$@"
