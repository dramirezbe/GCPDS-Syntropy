# RTL-SDR Remote Server Toolkit

Stream IQ samples from RTL-SDR dongles attached to remote Raspberry Pi 5 nodes
to students on the university network, using only outbound TCP.

## 1. Architecture

```
[RPi outside]                              [University server]            [Students]
 rtl_tcp -d 0 -> 127.0.0.1:1234  --\
 rtl_tcp -d 1 -> 127.0.0.1:1235  ---+-- autossh -R (outbound TCP/22) -->  127.0.0.1:28001..
 autossh (auto reconnect)          --/                                    FastAPI mgmt API :8000
                                                                           dongle registry,
                                                                           reservations
                                                  Students: API (reserve) + TCP to dongle port
```

Components:

- `rpi/`: dongle detection, one `rtl_tcp` per dongle, autossh reverse tunnel, systemd units.
- `server/`: FastAPI service with the dongle registry (`config.yaml`) and in-memory reservations.
- `client/`: `sdr_client.py`, a thin wrapper over the API plus pyrtlsdr's `RtlSdrTcpClient`.

## 2. Network constraints

The university firewall blocks UDP and VPN protocols; only outbound TCP works. So:

- Nothing connects into the RPi. The RPi opens an outbound SSH connection (TCP/22) to the server.
- `ssh -R` makes the server listen on a port whose traffic is carried back through that connection to the
  RPi's local `rtl_tcp`.
- `rtl_tcp` binds to `127.0.0.1` on the RPi, so dongles are never exposed on the RPi network.
- autossh restarts the SSH session if it drops; `ServerAliveInterval=30` and `ServerAliveCountMax=3` detect
  a dead link in about 90 seconds.

Port scheme: dongle `i` on an RPi is `BASE_PORT + i` locally (default 1234) and `REMOTE_BASE_PORT + i` on
the server. Give each RPi a distinct `REMOTE_BASE_PORT` range (the sample `config.yaml` uses 28001, 28011,
28021) so ports are unique across the fleet.

By default, `ssh -R` binds the server end to loopback only. See "Exposing tunnel ports" below.

## 3. RPi setup

On each RPi (Raspberry Pi OS / Debian):

1. Copy the `rpi/` directory to the Pi and run `sudo ./setup.sh`. It installs `rtl-sdr`, `autossh`, python3,
   creates the `rtlsdr` user, installs the udev rule (0bda:2838), blacklists the DVB kernel driver, installs
   configs in `/etc/rtlsdr/` and the systemd units, and generates `/home/rtlsdr/.ssh/id_rtlsdr`.
2. Copy the printed public key; you will add it on the server (section 4).
3. Edit `/etc/rtlsdr/tunnel.conf`: `SERVER_HOST`, `SERVER_USER`, `REMOTE_BASE_PORT` (unique per RPi) and
   `MAX_DONGLES`. Edit `/etc/rtlsdr/rtlsdr.conf` only if you need a different local base port.
4. Replug the dongles (or reboot), then:
   ```bash
   sudo systemctl start rtlsdr-dongles rtlsdr-tunnel
   ```
5. Check detection and logs:
   ```bash
   python3 /opt/rtlsdr/detect_dongles.py
   journalctl -u rtlsdr-dongles -u rtlsdr-tunnel -f
   ```

Note: `MAX_DONGLES` forwards that many ports regardless of how many dongles are plugged in; ports without a
dongle simply refuse connections and the API reports them as `offline`.

## 4. Server setup

1. Create a restricted tunnel account and authorize each RPi key with no shell and forwarding only:
   ```bash
   sudo useradd --create-home --shell /usr/sbin/nologin rtlsdr
   # in /home/rtlsdr/.ssh/authorized_keys, one line per RPi:
   restrict,port-forwarding,permitlisten="127.0.0.1:28001",permitlisten="127.0.0.1:28002" ssh-ed25519 AAAA... rtlsdr-rpi-lab-01
   ```
   `restrict` disables everything except what is re-enabled, and `permitlisten` limits which ports each
   key may open, so a stolen key cannot hijack another node's ports.
   If you change the bind address, adjust the `permitlisten` entries accordingly.
2. Edit `server/config.yaml` to match your nodes, dongle serials and ports.
3. Run the API:
   ```bash
   cd server
   python3 -m venv .venv && . .venv/bin/activate
   pip install -r requirements.txt
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```
   Open `http://<server>:8000/` for the status table. Set `RTLSDR_CONFIG` to use another YAML file.
   Run it under systemd or tmux for persistence.

API summary:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/dongles` | All dongles with node, port, status, description |
| GET | `/dongles/{port}` | One dongle |
| POST | `/dongles/{port}/reserve` | Body `{"user": "...", "duration_minutes": 60}` |
| POST | `/dongles/{port}/release` | Release (optional body `{"user": "..."}` enforces ownership) |
| GET | `/status` | Health and counts of available/reserved/offline |

Status is `offline` when a TCP connect to `127.0.0.1:<port>` fails within 2 s, `reserved` when a live
reservation exists, otherwise `available`. Reservations are in memory and expire automatically; restarting
the API clears them. Reservations are advisory: they do not block a client that connects to the port
directly, so this suits a course, not a hostile environment.

### Exposing tunnel ports

With default sshd settings, forwarded ports listen on the server's loopback only. Students then need one of:

- Run their code on the server itself (e.g. a shared JupyterHub), or
- Forward ports from their machine: `ssh -L 28001:127.0.0.1:28001 student@server`, then use
  `SDRClient(url, data_host="127.0.0.1")`, or
- The server admin deliberately exposes the ports (sshd `GatewayPorts clientspecified` and a non-loopback
  bind in the `-R` spec, restricted by the server firewall to the campus network). This decision and the
  matching `permitlisten` entries are left to the admin; this toolkit does not enable it by default.

## 5. Student usage

```bash
pip install -r client/requirements.txt
```

```python
from sdr_client import SDRClient

client = SDRClient("http://server.university.edu:8000")

# Option A: automatic. Reserves the first free dongle and releases it on exit.
with client.auto_connect("me@uni.edu", duration=30) as sdr:
    sdr.sample_rate = 2.4e6
    sdr.center_freq = 100.1e6
    sdr.gain = "auto"
    samples = sdr.read_samples(256 * 1024)

# Option B: choose a dongle.
for d in client.list_dongles():
    print(d["port"], d["node"], d["description"])
info = client.reserve(28003, "me@uni.edu", duration=60)
sdr = client.connect(28003)
try:
    sdr.center_freq = 98.5e6
    samples = sdr.read_samples(1024 * 1024)
finally:
    sdr.close()
    client.release(28003)
```

Quick API check from a shell: `curl http://server.university.edu:8000/dongles`.

## 6. Troubleshooting

| Symptom | Check |
| --- | --- |
| No dongles found | `lsusb`, `rtl_test`; replug after setup so the DVB blacklist applies; `groups rtlsdr`; `udevadm info` |
| `usb_claim_interface error -6` | Another process (or the kernel DVB driver) holds the dongle; stop duplicates, check the blacklist |
| Tunnel never connects | `journalctl -u rtlsdr-tunnel`; test `ssh -i /home/rtlsdr/.ssh/id_rtlsdr -p 22 user@server` by hand as the `rtlsdr` user |
| "remote port forwarding failed" | Port already bound on the server by a stale session; `ss -ltnp | grep 280`, kill the old sshd child; check `permitlisten` |
| Tunnel up, API says offline | The RPi side `rtl_tcp` is not running: `systemctl status rtlsdr-dongles`; `ss -ltn | grep 1234` on the RPi |
| Drops every few minutes | NAT/firewall idle timeout; keep `ServerAliveInterval` at 30 or lower |
| SSH blocked on port 22 | Ask IT, or run sshd on 443 on the server and set `SERVER_PORT=443` |
| Choppy or lagging samples | Lower sample rate; check RPi uplink with `iperf3` (TCP) |

Debug a tunnel by hand: `ssh -vvv -N -R 28001:127.0.0.1:1234 -i KEY user@server`.

## 7. Bandwidth planning

`rtl_tcp` sends 8-bit I/Q: 2 bytes per sample.

| Sample rate | Per dongle | Per dongle (Mbit/s) | Fits a 50 Mbit/s uplink |
| --- | --- | --- | --- |
| 0.25 MSps | 0.5 MB/s | 4 | 12 dongles |
| 1.0 MSps | 2.0 MB/s | 16 | 3 dongles |
| 2.048 MSps | 4.1 MB/s | 33 | 1 dongle |
| 2.4 MSps | 4.8 MB/s | 38 | 1 dongle |

The figures are raw payload; add overhead for SSH encryption (a few percent) and note that SSH encryption
on an RPi5 handles this load comfortably. If a link is slower than the table suggests, the TCP stream
backs up and `rtl_tcp` drops samples. Budget 1-2 dongles per external RPi at high rates and measure the
real upload speed first. Students on slow links should reduce the sample rate.

## 8. Security notes

- Key-based SSH only; no passwords anywhere. The tunnel key has an empty passphrase so systemd can start
  it unattended: protect it (`chmod 600`, owned by `rtlsdr`) and treat the RPi as a trusted device.
- Restrict each key on the server with `restrict,port-forwarding,permitlisten=...` and a no-shell account.
- `rtl_tcp` has no authentication. Keep it on `127.0.0.1` and reach it only via the tunnel.
- The management API has no authentication and trusts the `user` field. Place it behind the campus network
  or a reverse proxy with auth if that matters.
- `StrictHostKeyChecking=accept-new` trusts the server key on first connect; pre-seed
  `/home/rtlsdr/.ssh/known_hosts` if you want to eliminate that window.
- Run services as the non-root `rtlsdr` user only; USB access comes from the udev rule.
