#!/usr/bin/env python3
"""Student client: reserve a remote RTL-SDR dongle and get a ready RtlSdrTcpClient.

Example:
    from sdr_client import SDRClient
    client = SDRClient("http://server.university.edu:8000")
    with client.auto_connect("me@uni.edu") as sdr:
        sdr.center_freq = 100.1e6
        samples = sdr.read_samples(256 * 1024)
"""
from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import requests


class SDRError(RuntimeError):
    """Raised when no dongle can be reserved or the API reports an error."""


class _Session:
    """Wraps an RtlSdrTcpClient and releases the reservation on close."""

    def __init__(self, owner: "SDRClient", port: int, sdr: Any) -> None:
        self._owner = owner
        self.port = port
        self._sdr = sdr

    def __getattr__(self, name: str) -> Any:
        # Delegate everything else (center_freq, read_samples, ...) to the SDR.
        return getattr(self._sdr, name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in {"_owner", "port", "_sdr"}:
            super().__setattr__(name, value)
        else:
            setattr(self._sdr, name, value)

    def close(self) -> None:
        try:
            self._sdr.close()
        finally:
            self._owner.release(self.port)

    def __enter__(self) -> "_Session":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class SDRClient:
    def __init__(
        self,
        server_url: str,
        user: str | None = None,
        timeout: float = 10.0,
        data_host: str | None = None,
    ) -> None:
        self.server_url = server_url.rstrip("/")
        # Host that serves the tunnel ports. Defaults to the API host; use
        # "127.0.0.1" when the ports are reached through an SSH -L forward.
        self.host = data_host or urlparse(self.server_url).hostname or "localhost"
        self.timeout = timeout
        self._user = user

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        resp = requests.request(
            method, f"{self.server_url}{path}", timeout=self.timeout, **kwargs
        )
        if not resp.ok:
            try:
                detail = resp.json().get("detail", resp.text)
            except ValueError:
                detail = resp.text
            raise SDRError(f"{resp.status_code}: {detail}")
        return resp.json()

    def list_dongles(self, only_available: bool = True) -> list[dict[str, Any]]:
        """Return dongles; by default only those currently available."""
        dongles = self._request("GET", "/dongles")
        if only_available:
            dongles = [d for d in dongles if d["status"] == "available"]
        return dongles

    def reserve(self, port: int, user: str, duration: int = 60) -> dict[str, Any]:
        """Reserve a dongle; returns its info including host and port."""
        info = self._request(
            "POST",
            f"/dongles/{port}/reserve",
            json={"user": user, "duration_minutes": duration},
        )
        self._user = user
        info["host"] = self.host
        return info

    def release(self, port: int) -> None:
        """Release a reservation (idempotent)."""
        self._request("POST", f"/dongles/{port}/release", json={"user": self._user})

    def connect(self, port: int) -> Any:
        """Return an RtlSdrTcpClient for an already reserved dongle."""
        from rtlsdr import RtlSdrTcpClient  # imported lazily: needs pyrtlsdr

        return RtlSdrTcpClient(hostname=self.host, port=port)

    def auto_connect(self, user: str, duration: int = 60) -> _Session:
        """Reserve the first available dongle and return a connected session."""
        for dongle in self.list_dongles():
            try:
                self.reserve(dongle["port"], user, duration)
            except SDRError:
                continue  # taken or went offline in the meantime
            try:
                sdr = self.connect(dongle["port"])
            except Exception:
                self.release(dongle["port"])
                raise
            return _Session(self, dongle["port"], sdr)
        raise SDRError("No available dongles")
