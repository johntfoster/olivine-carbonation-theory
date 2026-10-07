#!/usr/bin/env bash
set -euo pipefail
sudo install -d -m 0755 /run/sshd
# Keep the development listener separate from the host's standard SSH port.
printf 'Port 2222\nPasswordAuthentication no\n' | sudo tee /etc/ssh/sshd_config.d/90-olivine.conf >/dev/null
sudo ssh-keygen -A
sudo /usr/sbin/sshd -t
# The init script safely handles repeated calls on creation and resume.
sudo /etc/init.d/ssh start
