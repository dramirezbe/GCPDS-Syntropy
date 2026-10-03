#!/usr/bin/env bash
# Bootstrap an RPi node: packages, user, udev, configs, services, SSH key.
# Run as root from the rpi/ directory: sudo ./setup.sh
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "Run as root (sudo ./setup.sh)"
    exit 1
fi

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR=/opt/rtlsdr
CONF_DIR=/etc/rtlsdr
KEY=/home/rtlsdr/.ssh/id_rtlsdr

echo "[1/6] Installing packages"
apt-get update
apt-get install -y rtl-sdr autossh python3 usbutils

echo "[2/6] Creating rtlsdr user"
getent group rtlsdr >/dev/null || groupadd --system rtlsdr
id rtlsdr >/dev/null 2>&1 || useradd --system --create-home --home-dir /home/rtlsdr \
    --shell /usr/sbin/nologin -g rtlsdr -G plugdev rtlsdr

echo "[3/6] Installing udev rule"
cat > /etc/udev/rules.d/20-rtlsdr.rules <<'EOF'
# RTL-SDR (RTL2832U) USB access for the rtlsdr group
SUBSYSTEM=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2838", GROUP="rtlsdr", MODE="0660"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2832", GROUP="rtlsdr", MODE="0660"
EOF
udevadm control --reload-rules
udevadm trigger

# The kernel DVB driver would claim the dongle and block rtl_tcp.
echo "blacklist dvb_usb_rtl28xxu" > /etc/modprobe.d/blacklist-rtlsdr.conf

echo "[4/6] Installing scripts and configs"
install -d "$INSTALL_DIR" "$CONF_DIR"
install -m 0755 "$SRC_DIR/detect_dongles.py" "$SRC_DIR/launch_rtltcp.sh" \
    "$SRC_DIR/tunnel.sh" "$INSTALL_DIR/"
# Never overwrite existing configs.
[ -f "$CONF_DIR/rtlsdr.conf" ] || install -m 0644 "$SRC_DIR/rtlsdr.conf.template" "$CONF_DIR/rtlsdr.conf"
[ -f "$CONF_DIR/tunnel.conf" ] || install -m 0644 "$SRC_DIR/tunnel.conf.template" "$CONF_DIR/tunnel.conf"

echo "[5/6] Installing systemd services"
install -m 0644 "$SRC_DIR/rtlsdr-dongles.service" "$SRC_DIR/rtlsdr-tunnel.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable rtlsdr-dongles.service rtlsdr-tunnel.service

echo "[6/6] Generating SSH keypair"
install -d -m 0700 -o rtlsdr -g rtlsdr /home/rtlsdr/.ssh
if [ ! -f "$KEY" ]; then
    sudo -u rtlsdr ssh-keygen -t ed25519 -N "" -C "rtlsdr-$(hostname)" -f "$KEY"
fi

cat <<EOF

Setup complete. Next steps:
  1. Edit $CONF_DIR/tunnel.conf (server host, REMOTE_BASE_PORT unique per RPi).
  2. Add this public key to the server user's authorized_keys (see README):

$(cat "$KEY.pub")

  3. Replug the dongles (or reboot) so the DVB driver blacklist applies.
  4. systemctl start rtlsdr-dongles rtlsdr-tunnel
EOF
