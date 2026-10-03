#!/usr/bin/env python3
"""Detect connected RTL-SDR dongles and print them as JSON.

Primary method: parse the device list printed by `rtl_test` (index, product,
serial). Fallback: `lsusb` (vendor 0bda, product 2832/2838), which can only
report presence, not serial numbers.

Output example:
    {"count": 1, "source": "rtl_test",
     "dongles": [{"index": 0, "vendor": "Realtek", "product": "RTL2838UHIDIR",
                  "serial": "00000001"}]}

Exit code is always 0 when detection ran, even with zero dongles.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from typing import Any

# Matches lines such as: "  0:  Realtek, RTL2838UHIDIR, SN: 00000001"
RTL_TEST_LINE = re.compile(
    r"^\s*(?P<index>\d+):\s+(?P<vendor>[^,]*),\s*(?P<product>[^,]*),\s*SN:\s*(?P<serial>\S*)"
)
LSUSB_LINE = re.compile(r"ID 0bda:(2832|2838)\s*(?P<name>.*)$", re.IGNORECASE)


def run(cmd: list[str], timeout: float = 8.0) -> str:
    """Run a command and return stdout+stderr; empty string on failure."""
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        # rtl_test may hang after listing devices; keep partial output.
        partial = getattr(exc, "stdout", None) or ""
        err = getattr(exc, "stderr", None) or ""
        if isinstance(partial, bytes):
            partial = partial.decode(errors="replace")
        if isinstance(err, bytes):
            err = err.decode(errors="replace")
        return partial + err
    return proc.stdout + proc.stderr


def detect_with_rtl_test() -> list[dict[str, Any]]:
    """Parse the device listing printed by rtl_test."""
    if shutil.which("rtl_test") is None:
        return []
    output = run(["rtl_test", "-t"])
    dongles: list[dict[str, Any]] = []
    for line in output.splitlines():
        match = RTL_TEST_LINE.match(line)
        if match:
            dongles.append(
                {
                    "index": int(match["index"]),
                    "vendor": match["vendor"].strip(),
                    "product": match["product"].strip(),
                    "serial": match["serial"].strip(),
                }
            )
    return dongles


def detect_with_lsusb() -> list[dict[str, Any]]:
    """Fallback: count RTL-SDR USB devices; serials are unknown."""
    if shutil.which("lsusb") is None:
        return []
    dongles: list[dict[str, Any]] = []
    for line in run(["lsusb"]).splitlines():
        match = LSUSB_LINE.search(line)
        if match:
            dongles.append(
                {
                    "index": len(dongles),
                    "vendor": "Realtek",
                    "product": match["name"].strip() or "RTL2838",
                    "serial": "",
                }
            )
    return dongles


def main() -> int:
    dongles = detect_with_rtl_test()
    source = "rtl_test"
    if not dongles:
        dongles = detect_with_lsusb()
        source = "lsusb"
    print(
        json.dumps(
            {"count": len(dongles), "source": source, "dongles": dongles},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
