#!/usr/bin/env python3
"""Management API for remote RTL-SDR dongles reached through SSH reverse tunnels.

Run with:  uvicorn api:app --host 0.0.0.0 --port 8000
State is in memory only: restarting the API clears all reservations.
"""
from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

CONFIG_PATH = Path(os.environ.get("RTLSDR_CONFIG", Path(__file__).with_name("config.yaml")))
TUNNEL_HOST = os.environ.get("TUNNEL_CHECK_HOST", "127.0.0.1")
CONNECT_TIMEOUT_S = 2.0

app = FastAPI(title="RTL-SDR Remote Dongles")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# port -> static info (node, location, index, serial, description)
DONGLES: dict[int, dict[str, Any]] = {}
# port -> {"user": str, "expires_at": float}
RESERVATIONS: dict[int, dict[str, Any]] = {}


class ReserveRequest(BaseModel):
    user: str = Field(min_length=1)
    duration_minutes: int = Field(default=60, gt=0, le=480)


class ReleaseRequest(BaseModel):
    # Optional: when given, only the owner may release.
    user: str | None = None


@app.on_event("startup")
def load_config() -> None:
    """Load the dongle registry from YAML."""
    data = yaml.safe_load(CONFIG_PATH.read_text()) or {}
    DONGLES.clear()
    for node, info in (data.get("nodes") or {}).items():
        for d in info.get("dongles", []):
            port = int(d["remote_port"])
            if port in DONGLES:
                raise RuntimeError(f"Duplicate remote_port {port} in {CONFIG_PATH}")
            DONGLES[port] = {
                "node": node,
                "location": info.get("location", ""),
                "index": d.get("index"),
                "serial": d.get("serial", ""),
                "port": port,
                "description": d.get("description", ""),
            }


def active_reservation(port: int) -> dict[str, Any] | None:
    """Return the live reservation for a port, dropping it if expired."""
    res = RESERVATIONS.get(port)
    if res and res["expires_at"] <= time.time():
        del RESERVATIONS[port]
        return None
    return res


async def tunnel_alive(port: int) -> bool:
    """True if a TCP connect to the tunnel endpoint succeeds within the timeout."""
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(TUNNEL_HOST, port), timeout=CONNECT_TIMEOUT_S
        )
    except (OSError, asyncio.TimeoutError):
        return False
    writer.close()
    return True


async def describe(port: int) -> dict[str, Any]:
    """Build the public view of one dongle."""
    info = dict(DONGLES[port])
    res = active_reservation(port)
    alive = await tunnel_alive(port)
    if not alive:
        status = "offline"
    elif res:
        status = "reserved"
    else:
        status = "available"
    info["status"] = status
    info["reserved_by"] = res["user"] if res else None
    info["expires_at"] = res["expires_at"] if res else None
    return info


def get_or_404(port: int) -> None:
    if port not in DONGLES:
        raise HTTPException(status_code=404, detail=f"Unknown dongle port {port}")


@app.get("/dongles")
async def list_dongles() -> list[dict[str, Any]]:
    return await asyncio.gather(*(describe(p) for p in sorted(DONGLES)))


@app.get("/dongles/{port}")
async def get_dongle(port: int) -> dict[str, Any]:
    get_or_404(port)
    return await describe(port)


@app.post("/dongles/{port}/reserve")
async def reserve(port: int, req: ReserveRequest) -> dict[str, Any]:
    get_or_404(port)
    res = active_reservation(port)
    if res and res["user"] != req.user:
        raise HTTPException(status_code=409, detail="Dongle already reserved")
    if not await tunnel_alive(port):
        raise HTTPException(status_code=503, detail="Tunnel is offline")
    RESERVATIONS[port] = {
        "user": req.user,
        "expires_at": time.time() + req.duration_minutes * 60,
    }
    return await describe(port)


@app.post("/dongles/{port}/release")
async def release(port: int, req: ReleaseRequest | None = None) -> dict[str, Any]:
    get_or_404(port)
    res = active_reservation(port)
    if res and req and req.user and req.user != res["user"]:
        raise HTTPException(status_code=403, detail="Reserved by another user")
    RESERVATIONS.pop(port, None)
    return await describe(port)


@app.get("/status")
async def status() -> dict[str, Any]:
    dongles = await asyncio.gather(*(describe(p) for p in DONGLES))
    counts = {"available": 0, "reserved": 0, "offline": 0}
    for d in dongles:
        counts[d["status"]] += 1
    return {"ok": True, "total": len(dongles), **counts}


PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>RTL-SDR Dongles</title>
<style>
body{font-family:sans-serif;margin:2rem}
table{border-collapse:collapse}
td,th{border:1px solid #ccc;padding:.4rem .8rem;text-align:left}
.available{color:#127a2e}.reserved{color:#b36b00}.offline{color:#b00020}
</style></head><body>
<h1>RTL-SDR Dongles</h1>
<table id="t"><thead><tr><th>Port</th><th>Node</th><th>Location</th>
<th>Description</th><th>Status</th><th>Reserved by</th></tr></thead><tbody></tbody></table>
<script>
async function load(){
  const rows = await (await fetch('/dongles')).json();
  const tb = document.querySelector('#t tbody');
  tb.innerHTML = '';
  for (const d of rows){
    const tr = document.createElement('tr');
    const cells = [d.port, d.node, d.location, d.description, d.status, d.reserved_by || ''];
    cells.forEach((v, i) => {
      const td = document.createElement('td');
      td.textContent = v;
      if (i === 4) td.className = d.status;
      tr.appendChild(td);
    });
    tb.appendChild(tr);
  }
}
load(); setInterval(load, 10000);
</script></body></html>
"""


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return PAGE
