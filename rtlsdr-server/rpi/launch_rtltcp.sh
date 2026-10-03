#!/usr/bin/env bash
# Launch one rtl_tcp instance per detected RTL-SDR dongle.
# Port for each dongle = BASE_PORT + device index.
set -euo pipefail

CONFIG_FILE="${RTLSDR_CONF:-/etc/rtlsdr/rtlsdr.conf}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DETECT="${DETECT_SCRIPT:-$SCRIPT_DIR/detect_dongles.py}"

BASE_PORT=1234
BIND_ADDRESS=127.0.0.1
if [ -r "$CONFIG_FILE" ]; then
    # shellcheck disable=SC1090
    . "$CONFIG_FILE"
else
    echo "WARN: $CONFIG_FILE not readable, using defaults"
fi

PIDS=()

cleanup() {
    echo "Stopping ${#PIDS[@]} rtl_tcp process(es)"
    for pid in "${PIDS[@]:-}"; do
        [ -n "$pid" ] && kill "$pid" 2>/dev/null || true
    done
    wait 2>/dev/null || true
    exit 0
}
trap cleanup SIGTERM SIGINT

# Extract dongle indices from the JSON produced by detect_dongles.py.
INDICES="$(python3 "$DETECT" | python3 -c \
    'import json,sys; print(" ".join(str(d["index"]) for d in json.load(sys.stdin)["dongles"]))')"

if [ -z "$INDICES" ]; then
    echo "No RTL-SDR dongles detected; exiting with failure so systemd retries"
    exit 1
fi

for idx in $INDICES; do
    port=$((BASE_PORT + idx))
    echo "Starting rtl_tcp: device=$idx address=$BIND_ADDRESS port=$port"
    rtl_tcp -d "$idx" -a "$BIND_ADDRESS" -p "$port" &
    PIDS+=("$!")
done

# Exit as soon as any child dies so systemd restarts the whole group.
wait -n || true
echo "A rtl_tcp process exited; shutting down the group"
for pid in "${PIDS[@]}"; do
    kill "$pid" 2>/dev/null || true
done
wait 2>/dev/null || true
exit 1
