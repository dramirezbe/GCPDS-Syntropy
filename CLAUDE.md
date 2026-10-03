# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A 14-week graduate course on AI-assisted SDR (Software Defined Radio) system design. Students build a live modulation classifier: Python/NumPy/PyTorch training on Colab, ONNX export, deployed on Raspberry Pi 4 + RTL-SDR.

The repo holds instructor-authored notebooks, student workspaces, generation prompts, and supporting infrastructure (RTL-SDR remote server toolkit on `feat/rtl-server` branch).

## Architecture

```
notebooks/           ← Sequential curriculum: Pre-M0 (W1), M0 (W2), M1 (W3-W4), ...
prompts/             ← Generation contracts for notebooks and IIR exercises
<student-name>/      ← Per-student workspace (cristian/, isa/, Novoa/, pisso/, sebato/)
milestone/           ← Course roadmap (02a-DL-SDRRoadmap.md is the source of truth)
scaffold/            ← 3-layer documentation scaffold for agent navigation
.agents/skills/      ← Project-scoped agent skills (git-flow, pseudocode, notebook gen)
.atl/                ← Skill registry index
context/             ← Reference PDFs and LaTeX (pedagogical arcs, pseudocode)
```

Read `AGENTS.md` first — it carries mandatory environment, git-flow, and post-task gate rules.

## IQ Data Convention

All notebooks use the canonical IQ tensor layout:

```
X.shape == (N, 2, 128)   # axis 0: examples, axis 1: I/Q, axis 2: time samples
```

Per-window joint-power normalization uses the current window only — never dataset statistics. Never normalize I and Q independently without justification.

## Milestone Sequence

Roadmap source: `milestone/02a-DL-SDRRoadmap/02a-DL-SDRRoadmap.md`

| Milestone | Topic | Weeks |
|-----------|-------|-------|
| Pre-M0 | Python/NumPy through IQ signals | W1 |
| M0 | Tensors, autograd, environment checks | W2 |
| M1 | Training harness, baselines, ONNX export | W3-W4, W6 |
| M2 | IQ pipelines and streaming | W5, W7 |
| M3 | RF representations (STFT, spectrogram CNN) | W8 |
| M4 | Capture-domain evaluation | W9 |
| M5 | Diagnostics and profiling | W10-W11 |
| M6 | Pi deployment and integration | W6-W13 |
| M7 | Final capstone assessment | W14 |

## Notebook Naming

```
<milestone>_<sequence>_<descriptive_slug>.ipynb
```

Examples: `pre_m0_1_python_functions_for_iq.ipynb`, `m1_1_minimal_training_harness.ipynb`

## Scaffold Protocol

Before inspecting implementation, read in order:
1. `scaffold/INDEX.md`
2. `scaffold/<section>/main.md`
3. `scaffold/<section>/<sub>/main.md`

If source and scaffold disagree, trust the source and update the scaffold.

## Commands

### Environment setup

```bash
python3 -m venv --system-site-packages .venv   # MUST use --system-site-packages for GNU Radio
source .venv/bin/activate
pip install numpy matplotlib scipy torch onnx onnxruntime pyrtlsdr nbformat nbconvert
```

### Validate a notebook

```bash
python3 -c "import nbformat; nbformat.read('notebooks/<file>.ipynb', as_version=4); print('OK')"
```

### Check core packages

```bash
python3 -c "import numpy, matplotlib, scipy; print('Core packages OK')"
```

### Git flow (all branches from develop, PRs target develop)

```bash
git fetch origin --prune --tags
git checkout develop && git pull origin develop
git checkout -b feature/<name>
# ... work ...
gh pr create --base develop --title "feat(scope): description"
```

## Project Skills

Before any task that matches a skill trigger, load the corresponding `SKILL.md` from `.agents/skills/`. Do not use user-level or global skills when a project-scoped skill exists for the same concern.

| Skill | Trigger | Path |
|-------|---------|------|
| git-flow | Branch, PR, merge, git workflow | `.agents/skills/git-flow/SKILL.md` |
| python-notebook | Creating/editing `.ipynb` files | `.agents/skills/python-notebook/SKILL.md` |
| pseudocode-general | High-level code flow description | `.agents/skills/pseudocode-general/SKILL.md` |
| pseudocode-specific | Algorithm pseudocode design | `.agents/skills/pseudocode-specific/SKILL.md` |
| project-scaffold | Creating/updating scaffold docs | `.agents/skills/project-scaffold/SKILL.md` |

## Key Constraints

- **Compute budget**: 7200 seconds max cumulative training on one T4 per experiment.
- **Model limits**: 250,000 parameters, batch size 256, 20 epochs (adjustable design limits).
- **Determinism**: seed Python, NumPy, PyTorch; `torch.use_deterministic_algorithms(True)`; `cudnn.benchmark = False`.
- **Splits**: freeze train/val/test indices before experimentation. For captures, split by session/source before windowing.
- **GNU Radio**: system apt install only, never `pip install gnuradio`. Instructor-only tooling — not a student runtime dependency.
- **Student workspaces**: each student has a named directory and may have a dedicated branch (`feature/iir-<name>`). Don't mix student work.
