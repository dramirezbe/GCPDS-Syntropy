#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# --- Colors ---
$RED   = "`e[0;31m"
$YELLOW = "`e[0;33m"
$PURPLE = "`e[0;35m"
$RESET = "`e[0m"

function ts  { Get-Date -Format "yyyy-MM-dd HH:mm:ss" }
function info  { Write-Host "${PURPLE}$(ts) [INFO]${RESET}  $args" }
function warn  { Write-Host "${YELLOW}$(ts) [WARN]${RESET}  $args" }
function error { Write-Host "${RED}$(ts) [ERROR]${RESET} $args" -ForegroundColor Red }

# --- Detect script location and repo root ---
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$REPO_ROOT  = Split-Path -Parent $SCRIPT_DIR
Set-Location $REPO_ROOT

info "REPO_ROOT=$REPO_ROOT"

$py = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python -ErrorAction SilentlyContinue }
if (-not $py) {
  error "python not found. Install Python from https://www.python.org/downloads/"
  exit 1
}

info "Python: $(python --version 2>&1)"

# --- Check GNU Radio (Windows: usually via conda or standalone) ---
$missing = @()
try { python -c "import gnuradio" 2>$null } catch { $missing += "gnuradio" }
try { python -c "import venv" 2>$null } catch { $missing += "venv" }

if ($missing.Count -gt 0) {
  warn "Missing packages: $($missing -join ', ')"
  if ($missing -contains "gnuradio") {
    warn "GNU Radio on Windows: install via conda or https://www.gnuradio.org/download/"
  }
  if ($missing -contains "venv") {
    warn "venv: re-install Python and check 'Add to PATH' + 'Install stdlib modules'"
  }
  exit 1
}
info "System packages OK: gnuradio, venv"

$VENV_DIR = Join-Path $REPO_ROOT ".venv"

if (-not (Test-Path $VENV_DIR)) {
  info "Creating .venv with --system-site-packages (for GNU Radio access)..."
  python -m venv --system-site-packages $VENV_DIR
} else {
  info ".venv already exists at $VENV_DIR"
}

& "$VENV_DIR\Scripts\Activate.ps1"

info "Upgrading pip..."
pip install --upgrade pip

info "Installing required packages..."
pip install `
  numpy `
  matplotlib `
  scipy `
  nbformat `
  nbconvert `
  pytest

info "Verifying core packages..."
python -c "import numpy, matplotlib, scipy; print('Core packages OK')"
python -c "import nbformat, nbconvert, pytest; print('Tooling packages OK')"

info "Done. Activate with: $VENV_DIR\Scripts\Activate.ps1"
