#!/usr/bin/env bash
# Open autossh reverse tunnels: one -R per dongle.
# Server port REMOTE_BASE_PORT+i  ->  RPi localhost BASE_PORT+i
set -euo pipefail

TUNNEL_CONF="${TUNNEL_CONF:-/etc/rtlsdr/tunnel.conf}"
DONGLE_CONF="${RTLSDR_CONF:-/etc/rtlsdr/rtlsdr.conf}"

[ -r "$TUNNEL_CONF" ] || { echo "ERROR: cannot read $TUNNEL_CONF"; exit 1; }
# shellcheck disable=SC1090
. "$TUNNEL_CONF"

BASE_PORT=1234
if [ -r "$DONGLE_CONF" ]; then
    # shellcheck disable=SC1090
    . "$DONGLE_CONF"
fi

SERVER_PORT="${SERVER_PORT:-22}"
MAX_DONGLES="${MAX_DONGLES:-4}"

[ -r "$SSH_KEY" ] || { echo "ERROR: SSH key $SSH_KEY not readable"; exit 1; }

FORWARDS=()
for ((i = 0; i < MAX_DONGLES; i++)); do
    FORWARDS+=(-R "$((REMOTE_BASE_PORT + i)):127.0.0.1:$((BASE_PORT + i))")
done

echo "Connecting ${SERVER_USER}@${SERVER_HOST}:${SERVER_PORT}" \
     "with $MAX_DONGLES reverse forward(s) starting at remote port $REMOTE_BASE_PORT"

# Disable autossh's own monitor port; rely on SSH keepalives instead.
export AUTOSSH_GATETIME=0
export AUTOSSH_PORT=0

exec autossh -M 0 -N \
    -o "ServerAliveInterval=30" \
    -o "ServerAliveCountMax=3" \
    -o "ExitOnForwardFailure=yes" \
    -o "StrictHostKeyChecking=accept-new" \
    -o "BatchMode=yes" \
    -i "$SSH_KEY" \
    -p "$SERVER_PORT" \
    "${FORWARDS[@]}" \
    "${SERVER_USER}@${SERVER_HOST}"
