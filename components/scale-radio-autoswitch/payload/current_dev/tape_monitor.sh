#!/bin/bash
#
# Revox tape monitor toggle for Volumio 4 + HiFiBerry DAC+ ADC Pro
# Board-specific ADC routing:
#   ADC Left Input  -> VINL1
#   ADC Right Input -> VINR1
#
# Toggle behavior:
#   off -> stop Volumio playback and route ADC input on
#   on  -> route ADC input off
#
set -euo pipefail

STATEFILE="/home/volumio/.tape_state"

if [ ! -f "$STATEFILE" ]; then
    echo "off" > "$STATEFILE"
fi

STATE="$(cat "$STATEFILE")"

if [ "$STATE" = "off" ]; then
    volumio stop || true

    amixer -c 4 sset 'ADC Left Input' 'VINL1' >/dev/null
    amixer -c 4 sset 'ADC Right Input' 'VINR1' >/dev/null

    echo "on" > "$STATEFILE"
    logger -t revox-tape "Tape monitor enabled"
else
    amixer -c 4 sset 'ADC Left Input' 'Off' >/dev/null
    amixer -c 4 sset 'ADC Right Input' 'Off' >/dev/null

    echo "off" > "$STATEFILE"
    logger -t revox-tape "Tape monitor disabled"
fi
