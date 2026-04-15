#!/usr/bin/env bash
set -euo pipefail

PAYLOAD_NAME="${1:-tuner}"
LIVE_DIR="/data/plugins/user_interface/radio_scale_peppy"
CONFIG_DIR="/data/configuration/user_interface/radio_scale_peppy"
ARCHIVE_ROOT="/opt/scale-radio/removed/tuner"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR" "$ARCHIVE_ROOT"
echo "tuner_remove_${PAYLOAD_NAME}" > "$STATE_DIR/tuner.last_phase"

REMOVED_LIVE=""
if [[ -d "$LIVE_DIR" ]]; then
  REMOVED_LIVE="$ARCHIVE_ROOT/live.${PAYLOAD_NAME}.${TIMESTAMP}"
  mv "$LIVE_DIR" "$REMOVED_LIVE"
fi
if [[ -d "$CONFIG_DIR" ]]; then
  mv "$CONFIG_DIR" "$ARCHIVE_ROOT/config.${PAYLOAD_NAME}.${TIMESTAMP}"
fi

if [[ -n "$REMOVED_LIVE" && -f "$REMOVED_LIVE/uninstall.sh" ]]; then
  (cd "$REMOVED_LIVE" && bash ./uninstall.sh)
else
  sudo systemctl disable --now scale_fm_renderer.service || true
  sudo rm -f /etc/systemd/system/scale_fm_renderer.service || true
  sudo systemctl daemon-reload || true
fi

sudo systemctl restart volumio

for i in $(seq 1 60); do
  if systemctl is-active --quiet volumio; then
    break
  fi
  sleep 2
done

if ! systemctl is-active --quiet volumio; then
  echo "SR_TUNER: volumio did not recover after Tuner removal"
  exit 2
fi

echo "SR_TUNER: removed active Tuner runtime for $PAYLOAD_NAME"
