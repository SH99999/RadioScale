#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR"
echo "healthcheck" > "$STATE_DIR/tuner.last_phase"

echo "Tuner healthcheck hook entered"
echo "Healthcheck is pending until the real tuner plugin payload and runtime install contract are imported."
