#!/bin/bash
set -e
SERVICE="/etc/systemd/system/fun_linea_renderer.service"
sudo systemctl disable --now fun_linea_renderer.service >/dev/null 2>&1 || true
sudo rm -f "$SERVICE" || true
sudo systemctl daemon-reload >/dev/null 2>&1 || true
exit 0
