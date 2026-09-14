# AGENTS.md

## Scaffold Exploration Protocol

Before inspecting implementation details, read the documentation scaffold in this order:

1. `scaffold/INDEX.md` for the repository map.
2. The relevant `scaffold/<section>/main.md` for a section overview.
3. The relevant `scaffold/<section>/<sub-section>/main.md` when deeper detail exists.

Only then inspect source notebooks, prompts, or project files. If source and scaffold disagree, trust the source and update the affected scaffold documents plus `scaffold/_meta/manifest.json`.

| Section | Purpose | Documentation |
| --- | --- | --- |
| Examples | Study notebooks and IIR exercise notebooks | [scaffold/examples/main.md](scaffold/examples/main.md) |
| Project guidance | Agent environment rules, local skills, registry, and work backlog | [scaffold/project-guidance/main.md](scaffold/project-guidance/main.md) |

## Cristian Workspace Convention

Work requested for Cristian must be performed on the `feature/iir-cristian` branch and placed under `examples/iir-nnbs/cristian/`, unless a task explicitly requires modifying a shared project file. Read [`examples/iir-nnbs/cristian/WORKSPACE.md`](examples/iir-nnbs/cristian/WORKSPACE.md) for its notebook map and conventions.

## Git Flow

All development follows the git-flow convention. Load `.agents/skills/git-flow/SKILL.md` before any branch or PR operation.

**Quick reference:**
- `main` — production, no direct pushes
- `develop` — integration branch, all PRs target this
- `feature/<name>`, `fix/<name>`, `docs/<name>` — always branch from `develop`
- Never delete branches after merge
- Always `git fetch origin --prune --tags` before starting work

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

## Required Packages

This project needs Python packages for notebooks, testing, and skills.
Do NOT hardcode a `requirements.txt`. Instead, detect and install dynamically.

### Detection Flow

1. Check if package is importable: `python3 -c "import <pkg>"`
2. If missing, ask user to install system prerequisites:
   ```bash
   sudo apt update && sudo apt install -y python3-full python3-venv
   ```
3. Create virtual environment with system access:
   ```bash
   python3 -m venv --system-site-packages .venv
   source .venv/bin/activate
   pip install --upgrade pip
   ```
4. Install missing packages:
   ```bash
   pip install numpy matplotlib scipy nbformat nbconvert pytest
   ```
5. Verify: `python3 -c "import numpy, matplotlib, scipy"`

### Package Map

| Context | Packages | When Needed |
|---------|----------|-------------|
| Notebooks | numpy, matplotlib, scipy | Always |
| Notebook testing | nbformat, nbconvert | When validating .ipynb |
| Notebook execution | papermill | When running notebooks end-to-end |
| Pseudocode examples | numpy, matplotlib, scipy | When generating code examples |
| GNU Radio | gnuradio (system apt) | When running GR notebooks |
| Git flow | gh CLI | When creating PRs |

### GNU Radio Special Case

GNU Radio is installed via apt, not pip. Requires `--system-site-packages`:
```bash
sudo apt install -y gnuradio python3-venv
python3 -m venv --system-site-packages .venv
```

## Post-Task Gate

After completing ANY task, run this gate before saying "done":

### 1. Environment Check
```bash
python3 -c "import numpy, matplotlib, scipy; print('Core packages OK')"
```

### 2. Notebook Validation (if notebooks changed)
```bash
python3 -c "
import nbformat, sys
for nb in sys.argv[1:]:
    try:
        nbformat.read(nb, as_version=4)
        print(f'OK {nb}')
    except Exception as e:
        print(f'FAIL {nb}: {e}')
        sys.exit(1)
" path/to/notebook.ipynb
```

### 3. Scaffold Consistency (if structure changed)
- Verify `scaffold/_meta/manifest.json` matches actual files
- Update affected `scaffold/<section>/main.md` if needed

### 4. Skill Registry (if skills changed)
- Refresh `.atl/skill-registry.md` if skill files modified

### Gate Output Format
```
OK Environment: all packages available
OK Notebooks: 3 files validated
OK Scaffold: manifest current
OK Skill registry: up to date
```
