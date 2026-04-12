#!/bin/bash
set -e
export FUN_LINEA_PLUGIN_DIR="${FUN_LINEA_PLUGIN_DIR:-/data/plugins/user_interface/fun_linea_overlay}"
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-/home/volumio/.Xauthority}"
export SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-x11}"
export SDL_AUDIODRIVER="${SDL_AUDIODRIVER:-dummy}"
export PYGAME_HIDE_SUPPORT_PROMPT=1
exec python3 "$FUN_LINEA_PLUGIN_DIR/renderer/fun_linea_renderer.py"
