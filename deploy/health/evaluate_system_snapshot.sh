#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: evaluate_system_snapshot.sh <component> <pre_env> <post_env>"
  exit 1
fi

COMPONENT="$1"
PRE_FILE="$2"
POST_FILE="${3:-}"
STATE_ROOT="/opt/scale-radio/state/metrics"
mkdir -p "$STATE_ROOT"

if [[ -z "$POST_FILE" ]]; then
  POST_FILE="$STATE_ROOT/${COMPONENT}.post_deploy.env"
fi

# shellcheck disable=SC1090
source "$PRE_FILE"
pre_loadavg1="$LOADAVG1"
pre_mem_available_kb="$MEM_AVAILABLE_KB"
pre_rootfs_used_kb="$ROOTFS_USED_KB"
pre_failed_unit_count="$FAILED_UNIT_COUNT"

# shellcheck disable=SC1090
source "$POST_FILE"
post_loadavg1="$LOADAVG1"
post_mem_available_kb="$MEM_AVAILABLE_KB"
post_rootfs_used_kb="$ROOTFS_USED_KB"
post_failed_unit_count="$FAILED_UNIT_COUNT"
post_volumio="$SERVICE_VOLUMIO"
post_rootfs_used_percent="$ROOTFS_USED_PERCENT"

warn=0
hard_fail=0
notes=()

loadavg_delta=$(awk -v a="$post_loadavg1" -v b="$pre_loadavg1" 'BEGIN {printf "%.2f", (a-b)}')
mem_drop_kb=$(( pre_mem_available_kb - post_mem_available_kb ))
rootfs_delta_kb=$(( post_rootfs_used_kb - pre_rootfs_used_kb ))
failed_unit_delta=$(( post_failed_unit_count - pre_failed_unit_count ))

awk -v d="$loadavg_delta" 'BEGIN {exit !(d > 2.0)}' && { warn=1; notes+=("loadavg1 increased by more than 2.0"); } || true
if (( mem_drop_kb > 256000 )); then
  warn=1
  notes+=("available memory dropped by more than 250 MB")
fi
if (( rootfs_delta_kb > 204800 )); then
  warn=1
  notes+=("root filesystem grew by more than 200 MB")
fi
if [[ "$post_volumio" != "active" ]]; then
  hard_fail=1
  notes+=("volumio is not active after deploy")
fi
if (( post_rootfs_used_percent >= 95 )); then
  hard_fail=1
  notes+=("root filesystem reached 95 percent or more used")
fi
if (( failed_unit_delta > 0 )); then
  hard_fail=1
  notes+=("failed unit count increased after deploy")
fi

RESULT_FILE="$STATE_ROOT/${COMPONENT}.evaluation.env"
{
  echo "COMPONENT=$COMPONENT"
  echo "LOADAVG1_DELTA=$loadavg_delta"
  echo "MEM_AVAILABLE_DROP_KB=$mem_drop_kb"
  echo "ROOTFS_USED_DELTA_KB=$rootfs_delta_kb"
  echo "FAILED_UNIT_DELTA=$failed_unit_delta"
  echo "WARN=$warn"
  echo "HARD_FAIL=$hard_fail"
  printf 'NOTES=%s\n' "${notes[*]}"
} > "$RESULT_FILE"

cat "$RESULT_FILE"

if (( hard_fail == 1 )); then
  exit 2
fi

exit 0
