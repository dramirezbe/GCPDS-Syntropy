#!/usr/bin/env python3
"""Detect OS name and version without external libraries."""

import platform
import sys


def detect():
    system = platform.system()

    if system == "Linux":
        name, version, _ = platform.linux_distribution() if hasattr(platform, "linux_distribution") else ("", "", "")
        if not name:
            try:
                with open("/etc/os-release") as f:
                    info = dict(
                        line.split("=", 1) for line in f if "=" in line
                    )
                name = info.get("NAME", "").strip().strip('"')
                version = info.get("VERSION_ID", "").strip().strip('"')
            except OSError:
                pass
        return f"{name} {version}".strip() if name else f"Linux {platform.release()}"

    if system == "Darwin":
        mac_ver = platform.mac_ver()[0]
        return f"macOS {mac_ver}"

    if system == "Windows":
        ver = platform.version()
        release = platform.release()
        return f"Windows {release} (build {ver})"

    return f"{system} {platform.release()}"


if __name__ == "__main__":
    print(detect())
    sys.exit(0)
