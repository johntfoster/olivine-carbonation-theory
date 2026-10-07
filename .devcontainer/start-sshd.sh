#!/usr/bin/env bash
set -euo pipefail
sudo install -d -m 0755 /run/sshd
# Dev Container tools may run workspace commands while the entrypoint starts.
# Serialize key generation and daemon startup across both lifecycle paths.
sudo flock /run/sshd/olivine-start.lock bash -c '
  set -euo pipefail
  # Use port 22 for the Codespaces CLI and retain 2222 for private tunnels.
  printf "Port 22\nPort 2222\nPasswordAuthentication no\n" > /etc/ssh/sshd_config.d/90-olivine.conf
  ssh-keygen -A
  /usr/sbin/sshd -t
  /etc/init.d/ssh start
'
