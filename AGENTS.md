# AGENTS.md

## Python and GNU Radio Environment

Before running Python code that depends on GNU Radio, ensure the system has `python3-venv` installed.

### Required setup

First verify that the GNU Radio Python module is available:

```bash
python3 -c "import gnuradio"
```

If that command fails:

1. Ensure `python3-venv` is installed:

```bash
sudo apt update
sudo apt install -y python3-venv
```

2. Recreate the project's virtual environment with access to system Python packages:

```bash
rm -rf .venv
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
```

3. Verify GNU Radio is now importable:

```bash
python -c "import gnuradio"
```

### Important

Do not create a standard isolated virtual environment with:

```bash
python3 -m venv .venv
```

for this project, because GNU Radio is installed through `apt` and its Python modules are available through the system Python installation.

Use:

```bash
python3 -m venv --system-site-packages .venv
```

so the virtual environment can access the system-installed GNU Radio Python packages.

### GNU Radio installation

If GNU Radio itself is not installed, install it with:

```bash
sudo apt update
sudo apt install -y gnuradio python3-venv
```

After activating the environment, verify:

```bash
python -c "import gnuradio; print(gnuradio.__file__)"
```

GNU Radio command-line tools such as `gnuradio-companion` are installed system-wide and should remain available while the `.venv` is activated.
