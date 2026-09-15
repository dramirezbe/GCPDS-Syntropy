#!/usr/bin/env bash
set -euo pipefail

# --- Colors ---
RED='\033[0;31m'
YELLOW='\033[0;33m'
PURPLE='\033[0;35m'
RESET='\033[0m'

ts()  { TZ="America/Bogota" date "+%Y-%m-%d %H:%M:%S"; }
info()  { echo -e "${PURPLE}$(ts) [INFO]${RESET}  $*"; }
warn()  { echo -e "${YELLOW}$(ts) [WARN]${RESET}  $*"; }
error() { echo -e "${RED}$(ts) [ERROR]${RESET} $*" >&2; }

# --- Detect script location and repo root ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

info "REPO_ROOT=$REPO_ROOT"

# --- Check Python ---
if ! command -v python3 &>/dev/null; then
  error "python3 not found. Install via: brew install python"
  exit 1
fi

info "Python: $(python3 --version)"

# --- Ensure Homebrew is installed ---
if ! command -v brew &>/dev/null; then
  warn "Homebrew not found. Installing..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

info "Homebrew: $(brew --version | head -1)"

# --- Install GNU Radio via brew ---
if ! python3 -c "import gnuradio" &>/dev/null; then
  warn "GNU Radio not found, installing via brew..."
  brew install gnuradio
fi
info "GNU Radio OK"

# --- Create venv ---
VENV_DIR="$REPO_ROOT/.venv"

if [ ! -d "$VENV_DIR" ]; then
  info "Creating .venv with --system-site-packages (for GNU Radio access)..."
  python3 -m venv --system-site-packages "$VENV_DIR"
else
  info ".venv already exists at $VENV_DIR"
fi

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

info "Upgrading pip..."
pip install --upgrade pip

info "Installing required packages..."
pip install \
  numpy \
  matplotlib \
  scipy \
  nbformat \
  nbconvert \
  pytest

info "Verifying core packages..."
python3 -c "import numpy, matplotlib, scipy; print('Core packages OK')"
python3 -c "import nbformat, nbconvert, pytest; print('Tooling packages OK')"

info "Done. Activate with: source $VENV_DIR/bin/activate"
