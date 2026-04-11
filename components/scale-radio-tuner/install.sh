#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR"
echo "install" > "$STATE_DIR/tuner.last_phase"

echo "Tuner install hook entered"
echo "This hook expects real tuner payloads to be imported into this repo path before activation."
