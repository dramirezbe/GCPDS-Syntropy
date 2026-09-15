# Scaffold INDEX

> Last audited: 2026-09-15 @ commit `5e9b936`

## Purpose
Provide the layer-0 navigation map for agents working on the IQ-oriented Python/NumPy learning materials, their supporting prompts, and project guidance.

## Tech stack & conventions
- Jupyter Notebook with Python 3 kernels.
- NumPy `float32` tensors use the canonical shape `(N, 2, L)`.
- Axis 0 is examples, axis 1 is I/Q components, and axis 2 is time samples.
- Prompts and agent documentation are Markdown; scaffold metadata is JSON.
- All learning materials now live under `examples/` directory.

## Structure
```text
scaffold/
├── INDEX.md                         # ★ ENTRY POINT: repository map
├── cmd/                             # Environment bootstrap scripts
├── context/                         # Reference documents, audit materials, and design artifacts
│   └── audit/                       # ML notebook audit workflow documentation
├── examples/                        # Curriculum, IIR exercises, final notebooks, and NBQA playground
├── project-guidance/                # Repository-operating guidance
└── _meta/                           # Manifest and raw exploration notes
```

### Section map
| Section | Purpose | Docs |
| --- | --- | --- |
| Cmd | Cross-platform environment bootstrap scripts (OS detection, package install) | [cmd/main.md](cmd/main.md) |
| Context | Reference documents, design artifacts, and audit workflow materials | [context/main.md](context/main.md) |
| Examples | Study notebooks, IIR exercises, final notebooks, and NBQA playground | [examples/main.md](examples/main.md) |
| Project guidance | Agent environment rules, local skills, registry, and work backlog | [project-guidance/main.md](project-guidance/main.md) |

## Entry points
- `AGENTS.md` -> mandatory operating, environment, and package installation instructions.
- `cmd/detect_OS.py` -> cross-platform OS detection (zero dependencies).
- `cmd/linux-pkg.sh` -> Linux environment bootstrap (apt, venv, pip).
- `examples/study-nbs/pre_m0_1_python_functions_for_iq.ipynb` -> start of the learner sequence.
- `examples/iir-nnbs/prompts/create-nbs.md` -> generation contract for all eight notebooks.
- `examples/iir-nnbs/prompts/iir-pseudocode-to-code.md` -> pseudocode to SciPy implementation.
- `context/audit/Audit-ML-Notebook.tex` -> LaTeX audit workflow document with TikZ flowchart.
- `.agents/skills/git-flow/SKILL.md` -> branch strategy and PR workflow.

## Key interactions
```text
AGENTS.md -> scaffold/INDEX.md -> section docs -> repository files
cmd/detect_OS.py -> cmd/linux-pkg.sh | cmd/mac-pkg.sh | cmd/win-pkg.ps1
examples/iir-nnbs/prompts/*.md -> examples/iir-nnbs/<author>/*.ipynb
examples/study-nbs/prompts/create-nbs.md -> examples/study-nbs/*.ipynb
context/audit/ML-Audit-flow.md -> context/audit/Audit-ML-Notebook.tex -> context/audit/Audit-ML-Notebook.pdf
.agents/skills/* -> agent workflows; .atl/skill-registry.md indexes them
```

## Common tasks & gotchas
- Start with this index rather than scanning the repository blindly.
- Update the relevant section docs and manifest whenever repository structure or contracts change.
- Notebook pass gates combine automatic checks with a manually verified axis explanation.
- GNU Radio requires a virtual environment created with `--system-site-packages`; see `AGENTS.md`.
- All packages are detected and installed dynamically; never hardcode `requirements.txt`.
- Cross-platform scripts: `cmd/linux-pkg.sh` (bash), `cmd/mac-pkg.sh` (brew), `cmd/win-pkg.ps1` (PowerShell).

## Open questions / TODO
- No dependency lockfile currently documents exact NumPy and Matplotlib versions.
- Consider adding notebook execution tests to CI pipeline.
- Context directory contains mixed PDFs, LaTeX sources, and Excalidraw diagrams — consider further organization.
