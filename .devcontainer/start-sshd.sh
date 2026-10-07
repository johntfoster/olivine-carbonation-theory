#!/usr/bin/env bash
set -euo pipefail
sudo install -d -m 0755 /run/sshd
# Dev Container tools may run workspace commands while the entrypoint starts.
# Serialize key generation and daemon startup across both lifecycle paths.
sudo flock /run/sshd/olivine-start.lock bash -c '
  set -euo pipefail
  printf "Port 2222\nPasswordAuthentication no\n" > /etc/ssh/sshd_config.d/90-olivine.conf
  ssh-keygen -A
  /usr/sbin/sshd -t
  /etc/init.d/ssh start
'
