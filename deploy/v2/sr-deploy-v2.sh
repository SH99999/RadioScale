#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: sr-deploy-v2.sh <tuner> <ref|latest>"
  exit 1
fi

SCOPE="$1"
REQUESTED_REF="$2"
REPO_URL="git@github.com:SH99999/mediastreamer.git"
REPO_DIR="/opt/scale-radio/repo"
STATE_DIR="/opt/scale-radio/state"
INSTALL_ROOT="/opt/scale-radio/components"
CANONICAL_REF="$REQUESTED_REF"

if [[ "$CANONICAL_REF" == "latest" ]]; then
  CANONICAL_REF="main"
fi

if [[ "$SCOPE" != "tuner" ]]; then
  echo "Deploy V2 is currently enabled only for tuner"
  exit 1
fi

mkdir -p "$STATE_DIR" "$INSTALL_ROOT"

echo "preflight" > "$STATE_DIR/tuner.last_phase"

if [[ ! -d "$REPO_DIR/.git" ]]; then
  mkdir -p "$(dirname "$REPO_DIR")"
  git clone "$REPO_URL" "$REPO_DIR"
fi

git -C "$REPO_DIR" fetch --all --tags --prune
if git -C "$REPO_DIR" show-ref --verify --quiet "refs/remotes/origin/$CANONICAL_REF"; then
  git -C "$REPO_DIR" checkout -B "$CANONICAL_REF" "origin/$CANONICAL_REF"
else
  git -C "$REPO_DIR" checkout "$CANONICAL_REF"
fi

SRC="$REPO_DIR/components/scale-radio-tuner"
DST="$INSTALL_ROOT/tuner"
mkdir -p "$DST"
rm -rf "$DST"/*
cp -a "$SRC"/. "$DST"/

pushd "$DST" >/dev/null
bash ./install.sh
bash ./configure.sh
bash ./healthcheck.sh
popd >/dev/null

echo "$CANONICAL_REF" > "$STATE_DIR/tuner.last_ref"
echo "$CANONICAL_REF" > "$STATE_DIR/last_successful_ref"
echo "tuner" > "$STATE_DIR/last_scope"
date -u +%FT%TZ > "$STATE_DIR/last_deploy_request.txt"
echo "state_write" > "$STATE_DIR/tuner.last_phase"

echo "Deploy V2 completed for tuner"
