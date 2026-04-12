#!/bin/bash
set -e
PLUGIN_DIR="${FUN_LINEA_PLUGIN_DIR:-/data/plugins/user_interface/fun_linea_overlay}"
export FUN_LINEA_PLUGIN_DIR="$PLUGIN_DIR"
export FUN_LINEA_RESIDENT=1
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-/home/volumio/.Xauthority}"
export SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-x11}"
export SDL_AUDIODRIVER="${SDL_AUDIODRIVER:-dummy}"
export PYGAME_HIDE_SUPPORT_PROMPT=1

SERVICE_FLAG="$PLUGIN_DIR/runtime/service_enabled.flag"
EXPECT_SERVICE_FLAG="${FUN_LINEA_EXPECT_SERVICE_FLAG:-0}"
if [ "$EXPECT_SERVICE_FLAG" = "1" ]; then
  WAIT_FLAG_SEC=0
  while [ ! -f "$SERVICE_FLAG" ]; do
    sleep 1
    WAIT_FLAG_SEC=$((WAIT_FLAG_SEC + 1))
    if [ "$WAIT_FLAG_SEC" -ge 40 ]; then
      echo "[fun_linea_overlay] service flag not present after ${WAIT_FLAG_SEC}s - exiting without renderer start"
      exit 0
    fi
  done
fi

# Wait for the local X11 socket so the renderer can create the hidden window first.
WAIT_SEC=0
while [ ! -S /tmp/.X11-unix/X0 ]; do
  sleep 1
  WAIT_SEC=$((WAIT_SEC + 1))
  if [ "$WAIT_SEC" -ge 60 ]; then
    echo "[fun_linea_overlay] X11 socket wait timeout after ${WAIT_SEC}s"
    break
  fi
done

exec python3 "$PLUGIN_DIR/renderer/fun_linea_renderer.py"
