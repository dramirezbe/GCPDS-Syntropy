# Exploration Log

> Last audited: 2026-09-15 @ commit `5e9b936`

## Purpose
Preserve raw Phase 1 repository findings used to synthesize the scaffold hierarchy.

## Tech stack & conventions
- Findings are evidence snapshots, not higher-authority replacements for repository files.
- Dates and audited commit IDs identify when observations were verified.
- Future exploration should append or revise findings when source structure changes.

## Structure
```text
Repository findings
├── Root guidance and backlog
├── Notebook curriculum and report
├── Prompt contracts
└── Local skill metadata
```

## Entry points
- `scaffold/INDEX.md` -> synthesized navigation derived from these findings.
- `scaffold/_meta/manifest.json` -> machine-readable hierarchy produced from the same audit.

## Key interactions
- **Raw findings -> layer docs:** section documents summarize the verified evidence below.
- **Source changes -> new audit:** stale claims must be corrected in both this log and affected scaffold documents.

## Common tasks & gotchas
- Do not treat prompt examples as implemented code.
- Hidden directories contain project skills and generated registry information that matter to agent navigation.

## Open questions / TODO
- Verify future notebook execution in a clean environment if reproducibility becomes part of the scaffold audit.

## Phase 1 findings — 2026-09-12
- Git branch `main` matched `origin/main`; audited commit was `ce73307`; working tree was clean before scaffold creation.
- No scaffold directory existed.
- Root contained `AGENTS.md`, `tasks.md`, `.gitignore`, three local skills, a generated skill registry, eight notebooks, one generation report, and seven prompt/criterion files.
- The notebook generation report declares all eight notebooks complete and records canonical IQ shape `(N, 2, L)`, `float32`, and seed 42.
- All tracked notebooks had zero stored outputs at audit time.
- Notebook dependencies observed from code were NumPy, Matplotlib, and standard-library `pathlib`.
- Notebook 5 can create `demo_iq.npz`; no tracked data files exist.
- `prompts/create-nbs.md` references `prompts/nb-pass-criterion.txt`, but the tracked criterion is `prompts/pass-criterion.txt`.
- The GNU Radio prompt proposes a complex source, a float IIR block, and a complex sink; block signatures need verification before execution.
- The repository has no README, dependency lockfile, automated notebook execution suite, or implemented IIR script.

## Workspace update — 2026-09-12
- The active branch was verified as `feature/iir-cristian`, tracking `origin/feature/iir-cristian`.
- `cristian-work/` is a personal workspace rather than a scaffold section.
- Its local guide is `cristian-work/WORKSPACE.md`; no `scaffold/cristian-work/` mirror is maintained.

## GNU Radio notebook update — 2026-09-12
- `cristian-work/iir_gnuradio_filter.ipynb` implements the GNU Radio IIR prompt as a tutorial notebook.
- The prompt's direct complex-source to float-IIR connection is type-incompatible; the notebook splits I and Q into float streams, filters them independently, then recombines them.
- `single_pole_iir_filter_ff` belongs to `gnuradio.filter`, not `gnuradio.blocks`; the notebook uses the verified module namespace.
- GNU Radio was absent from the environment. `python3-venv` was installed, but GNU Radio installation could not proceed because `sudo` required interactive authentication.
- Notebook JSON and static cell contracts were validated; runtime execution remains pending until GNU Radio is installed.

## Pseudocode-to-code notebook update — 2026-09-12
- `cristian-work/iir_pseudocode_to_code.ipynb` implements the pseudocode prompt with explicit declarations, assignment symbols, comparisons, and block endings.
- The Python translation uses a second-order SciPy Butterworth low-pass filter and `lfilter(..., axis=2)` on deterministic `(5, 2, 1000)` float32 IQ data.
- Sequential clean-namespace execution passed: shape remained `(5, 2, 1000)` and power changed from `1.254055` to `1.001605` (ratio `0.798693`).
- `nbclient` executed all six code cells successfully in a clean kernel; the tracked notebook intentionally retains empty outputs.

## Plain-instructions notebook update — 2026-09-12
- `cristian-work/iir_plain_instructions_to_code.ipynb` implements the complete NumPy/SciPy workflow with four requested plots and compressed NPZ persistence.
- Clean sequential execution ran all seven code cells and created a temporary 37,858-byte `filtered_iq.npz` outside the repository.
- Runtime verification preserved `(5, 2, 1000)` float32 data and changed joint power from `1.207514` to `0.927528` (ratio `0.768130`).
- `nbclient` execution was unavailable because the environment has no registered `python3` kernelspec; clean-namespace sequential execution was used instead.

## Cross-platform bootstrap update — 2026-09-15
- `cmd/detect_OS.py` added: zero-dependency OS detection using `/etc/os-release` (Linux), `sw_vers` (macOS), `sys.platform` (Windows).
- `cmd/linux-pkg.sh` added: Linux bootstrap with colored logs (purple INFO, red ERROR, yellow WARNING), UTC-5 timestamps, apt install of `gnuradio` and `python3-venv`, venv creation with `--system-site-packages`, pip install of core packages.
- `cmd/mac-pkg.sh` added: macOS bootstrap using Homebrew; auto-installs Homebrew if missing.
- `cmd/win-pkg.ps1` added: Windows PowerShell bootstrap using winget/choco.
- All log timestamps use `TZ="America/Bogota"` (UTC-5), format `yyyy-mm-dd hh:mm:ss [LEVEL]`.
- Ruff notes: E901 removed in modern ruff (syntax errors always shown); F823 merged into F821; F822 is `__all__` undefined exports.

## Audit documentation update — 2026-09-15
- `context/audit/Audit-ML-Notebook.tex` created: full LaTeX document with three-gate ML audit workflow and TikZ flowchart.
- References: Yang (2022), Subotic (2023), Kaufman (2022), Breck (2019), Sculley (2011), NIST (2023).
- TikZ flowchart compiled to 4 pages, ~335 KB; diagram fits page width via `\resizebox{\textwidth}{!}{...}`.
- `context/audit/NBQA_USAGE.md` created: ruff/nbqa/black/yapf pipeline reference with `--ignore=F821` on fatal gate and style check.
- `context/audit/ML-Audit-flow.md` created: source ASCII flow diagram for the audit workflow.
- `context/audit/ML-audit-html.html` created: rendered HTML version of audit flow.

## Examples restructuring update — 2026-09-15
- `examples/final-nb/` added: contains `reference-nb.ipynb`, `reference-nb-requirements.txt`, and `issue-nb.ipynb`.
- `examples/nbqa-playground/` added: contains `fail-nb.ipynb` with intentional ruff F821/F822 failures for gate testing.
- `examples/fail-nb.ipynb` moved to `examples/nbqa-playground/fail-nb.ipynb`.
