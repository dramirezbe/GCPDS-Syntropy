# Cmd — Layer 1

> Parent: [../INDEX.md](../INDEX.md)
> Children: none
> Last audited: 2026-09-15 @ commit `5e9b936`

## Purpose
Provide cross-platform environment bootstrap scripts that detect the operating system and install all required system packages, Python virtual environment, and pip dependencies.

## Tech stack & conventions
- `detect_OS.py` — Python 3 stdlib only (no pip dependencies); parses `/etc/os-release` on Linux, `sw_vers` on macOS, `nt` on Windows.
- `linux-pkg.sh` — Bash; uses `apt` for system packages; creates `.venv` with `--system-site-packages` (required for GNU Radio).
- `mac-pkg.sh` — Bash; uses `brew`; auto-installs Homebrew if missing.
- `win-pkg.ps1` — PowerShell; uses `winget` or `choco`.
- All log timestamps are UTC-5 (`TZ="America/Bogota"`), format `yyyy-mm-dd hh:mm:ss [LEVEL]`.
- Colored output: purple INFO, red ERROR, yellow WARNING.
- GNU Radio is installed via `apt`, not pip; requires `--system-site-packages` on the venv.

## Structure
```text
cmd/
├── detect_OS.py        # ★ ENTRY POINT: run first; prints OS name and version
├── linux-pkg.sh        # Linux bootstrap (Ubuntu/Debian apt)
├── mac-pkg.sh          # macOS bootstrap (Homebrew)
└── win-pkg.ps1         # Windows PowerShell bootstrap
```

## Entry points
- `python3 cmd/detect_OS.py` -> prints e.g. `Ubuntu 26.04`; zero dependencies.
- `bash cmd/linux-pkg.sh` -> full Linux bootstrap (apt, venv, pip packages).
- `bash cmd/mac-pkg.sh` -> full macOS bootstrap (brew, venv, pip packages).
- `powershell cmd/win-pkg.ps1` -> full Windows bootstrap.

## Key interactions
- **AGENTS.md -> detect_OS.py:** AGENTS.md instructs agents to run detection first.
- **detect_OS.py -> platform scripts:** OS output selects the correct bootstrap script.
- **linux-pkg.sh -> apt:** installs `gnuradio`, `python3-venv` (requires `sudo`).
- **linux-pkg.sh -> pip:** installs `numpy matplotlib scipy nbformat nbconvert pytest`.
- **All scripts -> .venv:** created with `--system-site-packages` for GNU Radio access.

## Common tasks & gotchas
- `apt install` requires root — the script suggests the manual `sudo` command if not root.
- Never create `.venv` without `--system-site-packages` for this project.
- `detect_OS.py` has zero dependencies; safe to run before any venv exists.
- Logs go to stderr; stdout is clean for scripting.

## Open questions / TODO
- `win-pkg.ps1` and `mac-pkg.sh` are newer and less tested than `linux-pkg.sh`.
- Consider adding a unified `cmd/bootstrap.sh` that auto-detects and dispatches.
