#!/usr/bin/env bash
set -euo pipefail
set +u # Upstream Conda activation hooks reference optional unset variables.
source /opt/conda/etc/profile.d/conda.sh
conda activate moose
set -u
export MOOSE_DIR=/opt/moose
exec "$@"
