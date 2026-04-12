#!/bin/bash
set -e

export DEBIAN_FRONTEND=noninteractive
echo "Installing Fun Linea Overlay 0.6.0 dependencies"
sudo apt-get update
sudo apt-get -y install python3-pygame fonts-dejavu-core --no-install-recommends

PLUGIN_DIR="/data/plugins/user_interface/fun_linea_overlay"
RUNTIME_DIR="$PLUGIN_DIR/runtime"
mkdir -p "$RUNTIME_DIR"

if [ -d "$PLUGIN_DIR" ]; then
  sudo chmod +x "$PLUGIN_DIR/run_fun_linea.sh" || true
  sudo chmod +x "$PLUGIN_DIR/run_renderer_daemon.sh" || true
  sudo chmod +x "$PLUGIN_DIR/install.sh" || true
  sudo chmod +x "$PLUGIN_DIR/uninstall.sh" || true
fi

SERVICE_SRC="$PLUGIN_DIR/systemd/fun_linea_renderer.service"
SERVICE_DST="/etc/systemd/system/fun_linea_renderer.service"

if [ -f "$SERVICE_SRC" ]; then
  sudo cp "$SERVICE_SRC" "$SERVICE_DST"
  sudo chmod 644 "$SERVICE_DST"
  sudo systemctl daemon-reload || true
  # Do not enable or start the service automatically in 0.4.0.
  # The plugin can still preload a resident renderer by itself.
fi

echo "plugininstallend"
exit 0
