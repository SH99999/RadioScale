#!/usr/bin/env bash
set -euo pipefail

PROFILE="${1:-deploy}"

run_sudo() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
    return
  fi

  if [[ -n "${PI_SUDO_PASSWORD:-}" ]]; then
    printf '%s
' "$PI_SUDO_PASSWORD" | sudo -S -p '' "$@"
  else
    sudo -n "$@"
  fi
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "RS_BOOTSTRAP: required command missing: $cmd" >&2
    return 1
  fi
}

install_missing_packages() {
  local missing=()
  for p in "$@"; do
    if ! dpkg -s "$p" >/dev/null 2>&1; then
      missing+=("$p")
    fi
  done

  if [[ ${#missing[@]} -eq 0 ]]; then
    echo "RS_BOOTSTRAP: apt packages already satisfied"
    return 0
  fi

  echo "RS_BOOTSTRAP: installing missing apt packages: ${missing[*]}"
  run_sudo apt-get update -y
  run_sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "${missing[@]}"
}

if [[ "$PROFILE" != "deploy" && "$PROFILE" != "state" ]]; then
  echo "Usage: pi-bootstrap-v1.sh [deploy|state]" >&2
  exit 2
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "RS_BOOTSTRAP: apt-get not available; cannot guarantee repo-controlled dependency setup" >&2
  exit 2
fi

install_missing_packages bash coreutils curl jq python3

if [[ "$PROFILE" == "deploy" ]]; then
  install_missing_packages nodejs npm
  require_cmd systemctl
fi

run_sudo mkdir -p /opt/scale-radio/state
run_sudo mkdir -p /opt/scale-radio/removed/tuner
run_sudo mkdir -p /opt/scale-radio/removed/bridge
run_sudo mkdir -p /opt/scale-radio/removed/fun-line

if [[ "$PROFILE" == "deploy" ]]; then
  run_sudo mkdir -p /data/plugins/user_interface
  run_sudo mkdir -p /data/configuration/user_interface
fi

if id -u volumio >/dev/null 2>&1; then
  run_sudo chown -R volumio:volumio /opt/scale-radio/state /opt/scale-radio/removed || true
fi

echo "RS_BOOTSTRAP: complete (profile=$PROFILE)"
