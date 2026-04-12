#!/bin/bash
#
# Revox auto-switch for Volumio 4 + HiFiBerry DAC+ ADC Pro
#
# Optimized behavior:
#   - Poll interval: 1 second
#   - Start delay:  1 consecutive detection cycle
#   - Stop delay:   4 consecutive silent cycles
#
# Reason:
#   - Tape start should feel responsive
#   - Tape stop should not bounce on short quiet passages
#
set -euo pipefail

THRESHOLD="0.02"
POLL_SECONDS=1
START_CONFIRM_COUNT=1
STOP_CONFIRM_COUNT=4

LASTSTATE=0
DETECT_COUNT=0
SILENT_COUNT=0

while true
do
    LEVEL=$(arecord -D plughw:4,0 -d 1 -f cd 2>/dev/null | \
    sox -t raw -r 44100 -e signed -b 16 -c 2 - -n stat 2>&1 | \
    grep "Maximum amplitude" | awk '{print $3}')

    if [ -z "${LEVEL:-}" ]; then
        LEVEL=0
    fi

    if (( $(echo "$LEVEL > $THRESHOLD" | bc -l) )); then
        DETECT_COUNT=$((DETECT_COUNT + 1))
        SILENT_COUNT=0

        if [ "$LASTSTATE" = "0" ] && [ "$DETECT_COUNT" -ge "$START_CONFIRM_COUNT" ]; then
            /home/volumio/tape_monitor.sh
            LASTSTATE=1
            DETECT_COUNT=0
            logger -t revox-autoswitch "Tape signal detected, monitor enabled (level=$LEVEL)"
        fi
    else
        SILENT_COUNT=$((SILENT_COUNT + 1))
        DETECT_COUNT=0

        if [ "$LASTSTATE" = "1" ] && [ "$SILENT_COUNT" -ge "$STOP_CONFIRM_COUNT" ]; then
            /home/volumio/tape_monitor.sh
            LASTSTATE=0
            SILENT_COUNT=0
            logger -t revox-autoswitch "Tape silence confirmed, monitor disabled"
        fi
    fi

    sleep "$POLL_SECONDS"
done
